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
    APIKeyUpdateModel,
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
def get_api_keys(profile_id: UUID) -> list[APIKeyResponseModel]:
    """Returns api keys with the api key type as an object with the id, name, description etc."""
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

@router.patch("/api_keys/{api_key_id}")
def update_api_key(api_key_id: UUID, api_key_update: APIKeyUpdateModel) -> APIKeyResponseModel:
    return db.update_api_key(api_key_id, api_key_update)
