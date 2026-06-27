from collections import namedtuple

from rdflib import Namespace
from rdflib.namespace import RDF, RDFS, FOAF, XSD

# Namespaces - el resto estándar ya los trae rdflib
LOTR = Namespace("http://example.org/lotr/")
SCHEMA = Namespace("https://schema.org/")

# Tipo de dato para un predicado. 
# sintaxis: race = namedtuple('race', ['http://example.org/lotr/race', 'uri'])
# datatype solo se usa para longevity, porque es un xsd integer
PredicateInfo = namedtuple("PredicateInfo", ["predicate", "kind", "datatype"], defaults=[None])


# los predicados del ttl.
# La key es el nombre que viene del front.
ALL_PREDICATES = {
    # --- comunes ---
    "type":             PredicateInfo(RDF.type,"uri"),
    "label":            PredicateInfo(RDFS.label,"literal"),

    # --- Character ---
    "givenName":        PredicateInfo(FOAF.givenName,"literal"),
    "familyName":       PredicateInfo(FOAF.familyName,"literal"),
    "alternateName":    PredicateInfo(SCHEMA.alternateName,"literal"),
    "race":             PredicateInfo(LOTR.race,"uri"),
    "birthplace":       PredicateInfo(SCHEMA.birthplace,"uri"),
    "affiliation":      PredicateInfo(SCHEMA.affiliation,"uri"),

    # --- Race ---
    "longevity":        PredicateInfo(LOTR.longevity,"literal", XSD.integer),
    "knowsLanguage":    PredicateInfo(SCHEMA.knowsLanguage,"literal"),

    # --- Place ---
    "territoryOf":      PredicateInfo(SCHEMA.territoryOf,"uri"),

    # --- Faction ---
    "leader":           PredicateInfo(LOTR.leader,"uri"),
    "ally":             PredicateInfo(LOTR.ally,"uri"),
    "enemy":            PredicateInfo(LOTR.enemy,"uri"),
}


# Qué atributos corresponden a cada tipo de entidad .
CHARACTER_ATTRS = ("label", "givenName", "familyName", "alternateName",
                   "race", "birthplace", "affiliation")
RACE_ATTRS      = ("label", "longevity", "knowsLanguage")
PLACE_ATTRS     = ("label", "territoryOf")
FACTION_ATTRS   = ("label", "leader", "ally", "enemy")

# Tipo de entidad
ENTITY_CLASS = {
    "Character": LOTR.Character,
    "Race":      LOTR.Race,
    "Place":     LOTR.Place,
    "Faction":   LOTR.Faction,
}

# Lista de Predicados de cada entidad
CHARACTER_PREDICATES = {attr: ALL_PREDICATES[attr] for attr in CHARACTER_ATTRS}
RACE_PREDICATES      = {attr: ALL_PREDICATES[attr] for attr in RACE_ATTRS}
PLACE_PREDICATES     = {attr: ALL_PREDICATES[attr] for attr in PLACE_ATTRS}
FACTION_PREDICATES   = {attr: ALL_PREDICATES[attr] for attr in FACTION_ATTRS}

CHARACTER_VALIDATORS = {
    "race":        ("exists_race",      "Race"),
    "birthplace":  ("exists_place",     "Birthplace"),
    "affiliation": ("exists_faction",   "Affiliation"),
}

PLACE_VALIDATORS = {
    "territoryOf": ("exists_faction", "TerritoryOf"),
}

FACTION_VALIDATORS = {
    "leader": ("exists_character",  "Leader"),
    "ally":   ("exists_faction",    "Ally"),
    "enemy":  ("exists_faction",    "Enemy"),
}
