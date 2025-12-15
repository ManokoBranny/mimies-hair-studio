"""
STEP 4: ADMIN LOGIN SYSTEM
-------------------------
This adds a simple authentication system to protect the admin dashboard.
- Hardcoded username/password (for simplicity)
- Issue a token upon login
- Only allow /appointments if token is valid

Note: In production, you'd use hashed passwords and a proper auth system.
"""
"""
STEP 4 UPDATED: ADMIN LOGIN USING JSON BODY (SHOWS IN /docs)
----------------------------------------------------------
This version uses a Pydantic model for login credentials so that the endpoint appears in Swagger UI.
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3
from datetime import datetime

# ---------------------------------
# APP SETUP
# ---------------------------------
app = FastAPI(title="Mimie's Hair Studio API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------
# DATABASE SETUP
# ---------------------------------
conn = sqlite3.connect("appointments.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS appointments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT,
    service TEXT,
    date TEXT,
    time TEXT,
    created_at TEXT
)
""")
conn.commit()

# ---------------------------------
# ADMIN CREDENTIALS
# ---------------------------------
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "password123"  # Change this for production!

# ---------------------------------
# DATA MODELS
# ---------------------------------
class Appointment(BaseModel):
    name: str
    email: str
    service: str
    date: str
    time: str

class AdminLoginRequest(BaseModel):
    username: str
    password: str

# ---------------------------------
# ROUTES
# ---------------------------------
@app.get("/")
def home():
    return {"status": "Backend running"}

@app.post("/book")
def book_appointment(appointment: Appointment):
    cursor.execute(
        """
        INSERT INTO appointments (name, email, service, date, time, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            appointment.name,
            appointment.email,
            appointment.service,
            appointment.date,
            appointment.time,
            datetime.now().isoformat()
        )
    )
    conn.commit()
    return {"message": "Appointment booked successfully"}

# ---------------------------------
# ADMIN LOGIN (SHOWS IN /docs)
# ---------------------------------
@app.post("/admin/login")
def admin_login(data: AdminLoginRequest):
    if data.username != ADMIN_USERNAME or data.password != ADMIN_PASSWORD:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    return {"message": "Login successful", "token": "admin-token-12345"}

# ---------------------------------
# PROTECTED APPOINTMENTS ENDPOINT
# ---------------------------------
@app.get("/appointments")
def get_appointments(request: Request):
    token = request.headers.get("Authorization")
    if token != "Bearer admin-token-12345":
        raise HTTPException(status_code=401, detail="Unauthorized")

    cursor.execute("SELECT * FROM appointments")
    rows = cursor.fetchall()

    appointments = []
    for row in rows:
        appointments.append({
            "id": row[0],
            "name": row[1],
            "email": row[2],
            "service": row[3],
            "date": row[4],
            "time": row[5],
            "created_at": row[6]
        })
    return appointments

