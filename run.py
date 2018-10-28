def run(network, begin, end, interval):###############################
    net = sumolib.net.readNet("...\\PATH\\Your.net.xml")
    road_graph_travel_time = build_road_graph(network, net) 
    buffered_paths = {}	
    list_of_vehicle=[]
    subgraph_g={}
    dicttt_edgeRSUs={}
    f = open('RSUsLocationUBC.xml', 'r')
    data = f.read()
    soup = BeautifulSoup(data)
    f.close()
    RSU_ids=[]
    RSU_x={}
    RSU_y={}
    edgelist={}
    closestEdge=[]
    edg_ids=[]
    listalledge=[]
    for RSU_tag in soup.findAll("poly"):
      RSU_id = RSU_tag["id"]
      RSU_ids.append(RSU_id)
      RSU_center = RSU_tag["center"]
      RSU_x[RSU_id], RSU_y[RSU_id] = RSU_center.split(",")
      x =float(RSU_x[RSU_id])
      y =float(RSU_y[RSU_id])
      list_EdgeId=[]
      list_NormalEdges=[]
      list_junctions=[]
      edges = net.getNeighboringEdges(x, y, 1000)
      for ege in edges:
	    closestEdge , dist = ege
 	    list_NormalEdges.append(str(closestEdge))
	    data = list_NormalEdges[0].split('id=')[1]
	    EdgeId = data.split(' ')[0]   
	    listalledge.append(ast.literal_eval(EdgeId))
	    list_EdgeId.append(ast.literal_eval(EdgeId))
	    #########################################
	  # print("{0} list_EdgeId= {1}" .format(RSU_id ,list_EdgeId ))##########################
	  
          # JunctionFrom = data.split('from=')[1]
	  # JunctionFrom = JunctionFrom.split(' ')[0]
       	  # list_junctions.append(ast.literal_eval(JunctionFrom))
          # JunctionTo = data.split('to=')[-1]
          # JunctionTo = JunctionTo.split('/>')[0]
          # list_junctions.append(ast.literal_eval(JunctionTo))
	    del list_NormalEdges[:]# : means all memebers
      # print ("{0} list_junctions:::: {1}" .format(RSU_id ,list_junctions ))
	  # ############################################################################################
      # subgraph_g[RSU_tag]=road_graph_travel_time.subgraph(list_junctions)
	  # ############################################################################################
      # print ("{0} graph_list_junctions:::: {1}" .format(RSU_id ,subgraph_g[RSU_tag].nodes() ))
	  # ############################################################################################
      #subgraph_g[RSU_id]=road_graph_travel_time.subgraph(list_EdgeId)## SUBGRAPH  SUBGRAPH   SUBGRAPH   SUBGRAPH  ##
	  ##############################################################################################
      # print ("{0} graph_list_EdgeIdedge:::: {1}" .format(RSU_id ,   subgraph_g[RSU_id].edges() ))
	  
      dicttt_edgeRSUs[RSU_id]=list_EdgeId
      edgelist[RSU_id]= list_EdgeId
      del list_NormalEdges[:]
    buffered_paths = {}
    step = 1
    rerouting_step = begin #800
    travel_time_cycle_begin = interval  #600
    duration = 600
    beginp = 0
    endp = 1
    periodic  = 1
    zone_conges={}
    lengthSum = 0.0
    edgeCount=0
    sum_speed_net=0
    for edge in edgeallgraph:
		     sum_speed_net += traci.lane.getMaxSpeed(edge + '_' + '0')
		     lengthSum += traci.lane.getLength(edge + '_' + '0')    
		     edgeCount += 1		 
    avgLengthall = lengthSum / edgeCount
    avgSpeedall = sum_speed_net / edgeCount
    sys.stdout = open('TestAll.txt','wt')
    while step == 1 or traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()
        detect_vehicle_in_RSU_other=[]
        logging.debug("Simulation time %d" % step)  
        if periodic >=600 and periodic <= end and periodic%duration==0:
		   logging.debug("Simulation Step: %d" % step)
		   for rsuid in RSU_ids:
		    if len(edgelist[rsuid]) > 0:
			 logging.debug("rsuid for zone_conges start %s" % rsuid)
			 logging.debug("rsuid edgelist[%s]  %s" % (rsuid,edgelist[rsuid]))
			 zone_conges[rsuid] = float(Road_RSU_congestion_index(edgelist, rsuid, net))
			 subgraph_gg=road_graph_travel_time.subgraph(dicttt_edgeRSUs[rsuid])
			 prediction_area_RSU(subgraph_gg,road_graph_travel_time, edgelist,rsuid, net)
			
			 logging.debug("rsuid for zone_conges end %s" % zone_conges[rsuid])
			 
        if step >= travel_time_cycle_begin and travel_time_cycle_begin <= end and step%interval == 0:
            periodic  = 1
            # logging.debug("Updating travel time on roads at simulation time %d" % step)
            list_present_network=[]
			################ Update Travel Time ##############################
            print("first")
            travel_time_on_roads(road_graph_travel_time, step, travel_time_cycle_begin == step)
            prediction_on_edge(road_graph_travel_time, net)
            road_congestion_at_traffic_area(road_graph_travel_time, edgelist, zone_conges, RSU_ids,net)
            update_travel_time_on_roads(road_graph_travel_time, time, begin_of_cycle)
            Update_Travel_Time(road_graph_travel_time, net)
            for edge in edgeallgraph:
			 list_present_network.append(traci.edge.getLastStepVehicleIDs(edge))
			
            for vehicle in list_present_network:#list_vehicle_set_route:
               for v in vehicle :# if vehicle in list_present_network:
                    source = traci.vehicle.getRoadID(v)
                    dict_fc[source] = dict_fc[source] + 1
                   
			
	#########################################################################################################################################		
	   ########################################## select congested Roads for rerouting by cloud server####################################	   

	    congestedRoadsss=[]
	    for edge in edgeallgraph:
		 #for lanelist in dict_lane[edge]:
		    #for lane in lanelist:
			   listspeedss=[]
			   listvss=[]
			   Max_speed_LaneC = traci.lane.getMaxSpeed(edge + '_' + '0')# Get Maximum Allowed speed
			   listvss.append(traci.edge.getLastStepVehicleIDs(edge))
			   MeanSpeeds= traci.edge.getLastStepMeanSpeed(edge)
			   sumspeedss=0
			   averagespeedss=0
			   jjj=0
			   wwwedge=0
			   listvehicless=[]
			   vehiclecongestedss=[]
			   Wedge_cloud = 1-(MeanSpeeds / Max_speed_LaneC)
			   logging.debug("Wedge_cloud: %s" % Wedge_cloud)
			   Denc=0
			   edge_road = net.getEdge(edge)
			   N_Lane = edge_road.getLaneNumber()
			   number_vehicles =(traci.edge.getLastStepVehicleNumber(edge))
			   Kjam = float ((Lenght_Lane * N_Lane)/ (7.5))
			   if number_vehicles !=0 and Lenght_Lane >= 9:
				    Density = float (number_vehicles / Kjam)
				   else:
				    Density = 0.0
			   if (  Wedge_cloud  +   Density  ) / 2) >= 0.5:
				 congestedRoadsss.append(edge)
		#############################################  select vehicle for rerouting by cloud server  #######################################	   
	    list_of_vehiclecloud=[]
	    for edge in edgeallgraph:
		     if edge in listalledge:continue
		     list_of_vehiclecloud.append(traci.edge.getLastStepVehicleIDs(edge))   			
 	    if len(congestedRoadsss) != 0 :
			logging.debug("cloud_reroute_vehicles is start: " )  
			cloud_reroute_vehicles(road_graph_travel_time,list_of_vehiclecloud,congestedRoadsss,buffered_paths, list_present_network, travel_time_cycle_begin == step, net)
			logging.debug("cloud_reroute_vehicles is end: " )
		#######################################################  Re-Routing for each RSU ################################################
            for rsuid in RSU_ids:
			 subgraph_g[rsuid]=road_graph_travel_time.subgraph(dicttt_edgeRSUs[rsuid])
			 list_of_vehicle=[]
			 congestedRoads=[]
			 vehiclecongested=[]
			 list_present=[]
			 if len(edgelist[rsuid])== 0:continue
			 for edge in edgelist[rsuid]:
				   del visit_bfs[:]
				   logging.debug("edgelist (%s, %s)" % (rsuid, edge))
				   MeanSpeed=0.0
				   number_vehicle=0 
				   max_speed_Lane = float(traci.lane.getMaxSpeed(edge + '_' + '0'))# Get Maximum Allowed speed
				   Lenght_Lane = float(traci.lane.getLength(edge + '_' + '0'))
				   LastStepLength = float(traci.edge.getLastStepLength(edge))
				   listv=traci.edge.getLastStepVehicleIDs(edge) # Get the all vehicle in lane
				   MeanSpeed= float(traci.edge.getLastStepMeanSpeed(edge))
				   Wedge = float(1 - (MeanSpeed / max_speed_Lane))
				   Denc=0
				   edge_road = net.getEdge(edge)
				   N_Lane = edge_road.getLaneNumber()
				   number_vehicles =(traci.edge.getLastStepVehicleNumber(edge))
				   Kjam = float ((Lenght_Lane * N_Lane)/ (7.5))
				   if number_vehicles !=0 and Lenght_Lane >= 9:
				    Density = float (number_vehicles / Kjam)
				   else:
				    Density = 0.0
				   ZoneC = zone_conges[rsuid]
				   sum_conges= (Wedge+ZoneC+Density)/3
				   listcdm.append(sum_conges)	
				   if ZoneC >=0.5:
				    sum_conges= (Wedge+ZoneC+Density)/3
				   else:
				    sum_conges= ( Wedge + Density )
				   
				   if sum_conges >= 0.5:#if  (( Wedge )+ ( Density )) / 2 >= 0.5: # sum_conges >= 0.5:# (Wedge+Density)/2 >= 0.5: # ((sum_conges + ZoneC)/ 2) >= 0.5: 
				        print(list(bfs_edges(subgraph_g[rsuid], edge, reverse=True, L=3)))
				        congestedRoads.append(edge)
 				        for v in visit_bfs:
				            if v in list_present: continue
 				            list_present.append(v)
				            if v.startswith(":"): continue
				            vehiclecongested.append(traci.edge.getLastStepVehicleIDs(v))
				   if len(detect_vehicle_in_RSU_other)!= 0:
				      for vv in vehiclecongested:
				        for v in vv:
						  if v not in detect_vehicle_in_RSU_other:
						   list_of_vehicle.append(v)
						   detect_vehicle_in_RSU_other.append(v)
					        
							
				   else:
				      for vv in vehiclecongested:
				        for v in vv:
						  list_of_vehicle.append(v)
						  detect_vehicle_in_RSU_other.append(v)
                         
			 if len(congestedRoads) > 0 :
			   logging.debug("Simulation for  %s" % rsuid)
			   logging.debug("Simulation time %d" % step)
			   logging.debug("congestedRoads %s" % congestedRoads)
			   logging.debug("list_of_vehicle %s" % list_of_vehicle)
			   logging.debug("detect_vehicle_in_RSU_other: %s" % detect_vehicle_in_RSU_other)
			   reroute_vehicles_RSUs(subgraph_g[rsuid],list_of_vehicle,edgelist[rsuid],congestedRoadsss,congestedRoads,road_graph_travel_time,buffered_paths, list_present_network, travel_time_cycle_begin == step,net)
			  
            rerouting_step += interval
            travel_time_cycle_begin = step + 1
        step += 1 
        periodic +=1
   
    time.sleep(10)
    logging.debug("Simulation finished")
    traci.close()
    sys.stdout.flush()
    time.sleep(10)
	
    
