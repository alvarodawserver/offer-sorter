from itertools import count

from fastapi import APIRouter, HTTPException

from app.schemas import OfferCreate, OfferRead, WorkMode

router = APIRouter(prefix="/offers", tags=["offers"])

db_offers: dict[int, OfferRead] = {
    1: OfferRead(
        id=1,
        title="Python Developer",
        company="ABC Corp",
        description="Backend role with Python and FastAPI. 2+ years of experience. Fully remote.",
        work_mode=WorkMode.remote,
    ),
    2: OfferRead(
        id=2,
        title="Frontend Developer",
        company="Tech Inc",
        description="React and TypeScript developer for our office team. English required.",
        work_mode=WorkMode.onsite,
    ),
    3: OfferRead(
        id=3,
        title="Fullstack Developer",
        company="Python&Co",
        description="Django and Vue.js. 3 days at the office, 2 from home. 1+ year of experience.",
        work_mode=WorkMode.hybrid,
    ),
}
# Starts at 4 because ids 1-3 are taken by the sample offers above.
id_counter = count(start=4)


def get_offer_or_404(offer_id: int) -> OfferRead:
    if offer_id not in db_offers:
        raise HTTPException(status_code=404, detail="Offer not found")
    return db_offers[offer_id]


@router.get("")
def read_offers() -> list[OfferRead]:
    return list(db_offers.values())


@router.get("/{offer_id}")
def read_offer(offer_id: int) -> OfferRead:
    return get_offer_or_404(offer_id)


@router.post("", status_code=201)
def create_offer(offer: OfferCreate) -> OfferRead:
    new_id = next(id_counter)
    new_offer = OfferRead(id=new_id, **offer.model_dump())
    db_offers[new_id] = new_offer
    return new_offer


@router.delete("/{offer_id}", status_code=204)
def delete_offer(offer_id: int) -> None:
    get_offer_or_404(offer_id)
    del db_offers[offer_id]
