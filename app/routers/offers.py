from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import SessionDep
from app.models import Offer
from app.schemas import OfferCreate, OfferRead

router = APIRouter(prefix="/offers", tags=["offers"])


def get_offer_or_404(offer_id: int, db: Session) -> Offer:
    offer = db.get(Offer, offer_id)
    if offer is None:
        raise HTTPException(status_code=404, detail="Offer not found")
    return offer


@router.get("")
def read_offers(db: SessionDep) -> list[OfferRead]:
    return db.scalars(select(Offer)).all()


@router.get("/{offer_id}")
def read_offer(offer_id: int, db: SessionDep) -> OfferRead:
    return get_offer_or_404(offer_id, db)


@router.post("", status_code=201)
def create_offer(offer: OfferCreate, db: SessionDep) -> OfferRead:
    new_offer = Offer(**offer.model_dump())
    db.add(new_offer)
    db.commit()
    db.refresh(new_offer)
    return new_offer


@router.delete("/{offer_id}", status_code=204)
def delete_offer(offer_id: int, db: SessionDep) -> None:
    offer = get_offer_or_404(offer_id, db)
    db.delete(offer)
    db.commit()
