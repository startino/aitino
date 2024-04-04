import logging
from uuid import UUID

from fastapi import APIRouter, HTTPException

from src.interfaces import db
from src.models import (
    ProfileResponseModel,
    ProfileUpdateModel,
    ProfileRequestModel,
    APIKeyResponseModel,
    APIKeyRequestModel,
)

router = APIRouter(prefix="/profiles", tags=["profiles"])

@router.get("/")
def get_profiles() -> list[ProfileResponseModel]:
    return db.get_profiles()


@router.post("/", status_code=201)
def insert_profile(profile: ProfileRequestModel) -> ProfileResponseModel:
    return db.insert_profile(profile)


@router.get("/{profile_id}")
def get_profile(profile_id: UUID) -> ProfileResponseModel:
    profile = db.get_profile_from_id(profile_id)
    if not profile:
        raise HTTPException(404, "profile not found")

    return profile
    

@router.get("/{profile_id}/api_keys")
def get_api_keys(profile_id: UUID) -> dict[UUID, str]:
    """Returns api keys with the format: {api_key_type_id: api_key}."""
    if not db.get_profile_from_id(profile_id):
        raise HTTPException(404, "profile not found")

    return db.get_api_keys(profile_id)


@router.patch("/{profile_id}")
def update_profile(
    profile_id: UUID, profile_update_request: ProfileUpdateModel
) -> ProfileResponseModel:
    if not db.get_profile_from_id(profile_id):
        raise HTTPException(404, "profile not found")

    return db.update_profile(profile_id, profile_update_request)


@router.post("/api_keys", status_code=201)
def insert_api_key(api_key_request: APIKeyRequestModel) -> APIKeyResponseModel:
    return db.insert_api_key(api_key_request)


@router.delete("/api_keys/{api_key_id}")
def delete_api_key(api_key_id: UUID) -> APIKeyResponseModel:
    deleted_key = db.delete_api_key(api_key_id)
    if not deleted_key:
        raise HTTPException(404, "api key id not found")

    return deleted_key
