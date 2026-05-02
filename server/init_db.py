"""Bootstrap script — creates all tables in the SQLite database.

Run from the `trilha-cic/` directory:
    python -m server.init_db
"""

from server.database import Base, engine
from server import models  # noqa: F401  -- registers all models with Base.metadata


def main() -> None:
    Base.metadata.create_all(engine)
    print(f"Database initialized at {engine.url}")
    print(f"Tables created: {sorted(Base.metadata.tables.keys())}")


if __name__ == "__main__":
    main()
