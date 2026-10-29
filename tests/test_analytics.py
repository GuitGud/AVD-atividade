"""Casos pequenos com resultados conhecidos, independentes da interface."""
# [IA] Codex/OpenAI - verificação das fórmulas, denominadores e extremos.
import unittest
import numpy as np
import pandas as pd
from src.analytics import compute_kpis, correlation_table, filter_data, grouped_outcomes


class AnalyticsTest(unittest.TestCase):
    def setUp(self):
        self.df = pd.DataFrame({
            "age": [40, 50, 60], "chol": [100, 200, 900], "thalach": [180, 150, 120],
            "exang": [0, 1, 1], "doenca_cardiaca": ["Normal", "Cardíaco", "Cardíaco"],
            "sexo_label": ["Feminino", "Masculino", "Masculino"], "faixa_etaria": ["<45", "45-54", "55-64"]})

    def test_formulas_nao_confundem_mediana_e_media(self):
        k = compute_kpis(self.df)
        self.assertAlmostEqual(k["diagnostico_pct"], 200 / 3)
        self.assertAlmostEqual(k["angina_pct"], 200 / 3)
        self.assertEqual(k["idade_mediana"], 50)
        self.assertEqual(k["colesterol_mediano"], 200)
        self.assertEqual(k["fc_mediana"], 150)

    def test_amostra_vazia_nao_vira_zero(self):
        k = compute_kpis(self.df.iloc[:0])
        self.assertIsNone(k["diagnostico_pct"])
        self.assertIsNone(k["colesterol_mediano"])
        self.assertEqual(k["n"], 0)

    def test_limites_inclusivos_e_sem_mutacao(self):
        before = self.df.copy(deep=True)
        filtered = filter_data(self.df, {"age": (40, 50), "chol": (100, 200)}, ["Normal", "Cardíaco"])
        self.assertEqual(filtered.index.tolist(), [0, 1])
        pd.testing.assert_frame_equal(before, self.df)

    def test_denominador_e_do_grupo(self):
        table = grouped_outcomes(self.df, "sexo_label")
        men = table[(table.sexo_label == "Masculino") & (table.doenca_cardiaca == "Cardíaco")].iloc[0]
        self.assertEqual(men.total_grupo, 2)
        self.assertEqual(men.proporcao, 1)
        age = grouped_outcomes(self.df, "faixa_etaria")
        self.assertEqual(age.pacientes.sum(), 3)
        self.assertTrue((age.loc[age.faixa_etaria == "65+", "pacientes"] == 0).all())

    def test_correlacao_constante_e_indefinida(self):
        df = pd.DataFrame({"constante": [1, 1, 1], "a": [1, 2, 3], "b": [3, 2, 1]})
        for method in ["pearson", "spearman", "kendall"]:
            t = correlation_table(df, ["constante", "a", "b"], method)
            value = t.loc[(t.x == "a") & (t.y == "b"), "r"].iloc[0]
            self.assertAlmostEqual(value, -1)
            self.assertTrue(np.isnan(t.loc[(t.x == "constante") & (t.y == "a"), "r"].iloc[0]))


if __name__ == "__main__":
    unittest.main()
