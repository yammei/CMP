# Custom class imports.
from backend.util.recommendation_system import RecommendationSystem
from backend.util.crud_functions import CrudFunctions

# Custom method imports.
from backend.tests.check_server_status import check_test_endpoint_status
from backend.util.drop_database import drop_existing_database
from backend.util.build_database import build_database

# Common Python libraries.
from flask import Flask, jsonify, request, Response, make_response, render_template
from dotenv import load_dotenv
from threading import Thread
import pandas as pd
import psycopg2
import random
import os

# Load environment variables
load_dotenv()

# Initiate flask app.
flask_app_port: int = 5123
app = Flask(__name__)

# ENDPOINTS --------------------------------------------------------------------.

@app.route('/')
def index():
    try:
        print(f"Served index.")
        index_file_path: str = 'index.html'
        main_page = render_template(index_file_path)
        return main_page
    except Exception as e:
        print(f"ERROR .. Failed to serve index.html.\n\nError Message:\n{e}")

@app.route('/api/insert_caregiver', methods=['POST'])
def insert_caregiver_endpoint():
    try:
        print(f"/api/insert_caregiver")
        caregiver_data: tuple = request.get_json()
        is_valid, response = cf.validate_caregiver_data(caregiver_data)
        cf.insert_caregiver_query_execution(caregiver_data) if is_valid else None
        return response
    except Exception as e:
        print(f"ERROR .. {e}")

@app.route('/api/retrieve_caregiver', methods=['GET'])
def retrieve_caregiver_endpoint():
    try:
        table_data = cf.retrieve_all_user_profiles()
        return make_response(jsonify(table_data), 200)
    except Exception as e:
        print(f"ERROR .. {e}")
        return make_response("Could not retrieve caregivers.", 500)

@app.route('/api/update_caregiver', methods=['POST'])
def update_caregiver_endpoint():
    if request.method == 'POST':
        pass

@app.route('/api/delete_caregiver', methods=['POST'])
def delete_caregiver_endpoint():
    if request.method == 'POST':
        pass

@app.route('/api/recommend_caregivers', methods=['GET'])
def recommend_caregivers():
    print(f"Endpoint reached: recommend_caregivers()")
    if request.method == 'GET':
        try:
            recommended_caregivers: list = rs.recommend_caregivers()
        except Exception as e:
            print(f"ERROR .. {e}")

@app.route('/api/test')
def api_test():
    print(f"Endpoint reached: api_test()")
    try:
        success_response: Response = make_response("Endpoint '/api/test\n", 200)
        success_response.headers['Content-Type'] = 'text/plain'
        return success_response
    except Exception as e:
        failure_response: Response = make_response(f"ERROR .. Server-side error has occurred: {e}\n", 500)
        failure_response.headers['Content-Type'] = 'text/plain'
        return failure_response

# APP SETUP --------------------------------------------------------------------.

# Run Flask app in thread.
def run_app():
    print(f"\nStarting flask app @ port {flask_app_port}.")
    app.run(port=flask_app_port)

def tests():
    print(f"\nRunning development tests.")

# Main entry point.
if __name__ == '__main__':
    # [ PRODUCTION NECESSITIES ]
    # Reset/update existing database.
    print(f"App running from: {os.getcwd()}")
    drop_existing_database()
    build_database()

    # Run server.
    flask_thread: Thread = Thread(target=run_app)
    flask_thread.start()

    # Check server responsiveness.
    check_test_endpoint_status()

    # Initialize utility class instances.
    cf = CrudFunctions()
    rs = RecommendationSystem()

    # Initialize recommendation system.
    rs.initialize_recommendation_system(mode="test")