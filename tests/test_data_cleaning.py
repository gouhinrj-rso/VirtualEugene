from pathlib import Path
import io
import sys

# ensure module import
sys.path.append(str(Path(__file__).resolve().parents[1]))

import pandas as pd
import data_cleaning
import types


class DummyContext:
    def __enter__(self):
        return None
    def __exit__(self, exc_type, exc, tb):
        pass


def test_clean_data_basic_flow(monkeypatch):
    sample_csv = "col1,col2\n1,2\n,3\n1,2\n"
    uploaded = io.StringIO(sample_csv)

    monkeypatch.setattr(data_cleaning.st, "file_uploader", lambda *a, **k: uploaded)
    monkeypatch.setattr(data_cleaning.st, "columns", lambda n: (DummyContext(), DummyContext()))
    monkeypatch.setattr(data_cleaning.st, "write", lambda *a, **k: None)
    monkeypatch.setattr(data_cleaning.st, "subheader", lambda *a, **k: None)
    monkeypatch.setattr(data_cleaning.st, "selectbox", lambda *a, **k: "Drop")
    monkeypatch.setattr(data_cleaning.st, "button", lambda *a, **k: True)
    monkeypatch.setattr(data_cleaning.st, "checkbox", lambda *a, **k: False)
    monkeypatch.setattr(data_cleaning.st, "download_button", lambda *a, **k: None)
    monkeypatch.setattr(data_cleaning.st, "warning", lambda *a, **k: None)
    monkeypatch.setattr(data_cleaning.st, "error", lambda *a, **k: None)
    data_cleaning.st.session_state = types.SimpleNamespace()

    class DummyExcelWriter:
        def __init__(self, *a, **k):
            pass
        def __enter__(self):
            return self
        def __exit__(self, exc_type, exc, tb):
            pass

    monkeypatch.setattr(data_cleaning.pd, "ExcelWriter", DummyExcelWriter)

    data_cleaning.clean_data()
    cleaned = getattr(data_cleaning.st.session_state, "cleaned_df", None)
    assert cleaned is not None
    assert cleaned.shape == (1, 2)
    assert list(cleaned.columns) == ["col1", "col2"]
