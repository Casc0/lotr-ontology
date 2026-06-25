from pathlib import Path
from rdflib import Graph, URIRef, Literal
from rdflib.query import Result

class Ontology:
    def __init__(self) -> None:
        self.g = Graph()
        self.g.parse(Path(__file__).parent / "lotr.ttl")

    def save_graph(self) -> None:
        self.g.serialize(destination="your-lotr.ttl")

    def add_triple(self, subject: str, predicate: str, object: str) -> None:
        # validated by the controller
        self.g.add((subject, predicate, object))

    # QUERY DEFINITIONS

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
    
    def _get_all_by_prop_query(self, entity_type: str, pred_uri: str, obj: str) -> str:
        return f"""
        PREFIX lotr: <http://example.org/lotr/>

        SELECT DISTINCT ?sub ?pred ?obj
        WHERE {{
            ?sub a lotr:{entity_type} ;
                {pred_uri} {obj} .
            ?sub ?pred ?obj .
        }} """
    
    # CHARACTERS

    def get_character_data(self, subject: str) -> Result:
        query = self._get_one_query("Character", subject)

        return self.g.query(query)

    def get_all_characters_data(self) -> Result:
        query = self._get_all_query("Character")

        return self.g.query(query)
    
    def get_characters_by_prop(self, pred_uri: str, value: str, value_type: str) -> Result:
        obj = f'"{value}"' if value_type == "literal" else f"lotr:{value}"
        query = self._get_all_by_prop_query("Character", pred_uri, obj)

        return self.g.query(query)
    
    # FACTIONS
    
    def get_faction_data(self, subject: str) -> Result:
        query = self._get_one_query("Faction", subject)

        return self.g.query(query)
    
    def get_all_factions_data(self) -> Result:
        query = self._get_all_query("Faction")

        return self.g.query(query)
    
    def get_factions_by_prop(self, pred_uri: str, value: str, value_type: str) -> Result:
        obj = f'"{value}"' if value_type == "literal" else f"lotr:{value}"
        query = self._get_all_by_prop_query("Faction", pred_uri, obj)

        return self.g.query(query)
    
    # PLACES

    def get_place_data(self, subject: str) -> Result:
        query = self._get_one_query("Place", subject)

        return self.g.query(query)
    
    def get_all_places_data(self) -> Result:
        query = self._get_all_query("Place")

        return self.g.query(query)
    
    def get_places_by_prop(self, pred_uri: str, value: str, value_type: str) -> Result:
        obj = f'"{value}"' if value_type == "literal" else f"lotr:{value}"
        query = self._get_all_by_prop_query("Place", pred_uri, obj)

        return self.g.query(query)

    # RACES

    def get_race_data(self, subject: str) -> Result:
        query = self._get_one_query("Race", subject)

        return self.g.query(query)
    
    def get_all_races_data(self) -> Result:
        query = self._get_all_query("Race")

        return self.g.query(query)
    
    def get_races_by_prop(self, pred_uri: str, value: str, value_type: str) -> Result:
        obj = f'"{value}"' if value_type == "literal" else f"lotr:{value}"
        query = self._get_all_by_prop_query("Race", pred_uri, obj)

        return self.g.query(query)