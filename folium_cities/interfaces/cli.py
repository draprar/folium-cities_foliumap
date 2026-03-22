import argparse

from folium_cities.service import create_database, generate_map


def build_parser() -> argparse.ArgumentParser:
    """Build CLI parser for database bootstrap and map generation commands."""
    parser = argparse.ArgumentParser(
        description="Generate Folium maps from SQLite city visit data."
    )
    subparsers = parser.add_subparsers(dest="command")

    init_db = subparsers.add_parser(
        "init-db", help="Create and seed the SQLite database."
    )
    init_db.add_argument(
        "--db-path", default="visits.db", help="Path to the SQLite database file."
    )
    init_db.add_argument(
        "--reset",
        action="store_true",
        help="Delete existing database before initialization.",
    )

    build_map = subparsers.add_parser(
        "build-map", help="Generate HTML map from existing database."
    )
    build_map.add_argument(
        "--db-path", default="visits.db", help="Path to the SQLite database file."
    )
    build_map.add_argument(
        "--output", default="visits_map.html", help="Path to generated HTML file."
    )

    run_all = subparsers.add_parser("run", help="Initialize database and generate map.")
    run_all.add_argument(
        "--db-path", default="visits.db", help="Path to the SQLite database file."
    )
    run_all.add_argument(
        "--output", default="visits_map.html", help="Path to generated HTML file."
    )
    run_all.add_argument(
        "--reset",
        action="store_true",
        help="Delete existing database before initialization.",
    )

    return parser


def main() -> int:
    """Run CLI command and return process exit code."""
    parser = build_parser()
    args = parser.parse_args()
    command = args.command or "run"
    db_path = getattr(args, "db_path", "visits.db")
    output_path = getattr(args, "output", "visits_map.html")
    reset = getattr(args, "reset", False)

    if command == "init-db":
        create_database(db_path=db_path, reset=reset)
        print(f"Database initialized at '{db_path}'.")
        return 0

    if command == "build-map":
        marker_count = generate_map(db_path=db_path, output_path=output_path)
        print(f"Map generated at '{output_path}' with {marker_count} markers.")
        return 0

    if command == "run":
        create_database(db_path=db_path, reset=reset)
        marker_count = generate_map(db_path=db_path, output_path=output_path)
        print(
            f"Database ready at '{db_path}'. Map generated at "
            f"'{output_path}' with {marker_count} markers."
        )
        return 0

    parser.print_help()
    return 1

