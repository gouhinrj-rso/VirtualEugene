import sqlite3
from pathlib import Path
import sys

import pandas as pd

# ensure module import
sys.path.append(str(Path(__file__).resolve().parents[1]))

from etl_agent import load_data_dictionary, build_etl_plan


def _create_data_dictionary(db_path: Path):
    conn = sqlite3.connect(db_path)
    df = pd.DataFrame(
        {
            "database_name": ["db"],
            "table_name": ["users"],
            "column_name": ["id"],
            "data_type": ["INTEGER"],
            "description": ["user id"],
            "relationships": [""]
        }
    )
    df.to_sql("data_dictionary", conn, if_exists="replace", index=False)
    conn.close()


def test_load_data_dictionary(tmp_path, monkeypatch):
    db_path = tmp_path / "app.db"
    _create_data_dictionary(db_path)
    monkeypatch.chdir(tmp_path)
    df_loaded = load_data_dictionary()
    assert df_loaded.iloc[0]["table_name"] == "users"
    assert "description" in df_loaded.columns


def test_build_etl_plan():
    df = pd.DataFrame(
        {
            "table_name": ["users", "orders"],
            "relationships": ["", "users.id -> orders.user_id"],
        }
    )
    tables = ["users", "orders"]
    steps = build_etl_plan(df, tables)
    assert steps[0] == "Load table `users`"
    assert any("Join `orders`" in step for step in steps)
    assert steps[-1] == "Select necessary columns and apply transformations"
