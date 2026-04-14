import hashlib

from app.integracao.conciliacao.factory.parser_factory import ParserFactory


class Conciliador:

    @staticmethod
    def _normalizar_texto(valor: str) -> str:
        return valor.strip().lower() if valor else ""

    @staticmethod
    def _normalizar_valor(valor: float) -> float:
        return round(float(valor), 2)

    @staticmethod
    def _gerar_hash(lancamento: dict) -> str:
        base = f"{lancamento['data_pagamento']}_{lancamento['valor']}_{lancamento['descricao']}_{lancamento['observacao']}"
        return hashlib.md5(base.encode()).hexdigest()

    @staticmethod
    def processar(file_path: str, nome_arquivo: str, is_duplicado_callback):
        parser = ParserFactory.get_parser(nome_arquivo)

        registros = parser.parse(file_path)

        novos = []
        ignorados = 0
        erros = []

        for idx, r in enumerate(registros, start=1):
            try:
                hash_value = Conciliador._gerar_hash(r)
                r["hash_transacao"] = hash_value

                if is_duplicado_callback(hash_value):
                    ignorados += 1
                    continue

                novos.append(r)

            except Exception as e:
                erros.append({
                    "linha": idx,
                    "erro": str(e),
                    "conteudo": r
                })

        return {
            "total_processado": len(registros),
            "total_novos": len(novos),
            "total_ignorados": ignorados,
            "total_erros": len(erros),
            "novos": novos,
            "erros": erros
        }