from fastapi import APIRouter, Request
from api.src.controllers.character_controller import *
from api.src.schemas import Character


router = APIRouter(prefix="/characters", tags=["characters"])


@router.get("")
async def get_characters(prop: str, obj: str, request: Request):
    ontology = request.app.state.ontology
    return get_characters(ontology, prop, obj)


@router.get("/{name}")
async def get_a_character(name: str, request: Request):
    ontology = request.app.state.ontology
    return get_a_character(ontology, name)


#lo pense que el body traiga una tupla de tuplas o algo asi
#para el update trae todas las tuplas y pisa los valores que tenga
#para el create trae todas las tuplas del nuevo personaje y las agrega. Unica obligatoria es name. Ver en schema
@router.put("/{name}")
async def update_character(body: Character, request: Request):
    ontology = request.app.state.ontology
    return update_character(ontology, body)

@router.post("")
async def create_character(body: Character, request: Request):
    ontology = request.app.state.ontology
    return add_character(ontology, body)