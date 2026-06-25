from pydantic import BaseModel, field_validator
from typing import Optional

class EntityBase(BaseModel):
    name: str   # común a todas: sujeto lotr:{name} + rdfs:label

class Character(EntityBase):
    givenName: Optional[str] = None
    familyName: Optional[str] = None
    alternateName: list[str] = []
    race: Optional[str] = None
    birthplace: Optional[str] = None
    affiliation: list[str] = []

class Race(EntityBase):
    @field_validator("longevity")
    def not_negative(cls, value):
        if value < 0:
            raise ValueError("cannot be negative")
        return value
    
    longevity: Optional[int] = None
    knowsLanguage: Optional[str] = None

class Place(EntityBase):
    territoryOf: Optional[str] = None

class Faction(EntityBase):
    leader: Optional[str] = None
    ally: list[str] = []
    enemy: list[str] = []
