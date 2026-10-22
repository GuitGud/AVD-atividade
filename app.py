"""Aula 21: estrutura do Dashboard 1, com filtros e espaços para gráficos."""
import streamlit as st

from src.data_loader import LABELS, VARS_QUANT, load_data

NOMES_CURTOS = {
    "age": "Idade", "trestbps": "Pressão", "chol": "Colesterol",
    "thalach": "FC máxima", "oldpeak": "Depressão ST",
}

st.set_page_config(
    page_title="Heart Disease | Aula 21",
    page_icon=":material/monitor_heart:",
    layout="wide",
)

st.caption("ANÁLISE E VISUALIZAÇÃO DE DADOS · AULA 21")
st.title("Heart Disease: exploração das variáveis")
st.markdown(
    "Escolha as medidas e ajuste os intervalos para preparar a análise "
    "de **correlação** e **distribuição** dos pacientes."
)

try:
    df = load_data()
except (OSError, ValueError) as error:
    st.error(f"Não foi possível carregar os dados: {error}")
    st.info("Execute notebooks/eda.ipynb para gerar data/clean/dataset.csv.")
    st.stop()

with st.sidebar:
    st.header("Filtros", anchor=False)
    variaveis = st.multiselect(
        "Variáveis da correlação",
        options=VARS_QUANT,
        default=VARS_QUANT,
        format_func=lambda col: NOMES_CURTOS[col],
        key="variaveis",
        help="Selecione pelo menos duas medidas para a futura matriz de correlação.",
    )
    st.caption("Os intervalos são combinados: o paciente deve atender a todos eles.")
    intervalos = {}
    for var in variaveis:
        minimo, maximo = float(df[var].min()), float(df[var].max())
        # chaves estáveis preservam cada intervalo entre reexecuções.
        intervalos[var] = st.slider(
            LABELS[var],
            min_value=minimo,
            max_value=maximo,
            value=(minimo, maximo),
            step=0.1 if var == "oldpeak" else 1.0,
            format="%.1f" if var == "oldpeak" else "%.0f",
            key=f"intervalo_{var}",
        )
    st.divider()
    st.caption("Fonte: UCI · Cleveland Heart Disease")
    st.caption("Guilherme Alcoforado Rabelo · 2026.2")

df_filtrado = df.copy()
for var, (inicio, fim) in intervalos.items():
    df_filtrado = df_filtrado.loc[df_filtrado[var].between(inicio, fim)]

st.caption(
    f"{len(df_filtrado)} de {len(df)} pacientes no recorte · "
    f"{len(variaveis)} variáveis selecionadas"
)
if df_filtrado.empty:
    st.warning("Nenhum paciente atende a todos os intervalos. Amplie os filtros.")

correlacao, distribuicao = st.columns(2, gap="large")
with correlacao, st.container(border=True, height="stretch"):
    st.subheader("Correlação", anchor=False)
    if len(variaveis) < 2:
        st.warning("Selecione pelo menos duas variáveis na barra lateral.")
    else:
        st.markdown("**Como as medidas se relacionam?**")
        st.caption("Medidas: " + ", ".join(LABELS[var] for var in variaveis))
        st.info("Espaço reservado para o heatmap na próxima aula.")
        # Aula 22: calcular a correlação usando df_filtrado[variaveis].

with distribuicao, st.container(border=True, height="stretch"):
    st.subheader("Distribuição", anchor=False)
    if variaveis:
        variavel_distribuicao = st.selectbox(
            "Medida para distribuição",
            options=variaveis,
            format_func=lambda col: LABELS[col],
            key="variavel_distribuicao",
        )
        st.info("Espaço reservado para o histograma na próxima aula.")
        # Aula 22: desenhar o histograma de df_filtrado[variavel_distribuicao].
    else:
        st.warning("Selecione uma variável na barra lateral.")

with st.expander("Conferir os dados do recorte"):
    st.caption("Prévia dos primeiros 20 pacientes; nenhum filtro altera o arquivo original.")
    colunas = variaveis + ["doenca_cardiaca"]
    st.dataframe(
        df_filtrado[colunas].head(20),
        hide_index=True,
        width="stretch",
        column_config={col: LABELS[col] for col in variaveis},
        alt="Prévia dos pacientes que atendem aos filtros selecionados",
    )

st.caption("Etapa 1/3 · Esqueleto funcional. Os gráficos serão adicionados na Aula 22.")
