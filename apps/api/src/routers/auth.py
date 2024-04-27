import os

from dotenv import load_dotenv
from fastapi import APIRouter
from gotrue import OAuthResponse, SignInWithOAuthCredentials
from supabase import Client, create_client

router = APIRouter(
    prefix="/auth",
    tags=["authentication"],
)
load_dotenv()

url: str | None = os.environ.get("SUPABASE_URL")
key: str | None = os.environ.get("SUPABASE_ANON_KEY")

if url is None or key is None:
    raise ValueError("SUPABASE_URL and SUPABASE_ANON_KEY must be set")


@router.post("/sign_in/provider")
def provider_sign_in(provider_request: SignInWithOAuthCredentials) -> OAuthResponse:
    supabase: Client = create_client(url, key)
    return supabase.auth.sign_in_with_oauth(provider_request)
