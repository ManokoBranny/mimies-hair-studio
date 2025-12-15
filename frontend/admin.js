// admin.js - fetch appointments with token from sessionStorage

// admin.js - fetch appointments with token from sessionStorage
const API_BASE_URL = "https://mimies-hair-studio-9.onrender.com";

// Check for token in URL first
const urlParams = new URLSearchParams(window.location.search);
let token = urlParams.get("token") || sessionStorage.getItem('adminToken');

if (!token) {
    alert('Please log in first.');
    window.location.href = 'login.html';
} else {
    sessionStorage.setItem('adminToken', token); // store in sessionStorage

    // Clean the URL so token is not visible
    if (urlParams.get("token")) {
        const cleanUrl = window.location.origin + window.location.pathname;
        window.history.replaceState({}, document.title, cleanUrl);
    }
}


async function loadAppointments() {
    try {
        const response = await fetch(`${API_BASE_URL}/appointments`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        if (!response.ok) {
            throw new Error('Unauthorized or failed to fetch');
        }

        const appointments = await response.json();

        const tableBody = document.querySelector("#appointments-table tbody");
        tableBody.innerHTML = "";

        appointments.forEach(appointment => {
            const row = document.createElement("tr");
            row.innerHTML = `
                <td>${appointment.name}</td>
                <td>${appointment.email}</td>
                <td>${appointment.service}</td>
                <td>${appointment.date}</td>
                <td>${appointment.time}</td>
            `;
            tableBody.appendChild(row);
        });

    } catch (error) {
        alert(error.message);
        window.location.href = 'login.html';
    }
}

loadAppointments();