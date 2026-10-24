from pydantic import BaseModel
from enum import Enum


class WorkMode(str, Enum):
    onsite = "onsite"
    remote = "remote"
    hybrid = "hybrid"


class OfferBase(BaseModel):
    title: str
    description: str
    company: str
    work_mode: WorkMode


class OfferCreate(OfferBase):
    pass


class OfferRead(OfferBase):
    id: int
