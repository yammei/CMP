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
    date_of_birth DATE,
    latitude DOUBLE PRECISION CHECK(latitude BETWEEN -90 AND 90),
    longitude DOUBLE PRECISION CHECK(latitude BETWEEN -180 AND 180)
);

CREATE TABLE user_profiles (
    uid INTEGER PRIMARY KEY REFERENCES user_accounts(uid),
    seeking_employment BOOLEAN DEFAULT FALSE,
    years_of_experience INTEGER CHECK(years_of_experience BETWEEN 0 AND 100),
    fluent_languages TEXT,
    tb_vaccination BOOLEAN DEFAULT FALSE,
    covid_vaccination BOOLEAN DEFAULT FALSE,
    hca_registered BOOLEAN DEFAULT FALSE,
    rcfe_certified BOOLEAN DEFAULT FALSE,
    hospice_experience BOOLEAN DEFAULT FALSE,
    dementia_experience BOOLEAN DEFAULT FALSE,
    facility_experience BOOLEAN DEFAULT FALSE,
    in_home_care_experience BOOLEAN DEFAULT FALSE,
    profile_description TEXT CHECK(char_length(profile_description) <= 400),
    resume_file_url TEXT
);

CREATE TABLE user_preferences (
    uid INTEGER PRIMARY KEY REFERENCES user_accounts(uid),
    pay_rate INTEGER CHECK(pay_rate BETWEEN 0 AND 999),
    commute_distance INTEGER CHECK(commute_distance BETWEEN 0 AND 250),
    desired_employment INTEGER CHECK(desired_employment BETWEEN 0 AND 2),
    cat_friendly BOOLEAN DEFAULT FALSE,
    dog_friendly BOOLEAN DEFAULT FALSE
);

CREATE VIEW user_quantifiable_booleans AS
SELECT
    ua.uid,
    up.seeking_employment::int,
    up.tb_vaccination::int,
    up.covid_vaccination::int,
    up.hca_registered::int,
    up.rcfe_certified::int,
    up.hospice_experience::int,
    up.dementia_experience::int,
    up.facility_experience::int,
    up.in_home_care_experience::int,
    upref.cat_friendly::int,
    upref.dog_friendly::int
FROM user_accounts ua
JOIN user_profiles up ON ua.uid = up.uid
JOIN user_preferences upref ON ua.uid = upref.uid
;

CREATE VIEW user_quantifiable_integers AS
SELECT 
    ua.uid,
    up.years_of_experience,
    upref.pay_rate
FROM user_accounts ua
JOIN user_profiles up ON ua.uid = up.uid
JOIN user_preferences upref ON ua.uid = upref.uid
;