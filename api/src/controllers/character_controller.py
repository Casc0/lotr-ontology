from api.src.middleware.hobbit import normalize_tuples
from api.src.models import ontology
from api.src.schemas import Character


def get_a_character(lotr: ontology, character):
    return normalize_tuples(lotr.get_character_data(character))


#Incompleto todo lo de abajo.

def get_characters(lotr: ontology, prop, value):
    return normalize_tuples(lotr.get_characters(prop, value))

def update_character(lotr: ontology, subject, predicate, object):
    tuple = normalize_tuples(lotr.update_character(subject, predicate, object))
    if len(tuple) > 0:
        #error handling if not found
        pass

def add_character(lotr: ontology, body: Character):
    #add each tuple to the ontology, if it already exists, return an error
    pass