Caregiving Management Platform Software.

This is software designed for caregiving businesses to promote and manage their talents and services.

DATA SCHEMA

```sql
user_accounts
    uid                 INTEGER PRIMARY KEY AUTOINCREMENT
    username            TEXT
    hashed_password     TEXT
    first_name          TEXT
    middle_name         TEXT
    last_name           TEXT 
    email_address       TEXT (personal@email.com)
    phone_number        TEXT (12345678910)
    date_of_birth       TEXT (YYYY-MM-DD)

user_profiles
    uid                 INTEGER PRIMARY KEY AUTOINCREMENT
    seeking_employment  INTEGER (0 or 1)
    hca_registered      INTEGER (0 or 1)
    profile_description TEXT
    years_of_experience INTEGER
    resume_file_url     TEXT

user_preferences
    uid                 INTEGER PRIMARY KEY AUTOINCREMENT
    pay_rate            INTEGER (hourly)
    commute_distance    INTEGER
    desired_employment  INTEGER (0: fulltime, 1: parttime, 2: seasonal)

user_posts
    post_uid            INTEGER PRIMARY KEY AUTOINCREMENT
    poster_id           INTEGER
    post_type           INTEGER (0-5, types currently undetermined)
    date_of_post        TEXT (YYYY-MM-DD)
```