def Road_RSU_congestion_index(edgelist,rsuid, net): # Zone Congestion
 			 list_of_vehicle=[]
			 congestedRoads=[]
			 vehiclecongested=[]
			 Sum_Zone_RSUs={}
			 Sum_Zone=0
			 Sum_Lane_L=0
			 Sum_Lane_WedgeZ=0
			 for edge in edgelist[rsuid]:
 				  lanelen = traci.lane.getLength(edge + '_' + '0')
				  Max_speed_LaneZ = traci.lane.getMaxSpeed(edge + '_' + '0')
				  MeanSpeedZ= traci.edge.getLastStepMeanSpeed(edge)

				  edge_road = net.getEdge(edge)
				  N_Lane = edge_road.getLaneNumber()
				  logging.debug("N_Lane[edge]::::(%s)" % (N_Lane))
				  Kjam = float ((lanelen * N_Lane)/ (7.5))
				  number_vehicles = traci.edge.getLastStepVehicleNumber(edge)
				  Wedgev = 1 - (MeanSpeedZ / Max_speed_LaneZ)
				  Wedgek = float(number_vehicles / Kjam)
				  WedgeZ = float((Wedgev + Wedgek) / (2))
				  Sum_Lane_L += lanelen 
				  Sum_Lane_WedgeZ  += lanelen * WedgeZ
			 Sum_Zone = float(Sum_Lane_WedgeZ  / Sum_Lane_L )
			 logging.debug("Sum_ZoneSum_Zone: (%s, %s)" % (Sum_Zone, rsuid))
			 return float(Sum_Zone)