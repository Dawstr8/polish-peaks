"""
Script to seed the database with sample Polish peaks
"""

from sqlmodel import Session, select

from src.database.core import create_db_and_tables, engine
from src.peaks.models import Peak


def seed_peaks():
    """Seed the database with sample Polish peaks"""

    create_db_and_tables()

    # Sample Polish peaks data
    peaks_data = [
        {
            "name": "Rysy",
            "elevation": 2499,
            "latitude": 49.1795,
            "longitude": 20.0881,
            "range": "Tatry",
        },
        {
            "name": "Śnieżka",
            "elevation": 1602,
            "latitude": 50.7361,
            "longitude": 15.7400,
            "range": "Karkonosze",
        },
        {
            "name": "Babia Góra",
            "elevation": 1725,
            "latitude": 49.5731,
            "longitude": 19.5297,
            "range": "Beskidy",
        },
        {
            "name": "Tarnica",
            "elevation": 1346,
            "latitude": 49.0758,
            "longitude": 22.7267,
            "range": "Bieszczady",
        },
        {
            "name": "Śnieżnik",
            "elevation": 1425,
            "latitude": 50.2067,
            "longitude": 16.8483,
            "range": "Masyw Śnieżnika",
        },
        {
            "name": "Kalenica",
            "elevation": 964,
            "latitude": 50.6428,
            "longitude": 16.5464,
            "range": "Góry Sowie",
        },
    ]

    with Session(engine) as session:
        existing_peaks = session.exec(select(Peak)).all()
        if existing_peaks:
            print(
                f"Database already contains {len(existing_peaks)} peaks. Skipping seeding."
            )

            return

        for peak_data in peaks_data:
            peak = Peak(**peak_data)
            session.add(peak)
            print(f"Added peak: {peak_data['name']}")

        session.commit()
        print("Database seeding completed successfully!")


if __name__ == "__main__":
    seed_peaks()
