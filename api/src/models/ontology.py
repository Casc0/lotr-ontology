from rdflib import Graph

class Ontology:
    def __init__(self):
        self.g = Graph()
        self.g.parse("lotr.ttl")

    def save_graph(self):
        self.g.serialize(destination="your-lotr.ttl")

    def add_triple(self, subject, predicate, object):
        # validated by the controller
        self.g.add(subject, predicate, object)

    def _get_query(self, type, subject):
        return f"""
        PREFIX lotr: <http://example.org/lotr/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

        SELECT DISTINCT ?sub ?pred ?obj
        WHERE {{
            ?sub ?pred ?obj ;
                a lotr:{type} ;
                rdfs:label "{subject}" .
        }} """

    def get_character_data(self, subject):
        query = self._get_query("Character", subject)

        response = self.g.query(query)
        return response
    
    def get_faction_data(self, subject):
        query = self._get_query("Faction", subject)

        response = self.g.query(query)
        return response
    
    def get_place_data(self, subject):
        query = self._get_query("Place", subject)

        response = self.g.query(query)
        return response

    def get_race_data(self, subject):
        query = self._get_query("Race", subject)

        response = self.g.query(query)
        return response