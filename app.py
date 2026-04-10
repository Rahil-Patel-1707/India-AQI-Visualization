from flask import Flask, render_template, request, jsonify
from models import db, AirQuality
import pandas as pd
import json
from datetime import datetime
import os

app = Flask(__name__)

# Use absolute path for database
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'instance', 'air_quality.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('index.html')

@app.route('/api/states')
def get_states():
    """Get all unique states"""
    try:
        states = db.session.query(AirQuality.state).distinct().all()
        return jsonify([state[0] for state in states if state[0]])
    except Exception as e:
        return jsonify([])

@app.route('/api/cities/<state>')
def get_cities(state):
    """Get all cities in a state"""
    try:
        cities = db.session.query(AirQuality.city).filter_by(state=state).distinct().all()
        return jsonify([city[0] for city in cities if city[0]])
    except Exception as e:
        return jsonify([])

@app.route('/api/pollutants')
def get_pollutants():
    """Get all unique pollutants"""
    try:
        pollutants = db.session.query(AirQuality.pollutant_id).distinct().all()
        return jsonify([pollutant[0] for pollutant in pollutants if pollutant[0]])
    except Exception as e:
        return jsonify([])

@app.route('/api/data')
def get_data():
    """Get air quality data with optional filters"""
    try:
        # Base query
        query = AirQuality.query

        # Apply filters
        state = request.args.get('state')
        city = request.args.get('city')
        pollutant = request.args.get('pollutant')
        limit = request.args.get('limit', 1000, type=int)

        if state:
            query = query.filter_by(state=state)
        if city:
            query = query.filter_by(city=city)
        if pollutant:
            query = query.filter_by(pollutant_id=pollutant)

        data = query.limit(limit).all()
        return jsonify([item.to_dict() for item in data])
    except Exception as e:
        return jsonify([])

@app.route('/api/data/summary')
def get_summary():
    """Get summary statistics by state"""
    try:
        summary = db.session.query(
            AirQuality.state,
            AirQuality.pollutant_id,
            db.func.avg(AirQuality.pollutant_avg).label('avg_value'),
            db.func.max(AirQuality.pollutant_max).label('max_value'),
            db.func.min(AirQuality.pollutant_min).label('min_value')
        ).group_by(AirQuality.state, AirQuality.pollutant_id).all()

        result = {}
        for row in summary:
            state = row.state
            pollutant = row.pollutant_id
            if state and pollutant:
                if state not in result:
                    result[state] = {}
                result[state][pollutant] = {
                    'avg': float(row.avg_value) if row.avg_value else 0,
                    'max': float(row.max_value) if row.max_value else 0,
                    'min': float(row.min_value) if row.min_value else 0
                }

        return jsonify(result)
    except Exception as e:
        return jsonify({})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)
