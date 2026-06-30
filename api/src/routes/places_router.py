from typing import Annotated
from fastapi import APIRouter, Depends, Request
from api.src.controllers.place_controller import (
    get_place,
    get_all_places,
    get_places_by_prop,
    update_place as update_place_ctrl,
    add_place as add_place_ctrl,
)
from api.src.middleware.hobbit import validate_place_props, validate_place_body
from api.src.schemas import Place

router = APIRouter(prefix="/places", tags=["places"])

# Depends en el tipado de props agrega una validacion llamando a la funcion de validate del middleware
@router.get("")
async def get_places(
    request: Request,
    props: Annotated[tuple[str, str], Depends(validate_place_props)],
    allData: bool = True
    ) -> list[dict[str, str]]:
    pred, obj = props
    ontology = request.app.state.ontology
    if pred and obj:
        return get_places_by_prop(ontology, pred, obj, allData)
    return get_all_places(ontology, allData)

@router.get("/{name}")
async def get_a_place(name: str, request: Request) -> list[dict[str, str]]:
    ontology = request.app.state.ontology
    return get_place(ontology, name)

@router.post("")
async def add_place(body: Annotated[Place, Depends(validate_place_body)], request: Request):
    ontology = request.app.state.ontology
    return add_place_ctrl(ontology, body)

@router.put("/{name}")
async def update_place(name: str, body: Annotated[Place, Depends(validate_place_body)], request: Request):
    ontology = request.app.state.ontology
    return update_place_ctrl(ontology, name, body)