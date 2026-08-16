from fastapi import Header, HTTPException

from auth import get_user_from_token


def get_current_user(authorization: str = Header(default=None)):
    
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Access token required")

    token = authorization.split(" ")[1]
    if not token:
        raise HTTPException(status_code=401, detail="Access token required")

    try:
        response = get_user_from_token(token)
        user = response.user
        if user is None:
            raise HTTPException(status_code=401, detail="Invalid or expired token")
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    return user