import os
import random
import sqlite3
from pathlib import Path

from folium_cities.domain.models import CityVisit

VOIVODESHIPS: dict[str, list[tuple[str, float, float]]] = {
    "Lower Silesian": [("Wroclaw", 51.1079, 17.0385), ("Legnica", 51.2070, 16.1555), ("Jelenia Gora", 50.9045, 15.7389)],
    "Kuyavian-Pomeranian": [("Bydgoszcz", 53.1235, 18.0084), ("Torun", 53.0138, 18.5984), ("Wloclawek", 52.6482, 19.0677)],
    "Lublin": [("Lublin", 51.2465, 22.5684), ("Zamosc", 50.7214, 23.2516), ("Chelm", 51.1431, 23.4718)],
    "Lubusz": [("Zielona Gora", 51.9356, 15.5062), ("Gorzow Wielkopolski", 52.7368, 15.2288)],
    "Lodz": [("Lodz", 51.7592, 19.4550), ("Piotrkow Trybunalski", 51.4056, 19.7038), ("Pabianice", 51.6643, 19.3542)],
    "Lesser Poland": [("Krakow", 50.0647, 19.9450), ("Tarnow", 50.0121, 20.9858), ("Nowy Sacz", 49.6217, 20.6970)],
    "Masovian": [("Warsaw", 52.2297, 21.0122), ("Radom", 51.4027, 21.1471), ("Plock", 52.5463, 19.7065)],
    "Opole": [("Opole", 50.6751, 17.9213), ("Nysa", 50.4746, 17.3325), ("Brzeg", 50.8600, 17.4672)],
    "Podkarpackie": [("Rzeszow", 50.0413, 21.9990), ("Przemysl", 49.7840, 22.7675), ("Krosno", 49.6881, 21.7705)],
    "Podlaskie": [("Bialystok", 53.1325, 23.1688), ("Lomza", 53.1780, 22.0593), ("Suwalki", 54.0996, 22.9332)],
    "Pomeranian": [("Gdansk", 54.3520, 18.6466), ("Sopot", 54.4416, 18.5601), ("Gdynia", 54.5189, 18.5305)],
    "Silesian": [("Katowice", 50.2649, 19.0238), ("Gliwice", 50.2945, 18.6714), ("Czestochowa", 50.8115, 19.1203)],
    "Holy Cross": [("Kielce", 50.8661, 20.6286), ("Sandomierz", 50.6821, 21.7487)],
    "Warmian-Masurian": [("Olsztyn", 53.7784, 20.4801), ("Elblag", 54.1524, 19.4082), ("Elk", 53.8286, 22.3646)],
    "Greater Poland": [("Poznan", 52.4064, 16.9252), ("Kalisz", 51.7611, 18.0910), ("Konin", 52.2234, 18.2516)],
    "West Pomeranian": [("Szczecin", 53.4285, 14.5528), ("Koszalin", 54.1944, 16.1722), ("Stargard", 53.3365, 15.0496)],
}


def _connect(db_path: str) -> sqlite3.Connection:
    connection = sqlite3.connect(db_path)
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def bootstrap_database(db_path: str, reset: bool = False, rng_seed: int = 42) -> None:
    if reset and os.path.exists(db_path):
        os.remove(db_path)

    db_dir = Path(db_path).parent
    if str(db_dir) and str(db_dir) != ".":
        db_dir.mkdir(parents=True, exist_ok=True)

    with _connect(db_path) as connection:
        cursor = connection.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL UNIQUE,
                voivodeship TEXT NOT NULL UNIQUE
            )
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS visited_cities (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                city_name TEXT NOT NULL,
                latitude REAL NOT NULL,
                longitude REAL NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                UNIQUE(user_id, city_name)
            )
            """
        )

        users = [(index, f"User_{index}", voivodeship) for index, voivodeship in enumerate(VOIVODESHIPS.keys(), start=1)]
        cursor.executemany(
            "INSERT OR IGNORE INTO users (id, name, voivodeship) VALUES (?, ?, ?)",
            users,
        )

        rng = random.Random(rng_seed)
        for user_id, voivodeship in enumerate(VOIVODESHIPS.keys(), start=1):
            cities = VOIVODESHIPS[voivodeship]
            sampled = rng.sample(cities, min(10, len(cities)))
            cursor.executemany(
                """
                INSERT OR IGNORE INTO visited_cities (user_id, city_name, latitude, longitude)
                VALUES (?, ?, ?, ?)
                """,
                [(user_id, city_name, latitude, longitude) for city_name, latitude, longitude in sampled],
            )


class SQLiteCityVisitRepository:
    def __init__(self, db_path: str):
        self.db_path = db_path

    def fetch_city_visits(self) -> list[CityVisit]:
        with _connect(self.db_path) as connection:
            cursor = connection.cursor()
            cursor.execute(
                """
                SELECT users.id, users.name, visited_cities.city_name, visited_cities.latitude, visited_cities.longitude
                FROM visited_cities
                INNER JOIN users ON visited_cities.user_id = users.id
                ORDER BY users.id, visited_cities.city_name
                """
            )
            rows = cursor.fetchall()

        return [
            CityVisit(
                user_id=row[0],
                user_name=row[1],
                city_name=row[2],
                latitude=row[3],
                longitude=row[4],
            )
            for row in rows
        ]

