# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

VirtualEugene is a single-page **Streamlit** app (`app.py`) that bundles several data-analytics utilities into seven tabs: Overview, Data Cleaning, EDA, Notebook, ETL Assistant, Resource Hub, and Prompt Builder. State flows between tabs primarily through `st.session_state.cleaned_df`, which `data_cleaning.clean_data()` populates and every downstream tab reads. An SQLite file `app.db` backs two tables: `knowledge_base` (seeded + optionally scraped docs) and `data_dictionary` (user-uploaded CSV of Databricks cluster metadata). `app.py` sets `openai.api_key` from `OPENAI_API_KEY` at startup and falls back to a `print` warning (not `st.warning`) if it's missing — LLM features degrade without raising.

`README.md` and `EXAMPLES.md` describe the product-facing features and sample workflows; `demo.py` is a standalone CLI script that reads `sample_data.csv` / `sample_sales_data.csv` and writes `demo_*_analysis.png` — it is not imported by the Streamlit app.

## Commands

```bash
pip install -r requirements.txt         # install deps (Python 3.10, per runtime.txt)
streamlit run app.py                    # launch the app on :8501
python demo.py                          # offline smoke/demo script (writes demo_*.png)
pytest                                  # run the full suite
pytest tests/test_knowledge_base.py     # single file
pytest tests/test_knowledge_base.py::test_search_returns_results  # single test
flake8 . --select=E9,F63,F7,F82         # the only lint gate enforced by CI
```

CI workflows under `.github/workflows/`: `python-app.yml` (Python 3.10, flake8 syntax gate + pytest) and `python-package.yml` (same steps across a 3.9/3.10/3.11 matrix) both run on push/PR to `main`. `debricked.yml`, `dependency-review.yml`, and `python-publish.yml` are security/release workflows. The devcontainer auto-launches `streamlit run app.py` on attach.

## Architecture

**Tab wiring.** `app.py` calls `st.tabs([...])` with 7 labels and unpacks into `tab1..tab7`. `tab1` (Overview) contains sample-data loading buttons that write `sample_data.csv` / `sample_sales_data.csv` into `st.session_state.cleaned_df`. `tab2..tab7` each delegate to one module's top-level function (`clean_data`, `perform_eda`, `run_notebook`, `run_etl_agent`, `search_knowledge_base` inline, `build_prompt`). Imports of `notebook` and `eda` are wrapped in `try/except` with no-op fallbacks so the app keeps working when PySpark or other heavy deps fail — preserve this pattern when adding tabs. `init_knowledge_base()` and `init_data_dictionary()` run at startup inside an `st.spinner`.

**Shared state.** The canonical data handoff is `st.session_state.cleaned_df` (a pandas DataFrame). `data_cleaning` and the Overview sample-load buttons write it; `eda`, `notebook`, and `etl_agent` read it. Don't introduce parallel state containers for the same data.

**Notebook sandbox.** `notebook.run_notebook()` builds an `exec_globals` dict with pre-imported `pd`, `np`, `plt`, `sns`, `sqlite3`, `col`, `st`, and a lazily-created `SparkSession` (`spark`). User code runs under `exec(code, exec_globals)` with stdout redirected to a `StringIO`. After execution it walks `exec_globals`, rendering any `pd.DataFrame`/`pd.Series` (with CSV + Excel download buttons) and flushing `plt.get_fignums()`. The "Coding Assistant" helpers `get_code_suggestions`, `get_next_step_suggestions`, `get_error_fix_suggestions`, and `get_assistant_response` are **keyword-driven**, not LLM-driven — despite `notebook.py` importing `run_agent` from `openai_agent`, that import is unused.

**Knowledge base.** `knowledge_base.init_knowledge_base(db_path="app.db")` is idempotent: the `knowledge_base` table has `UNIQUE(title)` and inserts use `INSERT OR IGNORE`. After seeding it calls `fetch_web_docs()`, which hits several external doc sites with `requests`+`BeautifulSoup` — both imports are guarded so the function is a no-op when they're unavailable, and so is Streamlit (via a `_Stub` class). `search_knowledge_base()` does a plain `LIKE` over `title`/`content`/`tags`.

