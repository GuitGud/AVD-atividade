"""Validações dos dados exportados e dos filtros interativos da entrega."""
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
        self.assertEqual(len(app.slider), 5)
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
        self.assertEqual(len(app.slider), 0)
        self.assertTrue(any("duas variáveis" in w.value for w in app.warning))

    def test_recorte_vazio(self):
        app = AppTest.from_file(str(ROOT / "app.py")).run()
        app.slider(key="intervalo_age").set_value((29.0, 29.0))
        app.slider(key="intervalo_chol").set_value((564.0, 564.0)).run()
        self.assertFalse(app.exception)
        self.assertTrue(any("Nenhum paciente" in w.value for w in app.warning))
        self.assertEqual(len(app.dataframe[0].value), 0)

    def test_selecao_reduzida_e_intervalo_persistente(self):
        app = AppTest.from_file(str(ROOT / "app.py")).run()
        app.slider(key="intervalo_age").set_value((45.0, 60.0)).run()
        app.multiselect(key="variaveis").set_value(["age"]).run()
        self.assertFalse(app.exception)
        self.assertEqual(tuple(app.slider(key="intervalo_age").value), (45.0, 60.0))
        self.assertTrue(any("duas variáveis" in w.value for w in app.warning))


if __name__ == "__main__":
    unittest.main()
