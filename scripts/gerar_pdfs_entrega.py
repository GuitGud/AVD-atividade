"""Gera dois rascunhos vetoriais e um exemplo fictício de declaração."""
# [IA] Codex/OpenAI - diagramação dos rascunhos e do exemplo fictício.
from pathlib import Path
import re
from xml.sax.saxutils import escape
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle

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
        box(c, x, h - 188, width, 40, "Controles do laboratório", "Método de correlação / máximo de classes / separar desfechos")
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


def example_pdf():
    out = ROOT / "prompts/EXEMPLO_FICTICIO_DECLARACAO_IA.pdf"
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="BodyCustom", fontName="Helvetica", fontSize=10, leading=14, spaceAfter=9, textColor=INK))
    styles.add(ParagraphStyle(name="TitleCustom", fontName="Helvetica-Bold", fontSize=21, leading=25, spaceAfter=15, textColor=INK))
    styles.add(ParagraphStyle(name="LabelCustom", fontName="Helvetica-Bold", fontSize=12, leading=16, spaceBefore=12, spaceAfter=8, textColor=ACCENT))
    doc = SimpleDocTemplate(str(out), pagesize=A4, leftMargin=46, rightMargin=46, topMargin=65, bottomMargin=55)
    story = []
    def p(s, style="BodyCustom"):
        story.append(Paragraph(s, styles[style]))
    def heading(s): p(s, "LabelCustom")
    p("EXEMPLO FICTÍCIO<br/>Declaração de uso de IA", "TitleCustom")
    p("<b>NÃO É REGISTRO REAL. NÃO ASSINAR NEM ENTREGAR COMO DECLARAÇÃO VERDADEIRA.</b>")
    p("Este modelo foi inventado para ilustrar a organização do template da atividade Streamlit AVD 2026.2. Não reproduz a conversa real, não comprova escolhas do aluno e não substitui o documento verdadeiro e assinado, que será elaborado pessoalmente por ele.")
    heading("1. Identificação - exemplo")
    for s in ["Aluno: estudante fictício", "Turma e e-mail: não preenchidos", "Projeto ilustrativo: dois dashboards Heart Disease", "Data ilustrativa: 29/10/2026"]: p(s)
    heading("2 e 3. Diretrizes e declaração geral")
    p("Num registro verdadeiro, o aluno precisa declarar fielmente quais usos ocorreram, conferir as diretrizes da professora e assinalar somente uma opção que corresponda à realidade. Nenhuma opção de veracidade é assinalada neste exemplo.")
    heading("4. Ferramentas - cenário fictício")
    p("Assistente de programação: Codex/OpenAI; versão e plano não especificados. Skill oficial do Streamlit: developing-with-streamlit. Apoio ilustrativo: estrutura de layout, sintaxe dos gráficos e depuração.")
    story.append(PageBreak())
    heading("5. Registro de usos - diálogo inteiramente inventado")
    md = (ROOT / "prompts/exemplo-dialogo-ficticio.md").read_text(encoding="utf-8")
    dialogue = md.split("## Diálogo ilustrativo", 1)[1].split("## Como aproveitar", 1)[0]
    for para in dialogue.strip().split("\n\n"):
        safe = escape(para.strip())
        safe = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", safe)
        p(safe)
    story.append(PageBreak())
    heading("5. Exemplo de bloco de registro - fictício")
    for label, body in [
        ("Data / ferramenta", "29/10/2026 / assistente fictício de programação"),
        ("Parte da atividade", "Sintaxe do mapa de calor e dos histogramas"),
        ("Finalidade ilustrada", "Implementar os tipos de gráfico já definidos no diálogo fictício."),
        ("Pedido inventado", "Desenhar o mapa com escala fixa e gerar um histograma por medida."),
        ("Aproveitamento hipotético", "No exemplo, o aluno aproveita a sintaxe e ajusta textos e cores."),
        ("Verificação hipotética", "Num caso real, registrar os testes efetivamente realizados e seus resultados."),
        ("Anexo", "Diálogo fictício das páginas anteriores; não há link de conversa real.")]:
        p(f"<b>{label}:</b> {body}")
    heading("6. Trechos com apoio de IA - exemplo")
    p("Em um registro verdadeiro, marcar cada trecho apoiado com # [IA] ferramenta - finalidade e relacionar os arquivos correspondentes. O exemplo de anotação não prova autoria nem validação.")
    heading("7. Reflexão individual")
    p("Não foi redigida uma reflexão em nome do aluno. No documento real, ele escreverá pessoalmente de 10 a 15 linhas sobre o uso que efetivamente fez, as escolhas das métricas, as alterações e a conferência do trabalho.")
    heading("8. Termo de responsabilidade e assinatura")
    p("Não há termo de autenticidade preenchido nem assinatura simulada. O aluno produzirá e assinará pessoalmente sua declaração real como prompts/DECLARACAO_IA.pdf, seguindo o template da professora.")
    def page(c, doc):
        w, h = A4
        c.setFillColor(ACCENT); c.rect(0, h - 36, w, 36, fill=1, stroke=0)
        c.setFillColor(colors.white); c.setFont("Helvetica-Bold", 9)
        c.drawCentredString(w / 2, h - 23, "EXEMPLO FICTÍCIO - NÃO É DECLARAÇÃO REAL")
        c.setFillColor(MUTED); c.setFont("Helvetica", 8)
        c.drawString(46, 29, "Modelo ilustrativo sem assinatura - AVD 2026.2")
        c.drawRightString(w - 46, 29, str(doc.page))
    doc.build(story, onFirstPage=page, onLaterPages=page)


if __name__ == "__main__":
    (ROOT / "entregas").mkdir(exist_ok=True)
    sketch(1)
    sketch(2)
    example_pdf()
    print("Dois rascunhos e um exemplo fictício gerados.")
