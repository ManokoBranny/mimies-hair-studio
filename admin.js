// admin.js - fetch appointments with token from sessionStorage

const API_BASE_URL = "http://127.0.0.1:8000";

// Check if admin is logged in
const token = sessionStorage.getItem('adminToken');
if (!token) {
    alert('Please log in first.');
    window.location.href = 'login.html';
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