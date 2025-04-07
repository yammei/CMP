// POST request. Sends information to database manager to create new caregiver.
async function insertCaregiver() {
    insertCaregiverApiUrl = `/api/insert_caregiver`;
    caregiver_information = {
        username: 'yams',
        first_name: 'may',
        middle_name: 'a',
        last_name: 'zhang',
        hashed_password: 'fakePassword123!',
        email_address: 'yams@email.com',
        phone_number: '12345678910',
        date_of_birth: '2025/01/01',
    };
    response = fetch(insertCaregiverApiUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(caregiver_information)
    });
}

// GET request. Retrieves all caregivers from database.
async function retrieveCaregiver() {
    retrieveCaregiverApiUrl = `/api/retrieve_caregiver`;
    response = fetch(retrieveCaregiverApiUrl, {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' },
    });
}