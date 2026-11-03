"""Gera os dois rascunhos vetoriais dos dashboards."""
# [IA] Codex/OpenAI - diagramação dos rascunhos dos dashboards.
from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen.canvas import Canvas

ROOT = Path(__file__).resolve().parents[1]
BG = colors.HexColor("#FCFAF7")
INK = colors.HexColor("#302B29")
MUTED = colors.HexColor("#756A60")
ACCENT = colors.HexColor("#B44938")
SIDE = colors.HexColor("#F1EBE3")
LINE = colors.HexColor("#D9CFC4")


def wrap(text, width, font="Helvetica", size=9):
    from reportlab.pdfbase.pdfmetrics import stringWidth
    lines, line = [], ""
    for word in text.split():
        test = (line + " " + word).strip()
        if line and stringWidth(test, font, size) > width:
            lines.append(line)
            line = word
        else:
            line = test
    if line:
        lines.append(line)
    return lines


def text(c, x, y, content, width=500, size=9, bold=False, color=INK):
    font = "Helvetica-Bold" if bold else "Helvetica"
    c.setFont(font, size)
    c.setFillColor(color)
    for line in wrap(content, width, font, size):
        c.drawString(x, y, line)
        y -= size * 1.4
    return y


def box(c, x, y, w, h, title, body=""):
    c.setFillColor(colors.white)
    c.setStrokeColor(LINE)
    c.roundRect(x, y, w, h, 6, fill=1, stroke=1)
    text(c, x + 12, y + h - (15 if h < 50 else 22), title, w - 24, 11, True)
    if body:
        text(c, x + 12, y + h - (30 if h < 50 else 44), body, w - 24, 8.5, color=MUTED)


def sketch(number):
    out = ROOT / f"entregas/rascunho-dashboard-{number}.pdf"
    c = Canvas(str(out), pagesize=landscape(A4))
    w, h = landscape(A4)
    c.setTitle(f"Rascunho do Dashboard {number} - Heart Disease")
    c.setFillColor(BG); c.rect(0, 0, w, h, fill=1, stroke=0)
    text(c, 28, h - 28, f"RASCUNHO DE LAYOUT / DASHBOARD {number}", size=10, bold=True, color=ACCENT)
    text(c, 28, h - 49, "Heart Disease - AVD 2026.2 - Guilherme Alcoforado Rabelo", size=9)
    c.setFillColor(SIDE); c.roundRect(26, 54, 155, h - 127, 6, fill=1, stroke=0)
    text(c, 38, h - 96, "FILTROS GLOBAIS", 130, 11, True)
    y = h - 125
    for title in ["Seletor das 5 medidas", "Filtro do desfecho", "Idade: intervalo", "Pressão: intervalo", "Colesterol: intervalo", "FC máxima: intervalo", "Depressão ST: intervalo", "Restaurar filtros"]:
        y = text(c, 38, y, title, 130, 9) - 15
    text(c, 38, 91, "Mesmos filtros nos dois painéis; limites inclusivos.", 130, 8, color=MUTED)
    x, width = 200, w - 228
    text(c, x, h - 92, "Título + descrição do público + contagem do recorte", width, 12, True)
    box(c, x, h - 137, width, 27, "Abas: Dashboard 1 - Laboratório | Dashboard 2 - Panorama")
    if number == 1:
        box(c, x, h - 188, width, 40, "Controles do laboratório", "Método de correlação / número de classes / separar desfechos")
        box(c, x, h - 345, width, 145, "Mapa de calor da correlação", "Escala fixa -1 a +1; coeficientes anotados e número de pares no tooltip.")
        half = (width - 14) / 2
        box(c, x, 96, half, 135, "Histogramas: coluna 1", "Um histograma para cada medida selecionada, com unidade e contagem de pacientes.")
        box(c, x + half + 14, 96, half, 135, "Histogramas: coluna 2", "A grade continua abaixo para até cinco distribuições. Cores opcionais por desfecho.")
    else:
        cardw = (width - 24) / 3
        for i, (title, body) in enumerate([
            ("Diagnóstico positivo", "% de Cardíaco no recorte"), ("Angina no esforço", "% com exang = 1"),
            ("Idade mediana", "Anos"), ("Colesterol mediano", "mg/dL"), ("FC máxima mediana", "bpm")]):
            row, col = divmod(i, 3)
            box(c, x + col * (cardw + 12), h - 204 - row * 65, cardw, 55, title, body)
        half = (width - 14) / 2
        box(c, x, 205, half, 105, "Barras por sexo", "% positivo dentro do grupo; denominador visível.")
        box(c, x + half + 14, 205, half, 105, "Barras por faixa etária", "Contagem ou proporção por desfecho; faixas ordenadas.")
        box(c, x, 96, width, 98, "Dispersão: colesterol x frequência cardíaca máxima", "Cor pelo desfecho; tooltip com idade e medidas. Público: coordenadores de pesquisa cardiovascular.")
    text(c, x, 72, "Expander: dados públicos do recorte, método e download CSV", width, 9)
    text(c, 28, 30, "Rascunho esquemático, não captura de tela. Gráficos e cartões se adaptam à largura disponível no app.", w - 56, 8, color=MUTED)
    c.showPage(); c.save()


if __name__ == "__main__":
    (ROOT / "entregas").mkdir(exist_ok=True)
    sketch(1)
    sketch(2)
    print("Dois rascunhos de dashboards gerados.")
