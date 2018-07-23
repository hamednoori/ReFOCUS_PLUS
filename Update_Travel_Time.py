def Update_Travel_Time(graph, net): # Road Weight Measurement
 maxLenght = max(edgListLength)
 for road in graph.nodes_iter():
  for successor_road in graph.successors_iter(road):
   minold= min(listtraveltime)
   maxold= max(listtraveltime)
   minnew = minold
   rescale= ((1-minnew)/ (maxold - minold))* (graph[road][successor_road]["weight"] - minold) + minnew  
   graph.edge[road][successor_road]["weight"] = rescale
   if road in listEdgeRSU:
    Lenght_Lane = traci.lane.getLength(road + '_' + '0')
    N_Lane = number_of_lane[road]
    Kjam = float ((Lenght_Lane * N_Lane)/ (7.5))
    number_vehicles = traci.edge.getLastStepVehicleNumber(road)
    if number_vehicles !=0 and Lenght_Lane >= 9:
	 Density = float (number_vehicles / Kjam)
    else:
	 Density = 0.0
    if road.startswith(":") or successor_road.startswith(":"):
	 if dict_road_conges_traffic_area[road] >= 0.3:
	  graph.edge[road][successor_road]["TT"] = (math.exp(dict_road_conges_traffic_area[road])) + ((graph.edge[road][successor_road]["weight"])* 2 )
	 else:
	  graph.edge[road][successor_road]["TT"] = (math.exp(graph.edge[road][successor_road]["weight"])) + ((dict_road_conges_traffic_area[road])* 2 )
    else:
	 if dict_road_conges_traffic_area[road] >= 0.3:
	  graph.edge[road][successor_road]["TT"] = (math.exp(dict_road_conges_traffic_area[road])) + ((graph.edge[road][successor_road]["weight"]) * 2 )  + ((graph.edge[road][successor_road]["predict"]+graph.edge[road][successor_road]["predictArea"] )* 2)  
	 else:
	  graph.edge[road][successor_road]["TT"] = (math.exp(graph.edge[road][successor_road]["weight"] ))  + ((dict_road_conges_traffic_area[road] )* 2 ) + ((graph.edge[road][successor_road]["predict"]+graph.edge[road][successor_road]["predictArea"] )* 2) 
   else:
    Lenght_Lane = traci.lane.getLength(road + '_' + '0')
    Max_speed_LaneZ = traci.lane.getMaxSpeed(road + '_' + '0')
    MeanSpeedZ= traci.edge.getLastStepMeanSpeed(road)
    if road.startswith(":"):
	 N_Lane = number_of_lane[road]
    else:
     edge_road = net.getEdge(road)
     N_Lane = edge_road.getLaneNumber()
    logging.debug("N_Lane[edge]::::(%s)" % (N_Lane))
    Kjam = float ((Lenght_Lane * N_Lane)/ (7.5))
    number_vehicles = traci.edge.getLastStepVehicleNumber(road)
    Wedgev = 1 - (MeanSpeedZ / Max_speed_LaneZ)
    if number_vehicles !=0 and Lenght_Lane >= 9:
	 Density = float (number_vehicles / Kjam)
    else:
	 Density = 0.0
    sum_conges= (Wedgev+Density)/2
    if road.startswith(":") or successor_road.startswith(":"):
			 if sum_conges >= 0.3:
			  graph.edge[road][successor_road]["TT"] = (math.exp(sum_conges)) + (graph.edge[road][successor_road]["weight"]*2) 
			 else:
			  graph.edge[road][successor_road]["TT"] = (math.exp(graph.edge[road][successor_road]["weight"] ) ) + (sum_conges  * 2)
    else:
	 if sum_conges >= 0.3:
	  graph.edge[road][successor_road]["TT"] = (math.exp(sum_conges) ) + ((graph.edge[road][successor_road]["weight"] + graph.edge[road][successor_road]["predict"] +graph.edge[road][successor_road]["predictArea"])* 2)   
			 
	 else:
	  graph.edge[road][successor_road]["TT"] = (math.exp(graph.edge[road][successor_road]["weight"]  ) ) +( (sum_conges * 2)) + ((graph.edge[road][successor_road]["predict"] +graph.edge[road][successor_road]["predictArea"])* 2)  
		       
   d = graph.edge[road][successor_road]["TT"]
    