from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_swagger_ui import get_swaggerui_blueprint
from models import db, WeatherData, WeatherStats

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://weather_user:weather_pass123@localhost/weather_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SWAGGER_UI_URL'] = '/api/docs'
app.config['SWAGGER_UI_DOC_EXPANSION'] = 'list'
app.config['SWAGGER_UI_OPERATION_ID'] = True

db.init_app(app)
ma = Marshmallow(app)

# Swagger UI setup
swagger_url = '/api/docs'
swagger_ui = get_swaggerui_blueprint(
    swagger_url,
    '/static/swagger.json',
    config={'app_name': "Weather API"}
)
app.register_blueprint(swagger_ui, url_prefix=swagger_url)

class WeatherDataSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = WeatherData

class WeatherStatsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = WeatherStats

@app.route('/api/weather', methods=['GET'])
def get_weather_data():
    station_id = request.args.get('station_id')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    query = WeatherData.query
    
    if station_id:
        query = query.filter_by(station_id=station_id)
    if start_date:
        query = query.filter(WeatherData.date >= start_date)
    if end_date:
        query = query.filter(WeatherData.date <= end_date)
    
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    max_per_page = request.args.get('max_per_page', 100, type=int)

    paginated_data = query.paginate(
        page=page,
        per_page=per_page,
        max_per_page=max_per_page,
        error_out=False
    )
    data_schema = WeatherDataSchema(many=True)
    result = data_schema.dump(paginated_data.items)
    
    response = {
        'data': result,
        'total': paginated_data.total,
        'pages': paginated_data.pages,
        'current_page': paginated_data.page
    }
    return jsonify(response)

@app.route('/api/weather/stats', methods=['GET'])
def get_weather_stats():
    station_id = request.args.get('station_id')
    year = request.args.get('year')
    
    query = WeatherStats.query
    
    if station_id:
        query = query.filter_by(station_id=station_id)
    if year:
        query = query.filter_by(year=year)
    
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    max_per_page = request.args.get('max_per_page', 100, type=int)

    paginated_stats = query.paginate(
        page=page,
        per_page=per_page,
        max_per_page=max_per_page,
        error_out=False
    )
    
    stats_schema = WeatherStatsSchema(many=True)
    result = stats_schema.dump(paginated_stats.items)
    
    response = {
        'data': result,
        'total': paginated_stats.total,
        'pages': paginated_stats.pages,
        'current_page': paginated_stats.page
    }
    return jsonify(response)

if __name__ == "__main__":
    app.run(debug=True)
