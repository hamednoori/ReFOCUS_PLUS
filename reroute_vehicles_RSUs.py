def reroute_vehicles_RSUs(subgraph_g,list_of_vehicle,edgelist,congestedRoadsss, congestedRoads,graph,buffered_paths, list_present_network, begin_of_cycle, net):######################
 simple_paths = []
 listvehicle=[]
 listcongesvehicle=[]
 sys.stdout = open('edgee.txt','wt')
 for vehicle in list_of_vehicle:
  aux=[] 
  route=[]
  del aux[:]
  del route[:]
  source = traci.vehicle.getRoadID(vehicle)
  if source.startswith(":"): continue
  route = traci.vehicle.getRoute(vehicle)
  logging.debug("Route::::(%s)" % (route))
  destination = route[-1]
  logging.debug("edgelist::::(%s)" % (edgelist))
  L=[]
  Route=route[route.index(source):route.index(destination)]
  logging.debug("RRRoute::::(%s)" % (Route))
  if destination in edgelist:
    for road in Route:  
     if len(aux) > 0:continue
     if road in congestedRoads:#route:
       if source != destination:
                logging.debug("Calculating shortest paths for pair (%s, %s)" % (source, destination))
		paths=[]
		simple_paths=[]
		k_paths_lengths, k_paths = k_shortest_paths(subgraph_g, source, destination, 4, "TT")
		if k_paths_lengths==source and k_paths==destination:
		 logging.debug("no reroute for pair in RSU (%s, %s,%s)" % (source, destination, vehicle))
		 auxr= route[0:route.index(destination)]
		 traci.vehicle.setRoute(vehicle,auxr)
		 logging.debug("set path no reroute pair in RSU (%s, %s,%s ,%s)" % (source, destination, vehicle,auxr))
		else:
		  for path in k_paths:
		   paths.append(path)
		   simple_paths.append(path)
		  paths_and_weights = get_paths_and_weights(subgraph_g, simple_paths)
		  weights = paths_and_weights.values()
		  max_weight = max(weights)
		  k = calculate_boltzmann_k_value(weights, max_weight)
		  logging.debug("Calculating choose_route for pair in RSU::::: (%s, %s, %s)" % (source, destination, vehicle))
		  new_route = choose_route(paths_and_weights, simple_paths, k, max_weight, begin_of_cycle, subgraph_g, source, destination, net)
 
 		  logging.debug("set route for pair in RSU:::: (%s, %s,%s)" % (source,destination, vehicle))
		  aux = route[0:route.index(source)]
		  aux += new_route
		  logging.debug(" aux for pair in RSU ::::::%s" % aux)
 		  traci.vehicle.setRoute(vehicle, aux)
		  list_vehicle_set_route.append(vehicle)
  else:
    cloud_server(vehicle,route, source, destination,congestedRoadsss, graph, list_present_network, begin_of_cycle, net)
    
  
		   
	