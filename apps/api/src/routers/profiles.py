import logging
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from src.interfaces import db
from src.models import (
    Profile,
    ProfileGetRequest,
    ProfileInsertRequest,
    ProfileUpdateRequest,
)

router = APIRouter(prefix="/profiles", tags=["profiles"])


@router.get("/")
def get_profiles(q: ProfileGetRequest = Depends()) -> list[Profile]:
    return db.get_profiles(q.tier_id, q.display_name, q.stripe_customer_id)


@router.post("/", status_code=201)
def insert_profile(profile: ProfileInsertRequest) -> Profile:
    return db.insert_profile(profile)


@router.get("/{id}")
def get_profile_by_id(id: UUID) -> Profile:
    profile = db.get_profile(id)
    if not profile:
        raise HTTPException(404, "profile not found")

    return profile


@router.delete("/{id}")
def delete_profile(id: UUID) -> Profile:
    return db.delete_profile(id)


@router.patch("/{id}")
def update_profile(
    id: UUID, profile_update_request: ProfileUpdateRequest
) -> Profile:
    if not db.get_profile(id):
        raise HTTPException(404, "profile not found")

    return db.update_profile(id, profile_update_request)
