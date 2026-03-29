from enum import Enum

class TipoLancamento(str, Enum):
    RECEITA = "RECEITA"
    DESPESA = "DESPESA"


class FormaPagamento(str, Enum):
    PIX = "PIX"
    DINHEIRO = "DINHEIRO"
    CARTAO_CREDITO = "CARTAO_CREDITO"
    CARTAO_DEBITO = "CARTAO_DEBITO"


class StatusLancamento(str, Enum):
    CONCILIADO = "CONCILIADO"
    NAO_CONCILIADO = "NAO_CONCILIADO"