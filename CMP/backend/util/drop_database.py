from dotenv import load_dotenv
import psycopg2
import os

# Drops existing PostgreSQL database.
def drop_existing_database():
    print(f"\ndrop_existing_database()")
    try:
        # Ensure .env exists in Flask app root directory.
        flask_app_root_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
        env_path = os.path.join(flask_app_root_directory, ".env")
        
        if os.path.exists(env_path):
            load_dotenv(dotenv_path=env_path)
        else:
            print(f"[✘] .env path not found at location: {env_path}")
            return

        # Establish connection.
        database_to_drop_name: str = os.getenv("PSQL_NAME")
        connection = psycopg2.connect(
            dbname="postgres",
            user=os.getenv("PSQL_OWNER_LOCAL"),
            password=os.getenv("PSQL_PASS"),
            host=os.getenv("PSQL_HOST"),
            port=os.getenv("PSQL_PORT")
        )
        connection.autocommit = True
        cursor = connection.cursor()

        # End process to disconnect active database connections.
        print(f"├── Terminating database process: {database_to_drop_name}.")
        process_termination_query: str = f"""
            SELECT pg_terminate_backend(pid)
            FROM pg_stat_activity
            WHERE datname = '{database_to_drop_name}';
        """
        cursor.execute(process_termination_query, (database_to_drop_name,))

        # Drop database.
        print(f"└── Dropping database: {database_to_drop_name}.")
        drop_database_query = f"DROP DATABASE IF EXISTS {database_to_drop_name};"
        cursor.execute(drop_database_query)

        # Close out connection to database.
        connection.commit()
        cursor.close()
        connection.close()
    except Exception as e:
        print(f"[ERROR] {e}")
