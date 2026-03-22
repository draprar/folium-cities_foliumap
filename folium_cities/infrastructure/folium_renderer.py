from pathlib import Path

import folium

from folium_cities.config import MapConfig
from folium_cities.domain.color import color_for_user
from folium_cities.domain.models import CityVisit


class FoliumMapRenderer:
    def __init__(self, output_path: str, config: MapConfig | None = None):
        self.output_path = output_path
        self.config = config or MapConfig()

    def render(self, visits: list[CityVisit]) -> int:
        map_object = folium.Map(
            location=[self.config.center_latitude, self.config.center_longitude],
            zoom_start=self.config.zoom_start,
        )

        for visit in visits:
            marker_color = color_for_user(visit.user_id, self.config.colors)
            folium.CircleMarker(
                location=[visit.latitude, visit.longitude],
                radius=6,
                color=marker_color,
                fill=True,
                fill_color=marker_color,
                fill_opacity=0.6,
                popup=f"{visit.city_name} - {visit.user_name}",
            ).add_to(map_object)

        output = Path(self.output_path)
        output.parent.mkdir(parents=True, exist_ok=True)
        map_object.save(str(output))
        return len(visits)

