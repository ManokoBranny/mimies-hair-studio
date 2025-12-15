/*
STEP 2: FRONTEND → BACKEND CONNECTION
------------------------------------
This file connects your website booking form to the FastAPI backend.

What this does:
- Captures form data
- Sends it to the backend using fetch()
- Handles success and error responses

Think of fetch() like requests.post() in Python.
*/

// ---------------------------------
// CONFIGURATION
// ---------------------------------
// Local backend URL (change this when deployed)
const API_BASE_URL = "https://mimies-hair-studio-9.onrender.com";

// ---------------------------------
// FORM HANDLING
// ---------------------------------
const form = document.querySelector(".contact-form");

form.addEventListener("submit", async function (event) {
    event.preventDefault(); // Stop page refresh

    // ---------------------------------
    // COLLECT FORM DATA
    // ---------------------------------
    const appointmentData = {
        name: document.querySelector("#name").value,
        email: document.querySelector("#email").value,
        service: document.querySelector("#service").value,
        date: document.querySelector("#date").value,
        time: document.querySelector("#time").value
    };

    try {
        // ---------------------------------
        // SEND DATA TO BACKEND (POST)
        // ---------------------------------
        const response = await fetch(`${API_BASE_URL}/book`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(appointmentData)
        });

        if (!response.ok) {
            throw new Error("Failed to book appointment");
        }

        const result = await response.json();

        // ---------------------------------
        // SUCCESS FEEDBACK
        // ---------------------------------
        alert(result.message);
        form.reset();

    } catch (error) {
        console.error(error);
        alert("Something went wrong. Please try again.");
    }
});
