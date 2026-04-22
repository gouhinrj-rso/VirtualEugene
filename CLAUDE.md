# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

VirtualEugene is a single-page **Streamlit** app (`app.py`) that bundles several data-analytics utilities into tabs: Data Cleaning, EDA, a Databricks/Jupyter-like Notebook, an ETL Assistant, a searchable Resource Hub, a Prompt Builder, and an ETL Agent. State flows between tabs primarily through `st.session_state.cleaned_df`, which `data_cleaning.clean_data()` populates and every downstream tab reads. An SQLite file `app.db` backs two tables: `knowledge_base` (seeded + optionally scraped docs) and `data_dictionary` (user-uploaded CSV of Databricks cluster metadata). OpenAI calls go through `openai_agent.run_agent()` (uses `OPENAI_API_KEY`); absence of the key is non-fatal — LLM features degrade with a warning.

## Commands

```bash
pip install -r requirements.txt         # install deps (Python 3.10, per runtime.txt)
streamlit run app.py                    # launch the app on :8501
pytest                                  # run the full suite
pytest tests/test_knowledge_base.py     # single file
pytest tests/test_knowledge_base.py::test_search_returns_results  # single test
flake8 . --select=E9,F63,F7,F82         # the only lint gate enforced by CI
```

CI (`.github/workflows/python-app.yml`) runs on pushes/PRs to `main` with Python 3.10: flake8 syntax-only gate, then `pytest`. The devcontainer auto-launches `streamlit run app.py` on attach.

## Architecture

**Tab wiring.** `app.py` creates eight tabs and initializes SQLite tables at startup via `init_knowledge_base()` and `init_data_dictionary()`. Each tab delegates to one module's top-level function (`clean_data`, `perform_eda`, `run_notebook`, `run_etl_agent`, `build_prompt`). Some imports (`notebook`, `eda`) are wrapped in `try/except` with no-op fallbacks so the app keeps working when PySpark or other heavy deps fail to initialize — preserve this pattern when adding tabs.

**Shared state.** The canonical data handoff is `st.session_state.cleaned_df` (a pandas DataFrame). `data_cleaning` writes it; `eda`, `notebook`, and `etl_agent` read it. Don't introduce parallel state containers for the same data.

**Notebook sandbox.** `notebook.run_notebook()` builds an `exec_globals` dict with pre-imported `pd`, `np`, `plt`, `sns`, `sqlite3`, `col`, `st`, and a lazily-created `SparkSession` (`spark`). User code is run with `exec(code, exec_globals)` and stdout is redirected via a `StringIO`. After execution it walks `exec_globals`, rendering any `pd.DataFrame`/`pd.Series` and flushing `plt.get_fignums()`. Helper functions `get_code_suggestions`, `get_next_step_suggestions`, `get_error_fix_suggestions`, and `get_assistant_response` do pattern-matching on the code/error/query strings — they are keyword-driven, not LLM-driven.

**Knowledge base.** `knowledge_base.init_knowledge_base()` is idempotent: the `knowledge_base` table has `UNIQUE(title)` and inserts use `INSERT OR IGNORE`. After seeding it calls `fetch_web_docs()`, which hits several external doc sites with `requests`+`BeautifulSoup` — both imports are guarded so the function is a no-op when they're unavailable. `search_knowledge_base()` does a plain `LIKE` over `title`/`content`/`tags`.

**Data dictionary.** `data_dictionary.upload_data_dictionary()` validates the CSV has exactly `database_name, table_name, column_name, data_type, description, relationships` and writes via `df.to_sql(..., if_exists='replace')` — **uploads overwrite**, they don't merge.

**ETL Agent.** `etl_agent.run_etl_agent()` builds a Spark DataFrame from either an uploaded CSV or `cleaned_df`, then offers column selection, simple transformations, and writing to CSV or a SQLite table.

## Conventions & Gotchas

- **Local stub modules shadow real packages.** `openai.py`, `pandas.py`, and `streamlit.py` sit at the repo root alongside code that does `import openai` / `import pandas` / `import streamlit`. Depending on `sys.path` order at import time, the stubs may win — they exist to let some tests run without the heavy deps installed. Before adding files at the repo root, check you aren't introducing another shadow. `tests/pandas.py` uses `importlib.util` specifically to load the root-level stub.
- **Python 3.10 is the target** (`runtime.txt`, CI matrix). `devcontainer.json` pins 3.11 — prefer 3.10 features only.
- **`openai_agent.run_agent` uses the Responses API** (`client.responses.create(...).output_text`) with default model `gpt-4o-mini`. `agents.run_agent` uses the older Chat Completions API. These are separate entry points; don't assume one style.
- **Test imports use `sys.path.append(Path(__file__).resolve().parents[1])`** to pick up top-level modules. Follow the same pattern for new tests rather than restructuring the package.
- **Lint gate is minimal.** Only flake8 syntax/undefined-name errors (`E9,F63,F7,F82`) fail CI; the full-codebase run uses `--exit-zero`. Don't rely on flake8 to catch stylistic issues.

## Known Broken State (worth flagging before changes land near these)

- `app.py:123` references a bare `with tab:` — `tab` is undefined; `st.tabs([...])` unpacks into `tab1..tab8`, and `tab8` is never used. The "ETL Agent" tab is effectively dead.
- `tests/test_etl_agent.py` imports `load_data_dictionary` and `build_etl_plan` from `etl_agent`, but `etl_agent.py` defines neither — the test file will fail to collect. Either restore those helpers or update the tests.
- `.env.example` appears to contain a live-looking `OPENAI_API_KEY` value rather than a placeholder. Treat it as potentially leaked and rotate if real before touching it.
