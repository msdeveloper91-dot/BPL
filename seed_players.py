import os
from supabase import create_client

# Environment variables (Jo aapne Render/Termux mein set kiye honge)
url = "https://cppbrysqlzormgpbzhee.supabase.co/rest/v1/"
key = "sb_publishable_LplnzMp8DZ3wcFURl40BjA_YL1xykk6"
supabase = create_client(url, key)

# Sabhi IPL/BPL players ki list
players_list = [
    {"name": "Virat Kohli", "role": "Batsman", "rating": 95, "base_price": 2000000},
    {"name": "MS Dhoni", "role": "Wicketkeeper", "rating": 92, "base_price": 1500000},
    {"name": "Jasprit Bumrah", "role": "Bowler", "rating": 96, "base_price": 1800000},
    {"name": "Hardik Pandya", "role": "All-rounder", "rating": 90, "base_price": 1600000},
    {"name": "Rohit Sharma", "role": "Batsman", "rating": 93, "base_price": 1900000},
    {"name": "Rashid Khan", "role": "Bowler", "rating": 94, "base_price": 1700000}
    # Aap yahan jitne chahe players add kar sakte hain
]

def upload_players():
    print("Players upload ho rahe hain...")
    try:
        response = supabase.table("players").insert(players_list).execute()
        print("Success! Saare players Supabase mein set ho gaye hain.")
    except Exception as e:
        print(f"Error aaya hai: {e}")

if __name__ == "__main__":
    upload_players()
