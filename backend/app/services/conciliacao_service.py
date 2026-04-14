import os
from sqlalchemy.orm import Session

from app.integracao.conciliacao.conciliador import Conciliador
from app.services.extrato_bancario_service import ExtratoBancarioService
from app.services.lancamento_service import LancamentoService
from app.models.enums import StatusProcessamento


UPLOAD_DIR = "uploads"

class ConciliacaoService:

    @staticmethod
    def upload_and_process(file, db: Session):
        if not file.filename.endswith(".csv"):
            raise Exception("Arquivo deve ser CSV")

        os.makedirs(UPLOAD_DIR, exist_ok=True)
        file_path = os.path.join(UPLOAD_DIR, file.filename)

        with open(file_path, "wb") as buffer:
            buffer.write(file.file.read())

        extrato = ExtratoBancarioService.create(db, {
            "nome_arquivo": file.filename,
            "caminho_arquivo": file_path,
            "tamanho_bytes": os.path.getsize(file_path),
            "status": StatusProcessamento.PROCESSANDO
        })

        try:
            def is_duplicado(hash_value: str) -> bool:
                return LancamentoService.exists_by_hash(db, hash_value)

            resultado = Conciliador.processar(
                file_path,
                file.filename,
                is_duplicado
            )

            novos_lancamentos = []

            for r in resultado["novos"]:
                try:
                    obj = LancamentoService.create(db, r)
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
                "total_ignorados": resultado["total_ignorados"],
                "total_erros": resultado["total_erros"]
            }

        except Exception as e:
            # 🔥 erro grave → extrato ERRO
            ExtratoBancarioService.update_status(
                db,
                extrato.id,
                StatusProcessamento.ERRO
            )

            raise Exception(f"Erro ao processar arquivo: {str(e)}")