import logging
import os
from uuid import UUID

from dotenv import load_dotenv
from fastapi import APIRouter, BackgroundTasks, Depends, FastAPI, HTTPException
from gotrue import (
    AuthResponse,
    OAuthResponse,
    SignInWithEmailAndPasswordCredentials,
    SignInWithOAuthCredentials,
    SignUpWithEmailAndPasswordCredentials,
    errors,
)
from supabase import Client, create_client

from src.interfaces import db
from src.interfaces.db import supabase

router = APIRouter(
    prefix="/auth",
    tags=["authentication"],
)

logger = logging.getLogger("root")


@router.post("/sign_up")
def email_sign_up(
    sign_up_request: SignUpWithEmailAndPasswordCredentials,
) -> AuthResponse:
    """format for passing display name: 'options': {'data':{'display_name': 'name'}}"""
    try:
        response =supabase.auth.sign_up(sign_up_request)

    except errors.AuthApiError as e:
        raise HTTPException(e.status, e.to_dict())

    user = response.user
    if user and user.user_metadata.get("display_name"):
        display_name = user.user_metadata["display_name"]
        supabase.table("profiles").update({"display_name": display_name}).eq("id", user.id).execute()

    return response

@router.post("/sign_in")
def email_sign_in(
    sign_in_request: SignInWithEmailAndPasswordCredentials,
) -> AuthResponse:
    try:
        return supabase.auth.sign_in_with_password(sign_in_request)

    except errors.AuthApiError as e:
        raise HTTPException(e.status, e.to_dict())


@router.post("/sign_in/provider")
def provider_sign_in(provider_request: SignInWithOAuthCredentials) -> OAuthResponse:
    return supabase.auth.sign_in_with_oauth(provider_request)