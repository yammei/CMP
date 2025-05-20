from psycopg2.extras import execute_values
from dotenv import load_dotenv
from psycopg2 import connect
import random
import os

class GenerateTestData:
    def __init__(self) -> None:
        self.global_number_of_test_users: int = 10000

    def generate_n_test_users(self, number_of_test_users: int=100) -> None:
        print(f"\ngenerate_test_users(number_of_test_users={number_of_test_users})")
        if number_of_test_users <= 10:
            print(f"Number of test users must be at least 10 or more.")
            return
        self._generate_test_user_accounts()
        self._generate_test_user_profiles()
        self._generate_test_user_preferences()

    def _generate_test_user_accounts(self) -> None:
        # Sample data of people I look up to.
        sample_data: dict = {
            'usernames': ['LiteraryLeader', 'SavingScholar', 'ErrorproofEngineer', 'GiftingGuardian', 'VeneratedVisionary'],
            'hashed_password': ['NoStepBack.', 'Noli_Me_Tangere', 'reComput@tion', '#Rehabilitation', 'Convoluted!'],
            'first_name': ['Shirley', 'Jose', 'Margaret', 'Abdul', 'Yann'],
            'middle_name': ['Anita', 'Alonso Realonda', 'Elaine', 'Sattar', 'Andre'],
            'last_name': ['Chisholm', 'Rizal Mercado', 'Hamilton', 'Edhi', 'LeCun'],
            'email_address': ['@email.gov', '@email.edu', '@email.gov', '@email.org', '@email.net'],
            'phone_number': [str(random.randint(1e10, 1e11)) for _ in range(5)],
            'date_of_birth': ['1924-11-30', '1861-06-19', '1936-08-17', '1928-02-28', '1960-07-08']
        }

        test_user: list[tuple] = []
        for i in range(self.global_number_of_test_users):
            random_username: str = sample_data['usernames'][random.randint(0, 4)] + str(i)
            random_email_address: str = random_username + sample_data['email_address'][random.randint(0, 4)]
            test_user.append((
                random.choice([True, False]),                           # is_logged_in
                random_username,                                        # username
                sample_data['hashed_password'][random.randint(0, 4)],   # hashed_password
                sample_data['first_name'][random.randint(0, 4)],        # first_name
                sample_data['middle_name'][random.randint(0, 4)],       # middle_name
                sample_data['last_name'][random.randint(0, 4)],         # last_name
                random_email_address,                                   # email_address
                sample_data['phone_number'][random.randint(0, 4)],      # phone_number
                sample_data['date_of_birth'][random.randint(0, 4)],     # date_of_birth
                random.randint(-90000, 90000) / 1000,                   # latitude
                random.randint(-180000, 180000) / 1000                  # longitude
            ))

        # Query template for dummy data insertion.
        test_user_insertion_query: str = f"""
            INSERT INTO user_accounts (
                is_logged_in,
                username,
                hashed_password,
                first_name,
                middle_name,
                last_name,
                email_address,
                phone_number,
                date_of_birth,
                latitude,
                longitude
            )
            VALUES %s
        """

        print(f"├── Inserting {self.global_number_of_test_users} item(s) into user_accounts.")
        self._en_masse_query_insertion(table_name="user_accounts", insertion_query=test_user_insertion_query, test_data=test_user, reset_entries=True)

    def _generate_test_user_profiles(self):
        user_profile_test_data: list[tuple] = []
        for i in range(1, self.global_number_of_test_users + 1):
            user_profile_test_data.append((
                i,                                  # uid
                random.choice([True, False]),       # seeking_employment
                random.randint(0, 100),             # years_of_experience
                random.choice(["en", "zh", "es"]),  # fluent_languages
                random.choice([True, False]),       # tb_vaccination
                random.choice([True, False]),       # covid_vaccination
                random.choice([True, False]),       # hca_registered
                random.choice([True, False]),       # rcfe_certified
                random.choice([True, False]),       # hospice_experience
                random.choice([True, False]),       # dementia_experience
                random.choice([True, False]),       # facility_experience
                random.choice([True, False]),       # in_home_care_experience
                random.choice([""]),                # profile_description
                random.choice([""]),                # resume_file_url
            ))

        # Query template for dummy data insertion.
        test_user_profile_insertion_query: str = f"""
            INSERT INTO user_profiles (
                uid,
                seeking_employment,
                years_of_experience,
                fluent_languages,
                tb_vaccination,
                covid_vaccination,
                hca_registered,
                rcfe_certified,
                hospice_experience,
                dementia_experience,
                facility_experience,
                in_home_care_experience,
                profile_description,
                resume_file_url
            )
            VALUES %s
        """

        print(f"├── Inserting {self.global_number_of_test_users} item(s) into user_profiles.")
        self._en_masse_query_insertion(table_name="user_profiles", insertion_query=test_user_profile_insertion_query,test_data=user_profile_test_data, reset_entries=True)

    def _generate_test_user_preferences(self):
        user_preferences_test_data: list[tuple] = []
        for i in range(1, self.global_number_of_test_users + 1):
            user_preferences_test_data.append((
                i,                                  # uid
                random.randint(0, 150),             # pay_rate
                random.randint(0, 250),             # commute_distance
                random.randint(0, 2),               # desired_employment
                random.choice([True, False]),       # cat_friendly
                random.choice([True, False]),       # dog_friendly
            ))

        # Query template for dummy data insertion.
        test_user_preferences_insertion_query: str = f"""
            INSERT INTO user_preferences (
                uid,
                pay_rate,
                commute_distance,
                desired_employment,
                cat_friendly,
                dog_friendly
            )
            VALUES %s
        """

        print(f"└── Inserting {self.global_number_of_test_users} item(s) into user_preferences.")
        self._en_masse_query_insertion(table_name="user_preferences", insertion_query=test_user_preferences_insertion_query,test_data=user_preferences_test_data, reset_entries=True)

    # Mass insert test data into database.
    def _en_masse_query_insertion(self, table_name: str, insertion_query: str, test_data: list[tuple], reset_entries: bool=False) -> None:
        try:
            # Ensure .env exists in Flask app root directory.
            flask_app_root_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
            env_path = os.path.join(flask_app_root_directory, ".env")
            
            if os.path.exists(env_path):
                load_dotenv(dotenv_path=env_path)
            else:
                print(f"ERROR .. '.env' path not found at location: {env_path}")
                return

            # Establish PostgreSQL connection
            psql_dbname = os.getenv("PSQL_NAME")
            connection = connect(
                dbname=psql_dbname,
                user=os.getenv("PSQL_USER"),
                password=os.getenv("PSQL_PASS"),
                host=os.getenv("PSQL_HOST"),
                port=os.getenv("PSQL_PORT")
            )
            connection.autocommit = True
            cursor = connection.cursor()

            # Deletes all previous entries and resets identity (auto-incrementing ID count).
            if reset_entries:
                # cursor.execute(f"TRUNCATE TABLE {table_name} RESTART IDENTITY;")
                ...

            # Mass insert test users to database.
            execute_values(cursor, insertion_query, test_data)
        except Exception as e:
            print(f"[ERROR] {e}]")

    def truncate_database() -> None:
        # Establish PostgreSQL connection
        psql_dbname = os.getenv("PSQL_NAME")
        connection = connect(
            dbname=psql_dbname,
            user=os.getenv("PSQL_USER"),
            password=os.getenv("PSQL_PASS"),
            host=os.getenv("PSQL_HOST"),
            port=os.getenv("PSQL_PORT")
        )
        connection.autocommit = True
        cursor = connection.cursor()
        cursor.execute(f"TRUNCATE user_accounts CASCADE;")