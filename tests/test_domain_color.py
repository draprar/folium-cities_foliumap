import pytest

from folium_cities.domain.color import color_for_user


def test_color_for_user_returns_expected_color_by_position() -> None:
    palette = ("red", "blue", "green")

    assert color_for_user(1, palette) == "red"
    assert color_for_user(2, palette) == "blue"
    assert color_for_user(3, palette) == "green"


def test_color_for_user_wraps_around_palette() -> None:
    palette = ("red", "blue", "green")

    assert color_for_user(4, palette) == "red"
    assert color_for_user(7, palette) == "red"


def test_color_for_user_rejects_empty_palette() -> None:
    with pytest.raises(ValueError, match="Color palette cannot be empty"):
        color_for_user(1, ())

