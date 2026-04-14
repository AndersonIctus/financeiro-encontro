import hashlib

from app.integracao.conciliacao.factory.parser_factory import ParserFactory


class Conciliador:

    @staticmethod
    def _normalizar_texto(valor: str) -> str:
        if not valor:
            return ""

        return valor.strip().lower()  

    @staticmethod
    def _normalizar_valor(valor: float) -> float:
        return round(float(valor), 2)

    @staticmethod
    def _gerar_hash(lancamento: dict) -> str:
        descricao = Conciliador._normalizar_texto(lancamento.get("descricao"))
        observacao = Conciliador._normalizar_texto(lancamento.get("observacao"))

        valor = Conciliador._normalizar_valor(lancamento.get("valor"))
        data = lancamento.get("data_pagamento")

        base = f"{data}_{valor}_{descricao}_{observacao}"

        return hashlib.md5(base.encode()).hexdigest()

    @staticmethod
    def processar(file_path: str, nome_arquivo: str, is_duplicado_callback):
        parser = ParserFactory.get_parser(nome_arquivo)

        registros = parser.parse(file_path)

        novos = []
        ignorados = 0

        for r in registros:
            hash_value = Conciliador._gerar_hash(r)

            r["hash_transacao"] = hash_value 

            if is_duplicado_callback(hash_value):
                ignorados += 1
                continue

            novos.append(r)

        return {
            "total_processado": len(registros),
            "total_novos": len(novos),
            "total_ignorados": ignorados,
            "novos": novos
        }