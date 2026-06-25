from pydantic import BaseModel


class EntityBase(BaseModel):
    name: str   # común a todas: sujeto lotr:{name} + rdfs:label

class Character(EntityBase):
    givenName: str | None = None
    familyName: str | None = None
    alternateName: list[str] = []
    race: str | None = None
    birthplace: str | None = None
    affiliation: list[str] = []

class Race(EntityBase):
    longevity: int | None = None        # int → matchea xsd:integer
    knowsLanguage: str | None = None

class Place(EntityBase):
    containedInPlace: str | None = None

class Faction(EntityBase):
    leader: str | None = None
    ally: list[str] = []
    enemy: list[str] = []
