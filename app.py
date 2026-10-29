"""Heart Disease: laboratório e painel de pesquisa cardiovascular."""
# [IA] Codex/OpenAI - estrutura Streamlit, widgets e integração dos dashboards.
import streamlit as st
from src.analytics import CLASSES, compute_kpis, filter_data
from src.charts import SHORT_LABELS, age_composition, exams_scatter, heatmap, histogram, sex_comparison
from src.data_loader import LABELS, VARS_QUANT, load_data

st.set_page_config(page_title="Heart Disease | AVD", page_icon=":material/monitor_heart:", layout="wide")
st.caption("AVD · 2026.2 / CLEVELAND HEART DISEASE")
st.title("Da exploração ao panorama da amostra")
st.markdown("Um laboratório para investigar as medidas e um painel para **coordenadores de pesquisa cardiovascular**.")
try:
    df = load_data()
except (OSError, ValueError) as error:
    st.error(f"Não foi possível carregar os dados: {error}")
    st.info("Execute notebooks/eda.ipynb para gerar data/clean/dataset.csv.")
    st.stop()

# [IA] Codex/OpenAI - reinicialização explícita dos filtros.
def reset_filters():
    st.session_state["variaveis"] = VARS_QUANT.copy()
    st.session_state["classes"] = CLASSES.copy()
    for var in VARS_QUANT:
        st.session_state[f"intervalo_{var}"] = (float(df[var].min()), float(df[var].max()))


# Inicializar o estado antes dos widgets evita dois valores-padrão concorrentes.
st.session_state.setdefault("variaveis", VARS_QUANT.copy())
st.session_state.setdefault("classes", CLASSES.copy())

with st.sidebar:
    st.header("Recorte da amostra", anchor=False)
    st.caption("Os mesmos filtros alimentam os dois dashboards.")
    variaveis = st.multiselect("Variáveis quantitativas", VARS_QUANT,
                              format_func=lambda x: SHORT_LABELS[x], key="variaveis")
    classes = st.multiselect("Desfecho registrado", CLASSES, key="classes")
    intervalos = {}
    for var in variaveis:
        lower, upper = float(df[var].min()), float(df[var].max())
        st.session_state.setdefault(f"intervalo_{var}", (lower, upper))
        intervalos[var] = st.slider(LABELS[var], min_value=lower, max_value=upper,
                                   step=0.1 if var == "oldpeak" else 1.0,
                                   format="%.1f" if var == "oldpeak" else "%.0f", key=f"intervalo_{var}")
    st.button("Restaurar filtros", on_click=reset_filters, key="reset", width="stretch", icon=":material/restart_alt:")
    st.caption("Intervalos inclusivos, combinados com E. Desmarcar uma medida retira também seu filtro.")
    st.divider()
    st.caption("Fonte: UCI · Cleveland · 303 registros originais / 297 completos.")
    st.link_button("Fonte e dicionário dos dados", "https://archive.ics.uci.edu/dataset/45/heart+disease", width="stretch")

recorte = filter_data(df, intervalos, classes)
st.caption(f"{len(recorte)} de {len(df)} pacientes no recorte · {len(variaveis)} variáveis selecionadas")
if recorte.empty:
    st.warning("Nenhum paciente atende aos filtros. Amplie os intervalos ou restaure os filtros.")
# 297 linhas: a preparação dos dois painéis é barata; as abas usam a mesma amostra.
lab, painel = st.tabs(["Dashboard 1 · Laboratório", "Dashboard 2 · Panorama da pesquisa"], key="dashboards")
with lab:
    st.header("Distribuição e correlação", anchor=False)
    st.caption("Compare métodos e remova extremos temporariamente. Correlação não estabelece causalidade.")
    config1, config2, config3 = st.columns([1.3, 1, 1], vertical_alignment="bottom")
    with config1:
        method = st.selectbox("Método de correlação", ["Spearman", "Pearson", "Kendall"], key="metodo")
    with config2:
        bins = st.slider("Máximo de classes do histograma", 5, 50, 20, 5, key="bins")
    with config3:
        separate = st.toggle("Separar histogramas por desfecho", key="separar_classe")
    with st.container(border=True):
        st.subheader("Mapa de correlação", anchor=False)
        if len(variaveis) < 2:
            st.info("Selecione pelo menos duas variáveis para calcular a correlação.")
        elif len(recorte) < 2:
            st.info("São necessários pelo menos dois pacientes no recorte para a correlação.")
        else:
            st.altair_chart(heatmap(recorte, variaveis, method.lower()), width="stretch", key="heatmap",
                            alt=f"Matriz de correlação de {method} entre as medidas selecionadas no recorte")
            if recorte[variaveis].nunique().lt(2).any():
                st.caption("— indica coeficiente indefinido: uma das medidas é constante no recorte.")
        st.caption("Escala fixa de -1 a +1 · cada célula mostra o coeficiente; o tooltip informa o número de pares.")
    st.subheader("Um histograma por medida", anchor=False)
    if not variaveis:
        st.info("Selecione uma medida na barra lateral para visualizar sua distribuição.")
    elif recorte.empty:
        st.info("Não há observações para os histogramas neste recorte.")
    else:
        for i in range(0, len(variaveis), 2):
            for container, var in zip(st.columns(2), variaveis[i:i + 2]):
                with container, st.container(border=True):
                    st.markdown(f"**{LABELS[var]}**")
                    st.altair_chart(histogram(recorte, var, bins, separate), width="stretch", key=f"hist_{var}",
                                    alt=f"Distribuição de {LABELS[var]} entre os pacientes do recorte")
    st.caption("O controle define o máximo de classes; o Altair ajusta os limites para facilitar a leitura. Cores empilhadas representam contagens por desfecho.")

