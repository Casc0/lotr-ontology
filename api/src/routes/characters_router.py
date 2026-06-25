from typing import Annotated
from fastapi import APIRouter, Depends, Request
from api.src.controllers.character_controller import get_character, get_all_characters, get_characters_by_prop
from api.src.middleware.hobbit import validate_character_props

router = APIRouter(prefix="/characters", tags=["characters"])

@router.get("")
async def get_characters(request: Request, props: Annotated[tuple, Depends(validate_character_props)]) -> list[dict[str, str]]:
    prop, obj = props
    ontology = request.app.state.ontology
    if prop and obj:
        return get_characters_by_prop(ontology, prop, obj)
    return get_all_characters(ontology)

@router.get("/{name}")
async def get_a_character(name: str, request: Request) -> list[dict[str, str]]:
    ontology = request.app.state.ontology
    return get_character(ontology, name)

@router.post("/{name}")
async def update_character(subject: str, predicate: str, object: str, request: Request) -> dict[str, str]:
    ontology = request.app.state.ontology
    return get_character(ontology, subject, predicate, object) # CAMBIAR
