from api.src.models import Ontology
from api.src.middleware.hobbit import normalize_tuples
from api.src.constants import RACE_PREDICATES
from api.src.schemas import Race
from fastapi import HTTPException

def get_race(lotr: Ontology, race: str) -> list[dict[str, str]]:
    if not lotr.exists_race(race):
        raise HTTPException(status_code=404, detail=f"Race '{race}' not found")
    return normalize_tuples(lotr.get_race_data(race))

def get_all_races(lotr: Ontology) -> list[dict[str, str]]:
    return normalize_tuples(lotr.get_all_races_data())

def get_races_by_prop(lotr: Ontology, prop: str, value: str) -> list[dict[str, str]]:
    info = RACE_PREDICATES[prop]
    pred_uri = f"<{info.predicate}>"
    return normalize_tuples(lotr.get_races_by_prop(pred_uri, value, info.kind, info.datatype))

def add_race(lotr: Ontology, body: Race):
    if lotr.exists_race(body.name):
        raise HTTPException(status_code=400, detail=f"Race '{body.name}' already exists")
    lotr.add_race(body)
    lotr.save_graph()
    return normalize_tuples(lotr.get_race_data(body.name))

def update_race(lotr: Ontology, race: str, body: Race):
    if not lotr.exists_race(race):
        raise HTTPException(status_code=404, detail=f"Race '{race}' not found")

    body.name = race
    lotr.update_race(body)
    lotr.save_graph()
    return normalize_tuples(lotr.get_race_data(race))