with painel:
    st.header("Perfil do recorte para pesquisa", anchor=False)
    st.caption("Público-alvo: coordenadores de pesquisa cardiovascular. Indicadores descritivos do conjunto A selecionado pelo aluno.")
    kpis = compute_kpis(recorte)
    specs = [
        ("Diagnóstico positivo", "diagnostico_pct", "%", "100 × registros Cardíaco / total do recorte. Não é prevalência populacional."),
        ("Angina no esforço", "angina_pct", "%", "100 × registros com exang = 1 / total do recorte."),
        ("Idade mediana", "idade_mediana", "anos", "Mediana de age no recorte; não é média."),
        ("Colesterol mediano", "colesterol_mediano", "mg/dL", "Mediana de chol no recorte; não aplica limiares clínicos."),
        ("FC máxima mediana", "fc_mediana", "bpm", "Mediana de thalach no recorte; medida registrada no teste."),
    ]
    with st.container(horizontal=True):
        for label, field, unit, help_text in specs:
            value = "Sem dados" if kpis[field] is None else f"{kpis[field]:.1f}".replace(".", ",") + f" {unit}"
            st.metric(label, value, help=help_text, border=True, width=205)
    st.caption(f"Base de cálculo: {kpis['n']} pacientes · {kpis['positivos']} com diagnóstico positivo · {kpis['angina_n']} com angina no esforço.")
    if recorte.empty:
        st.info("Os três visuais do panorama reaparecem quando houver pacientes no recorte.")
    else:
        left, right = st.columns(2, gap="large")
        with left, st.container(border=True):
            st.subheader("Diagnóstico por sexo registrado", anchor=False)
            st.caption("Percentual positivo dentro de cada grupo; o tooltip mostra o denominador.")
            st.altair_chart(sex_comparison(recorte), width="stretch", key="sexo_chart",
                            alt="Percentual de diagnóstico positivo por sexo registrado, com contagens e denominadores")
        with right, st.container(border=True):
            st.subheader("Composição por faixa etária", anchor=False)
            percent = st.toggle("Mostrar proporções por faixa", key="faixas_percentual")
            st.altair_chart(age_composition(recorte, percent), width="stretch", key="idade_chart",
                            alt="Composição dos desfechos em quatro faixas etárias; contagens ou proporções dentro de cada faixa")
        with st.container(border=True):
            st.subheader("Colesterol e resposta ao esforço", anchor=False)
            st.caption("Cada ponto é um registro público. Amplie o gráfico com o mouse para explorar sobreposições.")
            st.altair_chart(exams_scatter(recorte), width="stretch", key="exames_chart",
                            alt="Colesterol e frequência cardíaca máxima, com cor pelo desfecho registrado")
    st.info("Base clínica histórica e selecionada: os percentuais descrevem este recorte e não estimam o risco da população. Os gráficos não orientam diagnóstico ou conduta.")

with st.expander("Dados, métodos e transparência"):
    st.markdown("O tratamento removeu seis registros sem `ca` ou `thal`. Outliers foram preservados. Os filtros não modificam os arquivos.")
    st.caption("Prévia dos primeiros 20 registros públicos do recorte; sem nomes, contatos ou identificadores pessoais.")
    cols = variaveis + ["doenca_cardiaca"]
    st.dataframe(recorte[cols].head(20), hide_index=True, width="stretch",
                 column_config={c: LABELS[c] for c in variaveis}, alt="Prévia dos registros públicos que atendem aos filtros")
    st.download_button("Baixar recorte em CSV", recorte[cols].to_csv(index=False).encode("utf-8"),
                       file_name="heart_disease_recorte.csv", mime="text/csv", key="download_recorte")
    st.caption("Apoio de IA na implementação: trechos marcados com [IA]. O registro ilustrativo em prompts/ é fictício; a declaração real será elaborada pelo aluno.")
st.caption("Guilherme Alcoforado Rabelo · AVD 2026.2 · UCI Heart Disease")
