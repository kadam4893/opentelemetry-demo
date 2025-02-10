from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import mysql.connector
import os

app = FastAPI()

DB_HOST = os.getenv("MYSQL_HOST", "mysql")
DB_USER = os.getenv("MYSQL_USER", "demo_user")
DB_PASSWORD = os.getenv("MYSQL_PASSWORD", "demo_password")
DB_NAME = os.getenv("MYSQL_DATABASE", "demo_db")

def get_db_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

class User(BaseModel):
    username: str
    password: str

@app.post("/login")
def login(user: User):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    query = "SELECT * FROM users WHERE username=%s AND password=%s"
    cursor.execute(query, (user.username, user.password))
    result = cursor.fetchone()
    
    cursor.close()
    conn.close()
    
    if result:
        return {"message": "Login successful"}
    raise HTTPException(status_code=401, detail="Invalid credentials")
