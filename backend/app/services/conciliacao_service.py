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
        descricao = dto.descricao.lower()

        if "oferta" in descricao:
            return 1

        if "campanha" in descricao:
            return 2

        if "inscricao" in descricao:
            return 3

        return 1 # padrão retorna oferta!
    
    @staticmethod
    def _to_lancamento_dict(dto):
        tipo = (
            TipoLancamento.RECEITA
            if dto.tipo == "entrada"
            else TipoLancamento.DESPESA
        )
        
        observacao = dto.observacao or f"Importado de {dto.banco}"

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

        with open(file_path, "wb") as buffer:
            buffer.write(file.file.read())

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
                "extrato_id": extrato.id,
                "total_processado": resultado["total_processado"],
                "total_inserido": resultado["total_novos"],
                "total_duplicados": resultado["total_duplicados"],
                "total_erros": resultado["total_erros"],
                "duplicados": resultado["duplicados"] if resultado["total_duplicados"] > 0 else [],
                "erros": resultado["erros"] if resultado["total_erros"] > 0 else []
            }

        except Exception as e:
            # 🔥 erro grave → extrato ERRO
            ExtratoBancarioService.update_status(
                db,
                extrato.id,
                StatusProcessamento.ERRO
            )

            raise Exception(f"Erro ao processar arquivo: {str(e)}")