from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
from psycopg2 import OperationalError

app = FastAPI()

# Allow frontend container (on different origin) to talk to this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or restrict to specific domain/IP
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database connection settings
DB_SETTINGS = {
    "host": "database-1.ch2cu2qaa4oh.ap-south-1.rds.amazonaws.com",
    "port": "5432",
    "database": "fullstack",
    "user": "daud",
    "password": "daud3738"
}

def get_db_connection():
    """Establish a new database connection."""
    try:
        conn = psycopg2.connect(
            host=DB_SETTINGS['host'],
            port=DB_SETTINGS['port'],
            database=DB_SETTINGS['database'],
            user=DB_SETTINGS['user'],
            password=DB_SETTINGS['password']
        )
        return conn
    except OperationalError as e:
        print(f"Error while connecting to PostgreSQL: {e}")
        return None

@app.post("/submit")
def submit(username: str = Form(...), email: str = Form(...)):
    conn = get_db_connection()
    if conn is None:
        return {"message": "Database connection failed!"}

    cur = conn.cursor()
    cur.execute("""
        INSERT INTO users (username, email)
        VALUES (%s, %s)
    """, (username, email))
    conn.commit()
    cur.execute("SELECT id, username, email FROM users")
    rows = cur.fetchall()
    user_list = [{"id": row[0], "username": row[1], "email": row[2]} for row in rows]
    cur.close()
    conn.close()

    
    
    return {"message": "User saved successfully!", "users": user_list}
