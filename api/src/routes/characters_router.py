from fastapi import APIRouter, Request
from api.src.controllers.character_controller import get_character, get_characters_by_prop


router = APIRouter(prefix="/characters", tags=["characters"])


@router.get("")
async def get_characters(prop: str, obj: str, request: Request):
    ontology = request.app.state.ontology
    return get_characters(ontology, prop, obj)


@router.get("/{name}")
async def get_a_character(name: str, request: Request):
    ontology = request.app.state.ontology
    return get_a_character(ontology, name)

@router.post("/{name}")
async def update_character(subject:str, predicate:str, object:str, request: Request):
    ontology = request.app.state.ontology
    return get_a_character(ontology, subject, predicate, object)
