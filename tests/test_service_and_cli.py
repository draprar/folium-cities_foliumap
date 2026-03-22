from pathlib import Path

import pytest

from folium_cities.interfaces import cli
from folium_cities.service import create_database, generate_map


def test_generate_map_raises_when_database_has_no_visits(tmp_path: Path) -> None:
    db_path = tmp_path / "empty.db"

    # Create empty database schema without seed data.
    import sqlite3

    with sqlite3.connect(str(db_path)) as connection:
        cursor = connection.cursor()
        cursor.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT NOT NULL, voivodeship TEXT NOT NULL)")
        cursor.execute(
            """
            CREATE TABLE visited_cities (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                city_name TEXT NOT NULL,
                latitude REAL NOT NULL,
                longitude REAL NOT NULL
            )
            """
        )
        connection.commit()

    with pytest.raises(ValueError, match="No city visits found"):
        generate_map(db_path=str(db_path), output_path=str(tmp_path / "map.html"))


def test_create_database_and_generate_map_work_together(tmp_path: Path) -> None:
    db_path = tmp_path / "visits.db"
    map_path = tmp_path / "visits_map.html"

    create_database(db_path=str(db_path), reset=True, rng_seed=3)
    marker_count = generate_map(db_path=str(db_path), output_path=str(map_path))

    assert db_path.exists()
    assert map_path.exists()
    assert marker_count > 0


def test_cli_init_db_command(monkeypatch: pytest.MonkeyPatch, tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    db_path = tmp_path / "cli_init.db"

    monkeypatch.setattr("sys.argv", ["main.py", "init-db", "--db-path", str(db_path), "--reset"])
    exit_code = cli.main()

    captured = capsys.readouterr()
    assert exit_code == 0
    assert db_path.exists()
    assert "Database initialized" in captured.out


def test_cli_build_map_command(monkeypatch: pytest.MonkeyPatch, tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    db_path = tmp_path / "cli_build.db"
    map_path = tmp_path / "cli_build.html"
    create_database(db_path=str(db_path), reset=True, rng_seed=2)

    monkeypatch.setattr("sys.argv", ["main.py", "build-map", "--db-path", str(db_path), "--output", str(map_path)])
    exit_code = cli.main()

    captured = capsys.readouterr()
    assert exit_code == 0
    assert map_path.exists()
    assert "Map generated" in captured.out


def test_cli_defaults_to_run_when_no_command(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    calls: list[tuple[str, tuple[object, ...], dict[str, object]]] = []

    def fake_create_database(*args: object, **kwargs: object) -> None:
        calls.append(("create_database", args, kwargs))

    def fake_generate_map(*args: object, **kwargs: object) -> int:
        calls.append(("generate_map", args, kwargs))
        return 123

    monkeypatch.setattr(cli, "create_database", fake_create_database)
    monkeypatch.setattr(cli, "generate_map", fake_generate_map)
    monkeypatch.setattr("sys.argv", ["main.py"])
    exit_code = cli.main()

    captured = capsys.readouterr()
    assert exit_code == 0
    assert calls == [
        ("create_database", (), {"db_path": "visits.db", "reset": False}),
        ("generate_map", (), {"db_path": "visits.db", "output_path": "visits_map.html"}),
    ]
    assert "Database ready" in captured.out


def test_cli_run_command_with_explicit_subcommand(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    db_path = tmp_path / "run_cmd.db"
    map_path = tmp_path / "run_cmd.html"

    monkeypatch.setattr("sys.argv", ["main.py", "run", "--db-path", str(db_path), "--output", str(map_path), "--reset"])
    assert cli.main() == 0
    assert db_path.exists()
    assert map_path.exists()


def test_create_db_wrapper_module(tmp_path: Path) -> None:
    from create_db import create_db

    db_path = tmp_path / "wrapper.db"
    create_db(db_path=str(db_path), reset=True)
    assert db_path.exists()


