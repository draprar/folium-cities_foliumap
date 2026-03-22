from dataclasses import dataclass


@dataclass(frozen=True)
class CityVisit:
    user_id: int
    user_name: str
    city_name: str
    latitude: float
    longitude: float

