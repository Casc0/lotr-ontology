from pydantic import BaseModel
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
    longevity: Optional[int] = None        # int → matchea xsd:integer
    knowsLanguage: Optional[str] = None

class Place(EntityBase):
    territoryOf: Optional[str] = None

class Faction(EntityBase):
    leader: Optional[str] = None
    ally: list[str] = []
    enemy: list[str] = []
