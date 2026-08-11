from fastapi import FastAPI

from auth import supabase

app = FastAPI(title="Auth Login & Protect API")


@app.on_event("startup")
def on_startup():
    print("Server running and connected to Supabase")


@app.get("/")
def root():
    return {"message": "Server is running"}