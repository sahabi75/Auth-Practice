import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


def sign_up_user(email: str, password: str):
    response = supabase.auth.sign_up({"email": email, "password": password})
    return response


def sign_in_user(email: str, password: str):
    response = supabase.auth.sign_in_with_password(
        {"email": email, "password": password}
    )
    return response


def sign_out_user(token: str):
    supabase.auth.sign_out()


def get_user_from_token(token: str):
    response = supabase.auth.get_user(token)
    return response