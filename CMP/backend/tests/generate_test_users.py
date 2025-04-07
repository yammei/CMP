import random
import sqlite3

def generate_test_users(number_of_test_users: int = 100) -> None:
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

    print(sample_data);

    test_user: dict = {}

    for i in range(number_of_test_users):
        random_username: str = sample_data['usernames'][random.randint(0, 4)] + str(i)
        random_email_address: str = random_username + sample_data['email_address'][random.randint(0, 4)]
        test_user[i] = {
            'username': random_username,
            'hashed_password': sample_data['hashed_password'][random.randint(0, 4)],
            'first_name': sample_data['first_name'][random.randint(0, 4)],
            'middle_name': sample_data['middle_name'][random.randint(0, 4)],
            'last_name': sample_data['last_name'][random.randint(0, 4)],
            'email_address': random_email_address,
            'phone_number': sample_data['phone_number'][random.randint(0, 4)],
            'date_of_birth': sample_data['date_of_birth'][random.randint(0, 4)],
        }
        print(f"New test user created with: {random_email_address}")

    # Dummy data for table query testing.
    sample_data_insertion_query: str = f"""
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
        VALUES (
            'Test_User',
            'testPassword123!',
            'Jane',
            'S.',
            'Doe',
            'janedoe@email.com',
            '12345678910',
            '2025-01-01'
        )
    """

generate_test_users()