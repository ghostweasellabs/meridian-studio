import os
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt

JWT_SECRET = os.getenv("JWT_SECRET", "super-secret-jwt-token-with-at-least-32-characters-long")
ALGORITHMS = ["HS256"]

http_bearer = HTTPBearer(auto_error=True)

class AuthenticatedUser(dict):
    pass

async def get_current_user(creds: HTTPAuthorizationCredentials = Depends(http_bearer)) -> AuthenticatedUser:
    token = creds.credentials
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=ALGORITHMS)
        role = payload.get("role")
        sub = payload.get("sub") or payload.get("uid") or payload.get("user_id")
        if not sub:
            raise ValueError("Missing user id in token")
        return AuthenticatedUser(user_id=sub, role=role)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token") from exc
