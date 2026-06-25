from api.src.models import Ontology
from api.src.middleware.hobbit import normalize_tuples

def get_character(lotr: Ontology, character: str) -> list[dict[str, str]]:
    character_data = lotr.get_character_data(character)

    return normalize_tuples(character_data)

def get_characters_by_prop(lotr, prop: str, value: str) -> list[dict[str, str]]:
    characters_data = lotr.get_characters_by_prop(prop, value)

    return normalize_tuples(characters_data)