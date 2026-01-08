from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"status": "SentinelCare API online"}

@app.get("/ping")
def ping():
    return {"ping": "pong"}
