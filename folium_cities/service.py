from folium_cities.infrastructure.folium_renderer import FoliumMapRenderer
from folium_cities.infrastructure.sqlite_repository import (
    SQLiteCityVisitRepository,
    bootstrap_database,
)


def create_database(db_path: str = "visits.db", reset: bool = False, rng_seed: int = 42) -> None:
    """Create or seed the SQLite database used by the application."""
    bootstrap_database(db_path=db_path, reset=reset, rng_seed=rng_seed)


def generate_map(db_path: str = "visits.db", output_path: str = "visits_map.html") -> int:
    """Generate an HTML visits map and return the number of rendered markers."""
    repository = SQLiteCityVisitRepository(db_path=db_path)
    renderer = FoliumMapRenderer(output_path=output_path)
    visits = repository.fetch_city_visits()
    if not visits:
        raise ValueError(
            "No city visits found. Initialize and seed the database first."
        )
    return renderer.render(visits)

