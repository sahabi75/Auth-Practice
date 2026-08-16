from fastapi import FastAPI, HTTPException, Depends

from auth import sign_up_user, sign_in_user, sign_out_user
from dependencies import get_current_user
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


@app.post("/auth/logout", status_code=204)
def logout(user=Depends(get_current_user)):
    sign_out_user(None)
    return


@app.get("/public/info")
def public_info():
    return {"message": "Welcome stranger! This info is public."}


@app.get("/protected/profile")
def protected_profile(user=Depends(get_current_user)):
    return {
        "id": user.id,
        "email": user.email,
        "created_at": user.created_at,
    }


@app.get("/protected/dashboard")
def protected_dashboard(user=Depends(get_current_user)):
    return {"message": f"Welcome to your dashboard, {user.email}!"}