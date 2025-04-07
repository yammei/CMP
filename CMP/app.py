# Custom libraries/functions.
from backend.tests.check_server_status import check_test_endpoint_status
from backend.functions.create_database import create_postgresql_database

# Common Python libraries.
from flask import Flask, jsonify, request, Response, make_response, render_template
from threading import Thread
from dotenv import load_dotenv
import psycopg2
import os

# Load environment variables
load_dotenv()

# Initiate flask app.
app = Flask(__name__)
flask_app_port: int = 5123

# Establish PostgreSQL connection
connection = psycopg2.connect(
    dbname=os.getenv("PSQL_NAME"),
    user=os.getenv("PSQL_USER"),
    password=os.getenv("PSQL_PASS"),
    host=os.getenv("PSQL_HOST"),
    port=os.getenv("PSQL_PORT")
)
connection.autocommit = True
cursor = connection.cursor()

# ENDPOINTS --------------------------------------------------------------------.

@app.route('/')
def index():
    try:
        print(f"[ENDPOINT REACHED] The endpoint '/' has been reached.")
        index_file_path: str = 'index.html'
        main_page = render_template(index_file_path)
        print(f"[SUCCESS] Served index.html from: {index_file_path}.")
        return main_page
    except Exception as e:
        print(f"[ERROR] Failed to serve index.html.\n\nError Message:\n{e}")

@app.route('/api/insert_caregiver', methods=['POST'])
def insert_caregiver_endpoint():
    try:
        print(f"[ENDPOINT REACHED] The endpoint '/api/insert_caregiver' has been reached.")
        caregiver_data: tuple = request.get_json()
        is_valid, response = _validate_caregiver_data(caregiver_data)
        _insert_caregiver_query_execution(caregiver_data) if is_valid else None
        return response
    except Exception as e:
        print(f"[ERROR] {e}")

@app.route('/api/retrieve_caregiver', methods=['GET'])
def retrieve_caregiver_endpoint():
    try:
        print(f"[ENDPOINT REACHED] The endpoint '/api/retrieve_caregiver' has been reached.")
        caregiver_data, response = _retrieve_caregiver_query_execution()
        return response
    except Exception as e:
        print(f"[ERROR] {e}")

@app.route('/api/update_caregiver', methods=['POST'])
def update_caregiver_endpoint():
    if request.method == 'POST':
        pass

@app.route('/api/delete_caregiver', methods=['POST'])
def delete_caregiver_endpoint():
    if request.method == 'POST':
        pass

@app.route('/api/test')
def api_test():
    print(f"[TEST METHOD REACHED] api_test() has been reached.")
    try:
        success_response: Response = make_response("[SUCCESS] Endpoint '/api/test' has been reached.\n", 200)
        success_response.headers['Content-Type'] = 'text/plain'
        return success_response
    except Exception as e:
        failure_response: Response = make_response(f"[ERROR] Server-side error has occurred: {e}\n", 500)
        failure_response.headers['Content-Type'] = 'text/plain'
        return failure_response

# API METHODS --------------------------------------------------------------------

def _validate_caregiver_data(caregiver_data: dict) -> tuple[bool, Response]:
    expected_item_count: int = 9
    if len(caregiver_data) != expected_item_count:
        print(f"[DATA ISSUE] Invalid data item count received.")
        failure_response: Response = make_response(
            f"[DATA ISSUE] Invalid number of items: {len(caregiver_data)}. Expected {expected_item_count}.\n", 200)
        failure_response.headers['Content-Type'] = 'text/plain'
        return False, failure_response

    for data in caregiver_data.values():
        if not isinstance(data, (str, int)):
            print(f"[DATA ISSUE] Invalid data formatting received.")
            failure_response: Response = make_response(
                f"[DATA ISSUE] Invalid data type for {data} of type {type(data)}. Must be str or int.\n", 200)
            failure_response.headers['Content-Type'] = 'text/plain'
            return False, failure_response

    print(f"[SUCCESS] Data has been successfully validated.")
    success_response: Response = make_response("[SUCCESS] Data validated and sent for storage.", 200)
    success_response.headers['Content-Type'] = 'text/plain'
    return True, success_response

def _insert_caregiver_query_execution(caregiver_data: dict):
    try:
        print(f"[METHOD REACHED] The method '_insert_caregiver_query_execution' has been reached.")

        insertion_query = """
            INSERT INTO user_accounts (
                username,
                hashed_password,
                first_name,
                middle_name,
                last_name,
                email_address,
                phone_number,
                date_of_birth
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
        """

        values = (
            caregiver_data['username'],
            caregiver_data['hashed_password'],
            caregiver_data['first_name'],
            caregiver_data['middle_name'],
            caregiver_data['last_name'],
            caregiver_data['email_address'],
            caregiver_data['phone_number'],
            caregiver_data['date_of_birth']
        )

        print(f"[ACTION] Executing parameterized insertion query.")
        cursor.execute(insertion_query, values)
        print(f"[SUCCESS] Caregiver inserted successfully.")
    except Exception as e:
        print(f"[ERROR] Failed to insert caregiver: {e}")

def _update_caregiver_query_execution():
    pass

def _retrieve_caregiver_query_execution() -> tuple[tuple, Response]:
    try:
        cursor.execute("SELECT * FROM user_accounts;")
        table_data: list[tuple] = cursor.fetchall()
        print(f"Length of table_data: {len(table_data)}\nMost recent element: {table_data[-1] if table_data else 'None'}")
        success_response: Response = make_response(f"[SUCCESS] Caregivers retrieved.", 200)
        success_response.headers['Content-Type'] = 'text/plain'
        return (), success_response
    except Exception as e:
        print(f"[ERROR] {e}")
        failure_response: Response = make_response(f"[ERROR] Could not retrieve caregivers.", 200)
        failure_response.headers['Content-Type'] = 'text/plain'
        return (), failure_response

def _delete_caregiver_query_execution():
    pass

# Run Flask app in thread
def run_app():
    print(f"[IN PROGRESS] Running Flask application.")
    app.run(port=flask_app_port)

# Main entry point
if __name__ == '__main__':
    flask_thread: Thread = Thread(target=run_app)
    flask_thread.start()

    # Routine checks
    create_postgresql_database()
    check_test_endpoint_status()
