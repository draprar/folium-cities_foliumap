from pathlib import Path

from folium_cities.config import MapConfig
from folium_cities.domain.models import CityVisit
from folium_cities.infrastructure.folium_renderer import FoliumMapRenderer


def test_renderer_creates_file_and_returns_marker_count(tmp_path: Path) -> None:
    output_path = tmp_path / "maps" / "visits_map.html"
    visits = [
        CityVisit(user_id=1, user_name="User_1", city_name="Warsaw", latitude=52.2297, longitude=21.0122),
        CityVisit(user_id=2, user_name="User_2", city_name="Krakow", latitude=50.0647, longitude=19.9450),
    ]

    renderer = FoliumMapRenderer(output_path=str(output_path))
    marker_count = renderer.render(visits)

    assert marker_count == 2
    assert output_path.exists()


def test_renderer_uses_custom_config_and_writes_popups(tmp_path: Path) -> None:
    output_path = tmp_path / "custom_map.html"
    visits = [CityVisit(user_id=18, user_name="User_18", city_name="Lublin", latitude=51.2465, longitude=22.5684)]
    config = MapConfig(center_latitude=51.0, center_longitude=19.0, zoom_start=5, colors=("orange", "black"))

    renderer = FoliumMapRenderer(output_path=str(output_path), config=config)
    renderer.render(visits)

    html = output_path.read_text(encoding="utf-8")
    assert "Lublin - User_18" in html
    assert "circleMarker" in html
    assert "black" in html

