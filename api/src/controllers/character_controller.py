from api.src.middleware.hobbit import normalize_tuples

lotr = app.state.ontology

def get_character(lotr, character):
    return normalize_tuples(lotr.get_character_data(character))