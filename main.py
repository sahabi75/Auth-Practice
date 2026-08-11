from fastapi import FastAPI, HTTPException, Header

from auth import supabase, sign_up_user, sign_in_user
from models import SignupRequest, LoginRequest

app = FastAPI(title="Auth Login & Protect API")


@app.on_event("startup")
def on_startup():
    print("Server running and connected to Supabase")


@app.get("/")
def root():
    return {"message": "Server is running"}


@app.post("/auth/signup", status_code=201)
def signup(payload: SignupRequest):
    if not payload.email or not payload.password:
        raise HTTPException(status_code=400, detail="Email and password are required")

    try:
        response = sign_up_user(payload.email, payload.password)
        return {"user": response.user}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/auth/login")
def login(payload: LoginRequest):
    if not payload.email or not payload.password:
        raise HTTPException(status_code=400, detail="Email and password are required")

    try:
        response = sign_in_user(payload.email, payload.password)
        return {
            "access_token": response.session.access_token,
            "refresh_token": response.session.refresh_token,
        }
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid login credentials")


@app.get("/public/info")
def public_info():
    return {"message": "Welcome stranger! This info is public."}


@app.get("/protected/profile")
def protected_profile(authorization: str = Header(default=None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Access token required")

    token = authorization.split(" ")[1]
    if not token:
        raise HTTPException(status_code=401, detail="Access token required")

    
    return {"message": "Token received (not yet verified)"}