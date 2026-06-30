from api.src.models import Ontology
from api.src.middleware.hobbit import normalize_tuples
from api.src.constants import FACTION_PREDICATES
from api.src.schemas import Faction
from fastapi import HTTPException

def get_faction(lotr: Ontology, faction: str) -> list[dict[str, str]]:
    if not lotr.exists_faction(faction):
        raise HTTPException(status_code=404, detail=f"Faction '{faction}' not found")
    return normalize_tuples(lotr.get_faction_data(faction))

def get_all_factions(lotr: Ontology) -> list[dict[str, str]]:
    return normalize_tuples(lotr.get_all_factions_data())

def get_factions_by_prop(lotr: Ontology, pred: str, value: str) -> list[dict[str, str]]:
    info = FACTION_PREDICATES[pred]
    pred_uri = f"<{info.predicate}>"
    return normalize_tuples(lotr.get_factions_by_prop(pred_uri, value, info.kind, info.datatype))

def add_faction(lotr: Ontology, body: Faction):
    if lotr.exists_faction(body.name):
        raise HTTPException(status_code=400, detail=f"Faction '{body.name}' already exists")
    lotr.add_faction(body)
    lotr.save_graph()
    return normalize_tuples(lotr.get_faction_data(body.name))

def update_faction(lotr: Ontology, faction: str, body: Faction):
    if not lotr.exists_faction(faction):
        raise HTTPException(status_code=404, detail=f"Faction '{faction}' not found")

    body.name = faction
    lotr.update_faction(body)
    lotr.save_graph()
    return normalize_tuples(lotr.get_faction_data(faction))