from typing import Annotated
from fastapi import APIRouter, Depends, Request
from api.src.controllers.faction_controller import (
    get_faction,
    get_all_factions,
    get_factions_by_prop,
    update_faction as update_faction_ctrl,
    add_faction as add_faction_ctrl,
)
from api.src.middleware.hobbit import validate_faction_props, validate_faction_body
from api.src.schemas import Faction

router = APIRouter(prefix="/factions", tags=["factions"])

# Depends en el tipado de props agrega una validacion llamando a la funcion de validate del middleware
@router.get("")
async def get_factions(request: Request, props: Annotated[tuple[str, str], Depends(validate_faction_props)]) -> list[dict[str, str]]:
    prop, obj = props
    ontology = request.app.state.ontology
    if prop and obj:
        return get_factions_by_prop(ontology, prop, obj)
    return get_all_factions(ontology)

@router.get("/{name}")
async def get_a_faction(name: str, request: Request) -> list[dict[str, str]]:
    ontology = request.app.state.ontology
    return get_faction(ontology, name)

@router.post("")
async def add_faction(body: Annotated[Faction, Depends(validate_faction_body)], request: Request):
    ontology = request.app.state.ontology
    return add_faction_ctrl(ontology, body)

@router.put("/{name}")
async def update_faction(name: str, body: Annotated[Faction, Depends(validate_faction_body)], request: Request):
    ontology = request.app.state.ontology
    return update_faction_ctrl(ontology, name, body)