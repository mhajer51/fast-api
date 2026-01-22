import argparse

from app.migrations.runner import upgrade
from app.seeders.runner import seed_all


def main() -> None:
    parser = argparse.ArgumentParser(description="Application console commands")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("migrate", help="Run database migrations")
    subparsers.add_parser("seed", help="Seed the database with initial data")

    args = parser.parse_args()

    if args.command == "migrate":
        upgrade()
    elif args.command == "seed":
        seed_all()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
