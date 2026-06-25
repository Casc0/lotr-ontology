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

    def _get_query(self, entity_type: str, subject: str) -> str:
        return f"""
        PREFIX lotr: <http://example.org/lotr/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

        SELECT DISTINCT ?sub ?pred ?obj
        WHERE {{
            ?sub ?pred ?obj ;
                a lotr:{entity_type} ;
                rdfs:label "{subject}" .
        }} """

    def get_character_data(self, subject: str) -> Result:
        query = self._get_query("Character", subject)

        response = self.g.query(query)
        return response

    def get_all_characters_data(self) -> Result:
        query = """
        PREFIX lotr: <http://example.org/lotr/>

        SELECT DISTINCT ?sub ?pred ?obj
        WHERE {
            ?sub a lotr:Character ;
                 ?pred ?obj .
        }"""
        return self.g.query(query)
    
    def get_characters_by_prop(self, pred_uri: str, value: str, value_type: str) -> Result:
        obj = f'"{value}"' if value_type == "literal" else f"lotr:{value}"

        query = f"""
        PREFIX lotr: <http://example.org/lotr/>

        SELECT DISTINCT ?sub ?pred ?obj
        WHERE {{
            ?sub a lotr:Character ;
                {pred_uri} {obj} .
            ?sub ?pred ?obj .
        }}"""
        response = self.g.query(query)
        return response
    
    def get_faction_data(self, subject: str) -> Result:
        query = self._get_query("Faction", subject)

        response = self.g.query(query)
        return response
    
    def get_place_data(self, subject: str) -> Result:
        query = self._get_query("Place", subject)

        response = self.g.query(query)
        return response

    def get_race_data(self, subject: str) -> Result:
        query = self._get_query("Race", subject)

        response = self.g.query(query)
        return response