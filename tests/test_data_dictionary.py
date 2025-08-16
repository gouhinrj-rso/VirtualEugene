import io
from pathlib import Path
import sys

# ensure module import
sys.path.append(str(Path(__file__).resolve().parents[1]))

import data_dictionary


def test_upload_and_search(tmp_path, monkeypatch):
    sample_csv = (
        "id,database_name,table_name,column_name,data_type,description,relationships\n"
        "1,db,users,id,INTEGER,identifier,"
    )
    uploaded = io.StringIO(sample_csv)

    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(data_dictionary.st, "file_uploader", lambda *a, **k: uploaded)
    monkeypatch.setattr(data_dictionary.st, "success", lambda *a, **k: None)
    monkeypatch.setattr(data_dictionary.st, "error", lambda *a, **k: None)

    data_dictionary.upload_data_dictionary()
    results = data_dictionary.search_data_dictionary("id")
    assert len(results) == 1
    assert results[0]["column_name"] == "id"
