import pandas as pd
from models import db, AirQuality
from app import app
import os

def load_csv_data():
    """Load CSV data into the database"""
    csv_file = 'AIQ_India_cleaned_no_nh3.csv'

    if not os.path.exists(csv_file):
        print(f"CSV file {csv_file} not found!")
        return

    print("Loading CSV data...")

    # Read CSV file
    df = pd.read_csv(csv_file)

    # Clean column names
    df.columns = df.columns.str.strip()

    print(f"Found {len(df)} records to process")

    with app.app_context():
        # Create tables
        db.create_all()

        # Clear existing data (optional - remove if you want to append)
        # db.session.query(AirQuality).delete()

        batch_size = 1000
        for i in range(0, len(df), batch_size):
            batch_df = df.iloc[i:i+batch_size]

            for _, row in batch_df.iterrows():
                # Skip if any required field is missing
                if pd.isna(row.get('country')) or pd.isna(row.get('state')) or pd.isna(row.get('city')):
                    continue

                air_quality = AirQuality(
                    country=str(row.get('country', '')),
                    state=str(row.get('state', '')),
                    city=str(row.get('city', '')),
                    station=str(row.get('station', '')),
                    last_update=str(row.get('last_update', '')),
                    latitude=float(row.get('latitude', 0)),
                    longitude=float(row.get('longitude', 0)),
                    pollutant_id=str(row.get('pollutant_id', '')),
                    pollutant_min=float(row.get('pollutant_min', 0)) if not pd.isna(row.get('pollutant_min')) else None,
                    pollutant_max=float(row.get('pollutant_max', 0)) if not pd.isna(row.get('pollutant_max')) else None,
                    pollutant_avg=float(row.get('pollutant_avg', 0)) if not pd.isna(row.get('pollutant_avg')) else None
                )

                db.session.add(air_quality)

            # Commit every batch
            db.session.commit()
            print(f"Processed {min(i+batch_size, len(df))}/{len(df)} records")

        print(f"Successfully loaded {len(df)} records into database")

if __name__ == '__main__':
    load_csv_data()
