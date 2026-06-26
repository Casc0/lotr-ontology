from rdflib.query import Result
from fastapi import HTTPException, Request
from api.src.constants import CHARACTER_PREDICATES, CHARACTER_VALIDATORS, FACTION_VALIDATORS, FACTION_PREDICATES, PLACE_PREDICATES, PLACE_VALIDATORS, RACE_PREDICATES
from typing import Optional
from api.src.schemas import Character, Faction, Place

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

def _validate_props(prop: Optional[str] = None, obj: Optional[str] = None, CLASS_SET: Optional[set] = None) -> tuple[Optional[str], Optional[str]]:
    if (prop is None) != (obj is None):
        raise HTTPException(status_code=400, detail="Provide both 'prop' and 'obj' or neither")
    if prop and CLASS_SET and prop not in CLASS_SET:
        raise HTTPException(status_code=400, detail=f"Invalid predicate: '{prop}'")
    return prop, obj


def validate_character_props(prop: Optional[str] = None, obj: Optional[str] = None) -> tuple[Optional[str], Optional[str]]:
    return _validate_props(prop, obj, CHARACTER_PREDICATES)

def validate_place_props(prop: Optional[str] = None, obj: Optional[str] = None) -> tuple[Optional[str], Optional[str]]:
    return _validate_props(prop, obj, PLACE_PREDICATES)

def validate_faction_props(prop: Optional[str] = None, obj: Optional[str] = None) -> tuple[Optional[str], Optional[str]]:
    return _validate_props(prop, obj, FACTION_PREDICATES)

def validate_race_props(prop: Optional[str] = None, obj: Optional[str] = None) -> tuple[Optional[str], Optional[str]]:
    return _validate_props(prop, obj, RACE_PREDICATES)


def _validate_body(body, request: Request, validators: dict):
    ontology = request.app.state.ontology
    for field, (method_name, label) in validators.items():
        value = getattr(body, field, None)
        
        if value is None: #skips validation if the field is not present in the body
            continue
        getter = getattr(ontology, method_name)
        items = value if isinstance(value, list) else [value] #makes it iterable
        for item in items:
            if not getter(item):
                raise HTTPException(status_code=400, detail=f"{label}: '{item}' invalid")
    return body

def validate_character_body(body: Character, request: Request) -> Character:
    return _validate_body(body, request, CHARACTER_VALIDATORS)

def validate_place_body(body: Place, request: Request) -> Place:
    return _validate_body(body, request, PLACE_VALIDATORS)

def validate_faction_body(body: Faction, request: Request) -> Faction:
    return _validate_body(body, request, FACTION_VALIDATORS)
