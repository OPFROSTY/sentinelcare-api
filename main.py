from fastapi import FastAPI
import os
from supabase import create_client, Client

app = FastAPI()

# Carrega variáveis de ambiente
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.get("/")
def home():
    return {"status": "SentinelCare API online"}

@app.get("/ping")
def ping():
    return {"ping": "pong"}

@app.get("/test-db")
def test_db():
    response = supabase.table("users").select("*").limit(1).execute()
    return {
        "connected": True,
        "data": response.data
    }
