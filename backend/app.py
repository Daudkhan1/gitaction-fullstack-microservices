from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
import psycopg2

app = FastAPI()

# Allow frontend container (on different origin) to talk to this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or restrict to specific domain/IP
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Connect to PostgreSQL hosted on AWS
conn = psycopg2.connect(
    host="database-1.ch2cu2qaa4oh.ap-south-1.rds.amazonaws.com",
    port="5432",
    database="fullstack",
    user="daud",
    password="daud3738"
)

@app.post("/submit")
def submit(username: str = Form(...), email: str = Form(...)):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO users (username, email)
        VALUES (%s, %s)
    """, (username, email))
    conn.commit()
    cur.close()
    conn.close()
    return {"message": "User saved successfully!"}
