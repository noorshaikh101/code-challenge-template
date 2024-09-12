import os
import logging
from datetime import datetime
from flask import Flask
from models import db, WeatherData
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)

# configure db connection 
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://weather_user:weather_pass123@localhost/weather_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# setting up logging files
logging.basicConfig(filename='ingestion.log', level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

# function to ingest weather data from a directory
def ingest_weather_data(directory):
    start_time = datetime.now()  
    logging.info(f"Start ingestion at {start_time}")      
    # check if the directory exists, log an error and return if it doesn't
    if not os.path.exists(directory):
        logging.error(f"Directory {directory} does not exist.")
        return
    
    for filename in os.listdir(directory):
        if filename.endswith(".txt"): 
            station_id = filename.replace(".txt", "")  # extract station ID from the filename
            file_path = os.path.join(directory, filename)
            
            try:
                with open(file_path, 'r') as file:
                    for line in file:
                        try:
                            # split each line into Date, Max Temp, Min Temp, Precipitation
                            date_str, max_temp, min_temp, precip = line.strip().split('\t')
                            
                            date_obj = datetime.strptime(date_str, '%Y%m%d').date()
                            
                            # handle missing data for temperatures and precipitation
                            max_temp = float(max_temp) / 10 if int(max_temp) != -9999 else None
                            min_temp = float(min_temp) / 10 if int(min_temp) != -9999 else None
                            precip = float(precip) / 10 if int(precip) != -9999 else None
                            
                            # create a wather data object to store the information in the database
                            weather_data = WeatherData(
                                station_id=station_id,
                                date=date_obj,
                                max_temp=max_temp,
                                min_temp=min_temp,
                                precipitation=precip
                            )
                            db.session.add(weather_data)
                        
                        except IntegrityError:
                            # rollback the session for duplicate entries and log the error
                            db.session.rollback()
                            logging.error(f"Duplicate entry found while processing line in {filename}: {line}")
                        except Exception as e:
                            logging.error(f"Error processing line in {filename}: {line}. Error: {e}")
                            db.session.rollback()

                db.session.commit() 

            except Exception as e:
                logging.error(f"Failed to process file {filename}: {e}")
                continue

    end_time = datetime.now()
    logging.info(f"Ingestion finished at {end_time}. Duration: {end_time - start_time}")

if __name__ == "__main__":
    try:
        with app.app_context():
            ingest_weather_data('code-challenge-template/wx_data')
    except Exception as e:
        logging.error(f"Unexpected error during ingestion process: {e}")
        print("An error occurred during ingestion. Please check the logs for details.")
