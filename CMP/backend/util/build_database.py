from dotenv import load_dotenv
import psycopg2
import os

# Builds user database and all necessary dependencies.
def build_database():
    print(f"\nbuild_database()")
    try:
        _create_database()
        _create_tables()
        _verify_build()
    except Exception as e:
        print(f"ERROR .. {e}")

# Checks for existing database and creates the database anew.
def _create_database():
    print(f"├── Creating database.")
    # Establish connection to default database.
    connection = psycopg2.connect(
        dbname="postgres",
        user=os.getenv("PSQL_USER"),
        password=os.getenv("PSQL_PASS"),
        host=os.getenv("PSQL_HOST"),
        port=os.getenv("PSQL_PORT")
    )
    connection.autocommit = True
    cursor = connection.cursor()

    # Check if there's an existing database.
    name_of_database_to_create: str = (os.getenv("PSQL_NAME"))
    check_for_existing_database_query: str = f"SELECT 1 FROM pg_database WHERE datname = %s"
    cursor.execute(check_for_existing_database_query, (name_of_database_to_create,))
    existing_database: bool = False if cursor.fetchone() == None else True

    # Create new database if no existing database found.
    if not existing_database:
        cursor.execute(f"CREATE DATABASE {name_of_database_to_create};")
    else:
        print(f"├── Database already exists.")

    cursor.close()
    connection.close()

# Runs .sql file to create all necessary tables.
def _create_tables():
    print(f"├── Creating tables.")
    name_of_database_to_create: str = (os.getenv("PSQL_NAME"))

    # Establish connection to DB.
    connection = psycopg2.connect(
        dbname=name_of_database_to_create,
        user=os.getenv("PSQL_USER"),
        password=os.getenv("PSQL_PASS"),
        host=os.getenv("PSQL_HOST"),
        port=os.getenv("PSQL_PORT")
    )
    connection.autocommit = True
    cursor = connection.cursor()

    # Read in CREATE queries from .sql file.
    file_path: str = "./backend/util/sql_queries/create_all_tables.sql"
    with open(file_path, "r") as file:
        create_all_tables_scripts: str = file.read()

    cursor.execute(create_all_tables_scripts)
    connection.commit()
    cursor.close()
    connection.close()

# Verify database, tables, and extensions have successfully been installed/initialized.
def _verify_build():
    print(f"├── Verifying build.")
    # Establish connection to DB.
    connection = psycopg2.connect(
        dbname="postgres",
        user=os.getenv("PSQL_USER"),
        password=os.getenv("PSQL_PASS"),
        host=os.getenv("PSQL_HOST"),
        port=os.getenv("PSQL_PORT")
    )
    connection.autocommit = True
    cursor = connection.cursor()

    # Create PostGIS extension.
    # postgis_creation_query: str = "CREATE EXTENSION IF NOT EXISTS postgis;"
    # cursor.execute(postgis_creation_query)

    # Verify PostGIS creation.
    # postgis_verification_query: str = "SELECT postgis_full_version();"
    # version = cursor.fetchone(postgis_verification_query)
    # print(f"└── Current PostGIS version: {version}.")

    # Final confirmation.
    # number_of_users_query: str = "SELECT COUNT(*) FROM user_accounts;"
    # cursor.execute(number_of_users_query)
    # count = cursor.fetchone()[0]
    # print(f"└── Current PostGIS version: {version}.")

    connection.commit()
    cursor.close()
    connection.close()