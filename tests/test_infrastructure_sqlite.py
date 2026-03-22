import sqlite3
from pathlib import Path

from folium_cities.infrastructure.sqlite_repository import (
    VOIVODESHIPS,
    SQLiteCityVisitRepository,
    bootstrap_database,
)


def test_bootstrap_database_creates_schema_and_seed_data(tmp_path: Path) -> None:
    db_path = tmp_path / "nested" / "visits.db"

    bootstrap_database(db_path=str(db_path), reset=True, rng_seed=7)

    assert db_path.exists()
    with sqlite3.connect(str(db_path)) as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM users")
        assert cursor.fetchone()[0] == len(VOIVODESHIPS)

        cursor.execute("SELECT COUNT(*) FROM visited_cities")
        assert cursor.fetchone()[0] > 0


def test_bootstrap_database_reset_calls_remove_when_file_exists(tmp_path: Path, monkeypatch) -> None:
    db_path = tmp_path / "visits.db"
    bootstrap_database(db_path=str(db_path), reset=True, rng_seed=1)

    removed_paths: list[str] = []

    def fake_remove(path: str) -> None:
        removed_paths.append(path)

    monkeypatch.setattr("folium_cities.infrastructure.sqlite_repository.os.remove", fake_remove)
    bootstrap_database(db_path=str(db_path), reset=True, rng_seed=1)

    assert str(db_path) in removed_paths


def test_bootstrap_database_without_reset_is_idempotent(tmp_path: Path) -> None:
    db_path = tmp_path / "visits.db"
    bootstrap_database(db_path=str(db_path), reset=True, rng_seed=11)

    with sqlite3.connect(str(db_path)) as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM visited_cities")
        first_count = cursor.fetchone()[0]

    bootstrap_database(db_path=str(db_path), reset=False, rng_seed=11)

    with sqlite3.connect(str(db_path)) as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM visited_cities")
        second_count = cursor.fetchone()[0]

    assert second_count == first_count


def test_repository_returns_deterministic_order(tmp_path: Path) -> None:
    db_path = tmp_path / "visits.db"
    bootstrap_database(db_path=str(db_path), reset=True, rng_seed=5)

    visits = SQLiteCityVisitRepository(db_path=str(db_path)).fetch_city_visits()

    assert visits
    sorting_key = [(visit.user_id, visit.city_name) for visit in visits]
    assert sorting_key == sorted(sorting_key)

