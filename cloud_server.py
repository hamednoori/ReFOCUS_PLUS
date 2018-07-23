def cloud_server(vehicle,route, source, destination,congestedRoadsss, graph, list_present_network, begin_of_cycle, net):
  aux=[]
 Route=route[route.index(source):route.index(destination)]
 logging.debug("RRRoute in cloud request rsu ::::(%s)" % (Route))
 for road in Route: 
  if len(aux) > 0:continue
  if road in congestedRoadsss: 
	if source != destination:
		paths=[]
		simple_paths=[]
		k_paths_lengths, k_paths = k_shortest_paths(graph, source, destination, 4, "TT")
		for path in k_paths:
		   paths.append(path)
		   simple_paths.append(path)
		paths_and_weights = get_paths_and_weights(graph, simple_paths)
		weights = paths_and_weights.values()
		max_weight = max(weights)
		k = calculate_boltzmann_k_value(weights, max_weight)
		logging.debug("Calculating choose_route for pair cloud_server that request RSU(%s, %s, %s)" % (source, destination, vehicle))
		new_route = choose_route(paths_and_weights, simple_paths, k, max_weight, begin_of_cycle, graph, source, destination, net)
		aux = route[0:route.index(source)]
		aux += new_route
                logging.debug("path for pair cloud_server that request RSU(%s, %s, %s, %s)" % (source, destination, vehicle, aux))
		traci.vehicle.setRoute(vehicle, aux)
		list_vehicle_set_route.append(vehicle)
		
	