from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import Mapping
from schemas import (
    MappingCreate,
    MappingUpdate,
    MappingResponse,
    MappingListResponse
)

router = APIRouter(
    prefix="/api/mappings",
    tags=["Mappings"]
)


@router.get("", response_model=MappingListResponse)
def get_mappings(db: Session = Depends(get_db)):
    mappings = db.query(Mapping).all()
    return {"mappings": mappings}


@router.post("", response_model=MappingResponse)
def create_mapping(
    mapping: MappingCreate,
    db: Session = Depends(get_db)
):
    existing = db.query(Mapping).filter(
        Mapping.master_account_id == mapping.master_account_id,
        Mapping.child_account_id == mapping.child_account_id
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Mapping already exists"
        )

    db_mapping = Mapping(
        master_account_id=mapping.master_account_id,
        child_account_id=mapping.child_account_id,
        multiplier=mapping.multiplier
    )

    db.add(db_mapping)
    db.commit()
    db.refresh(db_mapping)

    return db_mapping


@router.put("/{mapping_id}/toggle")
def toggle_mapping(
    mapping_id: str,
    db: Session = Depends(get_db)
):
    mapping = db.query(Mapping).filter(
        Mapping.id == mapping_id
    ).first()

    if not mapping:
        raise HTTPException(
            status_code=404,
            detail="Mapping not found"
        )

    mapping.is_active = not mapping.is_active

    db.commit()
    db.refresh(mapping)

    return {
        "id": mapping.id,
        "is_active": mapping.is_active,
        "message": "Mapping status updated"
    }


@router.put("/{mapping_id}", response_model=MappingResponse)
def update_mapping(
    mapping_id: str,
    mapping: MappingUpdate,
    db: Session = Depends(get_db)
):
    db_mapping = db.query(Mapping).filter(
        Mapping.id == mapping_id
    ).first()

    if not db_mapping:
        raise HTTPException(
            status_code=404,
            detail="Mapping not found"
        )

    db_mapping.multiplier = mapping.multiplier

    db.commit()
    db.refresh(db_mapping)

    return db_mapping

@router.delete("/{mapping_id}")
def delete_mapping(
    mapping_id: str,
    db: Session = Depends(get_db)
):
    mapping = db.query(Mapping).filter(
        Mapping.id == mapping_id
    ).first()

    if not mapping:
        raise HTTPException(
            status_code=404,
            detail="Mapping not found"
        )

    db.delete(mapping)
    db.commit()

    return {
        "message": "Mapping deleted successfully"
    }