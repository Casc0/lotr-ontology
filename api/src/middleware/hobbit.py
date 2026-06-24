def normalize_tuples(response):
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