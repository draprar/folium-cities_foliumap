from folium_cities.infrastructure.sqlite_repository import (
    VOIVODESHIPS,
    bootstrap_database,
)

voivodeships = VOIVODESHIPS


def create_db(db_path: str = "visits.db", reset: bool = False) -> None:
    """Backward-compatible wrapper for bootstrapping the database."""
    bootstrap_database(db_path=db_path, reset=reset)


if __name__ == "__main__":
    create_db()
