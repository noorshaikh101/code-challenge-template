import logging
from sqlalchemy import func, extract
from flask import Flask
from models import db, WeatherData, WeatherStats

# Initialize Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://weather_user:weather_pass123@localhost/weather_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

logging.basicConfig(filename='weather_stats.log', level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

# function to calculate weather statistics
def calculate_weather_stats():
    logging.info("Starting calculation of weather statistics.")
    
    try:
        records = db.session.query(
            WeatherData.station_id,
            extract('year', WeatherData.date).label('year'),
            func.avg(WeatherData.max_temp).label('avg_max_temp'),
            func.avg(WeatherData.min_temp).label('avg_min_temp'),
            func.sum(WeatherData.precipitation).label('total_precip')
        ).filter(
            WeatherData.max_temp.isnot(None),
            WeatherData.min_temp.isnot(None),
            WeatherData.precipitation.isnot(None)
        ).group_by(
            WeatherData.station_id,
            extract('year', WeatherData.date)
        ).all()

        if not records:
            logging.info("No records found to calculate statistics.")
        
        for record in records:
            weather_stats = WeatherStats(
                station_id=record.station_id,
                year=int(record.year),
                avg_max_temp=record.avg_max_temp,
                avg_min_temp=record.avg_min_temp,
                total_precip=record.total_precip / 10  # Convert mm to cm
            )
            db.session.add(weather_stats)
        
        db.session.commit()
        logging.info("Weather statistics have been calculated and stored successfully.")

    except Exception as e:
        logging.error(f"An error occurred while calculating weather statistics: {e}")

if __name__ == "__main__":
    with app.app_context():
        calculate_weather_stats()
