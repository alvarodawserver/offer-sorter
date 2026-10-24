from app.schemas import OfferRead, WorkMode
from fastapi import APIRouter

router = APIRouter(prefix="/offers", tags=["offers"])


premade_offers = [
    OfferRead(
        id=1,
        title="Python Developer",
        company="ABC Corp",
        description="Backend role with Python and FastAPI. 2+ years of experience. Fully remote.",
        work_mode=WorkMode.remote,
    ),
    OfferRead(
        id=2,
        title="Frontend Developer",
        company="Tech Inc",
        description="React and TypeScript developer for our office team. English required.",
        work_mode=WorkMode.onsite,
    ),
    OfferRead(
        id=3,
        title="Fullstack Developer",
        company="Python&Co",
        description="Django and Vue.js. 3 days at the office, 2 from home. 1+ year of experience.",
        work_mode=WorkMode.hybrid,
    ),
]


@router.get("")
def read_offers() -> list[OfferRead]:
    return premade_offers
