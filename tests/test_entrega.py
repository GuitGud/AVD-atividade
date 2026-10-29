"""Validações dos dados exportados e dos filtros interativos da entrega."""
# [IA] Codex/OpenAI - testes de regressão dos dados e interações do Streamlit.
import unittest
from pathlib import Path

import numpy as np
import pandas as pd
from streamlit.testing.v1 import AppTest

ROOT = Path(__file__).resolve().parents[1]


class EntregaTest(unittest.TestCase):
    def test_tratamento_reproduz_eda(self):
        original = pd.read_csv(ROOT / "data/raw/dataset_original.csv")
        tratado = pd.read_csv(ROOT / "data/clean/dataset.csv")
        self.assertEqual(original.shape, (303, 14))
        self.assertEqual(len(tratado), 297)
        self.assertEqual(original["ca"].isna().sum(), 4)
        self.assertEqual(original["thal"].isna().sum(), 2)
        esperado = original.dropna(subset=["ca", "thal"]).reset_index(drop=True)
        pd.testing.assert_frame_equal(tratado[esperado.columns.drop("num")], esperado.drop(columns="num"))
        self.assertEqual(tratado["doenca_cardiaca"].tolist(), np.where(esperado["num"] > 0, "Cardíaco", "Normal").tolist())
        np.testing.assert_allclose(tratado["chol_log"], np.log1p(esperado["chol"]))
        self.assertFalse(tratado.isna().any().any())

    def test_app_inicia_com_todos_os_pacientes(self):
        app = AppTest.from_file(str(ROOT / "app.py")).run()
        self.assertFalse(app.exception)
        self.assertEqual(len(app.slider), 6)
        self.assertEqual(len(app.tabs), 2)
        self.assertEqual(len(app.metric), 5)
        self.assertEqual(len(app.get("vega_lite_chart")), 9)
        self.assertTrue(any("297 de 297" in c.value for c in app.caption))

    def test_intervalos_combinados_inclusivos(self):
        app = AppTest.from_file(str(ROOT / "app.py")).run()
        app.slider(key="intervalo_age").set_value((45.0, 60.0))
        app.slider(key="intervalo_chol").set_value((200.0, 260.0)).run()
        df = pd.read_csv(ROOT / "data/clean/dataset.csv")
        esperado = df[df.age.between(45, 60) & df.chol.between(200, 260)]
        self.assertFalse(app.exception)
        self.assertTrue(any(f"{len(esperado)} de 297" in c.value for c in app.caption))
        pd.testing.assert_frame_equal(
            app.dataframe[0].value.reset_index(drop=True),
            esperado[["age", "trestbps", "chol", "thalach", "oldpeak", "doenca_cardiaca"]].head(20).reset_index(drop=True),
        )

    def test_sem_variaveis(self):
        app = AppTest.from_file(str(ROOT / "app.py")).run()
        app.multiselect(key="variaveis").set_value([]).run()
        self.assertFalse(app.exception)
        self.assertEqual(len(app.slider), 1)
        self.assertTrue(any("duas variáveis" in w.value for w in app.info))
        self.assertEqual(len(app.get("vega_lite_chart")), 3)

    def test_recorte_vazio(self):
        app = AppTest.from_file(str(ROOT / "app.py")).run()
        app.slider(key="intervalo_age").set_value((29.0, 29.0))
        app.slider(key="intervalo_chol").set_value((564.0, 564.0)).run()
        self.assertFalse(app.exception)
        self.assertTrue(any("Nenhum paciente" in w.value for w in app.warning))
        self.assertEqual(len(app.dataframe[0].value), 0)
        self.assertTrue(all(m.value == "Sem dados" for m in app.metric))
        self.assertEqual(len(app.get("vega_lite_chart")), 0)

    def test_selecao_reduzida_e_intervalo_persistente(self):
        app = AppTest.from_file(str(ROOT / "app.py")).run()
        app.slider(key="intervalo_age").set_value((45.0, 60.0)).run()
        app.multiselect(key="variaveis").set_value(["age"]).run()
        self.assertFalse(app.exception)
        self.assertEqual(tuple(app.slider(key="intervalo_age").value), (45.0, 60.0))
        self.assertTrue(any("duas variáveis" in w.value for w in app.info))

    def test_filtro_de_desfecho_e_reset(self):
        app = AppTest.from_file(str(ROOT / "app.py"), default_timeout=15).run()
        app.multiselect(key="classes").set_value(["Cardíaco"]).run()
        self.assertFalse(app.exception)
        self.assertEqual(app.metric[0].value, "100,0 %")
        self.assertTrue(any("137 de 297" in c.value for c in app.caption))
        app.slider(key="intervalo_age").set_value((45.0, 60.0)).run()
        app.button(key="reset").click().run()
        self.assertFalse(app.exception)
        self.assertEqual(app.multiselect(key="classes").value, ["Normal", "Cardíaco"])
        self.assertEqual(app.slider(key="intervalo_age").value, (29.0, 77.0))
        self.assertEqual(app.metric[0].value, "46,1 %")

    def test_widgets_dos_dois_dashboards(self):
        app = AppTest.from_file(str(ROOT / "app.py"), default_timeout=15).run()
        for method in ["Pearson", "Kendall", "Spearman"]:
            app.selectbox(key="metodo").set_value(method).run()
            self.assertFalse(app.exception)
        app.slider(key="bins").set_value(35).run()
        app.toggle(key="separar_classe").set_value(True).run()
        app.toggle(key="faixas_percentual").set_value(True).run()
        self.assertFalse(app.exception)
        self.assertEqual(len(app.get("vega_lite_chart")), 9)
        self.assertEqual(app.metric[3].value, "243,0 mg/dL")

    def test_sem_classes(self):
        app = AppTest.from_file(str(ROOT / "app.py")).run()
        app.multiselect(key="classes").set_value([]).run()
        self.assertFalse(app.exception)
        self.assertTrue(all(m.value == "Sem dados" for m in app.metric))

    def test_medida_constante_e_amostra_unitaria(self):
        app = AppTest.from_file(str(ROOT / "app.py"), default_timeout=15).run()
        app.slider(key="intervalo_age").set_value((56.0, 56.0)).run()
        self.assertFalse(app.exception)
        self.assertTrue(any("coeficiente indefinido" in c.value for c in app.caption))
        app.slider(key="intervalo_age").set_value((29.0, 29.0)).run()
        self.assertFalse(app.exception)
        self.assertTrue(any("pelo menos dois pacientes" in c.value for c in app.info))


if __name__ == "__main__":
    unittest.main()
