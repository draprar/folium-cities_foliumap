from folium_cities import create_database, generate_map
from folium_cities.config import DEFAULT_COLORS, MapConfig


def test_map_config_defaults_are_stable() -> None:
    config = MapConfig()

    assert config.center_latitude == 52.2297
    assert config.center_longitude == 21.0122
    assert config.zoom_start == 6
    assert config.colors == DEFAULT_COLORS


def test_package_exports_service_functions() -> None:
    assert callable(create_database)
    assert callable(generate_map)

