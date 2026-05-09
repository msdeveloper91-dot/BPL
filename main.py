import os
from fastapi import FastAPI, HTTPException
from supabase import create_client, Client
from pydantic import BaseModel

# 1. Setup Supabase Connection
# Maine aapki di hui keys yahan direct set kar di hain
URL: str = "https://cppbrysqlzormgpbzhee.supabase.co"
KEY: str = "sb_publishable_LplnzMp8DZ3wcFURl40BjA_YL1xykk6"

supabase: Client = create_client(URL, KEY)

app = FastAPI(title="BPL Backend")

# 2. Bidding Model
class BidRequest(BaseModel):
    player_id: int
    user_id: str
    bid_amount: int

# 3. API Endpoints

@app.get("/")
def home():
    return {"status": "Online", "msg": "Welcome to Bharat Premier League Server"}

@app.get("/players/all")
def get_all_players():
    """Database se saare players ki list laayega"""
    try:
        # Note: Table ka naam 'players' hona chahiye (small letters)
        response = supabase.table("players").select("*").execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database Error: {str(e)}")

@app.post("/auction/bid")
def place_bid(bid: BidRequest):
    """User ke tokens check karega aur bid update karega"""
    try:
        # 1. User ke tokens check karein (Default 100000 agar table bani hai)
        user = supabase.table("users").select("tokens").eq("id", bid.user_id).single().execute()
        
        if not user.data or user.data['tokens'] < bid.bid_amount:
            return {"status": "error", "message": "Tokens kam hain!"}

        # 2. Auction table update karein (Taaki Real-time update ho)
        # Table 'live_auction' honi chahiye
        supabase.table("live_auction").upsert({
            "player_id": bid.player_id,
            "current_bid": bid.bid_amount,
            "highest_bidder": bid.user_id
        }).execute()

        return {"status": "success", "msg": "Boli lag gayi!"}
    
    except Exception as e:
        return {"status": "error", "detail": str(e)}

# --- User Registration (Tokens dene ke liye) ---
@app.post("/user/register")
def register_user(user_id: str, username: str):
    try:
        supabase.table("users").insert({
            "id": user_id,
            "username": username,
            "tokens": 100000  # Welcome Bonus
        }).execute()
        return {"msg": "User Registered with 1 Lakh tokens!"}
    except:
        return {"msg": "User already exists"}
