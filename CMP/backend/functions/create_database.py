from dotenv import load_dotenv
import psycopg2
import os

# Creates PostgreSQL database tables if they don't exist.
def create_postgresql_database():
    print(f"[METHOD REACHED] Checking/creating PostgreSQL tables.")
    try:
        # Establish connection
        connection = psycopg2.connect(
            dbname=os.getenv("PSQL_NAME"),
            user=os.getenv("PSQL_USER"),
            password=os.getenv("PSQL_PASS"),
            host=os.getenv("PSQL_HOST"),
            port=os.getenv("PSQL_PORT")
        )
        cursor = connection.cursor()

        # Create 'user_accounts' table
        user_accounts_query = """
            CREATE TABLE IF NOT EXISTS user_accounts(
                uid SERIAL PRIMARY KEY,
                is_logged_in BOOLEAN DEFAULT FALSE,
                username TEXT CHECK(char_length(username) BETWEEN 3 AND 25),
                hashed_password TEXT,
                first_name TEXT CHECK(char_length(first_name) BETWEEN 1 AND 50),
                middle_name TEXT CHECK(char_length(middle_name) BETWEEN 0 AND 50),
                last_name TEXT CHECK(char_length(last_name) BETWEEN 0 AND 50),
                email_address TEXT CHECK(char_length(email_address) BETWEEN 6 AND 75),
                phone_number TEXT CHECK(char_length(phone_number) BETWEEN 10 AND 11),
                date_of_birth DATE
            );
        """
        print(f"[ACTION] Creating/checking table: 'user_accounts'.")
        cursor.execute(user_accounts_query)

        # Create 'user_profiles' table
        user_profiles_query = """
            CREATE TABLE IF NOT EXISTS user_profiles(
                uid SERIAL PRIMARY KEY,
                seeking_employment BOOLEAN DEFAULT FALSE,
                hca_registered BOOLEAN DEFAULT FALSE,
                profile_description TEXT CHECK(char_length(profile_description) <= 400),
                years_of_experience INTEGER CHECK(years_of_experience BETWEEN 0 AND 100),
                resume_file_url TEXT
            );
        """
        print(f"[ACTION] Creating/checking table: 'user_profiles'.")
        cursor.execute(user_profiles_query)

        # Create 'user_preferences' table
        user_preferences_query = """
            CREATE TABLE IF NOT EXISTS user_preferences(
                uid SERIAL PRIMARY KEY,
                pay_rate INTEGER CHECK(pay_rate BETWEEN 0 AND 999),
                commute_distance INTEGER CHECK(commute_distance BETWEEN 0 AND 250),
                desired_employment INTEGER CHECK(desired_employment BETWEEN 0 AND 2)
            );
        """
        print(f"[ACTION] Creating/checking table: 'user_preferences'.")
        cursor.execute(user_preferences_query)

        # Create 'user_posts' table
        user_posts_query = """
            CREATE TABLE IF NOT EXISTS user_posts(
                post_uid SERIAL PRIMARY KEY,
                poster_id INTEGER,
                post_type INTEGER CHECK(post_type BETWEEN 0 AND 5),
                date_of_post DATE
            );
        """
        print(f"[ACTION] Creating/checking table: 'user_posts'.")
        cursor.execute(user_posts_query)

        # Final confirmation
        cursor.execute("SELECT COUNT(*) FROM user_accounts;")
        count = cursor.fetchone()[0]
        print(f"[SUCCESS] PostgreSQL database is ready with {count} user account(s).")

        connection.commit()
        cursor.close()
        connection.close()

    except Exception as e:
        print(f"[ERROR] {e}")
