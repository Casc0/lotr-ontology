from api.src.middleware.hobbit import normalize_tuples


def get_a_character(lotr, character):
    return normalize_tuples(lotr.get_character_data(character))


def get_characters(lotr, prop, value):
    return normalize_tuples(lotr.get_characters(prop, value))