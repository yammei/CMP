const { response } = require("express");

// Constants
const apiUrlDomain = "localhost:5500";
// INSERT INTO user_accounts(username, hashed_password, email_address, phone_number, date_of_birth)

const testCaregiverInformation = ("May Z.", "hashedPassword+Salt", "mayz@thecaregivingcompany.com", "12345678910", "20250130");

// On page load event-handler.
window.addEventListener("load", () => {
    console.log(`All objects loaded.`);
});

// Component loader. Loads card template HTML for caregiver information.
async function loadCaregiverCardComponent() {
    const caregiverCardsContainer = document.getElementById("caregiver-cards");
    const caregiverCard = await fetch("static/components/caregiver_card.html");
    const caregiverCardHTML = await caregiverCard.text();
    caregiverCardsContainer.innerHTML += caregiverCardHTML;
}

// Component loader. Loads and unloads login/signup pop-up component.
async function loadLoginSignupComponent() {
    const loginSignupContainer = document.getElementById("floating-component");
    const loginSignup = await fetch("static/components/login_signup.html");
    const loginSignupHTML = await loginSignup.text();

    if (loginSignupContainer.innerHTML.trim() != "") {
        loginSignupContainer.innerHTML = "";
        toggleDarkenComponentBackground();
        console.log(`Unloading Login & Signup Component ...`);
    } else {
        loginSignupContainer.innerHTML += loginSignupHTML;
        toggleDarkenComponentBackground();
        console.log(`Loading Login & Signup Component ...`);
    }
}

// Component loader. Loads and unloads screen darkening element for pop-up components.
async function toggleDarkenComponentBackground() {
    const floatingComponentDarkBackground = document.getElementById("floating-component-dark-background");
    console.log(`Now: ${floatingComponentDarkBackground.style.display}.`)
    if (floatingComponentDarkBackground.style.display == "none") {
        floatingComponentDarkBackground.style.display = "block";
        console.log(`Toggling dark background on. Now: ${floatingComponentDarkBackground.style.display}.`)
    } else {
        floatingComponentDarkBackground.style.display = "none";
        console.log(`Toggling dark background off. Now: ${floatingComponentDarkBackground.style.display}.`)
    }
}

// Attribute modifyer. Toggles login/signup pop-up component password display between plain-text and discrete text.
async function changePasswordTextType() {
    const loginSignupPasswordInput = document.getElementById("login-signup-password-input");
    if (loginSignupPasswordInput.type == "password") {
        loginSignupPasswordInput.type = "text";
        console.log(`Changing password text input type to: text ...`);
    } else {
        loginSignupPasswordInput.type = "password";
        console.log(`Changing password text input type to: password ...`);

    }
}