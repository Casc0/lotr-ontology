from api.src.models import Ontology
from api.src.middleware.hobbit import normalize_tuples
from api.src.constants import CHARACTER_PREDICATES

def get_character(lotr: Ontology, character: str) -> list[dict[str, str]]:
    return normalize_tuples(lotr.get_character_data(character))


def get_all_characters(lotr: Ontology) -> list[dict[str, str]]:
    return normalize_tuples(lotr.get_all_characters_data())

def get_characters_by_prop(lotr: Ontology, prop: str, value: str) -> list[dict[str, str]]:
    pred_uri, value_type = CHARACTER_PREDICATES[prop]
    return normalize_tuples(lotr.get_characters_by_prop(pred_uri, value, value_type))