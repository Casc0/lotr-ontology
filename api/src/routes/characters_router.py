from fastapi import APIRouter, Request
from api.src.controllers.character_controller import get_character, get_characters_by_prop

router = APIRouter(prefix="/characters", tags=["characters"])

@router.get("")
async def get_characters(prop: str, obj: str, request: Request) -> list[dict[str, str]]:
    ontology = request.app.state.ontology
    return get_characters_by_prop(ontology, prop, obj)

@router.get("/{name}")
async def get_a_character(name: str, request: Request) -> list[dict[str, str]]:
    ontology = request.app.state.ontology
    return get_character(ontology, name)

@router.post("/{name}")
async def update_character(subject: str, predicate: str, object: str, request: Request) -> dict[str, str]:
    ontology = request.app.state.ontology
    return get_character(ontology, subject, predicate, object) # CAMBIAR
