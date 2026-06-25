from api.src.models import Ontology
from api.src.middleware.hobbit import normalize_tuples
from api.src.constants import CHARACTER_PREDICATES
from api.src.schemas import Character
from fastapi import HTTPException

def get_character(lotr: Ontology, character: str) -> list[dict[str, str]]:
    response = lotr.get_character_data(character)

    if not response:
        raise HTTPException(status_code=404, detail=f"Character '{character}' not found")

    return normalize_tuples(response)

def get_all_characters(lotr: Ontology) -> list[dict[str, str]]:
    return normalize_tuples(lotr.get_all_characters_data())

def get_characters_by_prop(lotr: Ontology, prop: str, value: str) -> list[dict[str, str]]:
    info = CHARACTER_PREDICATES[prop]
    pred_uri = f"<{info.predicate}>"
    value_type = info.kind
    return normalize_tuples(lotr.get_characters_by_prop(pred_uri, value, value_type))

def add_character(lotr: Ontology, body: Character):
    response = lotr.get_character_data(body.name)
    
    if response:
        raise HTTPException(status_code=400, detail=f"Character '{body.name}' already exists")
    
    lotr.add_character(body)
    lotr.save_graph()

def update_character(lotr: Ontology, character: str, body: Character):
    response = lotr.get_character_data(character)

    if not response:
        raise HTTPException(status_code=404, detail=f"Character '{character}' not found")
    
    body.name = character
    lotr.update_character(body)
    lotr.save_graph()