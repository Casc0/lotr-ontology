from rdflib.query import Result

def normalize_tuples(response: Result) -> list[dict[str, str]]:
    tuples = []
    for row in response:
        tuples.append(
            {
                "subject": str(row.sub),
                "predicate": str(row.pred),
                "object": str(row.obj)
            }
        )
    return tuples