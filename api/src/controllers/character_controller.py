from api.src.models import Ontology
from api.src.middleware.hobbit import normalize_tuples
from api.src.constants import CHARACTER_PREDICATES
from api.src.schemas import Character


def get_character(lotr: Ontology, character: str) -> list[dict[str, str]]:
    return normalize_tuples(lotr.get_character_data(character))


def get_all_characters(lotr: Ontology) -> list[dict[str, str]]:
    return normalize_tuples(lotr.get_all_characters_data())


def get_characters_by_prop(lotr: Ontology, prop: str, value: str) -> list[dict[str, str]]:
    info = CHARACTER_PREDICATES[prop]
    pred_uri = f"<{info.predicate}>"
    value_type = info.kind
    return normalize_tuples(lotr.get_characters_by_prop(pred_uri, value, value_type))


# Incompleto todo lo de abajo.

def update_character(lotr: Ontology, body: Character):
    # para el update trae todas las tuplas y pisa los valores que tenga
    pass


def add_character(lotr: Ontology, body: Character):
    # add each tuple to the ontology, if it already exists, return an error
    pass
