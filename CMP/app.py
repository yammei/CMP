# Custom libraries/functions.
from backend.tests.check_server_status import check_test_endpoint_status
from backend.functions.create_database import create_sqlite3_database

# Common Python libraries.
from flask import Flask, jsonify, request, Response, make_response, render_template
from threading import Thread
import sqlite3
import os

# Initiate flask app.
app = Flask(__name__)
flask_app_port: int = 5123

# Initiate connection and cursor.
connection: sqlite3.Connection = sqlite3.connect("cmps.db", check_same_thread=False)
cursor: sqlite3.Cursor = connection.cursor()

# ENDPOINTS --------------------------------------------------------------------.

# Serves rendered main page of application.
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

# Validates POST request data and sends valid data for table insertion.
@app.route('/api/insert_caregiver', methods=['POST'])
def insert_caregiver_endpoint():
    try:
        print(f"[ENDPOINT REACHED] The endpoint '/api/insert_caregiver' has been reached.")
        caregiver_data: tuple = request.get_json()
        is_caregiver_data_valid, caregiver_data_validity_response = _validate_caregiver_data(caregiver_data)
        #unclear why caregiver_data_validity_response is returned instead of response of _insert_caregiver_query_execution
        _insert_caregiver_query_execution(caregiver_data) if is_caregiver_data_valid else None
        return caregiver_data_validity_response
    except Exception as e:
        print(f"[ERROR] {e}")

# 
@app.route('/api/retrieve_caregiver', methods=['GET'])
def retrieve_caregiver_endpoint():
    try:
        print(f"[ENDPOINT REACHED] The endpoint '/api/insert_caregiver' has been reached.")
        caregiver_data, caregiver_data_retrieval_response = _retrieve_caregiver_query_execution()
        return caregiver_data_retrieval_response
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

# API endpoint for testing server status. Run check_server_status.py script to check.
@app.route('/api/test')
def api_test():
    print(f"[TEST METHOD REACHED] api_test() has been reached.")
    try:
        success_response: Response = make_response("[SUCCESS] Endpoint '/api/test' has been reached.\n", 200)
        success_response.headers['Content-Type'] = 'text/plain'
        return success_response
    except Exception as e:
        failure_response: Response = make_response(f"[ERROR] Server-side error has occured: {e}\n", 500)
        failure_response.headers['Content-Type'] = 'text/plain'
        return failure_response

# API METHODS --------------------------------------------------------------------

# Ensures data will be compatible with table insertion query. Formatting checks done database side.
def _validate_caregiver_data(caregiver_data: dict) -> tuple[bool, Response]:
    # Validates data item count.
    expected_item_count: int = 9
    if len(caregiver_data) != expected_item_count:
        print(f"[DATA ISSUE] Invalid data item count recieved.")
        failure_response: Response = make_response(f"[DATA ISSUE] Invalid number of items from data of item count {len(caregiver_data)}. Data must have exactly {expected_item_count} items.\n", 200)
        failure_response.headers['Content-Type'] = 'text/plain'
        return False, failure_response

    # Validates data type.
    for data in caregiver_data.values():
        if type(data) is not str and type(data) is not int:
            print(f"[DATA ISSUE] Invalid data formatting recieved.")
            failure_response: Response = make_response(f"[DATA ISSUE] Invalid data type for {data} of type {type(data)}. Data type must be str.\n", 200)
            failure_response.headers['Content-Type'] = 'text/plain'
            return False, failure_response

    # Data is valid.
    print(f"[SUCCESS] Data has been successfully validated.")
    success_response: Response = make_response(f"[SUCCESS] Data has been successfully validated and sent for database storage.", 200)
    success_response.headers['Content-Type'] = 'text/plain'
    return True, success_response

# Parses caregiver information and executes table insertion query.
def _insert_caregiver_query_execution(caregiver_data: dict):
    try:
        print(f"[METHOD REACHED] The method 'insert_caregiver_query_execution' has been reached.")

        # Parses and formats the table insertion query.
        #vul to injections
        insertion_query: str = f"""
            INSERT INTO user_accounts(
                username,
                hashed_password,
                first_name,
                middle_name,
                last_name,
                email_address,
                phone_number,
                date_of_birth
            )
            VALUES(
                '{caregiver_data['username']}',
                '{caregiver_data['hashed_password']}',
                '{caregiver_data['first_name']}',
                '{caregiver_data['middle_name']}',
                '{caregiver_data['last_name']}',
                '{caregiver_data['email_address']}',
                '{caregiver_data['phone_number']}',
                '{caregiver_data['date_of_birth']}'
            );
        """

        # Prints and executes the table insertion query.
        print(f"[ACTION] Executing insertion query:\n{insertion_query}")
        cursor.execute(insertion_query)
    except Exception as e:
        print(f"[ERROR] {e}")

def _update_caregiver_query_execution():
    pass

def _retrieve_caregiver_query_execution() -> tuple[tuple, Response]:
    try:
        table_data: list[tuple] = cursor.execute("SELECT * FROM user_accounts;").fetchall()
        print(f"Length of table_data: {len(table_data)}\nMost recent element of table_data: {table_data[-1]}")
        success_response: Response = make_response(f"[SUCCESS] Caregivers have been retrieved.", 200)
        success_response.headers['Content-Type'] = 'text/plain'
        return (), success_response
    except Exception as e:
        print(f"[ERROR] {e}")
        failure_response: Response = make_response(f"[ERROR] Caregivers could not be retrieved.", 200)
        failure_response.headers['Content-Type'] = 'text/plain'
        return (), failure_response

def _delete_caregiver_query_execution():
    pass

# Method for running flask app as a thread.
def run_app():
    print(f"[IN PROGRESS] Running Flask application.")
    app.run(port=flask_app_port)

# Run with "flask run" in terminal.
# NOTES: To delete all __pycache__. Use bash command: find . -type d -name "__pycache__" -exec rm -r {} +
if __name__ == '__main__':
    # Starts app/server as the main thread.
    flask_thread: Thread = Thread(target=run_app)
    flask_thread.start()
    
    # Routine checks.
    create_sqlite3_database()
    check_test_endpoint_status()