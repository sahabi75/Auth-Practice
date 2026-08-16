# Auth Login & Protect API

A secure FastAPI backend that handles user authentication (Sign Up, Log In,
Log Out) and protects specific routes using Supabase Auth as the Identity
Provider. Supabase manages the accounts and issues JSON Web Tokens (JWTs);
this API verifies those tokens to guard protected endpoints.

## How it works

1. Client sends email/password to `/auth/signup` or `/auth/login`.
2. Supabase validates the credentials and returns a JWT (access token).
3. Client sends that JWT in the `Authorization: Bearer <token>` header on
   protected requests.
4. The API verifies the token with Supabase before granting access.

No passwords or cryptography are handled directly by this server — Supabase
does all of that.

## Setup

### 1. Create a Supabase project
- Sign up at [supabase.com](https://supabase.com) (free, no card required)
- Create a new project
- Go to **Project Settings → API** and copy your **Project URL** and
  **anon public key**

### 2. Configure environment variables
Copy `.env.example` to `.env` and fill in your real values:

SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_anon_key
PORT=8000

`.env` is git-ignored and never committed.

### 3. Install dependencies
python -m venv venv
venv\Scripts\activate
python -m pip install -r requirements.txt
### 4. Run the server
python -m uvicorn main:app --reload
Server runs at `http://127.0.0.1:8000`. Interactive docs available at
`http://127.0.0.1:8000/docs`.

## API Reference

| Method | Endpoint               | Description                  | Auth required |
|--------|------------------------|-------------------------------|----------------|
| POST   | `/auth/signup`         | Create a new user account     | No             |
| POST   | `/auth/login`          | Authenticate & return a JWT   | No             |
| POST   | `/auth/logout`         | End the user's session        | Yes (Bearer)   |
| GET    | `/public/info`         | Public, unprotected data      | No             |
| GET    | `/protected/profile`   | Read private profile data     | Yes (Bearer)   |
| GET    | `/protected/dashboard` | Read protected dashboard data | Yes (Bearer)   |

## Status Codes

| Code | Meaning                              |
|------|----------------------------------------|
| 200  | Successful login / protected read       |
| 201  | Signup successful                       |
| 204  | Logout successful                       |
| 400  | Missing email or password               |
| 401  | Missing, malformed, invalid, or expired token / wrong credentials |

## Swagger UI — Bearer Auth

`/docs` shows a lock icon next to every protected route. Click
**Authorize**, paste your access token (no `Bearer` prefix needed), and
**Try it out** on any protected endpoint directly from the browser.

![Swagger UI Screenshot](swagger ui.png)

## Project Structure
auth-login-protect/
├── main.py # FastAPI app — all routes
├── auth.py # Supabase client + signup/login/logout logic
├── dependencies.py # Reusable bearer-token verification dependency
├── models.py # Pydantic request schemas
├── .env # Real secrets (git-ignored)
├── .env.example # Placeholder env template (committed)
└── requirements.txt