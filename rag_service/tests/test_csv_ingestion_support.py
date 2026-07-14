from app.rag.ingest.loaders import load_any
from scripts import ingest_folder, sync_folder, sync_orchestrator


def test_csv_is_supported_by_all_folder_sync_paths(tmp_path):
    csv_path = tmp_path / "gate.csv"
    csv_path.write_text("gate,status\nlocal,pass\n", encoding="utf-8")

    assert "*.csv" in ingest_folder.SUPPORTED_EXTENSIONS
    assert "*.csv" in sync_folder.SUPPORTED_EXTENSIONS
    assert "**/*.csv" in sync_orchestrator.DEFAULT_INCLUDE_GLOBS
    assert ingest_folder._collect_files(tmp_path, []) == [csv_path]
    assert sync_folder._collect_files(tmp_path, []) == [csv_path]
    assert load_any(csv_path) == "gate,status\nlocal,pass\n"
