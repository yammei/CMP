from flask import Response, make_response
from dotenv import load_dotenv
import psycopg2
import math
import os

class CrudFunctions:
    # Establish PostgreSQL connection
    def __init__(self):
        print(f"\nEstablishing server connection to database.")
        connection = psycopg2.connect(
            dbname=os.getenv("PSQL_NAME"),
            user=os.getenv("PSQL_USER"),
            password=os.getenv("PSQL_PASS"),
            host=os.getenv("PSQL_HOST"),
            port=os.getenv("PSQL_PORT")
        )
        connection.autocommit = True
        self.cursor = connection.cursor()

    def validate_caregiver_data(self, caregiver_data: dict) -> tuple[bool, Response]:
        try:
            expected_item_count: int = 9
            if len(caregiver_data) != expected_item_count:
                print(f"DATA ISSUE .. Invalid data item count received.")
                failure_response: Response = make_response(
                    f"DATA ISSUE .. Invalid number of items: {len(caregiver_data)}. Expected {expected_item_count}.\n", 200)
                failure_response.headers['Content-Type'] = 'text/plain'
                return False, failure_response

            for data in caregiver_data.values():
                if not isinstance(data, (str, int)):
                    print(f"DATA ISSUE .. Invalid data formatting received.")
                    failure_response: Response = make_response(
                        f"DATA ISSUE .. Invalid data type for {data} of type {type(data)}. Must be str or int.\n", 200)
                    failure_response.headers['Content-Type'] = 'text/plain'
                    return False, failure_response

            print(f"Data has been successfully validated.")
            success_response: Response = make_response("Data validated and sent for storage.", 200)
            success_response.headers['Content-Type'] = 'text/plain'
            return True, success_response
        except Exception as e:
            print(f"ERROR .. {e}")

    def insert_caregiver_query_execution(self, caregiver_data: dict):
        try:
            print(f"_insert_caregiver_query_execution()")

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

            self.cursor.execute(insertion_query, values)
            print(f"└── Caregiver inserted successfully.")
        except Exception as e:
            print(f"ERROR .. Failed to insert caregiver: {e}")

    def update_caregiver_query_execution(self):
        pass

    def retrieve_caregiver_query_execution(self) -> tuple[list, Response]:
        self.cursor.execute("SELECT * FROM user_accounts;")
        table_data = self.cursor.fetchall()
        print(f"Length of table_data: {len(table_data)}\nMost recent element: {table_data[-1] if table_data else 'None'}")
        return ()

    def delete_caregiver_query_execution(self):
        pass

    def retrieve_all_user_accounts(self) -> list:
        print(f"\nretrieve_all_user_accounts()")
        self.cursor.execute("SELECT * FROM user_accounts;")
        table_data = self.cursor.fetchall()
        print(f"└── Retrieved {len(table_data)} entries.")
        return table_data

    def retrieve_all_user_profiles(self) -> list:
        print(f"\nretrieve_all_user_profiles()")
        self.cursor.execute("SELECT * FROM user_profiles;")
        table_data = self.cursor.fetchall()
        print(f"└── Retrieved {len(table_data)} entries.")
        return table_data

    def retrieve_all_user_preferences(self) -> list:
        print(f"\nretrieve_all_user_preferences()")
        self.cursor.execute("SELECT * FROM user_preferences;")
        table_data = self.cursor.fetchall()
        print(f"└── Retrieved {len(table_data)} entries.")
        return table_data

    def retrieve_user_profile_from_uid(self, uid: int) -> list:
        print(f"\nretrieve_user_profile_from_uid()")
        select_by_uid_query: str = f"""
            SELECT *
            FROM user_profiles
            WHERE uid = {uid}
        """
        self.cursor.execute(select_by_uid_query)
        table_data = self.cursor.fetchall()
        print(f"└── Retrieved {len(table_data)} entries.")
        return table_data

    def retrieve_user_profiles_from_list_of_uids(self, uid_list: list) -> list:
        print(f"\nretrieve_user_profiles_from_list_of_uids()")
        print(f"├── uid_list:       {uid_list}")
        select_by_uid_query: str = f"""
            SELECT *
            FROM user_profiles
            WHERE uid in {tuple(uid_list)}
        """
        self.cursor.execute(select_by_uid_query)
        table_data = self.cursor.fetchall()
        print(f"├── Data UID Order: {[caregiver[0] for caregiver in table_data]}")
        print(f"└── Retrieved {len(table_data)} entries.")
        return table_data

    def retrieve_all_caregivers_for_preprocessing(self,) -> list:
        print(f"\nretrieve_all_caregivers_for_preprocessing()")

        select_all_caregivers_query: str = f"""
            SELECT 
                uqb.*,
                uqi.*
            FROM user_quantifiable_booleans uqb
            JOIN user_quantifiable_integers uqi ON uqb.uid = uqi.uid
        """
        self.cursor.execute(select_all_caregivers_query)
        table_data: list = self.cursor.fetchall()
        self.cursor.execute("SELECT COUNT(*) FROM information_schema.columns WHERE table_name = 'user_quantifiable_booleans';")
        partition_point: int = self.cursor.fetchone()[0]
        # print(f"├── partition_point: {partition_point}")
        for i in range(len(table_data)):
            table_data[i] = {
                'uids': table_data[i][0],
                'booleans': table_data[i][1:partition_point],
                'integers': table_data[i][partition_point+1:],
            }
        print(f"├── table_data[0]: {str(table_data[0])[:40]}...")
        print(f"└── Retrieved {len(table_data)} entries.")
        return table_data

    # Gets all caregivers within n-distance.
    # Latitude conversion rate: (1deg / 111.32km).
    # Longitude conversion rate: ((1deg / 111.32km) * cos(latitude)).
    # Longitudial distance decreases towards the poles.
    def retrieve_caregivers_within_n_distance_for_preprocessing(self, central_coordinates: dict, distance_constraint_in_meters: float) -> list:
        print(f"\nretrieve_caregivers_within_n_distance(({central_coordinates['latitude']}, {central_coordinates['longitude']}), {distance_constraint_in_meters})" )

        # Check if arguments are not None values.
        if (central_coordinates is None and distance_constraint_in_meters is None):
            print(f"Please pass all arguments.")
            return

        # Check if max distance approximation to opposite side of Earth's globe has exceeded.
        if (distance_constraint_in_meters > math.pi * 6371000):
            print(f"Please keep pass distance_constraint_in_meters value within 0 < x < {math.pi * 6371000}.")
            return

        # Selects users within n distance using Haversine computation.
        select_caregivers_within_n_distance: str = f"""
            WITH caregivers_within_n_distance AS (
                SELECT 
                    uid,
                    6371000 * 2 * ASIN(
                        SQRT(
                            POWER(SIN(RADIANS(latitude - {central_coordinates['latitude']}) / 2), 2) +
                            COS(RADIANS({central_coordinates['latitude']})) * COS(RADIANS(latitude)) *
                            POWER(SIN(RADIANS(longitude - {central_coordinates['longitude']}) / 2), 2)
                        )
                    ) AS distance_delta
                FROM user_accounts
            )
            SELECT 
                uqb.*,
                uqi.*,
                cwnd.distance_delta
            FROM caregivers_within_n_distance cwnd
            JOIN user_quantifiable_booleans uqb ON cwnd.uid = uqb.uid
            JOIN user_quantifiable_integers uqi ON cwnd.uid = uqi.uid
            JOIN user_preferences upref ON cwnd.uid = upref.uid
            WHERE cwnd.distance_delta <= {distance_constraint_in_meters}
              AND upref.commute_distance <= {distance_constraint_in_meters}     
            ORDER BY cwnd.distance_delta ASC;
            ;
        """
        self.cursor.execute(select_caregivers_within_n_distance)
        table_data: list = self.cursor.fetchall()
        self.cursor.execute("SELECT COUNT(*) FROM information_schema.columns WHERE table_name = 'user_quantifiable_booleans';")
        partition_point: int = self.cursor.fetchone()[0]
        # print(f"├── partition_point: {partition_point}")
        for i in range(len(table_data)):
            table_data[i] = {
                'uids': table_data[i][0],
                'booleans': table_data[i][1:partition_point],
                'integers': table_data[i][partition_point+1:-1],
                'distance': table_data[i][-1]
            }
        print(f"├── table_data[0]: {str(table_data[0])[:40]}...")
        print(f"└── Retrieved {len(table_data)} entries.")
        return table_data

    # Retrieves random caregiver(s) for careseeker test use.
    # Called by generate_test_data.generate_test_seeker().
    def retrieve_all_data_from_random_caregiver(self, retrieve_limit: int = 1) -> list:
        print(f"\nretrieve_random_caregiver(retrieve_limit={retrieve_limit})" )

        # Retrieve random uid available in user_accounts table.
        retrieve_random_user_query: str = f"""
            SELECT uid, latitude, longitude
            FROM user_accounts
            WHERE uid IS NOT NULL
                AND latitude IS NOT NULL
                AND longitude IS NOT NULL
            ORDER BY RANDOM()
            LIMIT {retrieve_limit};
        """
        self.cursor.execute(retrieve_random_user_query)
        random_user_data: list = self.cursor.fetchall()
        uid: list = random_user_data[0][0]
        coordinates: dict = {'latitude': float(random_user_data[0][1]), 'longitude': float(random_user_data[0][1])}
        print(f"├── uid: {uid}")
        print(f"├── coordinates: {coordinates}")

        # Retrieves all quantifiable boolean data of user.
        retrieve_quantifiable_booleans_query: str = f"""
            SELECT *
            FROM user_quantifiable_booleans
            WHERE uid = %s;
        """
        self.cursor.execute(retrieve_quantifiable_booleans_query, (uid,))
        quantifiable_boolean_data: list = list(self.cursor.fetchall()[0])[1:]
        print(f"├── booleans: {str(quantifiable_boolean_data)[:40]}...")

        # Retrieves all quantifiable integer data of user.
        retrieve_quantifiable_integers_query: str = f"""
            SELECT *
            FROM user_quantifiable_integers
            WHERE uid = %s;
        """
        self.cursor.execute(retrieve_quantifiable_integers_query, (uid,))
        quantifiable_integer_data: list = list(self.cursor.fetchall()[0])[1:]
        print(f"└── integers: {str(quantifiable_integer_data)[:40]}...")

        return [{
            'uids': uid,
            'coordinates': coordinates,
            'booleans': quantifiable_boolean_data,
            'integers': quantifiable_integer_data
        }]