import logging
import os
from uuid import UUID

import jwt
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.interfaces import db
from src.models import Profile

load_dotenv()

JWT_SECRET = os.environ.get("SUPABASE_JWT_SECRET")
ALGORITHM = "HS256"


async def get_current_user(token: HTTPAuthorizationCredentials = Depends(HTTPBearer())) -> Profile:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # authorises with test profile
    if token.credentials == "xdd":
        profile = db.get_profile(UUID("eebb6aaf-0412-41ff-ade9-547dbbc6d9f1"))
        assert profile
        return profile

    payload = jwt.decode(
        token.credentials, JWT_SECRET, algorithms=[ALGORITHM], audience="authenticated"
    )
    user_id: str = payload.get("sub")
    profile = db.get_profile(UUID(user_id))

    if not user_id or not profile:
        raise credentials_exception

    return profile
