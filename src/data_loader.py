"""Dados locais exportados pelo notebook da Aula 11."""
# [IA] Codex/OpenAI - leitura local, cache e verificação do esquema público.
from pathlib import Path

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
VARS_QUANT = ["age", "trestbps", "chol", "thalach", "oldpeak"]
LABELS = {
    "age": "Idade (anos)",
    "trestbps": "Pressão em repouso (mmHg)",
    "chol": "Colesterol (mg/dL)",
    "thalach": "Frequência cardíaca máxima (bpm)",
    "oldpeak": "Depressão do segmento ST",
}


@st.cache_data(ttl=300, max_entries=2)
def load_data() -> pd.DataFrame:
    """Lê somente o tratado; os filtros não alteram o CSV."""
    path = ROOT / "data" / "clean" / "dataset.csv"
    df = pd.read_csv(path)
    required = VARS_QUANT + ["doenca_cardiaca", "exang", "sexo_label", "faixa_etaria"]
    missing = set(required) - set(df.columns)
    if missing:
        raise ValueError(f"Colunas ausentes no CSV tratado: {', '.join(sorted(missing))}")
    if df.empty:
        raise ValueError("O dataset tratado está vazio. Execute o notebook da EDA.")
    if df[required].isna().any().any():
        raise ValueError("Há valores ausentes nas colunas do painel. Revise a EDA.")
    # Apenas o esquema público conhecido chega ao app; colunas extras não são expostas.
    return df[required].copy()
