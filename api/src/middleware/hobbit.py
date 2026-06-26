from rdflib.query import Result
from fastapi import HTTPException, Request
from api.src.constants import CHARACTER_PREDICATES
from typing import Optional
from api.src.schemas import Character

def normalize_tuples(response: Result) -> list[dict[str, str]]:
    tuples = []
    for row in response:
        tuples.append(
            {
                "subject": str(row.sub),
                "predicate": str(row.pred),
                "object": str(row.obj)
            }
        )
    return tuples

def validate_character_props(prop: Optional[str] = None, obj: Optional[str] = None) -> tuple[Optional[str], Optional[str]]:
    if (prop is None) != (obj is None):
        raise HTTPException(status_code=400, detail="Provide both 'prop' and 'obj' or neither")
    if prop and prop not in CHARACTER_PREDICATES:
        raise HTTPException(status_code=400, detail=f"Invalid predicate: '{prop}'")
    return prop, obj

def validate_character_body(body: Character, request: Request) -> Character:
    ontology = request.app.state.ontology
    if body.race and not ontology.get_race_data(body.race):
        raise HTTPException(status_code=400, detail=f"Race: '{body.race}' invalid")
    if body.birthplace and not ontology.get_place_data(body.birthplace):
        raise HTTPException(status_code=400, detail=f"Birthplace: '{body.birthplace}' invalid")
    for aff in body.affiliation:
        if not ontology.get_faction_data(aff):
            raise HTTPException(status_code=400, detail=f"Affiliation: '{aff}' invalid")
    return body