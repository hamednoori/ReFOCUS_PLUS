def cloud_reroute_vehicles(graph,list_of_vehiclecloud,congestedRoadsss, buffered_paths, list_present_network, begin_of_cycle, net):###########################
    simple_paths = []
    listvehicle=[]
    listcongesvehicle=[]
    for vv in list_of_vehiclecloud:
     for v in vv:
      listvehicle.append(v)
   
    
    for vehicle in listvehicle:
        aux=[]
        source = traci.vehicle.getRoadID(vehicle)
        if source.startswith(":"): continue
        route = traci.vehicle.getRoute(vehicle)
        destination = route[-1]
        Route=route[route.index(source):route.index(destination)]
        logging.debug("RRRoute in cloud ::::(%s)" % (Route))
        for road in route: 
         if len(aux) > 0:continue
         if road in congestedRoadsss: 
          if source != destination:
    		logging.debug("Calculating shortest paths for pair in cloud server (%s, %s ,%s)" % (source, destination, vehicle))
            paths = []
            simple_paths = []
            k_paths_lengths, k_paths = k_shortest_paths(graph, source, destination, 4, "TT")
            for path in k_paths:
			 paths.append(path)
			 simple_paths.append(path)
            paths_and_weights = get_paths_and_weights(graph, simple_paths)
            weights = paths_and_weights.values()
            max_weight = max(weights)
            k = calculate_boltzmann_k_value(weights, max_weight)
            new_route = choose_route(paths_and_weights, simple_paths, k, max_weight, begin_of_cycle, graph,source, destination, net)
            #new_route = nx.dijkstra_path(graph, source, destination,"weight")
            aux = route[0:route.index(source)]
            aux += new_route
            traci.vehicle.setRoute(vehicle, aux)
            list_vehicle_set_route.append(vehicle)
			
             
		
			
             
		