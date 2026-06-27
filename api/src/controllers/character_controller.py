from api.src.models import Ontology
from api.src.middleware.hobbit import normalize_tuples
from api.src.constants import CHARACTER_PREDICATES
from api.src.schemas import Character
from fastapi import HTTPException

def get_character(lotr: Ontology, character: str) -> list[dict[str, str]]:
    if not lotr.exists_character(character):
        raise HTTPException(status_code=404, detail=f"Character '{character}' not found")
    return normalize_tuples(lotr.get_character_data(character))

def get_all_characters(lotr: Ontology) -> list[dict[str, str]]:
    return normalize_tuples(lotr.get_all_characters_data())

def get_characters_by_prop(lotr: Ontology, prop: str, value: str) -> list[dict[str, str]]:
    info = CHARACTER_PREDICATES[prop]
    pred_uri = f"<{info.predicate}>"
    return normalize_tuples(lotr.get_characters_by_prop(pred_uri, value, info.kind, info.datatype))

def add_character(lotr: Ontology, body: Character):
    if lotr.exists_character(body.name):
        raise HTTPException(status_code=400, detail=f"Character '{body.name}' already exists")
    lotr.add_character(body)
    lotr.save_graph()

def update_character(lotr: Ontology, character: str, body: Character):
    if not lotr.exists_character(character):
        raise HTTPException(status_code=404, detail=f"Character '{character}' not found")
    
    body.name = character
    lotr.update_character(body)
    lotr.save_graph()