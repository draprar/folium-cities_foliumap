# Folium Cities

![Screenshot](img/ss.png)

This project generates an HTML map of Polish cities visited by users,
using SQLite for storage and Folium for rendering.

## Project Structure

- `folium_cities/domain/` - domain models and business rules
- `folium_cities/infrastructure/` - SQLite repository and Folium renderer
- `folium_cities/interfaces/` - CLI interface
- `folium_cities/service.py` - service orchestration between repository and renderer

## Quick Start

```powershell
python -m pip install -r requirements.txt
python main.py run --reset
```

After running, the default artifacts are:

- `visits.db`
- `visits_map.html`

## CLI

```powershell
python main.py init-db --db-path visits.db --reset
python main.py build-map --db-path visits.db --output visits_map.html
python main.py run --db-path visits.db --output visits_map.html --reset
```

## Testing

```powershell
pytest -q
```

## Requirements

- Python 3.12+
- Dependencies listed in `requirements.txt`

## License

MIT
