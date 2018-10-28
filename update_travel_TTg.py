def update_travel_time_on_roads(graph, time, begin_of_cycle):
    for road in graph.nodes_iter():
        travel_time = traci.edge.getAdaptedTraveltime(road.encode("ascii"), time)
        if travel_time <= 0:
            travel_time = traci.edge.getTraveltime(road.encode("ascii"))
        
        for successor_road in graph.successors_iter(road):
            if begin_of_cycle:
                graph.edge[road][successor_road]["TTg"] = travel_time
            else:
                t = (graph.edge[road][successor_road]["TTg"] + travel_time) / 2
                t = t if t > 0 else travel_time
                graph.edge[road][successor_road]["TTg"] = t