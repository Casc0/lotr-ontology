
from rdflib import Graph


g = Graph()
g.parse("lotr.ttl")

subject = "Gandalf"

query2 = f"""
        PREFIX lotr: <http://example.org/lotr/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        
        SELECT DISTINCT ?sub ?pred ?obj
        WHERE {{
            ?sub ?pred ?obj ;
                a lotr:Character ;
                rdfs:label "{subject}" .
        }} """

print(g.query(query2))

qres = g.query(query2)

for row in qres:    
    print(f"{row.sub} {row.pred} {row.obj}")
