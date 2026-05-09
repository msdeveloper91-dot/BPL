import os
from fastapi import FastAPI, HTTPException
from supabase import create_client, Client
from pydantic import BaseModel
from typing import List

# 1. Setup Supabase Connection
# Render ya Termux ke environment variables se keys uthayega
URL: str = os.environ.get("SUPABASE_URL")
KEY: str = os.environ.get("SUPABASE_KEY")

if not URL or not KEY:
    raise ValueError("SUPABASE_URL ya SUPABASE_KEY set nahi hai!")

supabase: Client = create_client(URL, KEY)

app = FastAPI(title="BPL Backend - Bharat Premier League")

# 2. Data Models (Jo data APK se aayega)
class BidRequest(BaseModel):
    player_id: int
    user_id: str
    bid_amount: int

# 3. API Endpoints

@app.get("/")
def home():
    return {"status": "Online", "game": "BPL - Bharat Premier League"}

# --- Player Management ---

@app.get("/players/all")
def get_all_players():
    """Saare players ki list Supabase se fetch karega"""
    try:
        response = supabase.table("players").select("*").execute()
        return {"status": "success", "data": response.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- Auction & Bidding Logic ---

@app.post("/auction/bid")
def place_bid(bid: BidRequest):
    """Bidding logic: Token check aur Real-time update"""
    try:
        # 1. User ke tokens check karein
        user_data = supabase.table("users").select("tokens").eq("id", bid.user_id).single().execute()
        if not user_data.data or user_data.data['tokens'] < bid.bid_amount:
            return {"status": "error", "message": "Aapke paas paryapt tokens nahi hain!"}

        # 2. Check karein ki bid current price se zyada hai ya nahi
        # (Yahan aap live_auction table call kar sakte hain)
        
        # 3. Update Auction Table
        # Kyunki Supabase mein Realtime ON hai, update hote hi sabhi APKs mein price badal jayega
        update_response = supabase.table("live_auction").upsert({
            "player_id": bid.player_id,
            "current_bid": bid.bid_amount,
            "highest_bidder": bid.user_id
        }).execute()

        return {"status": "success", "message": f"Boli lag gayi: {bid.bid_amount}", "data": update_response.data}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- User Profile ---

@app.get("/user/{user_id}")
def get_user_stats(user_id: str):
    """User ke tokens aur team stats fetch karega"""
    try:
        response = supabase.table("users").select("*").eq("id", user_id).single().execute()
        return {"status": "success", "data": response.data}
    except Exception as e:
        return {"status": "error", "message": "User nahi mila"}
