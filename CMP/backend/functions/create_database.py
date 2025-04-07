import sqlite3

# Creaates SQLite3 database and alle necessary tables.
def create_sqlite3_database() -> None:
    print(f"[METHOD REACHED] Checking/creating SQLite3 database.")
    try:
        # Initiate connection and cursor to database.
        connection: sqlite3.Connection = sqlite3.connect("cmps.db")
        cursor: sqlite3.Cursor = connection.cursor()

        # Query and execution to setup 'user_accounts' table.
        user_accounts_table_creation_query: str = f"""
            CREATE TABLE IF NOT EXISTS user_accounts(
                uid INTEGER PRIMARY KEY AUTOINCREMENT,
                is_logged_in INTEGER CHECK(is_logged_in == 0 or is_logged_in == 1),
                username TEXT CHECK(length(username) >= 3 and length(username) <= 25),
                hashed_password TEXT,
                first_name TEXT CHECK(length(first_name) >= 1 and length(first_name) <= 50),
                middle_name TEXT CHECK(length(middle_name) >=  0 and length(middle_name) <= 50),
                last_name TEXT CHECK(length(middle_name) >=  0 and length(middle_name) <= 50),
                email_address TEXT CHECK(length(email_address) >= 6 and length(email_address) <= 75),
                phone_number TEXT CHECK(length(phone_number) >= 10 and length(phone_number) <= 11),
                date_of_birth TEXT CHECK(length(date_of_birth) == 10)
            );
        """
        print(f"[ACTION] Creating/checking table: 'user_accounts'.")
        cursor.execute(user_accounts_table_creation_query)

        # Query and execution to setup 'user_profiles' table.
        user_profiles_table_creation_query: str = f"""
            CREATE TABLE IF NOT EXISTS user_profiles(
                uid INTEGER PRIMARY KEY AUTOINCREMENT,
                seeking_employment INTEGER CHECK(seeking_employment >= 0 and seeking_employment <= 1),
                hca_registered INTEGER CHECK(hca_registered == 0 or hca_registered == 1),
                profile_description TEXT CHECK(length(profile_description) <= 400),
                years_of_experience INTEGER CHECK(years_of_experience >= 0 and years_of_experience <= 100),
                resume_file_url TEXT
            );
        """
        print(f"[ACTION] Creating/checking table: 'user_profiles'.")
        cursor.execute(user_profiles_table_creation_query)

        # Query and execution to setup 'user_preferences' table.
        user_preferences_table_creation_query: str = f"""
            CREATE TABLE IF NOT EXISTS use_preferences(
                uid INTEGER PRIMARY KEY AUTOINCREMENT,
                pay_rate INTEGER CHECK(pay_rate >= 0 and pay_rate <= 999),
                commute_distance INTEGER CHECK(commute_distance >= 0 and commute_distance <= 250),
                desired_employment INTEGER CHECK(desired_employment >= 0 and desired_employment <= 2)
            );
        """
        print(f"[ACTION] Creating/checking table: 'user_preferences'.")
        cursor.execute(user_preferences_table_creation_query)

        user_posts_table_creation_query: str = f"""
            CREATE TABLE IF NOT EXISTS user_posts(
                post_uid INTEGER PRIMARY KEY AUTOINCREMENT,
                poster_id INTEGER,
                post_type INTEGER CHECK(post_type >= 0 and post_type <= 5),
                date_of_post TEXT CHECK(length(date_of_post) == 10)
            );
        """
        print(f"[ACTION] Creating/checking table: 'user_posts'.")
        cursor.execute(user_posts_table_creation_query)

        # Post-setup table review.
        table_data: list[tuple] = cursor.execute("SELECT * FROM user_accounts;").fetchall()
        # print(f"Length of table_data: {len(table_data)}\nFirst element of table_data: {table_data[0]}")
        print(f"[SUCCESS] SQLite3 database exists with {len(table_data)} entry/entries.")
    except Exception as e:
        #close cursor on exception
        print(f"ERROR: {e}")