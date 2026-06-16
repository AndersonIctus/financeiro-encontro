import os
from sqlalchemy.orm import Session

from app.core.config import UPLOAD_FOLDER
from app.integracao.conciliacao.conciliador import Conciliador
from app.services.extrato_bancario_service import ExtratoBancarioService
from app.services.lancamento_service import LancamentoService
from app.models.enums import FormaPagamento, StatusLancamento, StatusProcessamento, TipoLancamento
from app.utils.hash_utils import gerar_hash

class ConciliacaoService:
    
    @staticmethod
    def _sugerir_finalidade(dto) -> int | None:
        # descricao = dto.descricao.lower()

        if dto.valor == 120:
            return 4 # valor inscrição de enccontreiro
        
        if dto.valor >= 200 and dto.valor <= 220:
            return 3 # valor inscrição de encontrista
        
        if dto.tipo == "entrada":
            if dto.valor >= 10 and dto.valor <= 50:
                return 2 # valores padrão de campanhas
            if dto.valor > 50:
                return 99 # retorna outros para valores acima de 50 em receitas
            else:
                return 1 # para todos os outros casos de receitas
        else:
            return 99 # padrão retorna outros para despesas
    
    @staticmethod
    def _to_lancamento_dict(dto):
        tipo = (
            TipoLancamento.RECEITA
            if dto.tipo == "entrada"
            else TipoLancamento.DESPESA
        )
        
        observacao = dto.observacao or ""

        hash_value = gerar_hash(
            dto.descricao,
            dto.valor,
            dto.data,
            observacao,
        )

        sugestao_id = ConciliacaoService._sugerir_finalidade(dto)

        return {
            "descricao": dto.descricao,
            "valor": dto.valor,
            "tipo": tipo,
            "forma_pagamento": FormaPagamento.PIX,
            "status": StatusLancamento.NAO_CONCILIADO,
            "data_pagamento": dto.data,
            "hash_transacao": hash_value,
            "observacao": observacao,
            "finalidade_id": None,
            "sugestao_finalidade_id": sugestao_id
        }

    @staticmethod
    def upload_and_process(file, db: Session):
        if not file.filename.endswith(".csv"):
            raise Exception("Arquivo deve ser CSV")

        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)

        # Ler conteúdo do arquivo tentando UTF-8 primeiro
        conteudo_bytes = file.file.read()
        
        # Tentar decodificar com UTF-8, lança exceção se falhar
        try:
            conteudo = conteudo_bytes.decode('utf-8')
        except UnicodeDecodeError:
            raise Exception("Erro ao processar arquivo. Utilize o charset UTF-8 para evitar problemas de acentuação.")
        
        # Salvar arquivo com encoding UTF-8
        with open(file_path, "w", encoding="utf-8") as buffer:
            buffer.write(conteudo)

        extrato = ExtratoBancarioService.create(db, {
            "nome_arquivo": file.filename,
            "caminho_arquivo": file_path,
            "tamanho_bytes": os.path.getsize(file_path),
            "status": StatusProcessamento.PROCESSANDO
        })

        try:
            def is_duplicado(dto) -> bool:
                data = ConciliacaoService._to_lancamento_dict(dto)
                return LancamentoService.exists_by_hash(db, data["hash_transacao"])

            resultado = Conciliador.processar(
                file_path,
                file.filename,
                is_duplicado
            )

            novos_lancamentos = []

            for dto in resultado["novos"]:
                try:
                    lancamento_data = ConciliacaoService._to_lancamento_dict(dto)

                    obj = LancamentoService.create(db, lancamento_data)
                    novos_lancamentos.append(obj)

                except Exception as e:
                    print(f"[DB ERROR] {e}")

            ExtratoBancarioService.update_status(
                db,
                extrato.id,
                StatusProcessamento.PROCESSADO
            )

            return {
                "inseridos": resultado["total_novos"],
                "duplicados": resultado["total_duplicados"],
                "erros": resultado["total_erros"],
                "mensagem": f"Processamento concluído. {resultado['total_novos']} inseridos, {resultado['total_duplicados']} duplicados, {resultado['total_erros']} erros."
            }

        except Exception as e:
            # 🔥 erro grave → extrato ERRO
            ExtratoBancarioService.update_status(
                db,
                extrato.id,
                StatusProcessamento.ERRO
            )

            raise Exception(f"Erro ao processar arquivo: {str(e)}")