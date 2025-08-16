import sqlite3
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))
from knowledge_base import init_knowledge_base, search_knowledge_base


def test_init_idempotent(tmp_path):
    db = tmp_path / "kb.db"
    init_knowledge_base(db_path=str(db))
    first_count = len(search_knowledge_base("", db_path=str(db)))
    # calling again should not create duplicates
    init_knowledge_base(db_path=str(db))
    second_count = len(search_knowledge_base("", db_path=str(db)))
    assert first_count == second_count


def test_search_returns_results(tmp_path):
    db = tmp_path / "kb.db"
    init_knowledge_base(db_path=str(db))
    results = search_knowledge_base("python", db_path=str(db))
    assert results
