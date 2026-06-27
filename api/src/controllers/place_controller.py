from api.src.models import Ontology
from api.src.middleware.hobbit import normalize_tuples
from api.src.constants import PLACE_PREDICATES
from api.src.schemas import Place
from fastapi import HTTPException

def get_place(lotr: Ontology, place: str) -> list[dict[str, str]]:
    if not lotr.exists_place(place):
        raise HTTPException(status_code=404, detail=f"Place '{place}' not found")
    return normalize_tuples(lotr.get_place_data(place))

def get_all_places(lotr: Ontology) -> list[dict[str, str]]:
    return normalize_tuples(lotr.get_all_places_data())

def get_places_by_prop(lotr: Ontology, prop: str, value: str) -> list[dict[str, str]]:
    info = PLACE_PREDICATES[prop]
    pred_uri = f"<{info.predicate}>"
    value_type = info.kind
    return normalize_tuples(lotr.get_places_by_prop(pred_uri, value, value_type))

def add_place(lotr: Ontology, body: Place):
    if lotr.exists_place(body.name):
        raise HTTPException(status_code=400, detail=f"Place '{body.name}' already exists")
    lotr.add_place(body)
    lotr.save_graph()

def update_place(lotr: Ontology, place: str, body: Place):
    if not lotr.exists_place(place):
        raise HTTPException(status_code=404, detail=f"Place '{place}' not found")
    
    body.name = place
    lotr.update_place(body)
    lotr.save_graph()