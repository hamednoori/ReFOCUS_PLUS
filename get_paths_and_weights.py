def get_paths_and_weights(graph, simple_paths):
    paths_and_weights = {}
    for path in simple_paths:
        weight = 0
        for i in range(len(path) - 1):
            u = path[i]
            v = path[i + 1]
            weight += graph.edge[u][v]["weight"]
        paths_and_weights[tuple(path)] = weight
    return paths_and_weights 
 

	