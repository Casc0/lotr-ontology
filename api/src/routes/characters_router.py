from typing import Annotated
from fastapi import APIRouter, Depends, Request
from api.src.controllers.character_controller import (
    get_character,
    get_all_characters,
    get_characters_by_prop,
    update_character as update_character_ctrl,
    add_character as add_character_ctrl,
)
from api.src.middleware.hobbit import validate_character_props
from api.src.schemas import Character

router = APIRouter(prefix="/characters", tags=["characters"])

# Depends en el tipado de props agrega una validacion llamando a la funcion de validate del middleware
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

@router.post("")
async def add_character(body: Character, request: Request):
    ontology = request.app.state.ontology
    return add_character_ctrl(ontology, body)

@router.put("/{name}")
async def update_character(name: str, body: Character, request: Request):
    ontology = request.app.state.ontology
    return update_character_ctrl(ontology, name, body)