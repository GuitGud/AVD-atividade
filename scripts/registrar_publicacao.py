"""Registra somente uma URL real, após verificar acesso HTTP público."""
# [IA] Codex/OpenAI - validação da URL e atualização controlada do README.
import argparse
import json
from datetime import datetime
from pathlib import Path
from urllib.parse import urlsplit
from zoneinfo import ZoneInfo
import requests

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument("--url", required=True, help="URL real atribuída pelo Streamlit Community Cloud")
args = parser.parse_args()
url = args.url.strip()
parts = urlsplit(url)
if (parts.scheme != "https" or not parts.hostname or not parts.hostname.endswith(".streamlit.app")
        or parts.username or parts.password or parts.query or parts.fragment or parts.port):
    raise SystemExit("Informe uma URL HTTPS real de streamlit.app, sem credenciais ou parâmetros.")
response = requests.get(url, timeout=45)
response.raise_for_status()
if not (urlsplit(response.url).hostname or "").endswith(".streamlit.app"):
    raise SystemExit("A URL redirecionou para outra origem. Confira acesso público antes de registrar.")
start, end = "<!-- APP_PUBLICADO:INICIO -->", "<!-- APP_PUBLICADO:FIM -->"
path = ROOT / "README.md"
readme = path.read_text(encoding="utf-8-sig")
before, remainder = readme.split(start, 1)
_, after = remainder.split(end, 1)
block = f"\n**App publicado:** [Abrir os dois dashboards]({url})\n\nAcesso HTTP público conferido; teste dos widgets em janela anônima deve ser registrado em entregas/teste-app-publicado.md.\n"
path.write_text(before + start + block + end + after, encoding="utf-8")
record = {"app_url": url, "http_status": response.status_code,
          "checked_at": datetime.now(ZoneInfo("America/Fortaleza")).isoformat(),
          "anonymous_browser_test": "pending"}
(ROOT / "entregas/publicacao.json").write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding="utf-8")
print("Link real registrado. O teste em janela anônima continua pendente.")
