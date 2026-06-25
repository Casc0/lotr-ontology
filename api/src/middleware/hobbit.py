from rdflib.query import Result
from fastapi import HTTPException
from api.src.constants import CHARACTER_PREDICATES
from typing import Optional

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