from dataclasses import dataclass


DEFAULT_COLORS = (
    "red",
    "blue",
    "green",
    "purple",
    "orange",
    "darkred",
    "lightred",
    "beige",
    "darkblue",
    "darkgreen",
    "cadetblue",
    "pink",
    "lightblue",
    "lightgreen",
    "gray",
    "black",
)


@dataclass(frozen=True)
class MapConfig:
    center_latitude: float = 52.2297
    center_longitude: float = 21.0122
    zoom_start: int = 6
    colors: tuple[str, ...] = DEFAULT_COLORS

