from datetime import date, datetime
from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    HRFlowable,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)
from sqlalchemy.orm import Session, joinedload

from app.models.enums import TipoLancamento
from app.models.lancamento import Lancamento

_COR_PRIMARIA  = colors.HexColor("#1a237e")
_COR_LINHA_PAR = colors.HexColor("#f0f4ff")
_COR_TOTAIS    = colors.HexColor("#e8eaf6")
_COR_RECEITA   = colors.HexColor("#1b5e20")
_COR_DESPESA   = colors.HexColor("#b71c1c")


def _brl(value: float) -> str:
    return f"{value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


class RelatorioService:

    @staticmethod
    def gerar_livro_caixa(db: Session, data_inicio: date, data_fim: date) -> bytes:
        lancamentos = (
            db.query(Lancamento)
            .options(joinedload(Lancamento.finalidade))
            .filter(Lancamento.data_pagamento >= data_inicio)
            .filter(Lancamento.data_pagamento <= data_fim)
            .order_by(Lancamento.data_pagamento.asc(), Lancamento.id.asc())
            .all()
        )

        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            leftMargin=15 * mm,
            rightMargin=15 * mm,
            topMargin=20 * mm,
            bottomMargin=20 * mm,
        )

        titulo_style = ParagraphStyle(
            "titulo",
            fontName="Helvetica-Bold",
            fontSize=16,
            textColor=_COR_PRIMARIA,
            alignment=TA_CENTER,
            spaceAfter=2 * mm,
        )
        subtitulo_style = ParagraphStyle(
            "subtitulo",
            fontName="Helvetica-Bold",
            fontSize=12,
            textColor=_COR_PRIMARIA,
            alignment=TA_CENTER,
            spaceAfter=2 * mm,
        )
        info_style = ParagraphStyle(
            "info",
            fontName="Helvetica",
            fontSize=9,
            textColor=colors.grey,
            alignment=TA_CENTER,
            spaceAfter=5 * mm,
        )
        rodape_style = ParagraphStyle(
            "rodape",
            fontName="Helvetica",
            fontSize=8,
            textColor=colors.grey,
            alignment=TA_RIGHT,
        )

        story = []
        story.append(Paragraph("Encontro com Cristo", titulo_style))
        story.append(Paragraph("LIVRO CAIXA", subtitulo_style))
        story.append(Paragraph(
            f"Período: {data_inicio.strftime('%d/%m/%Y')} a {data_fim.strftime('%d/%m/%Y')}",
            info_style,
        ))
        story.append(HRFlowable(width="100%", thickness=1, color=_COR_PRIMARIA, spaceAfter=5 * mm))

        # Larguras: soma = 180mm (A4 210mm - 2x15mm margem)
        col_widths = [22 * mm, 63 * mm, 33 * mm, 21 * mm, 21 * mm, 20 * mm]

        header = ["Data", "Histórico", "Finalidade", "Entrada\n(R$)", "Saída\n(R$)", "Saldo\n(R$)"]
        rows = [header]

        saldo = 0.0
        total_entradas = 0.0
        total_saidas = 0.0

        for lanc in lancamentos:
            is_receita = lanc.tipo == TipoLancamento.RECEITA

            if is_receita:
                saldo += lanc.valor
                total_entradas += lanc.valor
                entrada_str = _brl(lanc.valor)
                saida_str   = "-"
            else:
                saldo -= lanc.valor
                total_saidas += lanc.valor
                entrada_str = "-"
                saida_str   = _brl(lanc.valor)

            historico = lanc.descricao
            if lanc.observacao:
                historico += f"\n{lanc.observacao}"

            rows.append([
                lanc.data_pagamento.strftime("%d/%m/%Y"),
                historico,
                lanc.finalidade.nome if lanc.finalidade else "-",
                entrada_str,
                saida_str,
                _brl(saldo),
            ])

        rows.append([
            "TOTAL", "", "",
            _brl(total_entradas),
            _brl(total_saidas),
            _brl(saldo),
        ])

        n = len(rows)
        style_cmds = [
            # Cabeçalho
            ("BACKGROUND", (0, 0), (-1, 0), _COR_PRIMARIA),
            ("TEXTCOLOR",  (0, 0), (-1, 0), colors.white),
            ("FONTNAME",   (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE",   (0, 0), (-1, 0), 8),
            ("ALIGN",      (0, 0), (-1, 0), "CENTER"),
            # Dados
            ("FONTNAME",   (0, 1), (-1, -2), "Helvetica"),
            ("FONTSIZE",   (0, 1), (-1, -2), 7.5),
            ("ALIGN",      (0, 1), (0, -2), "CENTER"),   # Data
            ("ALIGN",      (3, 1), (5, -2), "RIGHT"),    # Valores
            # Linhas pares
            *[("BACKGROUND", (0, i), (-1, i), _COR_LINHA_PAR) for i in range(2, n - 1, 2)],
            # Totais
            ("BACKGROUND", (0, -1), (-1, -1), _COR_TOTAIS),
            ("FONTNAME",   (0, -1), (-1, -1), "Helvetica-Bold"),
            ("FONTSIZE",   (0, -1), (-1, -1), 8),
            ("ALIGN",      (0, -1), (2, -1), "CENTER"),
            ("ALIGN",      (3, -1), (5, -1), "RIGHT"),
            ("LINEABOVE",  (0, -1), (-1, -1), 1, _COR_PRIMARIA),
            # Grade
            ("GRID",       (0, 0), (-1, -1), 0.3, colors.lightgrey),
            ("LINEBELOW",  (0, 0), (-1, 0), 1, colors.white),
            # Espaçamento interno
            ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING",    (0, 0), (-1, -1), 3),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ("LEFTPADDING",   (0, 0), (-1, -1), 4),
            ("RIGHTPADDING",  (0, 0), (-1, -1), 4),
        ]

        table = Table(rows, colWidths=col_widths, repeatRows=1)
        table.setStyle(TableStyle(style_cmds))
        story.append(table)

        story.append(Spacer(1, 8 * mm))
        story.append(Paragraph(
            f"Emitido em {datetime.now().strftime('%d/%m/%Y às %H:%M')}",
            rodape_style,
        ))

        doc.build(story)
        return buffer.getvalue()
