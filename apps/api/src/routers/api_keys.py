import logging
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from src.interfaces import db
from src.models import (
    APIKey,
    APIKeyInsertRequest,
    APIKeyUpdateRequest,
    APIKeyGetRequest,
)

router = APIRouter(prefix="/api_keys", tags=["api keys"])


@router.get("/")
def get_api_keys(q: APIKeyGetRequest = Depends()) -> list[APIKey]:
    """Returns api keys with the api key type as an object with the id, name, description etc."""
    if q.profile_id:
        if not db.get_profile(q.profile_id):
            raise HTTPException(404, "profile not found")
    
    return db.get_api_keys(q.profile_id, q.api_key_type_id, q.api_key)


@router.get("/{api_key_id}")
def get_api_key(api_key_id: UUID) -> APIKey:
    response = db.get_api_key(api_key_id)
    if not response:
        raise HTTPException(404, "id not found")

    return response


@router.post("/", status_code=201)
def insert_api_key(api_key_request: APIKeyInsertRequest) -> APIKey:
    response = db.insert_api_key(api_key_request)
    if not response:
        raise HTTPException(404, "could not find given type id")

    return response

@router.delete("/{api_key_id}")
def delete_api_key(api_key_id: UUID) -> APIKey:
    deleted_key = db.delete_api_key(api_key_id)
    if not deleted_key:
        raise HTTPException(404, "api key id not found")

    return deleted_key


@router.patch("/{api_key_id}")
def update_api_key(api_key_id: UUID, api_key_update: APIKeyUpdateRequest) -> APIKey:
    return db.update_api_key(api_key_id, api_key_update)