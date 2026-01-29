from fastapi import FastAPI
import os
from supabase import create_client, Client

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # depois a gente restringe
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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

from fastapi import HTTPException

@app.get("/users/{user_id}")
def get_user_by_id(user_id: str):
    response = supabase.table("users").select("*").eq("id", user_id).execute()

    if not response.data:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    return {
        "success": True,
        "user": response.data[0]
    }
class CheckinCreate(BaseModel):
    user_id: str
    glicemia: int
    dor: int
    fadiga: int
    falta_ar: bool = False

def calcular_risco(glicemia: int, dor: int, fadiga: int, falta_ar: bool) -> str:
    pontos = 0
    if glicemia > 250:
        pontos += 3
    if dor >= 7:
        pontos += 2
    if fadiga >= 7:
        pontos += 2
    if falta_ar:
        pontos += 3

    if pontos >= 6:
        return "ALTO"
    if pontos >= 3:
        return "MEDIO"
    return "BAIXO"

@app.post("/checkins")
def create_checkin(payload: CheckinCreate):
    risco = calcular_risco(payload.glicemia, payload.dor, payload.fadiga, payload.falta_ar)

    # opcional: validar se user existe
    user = supabase.table("users").select("id").eq("id", payload.user_id).limit(1).execute()
    if not user.data:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    inserted = supabase.table("checkins").insert({
        "user_id": payload.user_id,
        "glicemia": payload.glicemia,
        "dor": payload.dor,
        "fadiga": payload.fadiga,
        "falta_ar": payload.falta_ar,
    }).execute()

    return {
        "success": True,
        "risco": risco,
        "checkin": inserted.data[0] if inserted.data else None
    }



