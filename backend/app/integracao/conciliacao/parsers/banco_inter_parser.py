from datetime import datetime

from app.models.enums import TipoLancamento, FormaPagamento, StatusLancamento
from app.integracao.conciliacao.parsers.base_parser import BaseParser


class BancoInterParser(BaseParser):

    def _to_float(self, valor_str: str) -> float:
        return float(valor_str.replace(".", "").replace(",", "."))

    def _parse_tipo(self, historico: str) -> TipoLancamento:
        historico = historico.lower()

        if "recebido" in historico:
            return TipoLancamento.RECEITA

        return TipoLancamento.DESPESA

    def parse(self, file_path: str) -> list[dict]:
        import csv

        result = []
        erros = []

        with open(file_path, encoding="latin1") as csvfile:
            reader = csv.reader(csvfile, delimiter=";")

            header_found = False
            linha_num = 0

            for row in reader:
                linha_num += 1

                if not header_found:
                    if "Data Lançamento" in row:
                        header_found = True
                    continue

                if not row or len(row) < 5:
                    continue

                try:
                    data_str, historico, descricao, valor_str, saldo = row

                    result.append({
                        "descricao": descricao.strip(),
                        "valor": abs(self._to_float(valor_str)),
                        "data_pagamento": datetime.strptime(data_str, "%d/%m/%Y"),
                        "tipo": self._parse_tipo(historico),
                        "forma_pagamento": FormaPagamento.PIX,
                        "status": StatusLancamento.NAO_CONCILIADO,
                        "observacao": historico.strip(),
                        "finalidade_id": None,
                    })

                except Exception as e:
                    erros.append({
                        "linha": linha_num,
                        "erro": str(e),
                        "conteudo": row
                    })

        # 🔥 log simples (pode evoluir depois)
        if erros:
            print(f"[Parser] Linhas com erro: {len(erros)}")
            for e in erros:
                print(e)

        return result