from collections.abc import Iterator

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app
from app.models import Offer
from app.schemas import WorkMode

engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(bind=engine)

SAMPLE_OFFERS = [
    {
        "title": "Python Developer",
        "company": "ABC Corp",
        "description": "Backend role with Python and FastAPI. 2+ years of experience. Fully remote.",
        "work_mode": WorkMode.remote,
    },
    {
        "title": "Frontend Developer",
        "company": "Tech Inc",
        "description": "React and TypeScript developer for our office team. English required.",
        "work_mode": WorkMode.onsite,
    },
    {
        "title": "Fullstack Developer",
        "company": "Python&Co",
        "description": "Django and Vue.js. 3 days at the office, 2 from home. 1+ year of experience.",
        "work_mode": WorkMode.hybrid,
    },
]


def override_get_db() -> Iterator[Session]:
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(autouse=True)
def setup_database() -> Iterator[None]:
    Base.metadata.create_all(engine)
    session = TestingSessionLocal()
    session.add_all([Offer(**offer) for offer in SAMPLE_OFFERS])
    session.commit()
    session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield
    app.dependency_overrides.clear()
    Base.metadata.drop_all(engine)
