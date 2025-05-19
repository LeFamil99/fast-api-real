from fastapi import APIRouter, Depends
from sqlalchemy import insert
from sqlalchemy.orm import Session


from src.api.core.db import get_db
from src.api.schemas.item import Item, ItemSchema

router = APIRouter(
    prefix="/items",
    tags=["items"],
    responses={404: {"description": "Item not found"}},
)


@router.get("/", response_model=list[ItemSchema])
async def get_items(db: Session = Depends(get_db)):
    return db.query(Item).all()


@router.get("/{id}", response_model=ItemSchema)
async def get_item(id: str, db: Session = Depends(get_db)):
    return db.query(Item).filter(Item.id == id).first()

@router.post("/{id}", response_model=ItemSchema)
async def create_item(item: ItemSchema, db: Session = Depends(get_db)):
    db_item = Item(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.delete("/{id}")
async def delete_item(id: str, db: Session = Depends(get_db)):
    return db.query(Item).filter(Item.id == id).delete()