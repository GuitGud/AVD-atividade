"""Cálculos descritivos, sem diagnóstico ou recomendação clínica."""
# [IA] Codex/OpenAI - implementação dos cálculos e validações técnicas.
from collections.abc import Mapping, Sequence
import numpy as np
import pandas as pd

AGE_ORDER = ["<45", "45-54", "55-64", "65+"]
CLASSES = ["Normal", "Cardíaco"]


def filter_data(df: pd.DataFrame, intervals: Mapping, classes: Sequence[str]) -> pd.DataFrame:
    """Combina limites inclusivos com E e aplica o filtro de desfecho."""
    mask = df["doenca_cardiaca"].isin(classes)
    for column, (lower, upper) in intervals.items():
        mask &= df[column].between(lower, upper, inclusive="both")
    return df.loc[mask].copy()


def compute_kpis(df: pd.DataFrame) -> dict:
    """Conjunto A escolhido pelo aluno; percentuais usam todo o recorte."""
    n = len(df)
    return {
        "n": n,
        "positivos": int(df["doenca_cardiaca"].eq("Cardíaco").sum()),
        "diagnostico_pct": 100 * df["doenca_cardiaca"].eq("Cardíaco").mean() if n else None,
        "angina_n": int(df["exang"].eq(1).sum()),
        "angina_pct": 100 * df["exang"].eq(1).mean() if n else None,
        "idade_mediana": float(df["age"].median()) if n else None,
        "colesterol_mediano": float(df["chol"].median()) if n else None,
        "fc_mediana": float(df["thalach"].median()) if n else None,
    }


def correlation_table(df: pd.DataFrame, variables: Sequence[str], method: str) -> pd.DataFrame:
    """Coeficientes indefinidos permanecem NaN, nunca são substituídos por zero."""
    corr = df[list(variables)].corr(method=method)
    records = []
    for y in variables:
        for x in variables:
            r = corr.loc[y, x]
            records.append({"x": x, "y": y, "r": r,
                            "rotulo": f"{r:.2f}" if pd.notna(r) else "—",
                            "pares": int(df[[x, y]].dropna().shape[0])})
    return pd.DataFrame(records)


def grouped_outcomes(df: pd.DataFrame, group: str) -> pd.DataFrame:
    """Completa combinações ausentes com zero, sem criar observações."""
    groups = AGE_ORDER if group == "faixa_etaria" else ["Feminino", "Masculino"]
    index = pd.MultiIndex.from_product([groups, CLASSES], names=[group, "doenca_cardiaca"])
    counts = df.groupby([group, "doenca_cardiaca"], observed=True).size().reindex(index, fill_value=0)
    table = counts.rename("pacientes").reset_index()
    table["total_grupo"] = table.groupby(group)["pacientes"].transform("sum")
    table["proporcao"] = table["pacientes"].div(table["total_grupo"].replace(0, np.nan)).fillna(0)
    return table
