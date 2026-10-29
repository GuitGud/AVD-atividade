"""Gera prévias estáticas dos gráficos reais, sem simular captura do navegador."""
# [IA] Codex/OpenAI - exportação das especificações Altair para revisão visual.
import json
from pathlib import Path
import sys
import pandas as pd
import vl_convert as vlc

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.analytics import compute_kpis
from src.charts import age_composition, exams_scatter, heatmap, histogram, sex_comparison
from src.data_loader import VARS_QUANT

out = ROOT / "entregas" / "previews"
out.mkdir(parents=True, exist_ok=True)
df = pd.read_csv(ROOT / "data/clean/dataset.csv")
charts = {"correlacao": heatmap(df, VARS_QUANT, "spearman")}
charts.update({f"histograma-{v}": histogram(df, v, 20, False) for v in VARS_QUANT})
charts.update({"sexo": sex_comparison(df), "faixas-etarias": age_composition(df, False), "dispersao-exames": exams_scatter(df)})
for name, chart in charts.items():
    spec = chart.properties(width=600).to_dict()
    (out / f"{name}.png").write_bytes(vlc.vegalite_to_png(spec, scale=1.5))
(out / "kpis.json").write_text(json.dumps(compute_kpis(df), ensure_ascii=False, indent=2), encoding="utf-8")
print(f"{len(charts)} gráficos reais exportados para {out}")
