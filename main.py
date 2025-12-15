"""
STEP 1: BACKEND (FastAPI)
-----------------------
This file creates a simple backend server that:
- Runs 24/7 when hosted
- Receives booking data from the website
- Stores appointments in a database

Think of this like a Python script that never stops running.
"""
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3
from datetime import datetime

app = FastAPI(title="Mimie's Hair Studio API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database
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

# Admin credentials
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "password123"

# Models
class Appointment(BaseModel):
    name: str
    email: str
    service: str
    date: str
    time: str

class AdminLoginRequest(BaseModel):
    username: str
    password: str

# Routes
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
        (appointment.name, appointment.email, appointment.service, appointment.date, appointment.time, datetime.now().isoformat())
    )
    conn.commit()
    return {"message": "Appointment booked successfully"}

# Admin login using Pydantic body
@app.post("/admin/login")
def admin_login(data: AdminLoginRequest):
    if data.username != ADMIN_USERNAME or data.password != ADMIN_PASSWORD:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    return {"message": "Login successful", "token": "admin-token-12345"}

# Protected appointments
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



# ---------------------------------
# HOW TO RUN LOCALLY (IMPORTANT)
# ---------------------------------
# 1. pip install fastapi uvicorn
# 2. uvicorn main:app --reload
# 3. Open http://127.0.0.1:8000/docs
