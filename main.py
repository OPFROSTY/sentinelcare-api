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

from pydantic import BaseModel

class UserCreate(BaseModel):
    nome: str
    idade: int
    doenca: str

@app.post("/users")
def create_user(user: UserCreate):
    response = supabase.table("users").insert({
        "nome": user.nome,
        "idade": user.idade,
        "doenca": user.doenca
    }).execute()

    return {
        "success": True,
        "user": response.data
    }

@app.get("/users")
def get_users():
    response = supabase.table("users").select("*").execute()

    return {
        "success": True,
        "users": response.data
    }


