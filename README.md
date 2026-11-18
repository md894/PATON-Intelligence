# PATON Intelligence

Free, browser-based MVP for two practical research workflows:

- **Competitor Intelligence** — compare competitor positioning, maturity, integration readiness, pricing signals, and recent activity.
- **B2B Market Intelligence** — rank market opportunities with transparent, adjustable scoring weights.

The dashboard opens with **public-source market research**. The register contains 47 research entries with source links and English/German summaries. The product catalog also lists FELYA's PATON reference platform. Both intelligence sections offer a separately labeled **Demo dashboard** with fictional records and scoring examples. No credentials or paid APIs are required.

## What is included

- Streamlit browser dashboard with an overview and two analysis pages
- compact Felya-style English/German and light/dark controls whose preferences persist across pages
- filters, KPI cards, charts, and downloadable filtered CSV files
- transparent opportunity-scoring model with user-adjustable weights
- safe local demo data in `data/`
- lightweight tests for the scoring logic
- deployment instructions for Streamlit Community Cloud

## Project structure

```text
PATON-Intelligence/
├── app.py
├── pages/
│   ├── 1_Competitor_Intelligence.py
│   └── 2_B2B_Market_Intelligence.py
├── src/
│   ├── data.py
│   ├── scoring.py
│   └── ui.py
├── data/
│   ├── competitors_demo.csv
│   └── markets_demo.csv
├── tests/
│   └── test_scoring.py
├── .streamlit/config.toml
└── requirements.txt
```

## Run locally

Python 3.10+ is recommended.

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
python -m pip install -r requirements.txt
streamlit run app.py
```

Streamlit prints a local URL such as `http://localhost:8501`. Open it in a browser.

## Deploy free in the browser

1. Push this project to a GitHub repository.
2. Sign in at [share.streamlit.io](https://share.streamlit.io/) with GitHub.
3. Choose **Create app** and select this repository, branch `main`, and entry point `app.py`.
4. Click **Deploy**. No secrets are needed for the demo.

Streamlit Community Cloud availability and free-tier limits can change; check its current terms before relying on it for production.

## Replace demo data

Keep the existing CSV headers and replace the rows in `data/`. Set `is_demo` to `false`, use a traceable `source_url`, and update `last_checked`. Do not commit confidential data, credentials, API keys, or personal data.

The current scores are decision-support indicators, not verified market facts. Validate important claims against primary sources before using them in a report or business decision.

## Security and privacy

- `.env`, Streamlit secrets, virtual environments, caches, and local databases are ignored by Git.
- The app does not send data to an external service.
- Downloads are generated in memory from the currently filtered rows.
- If future integrations need credentials, store them in Streamlit Secrets or environment variables—never in source code or CSV files.

## Tests

```bash
python -m unittest discover -s tests -v
```

## Quick start (RU)

Это бесплатный демонстрационный MVP. Данные вымышлены и не являются результатами исследования. Для запуска установите зависимости из `requirements.txt`, затем выполните `streamlit run app.py`. Для публикации можно подключить GitHub-репозиторий к Streamlit Community Cloud; в демо-версии секреты и платные API не нужны.
