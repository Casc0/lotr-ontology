from api.src.models import Ontology
from api.src.middleware.hobbit import normalize_tuples
from api.src.constants import PLACE_PREDICATES
from api.src.schemas import Place
from fastapi import HTTPException

def get_place(lotr: Ontology, place: str) -> list[dict[str, str]]:
    if not lotr.exists_place(place):
        raise HTTPException(status_code=404, detail=f"Place '{place}' not found")
    return normalize_tuples(lotr.get_place_data(place))

def get_all_places(lotr: Ontology, all_data: bool = True) -> list[dict[str, str]]:
    if all_data:
        return normalize_tuples(lotr.get_all_places_data())
    else:
        return normalize_tuples(lotr.get_all_places_labels())

def get_places_by_prop(lotr: Ontology, pred: str, value: str, all_data: bool = True) -> list[dict[str, str]]:
    info = PLACE_PREDICATES[pred]
    pred_uri = f"<{info.predicate}>"
    if all_data:
        return normalize_tuples(lotr.get_places_by_prop(pred_uri, value, info.kind, info.datatype))
    else:
        return normalize_tuples(lotr.get_places_labels_by_prop(pred_uri, value, info.kind, info.datatype))

def add_place(lotr: Ontology, body: Place):
    if lotr.exists_place(body.name):
        raise HTTPException(status_code=400, detail=f"Place '{body.name}' already exists")
    lotr.add_place(body)
    lotr.save_graph()
    return normalize_tuples(lotr.get_place_data(body.name))

def update_place(lotr: Ontology, place: str, body: Place):
    if not lotr.exists_place(place):
        raise HTTPException(status_code=404, detail=f"Place '{place}' not found")

    body.name = place
    lotr.update_place(body)
    lotr.save_graph()
    return normalize_tuples(lotr.get_place_data(place))