**Data dictionary.** `data_dictionary.upload_data_dictionary()` validates the CSV has exactly `database_name, table_name, column_name, data_type, description, relationships` and writes via `df.to_sql(..., if_exists='replace')` — **uploads overwrite**, they don't merge.

**ETL Agent.** `etl_agent.run_etl_agent()` builds a Spark DataFrame from either an uploaded CSV or `cleaned_df`, then offers column selection, simple transformations (uppercase a string column, filter rows by equality), and writing to CSV or a SQLite table. Note that `etl_agent.py` does `from notebook import SparkSession` — it re-exports `notebook`'s PySpark import rather than importing PySpark directly, so changes to `notebook.py`'s imports can break the ETL tab.

**Prompt Builder.** `prompt_builder.build_prompt()` pulls categorized examples from `prompt_library.prompts` (a module that begins with `# Databricks notebook source` / `# COMMAND ----------` markers — it's meant to be round-trippable with a Databricks notebook). Prompts are filtered by category, composed with a tool selector and user details, and rendered as a string — there's no LLM call from this tab.

**OpenAI entry points (three, all different).** `openai_agent.run_agent(prompt, model='gpt-4o-mini')` uses the **Responses API** (`client.responses.create(...).output_text`) and raises if `OPENAI_API_KEY` is missing. `agents.run_agent()` is a Streamlit widget that uses the older **Chat Completions API** and warns instead of raising. `app.py` itself just sets `openai.api_key` at import time for compatibility with code that reads it. Don't assume these share behavior.

## Conventions & Gotchas

- **Local stub modules still shadow `streamlit`.** `streamlit.py` sits at the repo root alongside code that does `import streamlit as st` — depending on `sys.path` order at import time, the stub may win. The previously-shadowing `openai.py` and `pandas.py` have been renamed to `mock_openai.py` and `mock_pandas.py` (they're no longer on the default import path); `tests/pandas.py` uses `importlib.util` to load `mock_pandas.py` specifically. Before adding files at the repo root, check you aren't re-introducing a shadow.
- **Python 3.10 is the target** (`runtime.txt`, primary CI job). `devcontainer.json` pins 3.11 and the `python-package.yml` matrix also runs 3.9 — prefer 3.10 features only.
- **Test imports use `sys.path.append(Path(__file__).resolve().parents[1])`** to pick up top-level modules. Follow the same pattern for new tests rather than restructuring the package.
- **Lint gate is minimal.** Only flake8 syntax/undefined-name errors (`E9,F63,F7,F82`) fail CI; the full-codebase run uses `--exit-zero`. Don't rely on flake8 to catch stylistic issues.
- **`app.db` is committed.** It contains the seeded knowledge base and (potentially) a user-uploaded data dictionary. Deleting it is recoverable — `init_*` functions recreate tables — but other developers will lose any unseeded rows.
- **Sample data files (`sample_data.csv`, `sample_sales_data.csv`) are load-bearing.** The Overview tab and `demo.py` both read them by relative path; renaming or removing them breaks the quick-start flow.

## Known Broken State (worth flagging before changes land near these)

- `tests/test_etl_agent.py` imports `load_data_dictionary` and `build_etl_plan` from `etl_agent`, but `etl_agent.py` defines neither — the test file fails to collect. Either restore those helpers or update the tests.
- `.env.example` appears to contain a live-looking `OPENAI_API_KEY` value rather than a placeholder (and `.env` at the repo root has the same contents). Treat as potentially leaked and rotate before touching.
- `notebook.py` imports `run_agent` from `openai_agent` but never calls it — removing the import is safe, but be aware the "Coding Assistant" is intentionally keyword-based, not LLM-based.
