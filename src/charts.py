"""Especificações Altair compartilhadas pelos dois dashboards."""
# [IA] Codex/OpenAI - sintaxe dos gráficos, escalas, rótulos e tooltips.
import altair as alt
from src.analytics import AGE_ORDER, CLASSES, correlation_table, grouped_outcomes
from src.data_loader import LABELS

SHORT_LABELS = {"age": "Idade", "trestbps": "Pressão", "chol": "Colesterol",
                "thalach": "FC máxima", "oldpeak": "Depressão ST"}
CLASS_SCALE = alt.Scale(domain=CLASSES, range=["#81AAA6", "#B44938"])


def heatmap(df, variables, method):
    table = correlation_table(df, variables, method)
    table["medida_x"] = table["x"].map(SHORT_LABELS)
    table["medida_y"] = table["y"].map(SHORT_LABELS)
    order = [SHORT_LABELS[x] for x in variables]
    base = alt.Chart(table).encode(
        x=alt.X("medida_x:N", sort=order, title=None, axis=alt.Axis(labelAngle=-25)),
        y=alt.Y("medida_y:N", sort=order, title=None),
        tooltip=[alt.Tooltip("medida_x:N", title="Medida 1"), alt.Tooltip("medida_y:N", title="Medida 2"),
                 alt.Tooltip("r:Q", title="Correlação", format=".3f"), alt.Tooltip("pares:Q", title="Pares válidos")])
    color = alt.Color("r:Q", title="Coeficiente", scale=alt.Scale(domain=[-1, 0, 1], range=["#276D82", "#F7F3ED", "#B44938"]))
    squares = base.mark_rect(stroke="white", strokeWidth=2).encode(color=alt.condition("isValid(datum.r)", color, alt.value("#E1DDD6")))
    labels = base.mark_text(fontSize=14).encode(text="rotulo:N", color=alt.condition("abs(datum.r) >= 0.65", alt.value("white"), alt.value("#302B29")))
    return (squares + labels).properties(height=345)


def histogram(df, variable, bins, by_class):
    chart = alt.Chart(df).mark_bar(opacity=0.78, binSpacing=1).encode(
        x=alt.X(f"{variable}:Q", bin=alt.Bin(maxbins=bins), title=LABELS[variable]),
        y=alt.Y("count():Q", title="Pacientes", axis=alt.Axis(tickMinStep=1)),
        tooltip=[alt.Tooltip(f"{variable}:Q", bin=alt.Bin(maxbins=bins), title=LABELS[variable]), alt.Tooltip("count():Q", title="Pacientes")])
    if by_class:
        chart = chart.encode(color=alt.Color("doenca_cardiaca:N", title="Desfecho", scale=CLASS_SCALE), y=alt.Y("count():Q", stack="zero", title="Pacientes"))
    else:
        chart = chart.encode(color=alt.value("#B44938"))
    return chart.properties(height=230)


def sex_comparison(df):
    table = grouped_outcomes(df, "sexo_label")
    table = table.loc[(table["doenca_cardiaca"] == "Cardíaco") & (table["total_grupo"] > 0)]
    base = alt.Chart(table).encode(
        y=alt.Y("sexo_label:N", title=None),
        x=alt.X("proporcao:Q", title="Diagnóstico positivo no grupo", scale=alt.Scale(domain=[0, 1]), axis=alt.Axis(format=".0%")),
        tooltip=[alt.Tooltip("sexo_label:N", title="Sexo registrado"), alt.Tooltip("pacientes:Q", title="Positivos"),
                 alt.Tooltip("total_grupo:Q", title="Pacientes no grupo"), alt.Tooltip("proporcao:Q", title="Proporção", format=".1%")])
    return (base.mark_bar(color="#B44938", cornerRadiusEnd=4) + base.mark_text(align="left", dx=5, color="#302B29").encode(text=alt.Text("proporcao:Q", format=".1%"))).properties(height=245)


def age_composition(df, percent):
    table = grouped_outcomes(df, "faixa_etaria")
    chart = alt.Chart(table).mark_bar(cornerRadiusTopLeft=3, cornerRadiusTopRight=3).encode(
        x=alt.X("faixa_etaria:N", title="Faixa etária (anos)", sort=AGE_ORDER),
        color=alt.Color("doenca_cardiaca:N", title="Desfecho", scale=CLASS_SCALE),
        tooltip=[alt.Tooltip("faixa_etaria:N", title="Faixa"), alt.Tooltip("doenca_cardiaca:N", title="Desfecho"),
                 alt.Tooltip("pacientes:Q", title="Pacientes"), alt.Tooltip("total_grupo:Q", title="Total na faixa"),
                 alt.Tooltip("proporcao:Q", title="Proporção na faixa", format=".1%")])
    y = alt.Y("pacientes:Q", stack="normalize" if percent else "zero", title="Proporção na faixa" if percent else "Pacientes")
    if percent:
        y = y.axis(format=".0%")
    return chart.encode(y=y).properties(height=245)


def exams_scatter(df):
    return alt.Chart(df).mark_circle(size=70, opacity=0.7, stroke="white", strokeWidth=0.4).encode(
        x=alt.X("chol:Q", title=LABELS["chol"], scale=alt.Scale(zero=False)),
        y=alt.Y("thalach:Q", title=LABELS["thalach"], scale=alt.Scale(zero=False)),
        color=alt.Color("doenca_cardiaca:N", title="Desfecho", scale=CLASS_SCALE),
        tooltip=[alt.Tooltip("age:Q", title="Idade"), alt.Tooltip("chol:Q", title="Colesterol (mg/dL)"),
                 alt.Tooltip("thalach:Q", title="FC máxima (bpm)"), alt.Tooltip("doenca_cardiaca:N", title="Desfecho")]).properties(height=310).interactive()
