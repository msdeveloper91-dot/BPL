from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "BPL - Bharat Premier League Server is Running!"}

@app.get("/tokens/{user_id}")
def get_tokens(user_id: str):
    # Abhi ke liye sample data, baad mein Supabase se connect karenge
    return {"user_id": user_id, "tokens": 10000}
