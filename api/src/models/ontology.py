from pathlib import Path
from typing import Optional
from rdflib import Graph, URIRef, Literal
from rdflib.query import Result
from api.src.schemas import EntityBase, Character, Race, Place, Faction
from api.src.constants import PredicateInfo, RDF, LOTR, CHARACTER_PREDICATES, RACE_PREDICATES, PLACE_PREDICATES, FACTION_PREDICATES

DB_PATH = str(Path(__file__).parent.parent / "db" / "lotr.ttl")

class Ontology:
    def __init__(self) -> None:
        self.g = Graph()
        self.g.parse(DB_PATH)

    def save_graph(self) -> None:
        self.g.serialize(destination=DB_PATH)

    def add_triple(self, sub: URIRef, pred: URIRef, obj: URIRef | Literal) -> None:
        self.g.add((sub, pred, obj))

    def remove_triple(self, sub: URIRef, pred: Optional[URIRef] = None, obj: Optional[URIRef | Literal] = None) -> None:
        self.g.remove((sub, pred, obj))

    # QUERY DEFINITIONS

    def _exists_query(self, entity_type: str, subject: str) -> str:
        return f"""
        PREFIX lotr: <http://example.org/lotr/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

        ASK {{
            ?sub a lotr:{entity_type} ;
                rdfs:label "{subject}" .
        }} """    

    def _get_one_query(self, entity_type: str, subject: str) -> str:
        return f"""
        PREFIX lotr: <http://example.org/lotr/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

        SELECT DISTINCT ?sub ?pred ?obj
        WHERE {{
            ?sub ?pred ?obj ;
                a lotr:{entity_type} ;
                rdfs:label "{subject}" .
        }} """
    
    def _get_all_query(self, entity_type: str) -> str:
        return f"""
        PREFIX lotr: <http://example.org/lotr/>

        SELECT DISTINCT ?sub ?pred ?obj
        WHERE {{
            ?sub ?pred ?obj ;
                a lotr:{entity_type} ;
        }} """
    
    def _get_all_labels_query(self, entity_type: str) -> str:
        return f"""
        PREFIX lotr: <http://example.org/lotr/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

        SELECT DISTINCT ?sub ?pred ?obj
        WHERE {{
            ?sub ?pred ?obj ;
                a lotr:{entity_type} ;
            FILTER(?pred = rdfs:label)
        }} """
    
    def _get_all_by_prop_query(self, entity_type: str, pred_uri: str, obj: str) -> str:
        return f"""
        PREFIX lotr: <http://example.org/lotr/>

        SELECT DISTINCT ?sub ?pred ?obj
        WHERE {{
            ?sub a lotr:{entity_type} ;
                {pred_uri} {obj} .
            ?sub ?pred ?obj .
        }} """
    
    def _get_all_labels_by_prop_query(self, entity_type: str, pred_uri: str, obj: str) -> str:
        return f"""
        PREFIX lotr: <http://example.org/lotr/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

        SELECT DISTINCT ?sub ?pred ?obj
        WHERE {{
            ?sub a lotr:{entity_type} ;
                {pred_uri} {obj} .
            ?sub ?pred ?obj .
        FILTER(?pred = rdfs:label)
        }} """
    
    # COMMON FUNCTIONS

    def _add_entity(self, entity: EntityBase, predicates: dict[str, PredicateInfo]) -> None:
        sub = LOTR[entity.name]

        for pred_name, pred_info in predicates.items():
            if pred_name == "label":
                value = entity.name
            else:
                value = getattr(entity, pred_name, None)

            if value is None:
                continue

            pred = URIRef(pred_info.predicate)
            values = value if isinstance(value, list) else [value]

            for val in values:
                if pred_info.kind == "uri":
                    obj = LOTR[val]
                else:
                    obj = Literal(val, datatype=pred_info.datatype)

                self.add_triple(sub, pred, obj)

    def _update_entity(self, entity: EntityBase, predicates: dict[str, PredicateInfo]) -> None:
        sub = LOTR[entity.name]

        for pred_name, pred_info in predicates.items():
            if pred_name == "label":
                value = entity.name
            else:
                value = getattr(entity, pred_name, None)

            if value is None or value == []:
                continue

            pred = URIRef(pred_info.predicate)
            self.remove_triple(sub, pred)
            values = value if isinstance(value, list) else [value]

            for val in values:
                if pred_info.kind == "uri":
                    obj = LOTR[val]
                else:
                    obj = Literal(val, datatype=pred_info.datatype)

                self.add_triple(sub, pred, obj)

    # CHARACTERS

    def exists_character(self, subject: str) -> bool:
        query = self._exists_query("Character", subject)

        return self.g.query(query).askAnswer

    def get_character_data(self, subject: str) -> Result:
        query = self._get_one_query("Character", subject)

        return self.g.query(query)

    def get_all_characters_data(self) -> Result:
        query = self._get_all_query("Character")

        return self.g.query(query)
    
    def get_all_characters_labels(self) -> Result:
        query = self._get_all_labels_query("Character")

        return self.g.query(query)
    
    def get_characters_by_prop(self, pred_uri: str, value: str, value_type: str, datatype=None) -> Result:
        if value_type == "uri":
            obj = f"lotr:{value}"
        elif datatype:
            obj = f'"{value}"^^<{datatype}>'
        else:
            obj = f'"{value}"'
        query = self._get_all_by_prop_query("Character", pred_uri, obj)

        return self.g.query(query)
    
    def get_characters_labels_by_prop(self, pred_uri: str, value: str, value_type: str, datatype=None) -> Result:
        if value_type == "uri":
            obj = f"lotr:{value}"
        elif datatype:
            obj = f'"{value}"^^<{datatype}>'
        else:
            obj = f'"{value}"'
        query = self._get_all_labels_by_prop_query("Character", pred_uri, obj)

        return self.g.query(query)
    
    def add_character(self, char: Character) -> None:
        self.add_triple(LOTR[char.name], RDF.type, LOTR.Character)
        self._add_entity(char, CHARACTER_PREDICATES)

    def update_character(self, char: Character) -> None:
        self._update_entity(char, CHARACTER_PREDICATES)

    # FACTIONS

    def exists_faction(self, subject: str) -> bool:
        query = self._exists_query("Faction", subject)

        return self.g.query(query).askAnswer
    
    def get_faction_data(self, subject: str) -> Result:
        query = self._get_one_query("Faction", subject)

        return self.g.query(query)
    
    def get_all_factions_data(self) -> Result:
        query = self._get_all_query("Faction")

        return self.g.query(query)
    
    def get_all_factions_labels(self) -> Result:
        query = self._get_all_labels_query("Faction")

        return self.g.query(query)
    
    def get_factions_by_prop(self, pred_uri: str, value: str, value_type: str, datatype=None) -> Result:
        if value_type == "uri":
            obj = f"lotr:{value}"
        elif datatype:
            obj = f'"{value}"^^<{datatype}>'
        else:
            obj = f'"{value}"'
        query = self._get_all_by_prop_query("Faction", pred_uri, obj)

        return self.g.query(query)
    
    def get_factions_labels_by_prop(self, pred_uri: str, value: str, value_type: str, datatype=None) -> Result:
        if value_type == "uri":
            obj = f"lotr:{value}"
        elif datatype:
            obj = f'"{value}"^^<{datatype}>'
        else:
            obj = f'"{value}"'
        query = self._get_all_labels_by_prop_query("Faction", pred_uri, obj)

        return self.g.query(query)
    
    def add_faction(self, fact: Faction) -> None:
        self.add_triple(LOTR[fact.name], RDF.type, LOTR.Faction)
        self._add_entity(fact, FACTION_PREDICATES)

    def update_faction(self, fact: Faction) -> None:
        self._update_entity(fact, FACTION_PREDICATES)
    
    # PLACES

    def exists_place(self, subject: str) -> bool:
        query = self._exists_query("Place", subject)

        return self.g.query(query).askAnswer

    def get_place_data(self, subject: str) -> Result:
        query = self._get_one_query("Place", subject)

        return self.g.query(query)
    
    def get_all_places_data(self) -> Result:
        query = self._get_all_query("Place")

        return self.g.query(query)
    
    def get_all_places_labels(self) -> Result:
        query = self._get_all_labels_query("Place")

        return self.g.query(query)
    
    def get_places_by_prop(self, pred_uri: str, value: str, value_type: str, datatype=None) -> Result:
        if value_type == "uri":
            obj = f"lotr:{value}"
        elif datatype:
            obj = f'"{value}"^^<{datatype}>'
        else:
            obj = f'"{value}"'
        query = self._get_all_by_prop_query("Place", pred_uri, obj)

        return self.g.query(query)
    
    def get_places_labels_by_prop(self, pred_uri: str, value: str, value_type: str, datatype=None) -> Result:
        if value_type == "uri":
            obj = f"lotr:{value}"
        elif datatype:
            obj = f'"{value}"^^<{datatype}>'
        else:
            obj = f'"{value}"'
        query = self._get_all_labels_by_prop_query("Place", pred_uri, obj)

        return self.g.query(query)
    
    def add_place(self, place: Place) -> None:
        self.add_triple(LOTR[place.name], RDF.type, LOTR.Place)
        self._add_entity(place, PLACE_PREDICATES)

    def update_place(self, place: Place) -> None:
        self._update_entity(place, PLACE_PREDICATES)

    # RACES

    def exists_race(self, subject: str) -> bool:
        query = self._exists_query("Race", subject)

        return self.g.query(query).askAnswer

    def get_race_data(self, subject: str) -> Result:
        query = self._get_one_query("Race", subject)

        return self.g.query(query)
    
    def get_all_races_data(self) -> Result:
        query = self._get_all_query("Race")

        return self.g.query(query)
    
    def get_all_races_labels(self) -> Result:
        query = self._get_all_labels_query("Race")

        return self.g.query(query)
    
    def get_races_by_prop(self, pred_uri: str, value: str, value_type: str, datatype=None) -> Result:
        if value_type == "uri":
            obj = f"lotr:{value}"
        elif datatype:
            obj = f'"{value}"^^<{datatype}>'
        else:
            obj = f'"{value}"'
        query = self._get_all_by_prop_query("Race", pred_uri, obj)

        return self.g.query(query)
    
    def get_races_labels_by_prop(self, pred_uri: str, value: str, value_type: str, datatype=None) -> Result:
        if value_type == "uri":
            obj = f"lotr:{value}"
        elif datatype:
            obj = f'"{value}"^^<{datatype}>'
        else:
            obj = f'"{value}"'
        query = self._get_all_labels_by_prop_query("Race", pred_uri, obj)

        return self.g.query(query)
    
    def add_race(self, race: Race) -> None:
        self.add_triple(LOTR[race.name], RDF.type, LOTR.Race)
        self._add_entity(race, RACE_PREDICATES)

    def update_race(self, race: Race) -> None:
        self._update_entity(race, RACE_PREDICATES)