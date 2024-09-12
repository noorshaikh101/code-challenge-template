from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class WeatherData(db.Model):
    __tablename__ = 'weather_data'
    
    id = db.Column(db.Integer, primary_key=True)
    station_id = db.Column(db.String(50), nullable=False)
    date = db.Column(db.Date, nullable=False)
    max_temp = db.Column(db.Float)  # in degrees Celsius
    min_temp = db.Column(db.Float)  # in degrees Celsius
    precipitation = db.Column(db.Float)  # in millimeters
    
    __table_args__ = (
        db.UniqueConstraint('station_id', 'date', name='unique_station_date'),
    )

class WeatherStats(db.Model):
    __tablename__ = 'weather_stats'
    
    id = db.Column(db.Integer, primary_key=True)
    station_id = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    avg_max_temp = db.Column(db.Float)  # in degrees Celsius
    avg_min_temp = db.Column(db.Float)  # in degrees Celsius
    total_precip = db.Column(db.Float)  # in centimeters
    
    __table_args__ = (
        db.UniqueConstraint('station_id', 'year', name='unique_station_year'),
    )
