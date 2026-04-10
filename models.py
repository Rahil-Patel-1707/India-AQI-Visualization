from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class AirQuality(db.Model):
    __tablename__ = 'air_quality'
    id = db.Column(db.Integer, primary_key=True)
    country = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    station = db.Column(db.String(200), nullable=False)
    last_update = db.Column(db.String(50), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    pollutant_id = db.Column(db.String(50), nullable=False)
    pollutant_min = db.Column(db.Float, nullable=True)
    pollutant_max = db.Column(db.Float, nullable=True)
    pollutant_avg = db.Column(db.Float, nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'country': self.country,
            'state': self.state,
            'city': self.city,
            'station': self.station,
            'last_update': self.last_update,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'pollutant_id': self.pollutant_id,
            'pollutant_min': self.pollutant_min,
            'pollutant_max': self.pollutant_max,
            'pollutant_avg': self.pollutant_avg
        }
