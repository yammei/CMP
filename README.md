<h1>Caregiving Management Platform</h1>

This is software designed for caregiving businesses to promote and manage their talents and services.<br>
Latest Update: Migrated from SQLite3 to PostgreSQL.<br>

PostgreSQL Setup

```bash
brew install postgresql
brew services start postgresql
sudo -i -u postgres
psql -d postgres -f ./backend/functions/create_psql_admin.sql
\q
pip3 install psycopg2-binary
```

Database Schema

```sql
CREATE TABLE user_accounts (
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

CREATE TABLE user_profiles (
    uid SERIAL PRIMARY KEY,
    seeking_employment BOOLEAN DEFAULT FALSE,
    hca_registered BOOLEAN DEFAULT FALSE,
    profile_description TEXT CHECK(char_length(profile_description) <= 400),
    years_of_experience INTEGER CHECK(years_of_experience BETWEEN 0 AND 100),
    resume_file_url TEXT
);

CREATE TABLE user_preferences (
    uid SERIAL PRIMARY KEY,
    pay_rate INTEGER CHECK(pay_rate BETWEEN 0 AND 999),
    commute_distance INTEGER CHECK(commute_distance BETWEEN 0 AND 250),
    desired_employment INTEGER CHECK(desired_employment IN (0, 1, 2))
);

CREATE TABLE user_posts (
    post_uid SERIAL PRIMARY KEY,
    poster_id INTEGER,
    post_type INTEGER CHECK(post_type BETWEEN 0 AND 5),
    date_of_post DATE
);

```