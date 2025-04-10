# add_weight_history.py

from datetime import datetime
from app import create_app, db
from app.models import User, WeightEntry


def add_weight_history():
    # Create/obtain the Flask application context
    app = create_app()
    with app.app_context():
        # Look up the user to whom we'll add these entries
        user = User.query.filter_by(username='rogue').first()
        if not user:
            print("User not found. Aborting.")
            return

        # List of (date, weight_lbs); adjust if your data is in kg already
        entries = [
            (datetime(2025, 4, 7), 345.1),
            (datetime(2025, 3, 31), 347.9),
            (datetime(2025, 3, 27), 349.5),
            (datetime(2025, 3, 17), 350.3),
            (datetime(2025, 3, 4), 352.0),
            (datetime(2025, 2, 14), 365.0),
            (datetime(2025, 2, 24), 354.9),
        ]

        for entry_date, weight_lbs in entries:
            weight_kg = weight_lbs / 2.20462  # lbs → kg
            new_entry = WeightEntry(
                user_id=user.id,
                weight_kg=weight_kg,
                date=entry_date.date()  # or just entry_date if you prefer datetime
            )
            db.session.add(new_entry)

        # Commit the new records
        db.session.commit()
        print("Weight history added successfully.")


if __name__ == '__main__':
    add_weight_history()
