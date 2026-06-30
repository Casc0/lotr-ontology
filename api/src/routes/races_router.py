from typing import Annotated
from fastapi import APIRouter, Depends, Request
from api.src.controllers.race_controller import (
    get_race,
    get_all_races,
    get_races_by_prop,
    update_race as update_race_ctrl,
    add_race as add_race_ctrl,
)
from api.src.middleware.hobbit import validate_race_props
from api.src.schemas import Race

router = APIRouter(prefix="/races", tags=["races"])

# Depends en el tipado de props agrega una validacion llamando a la funcion de validate del middleware
@router.get("")
async def get_races(
    request: Request,
    props: Annotated[tuple[str, str], Depends(validate_race_props)],
    allData: bool = True
    ) -> list[dict[str, str]]:
    pred, obj = props
    ontology = request.app.state.ontology
    if pred and obj:
        return get_races_by_prop(ontology, pred, obj, allData)
    return get_all_races(ontology, allData)

@router.get("/{name}")
async def get_a_race(name: str, request: Request) -> list[dict[str, str]]:
    ontology = request.app.state.ontology
    return get_race(ontology, name)

@router.post("")
async def add_race(body: Race, request: Request):
    ontology = request.app.state.ontology
    return add_race_ctrl(ontology, body)

@router.put("/{name}")
async def update_race(name: str, body: Race, request: Request):
    ontology = request.app.state.ontology
    return update_race_ctrl(ontology, name, body)