def road_congestion_at_traffic_area(road_graph_travel_time, edgelist, zone_conges, RSU_ids,net):					
  for rsuid in RSU_ids:
	for edge in edgelist[rsuid]:
	   listEdgeRSU.append(edge)
	   Lenght_Lane = traci.lane.getLength(edge + '_' + '0')
	   Max_speed_LaneZ = traci.lane.getMaxSpeed(edge + '_' + '0')
	   MeanSpeedZ= traci.edge.getLastStepMeanSpeed(edge)
	   edge_road = net.getEdge(edge)
	   N_Lane = edge_road.getLaneNumber()
	   logging.debug("N_Lane[edge]::::(%s)" % (N_Lane))
	   Kjam = float ((Lenght_Lane * N_Lane)/ (7.5))
	   number_vehicles = traci.edge.getLastStepVehicleNumber(edge)
	   Wedgev = 1 - (MeanSpeedZ / Max_speed_LaneZ)
	   if number_vehicles !=0 and Lenght_Lane >= 9:
	     Density = float (number_vehicles / Kjam)
	   else:
	     Density = 0.0

	   ZoneC = zone_conges[rsuid]
	   sum_conges= (Wedgev+ZoneC+Density)/3
	   dict_road_conges_traffic_area[edge] = sum_conges
	   
	   
	     

	   