def prediction_on_edge(graph, net):
 # Input  
 f = open('...\\PATH\\Your.rou.xml', 'r')
 data = f.read()
 soup = BeautifulSoup(data)
 f.close()
 dict_edge_deparr={}
 for vehicle_tag in soup.findAll("vehicle"):
	  vehicle_id = vehicle_tag["id"]
	  vehicle_route = vehicle_tag.find("route")
	  vehicle_edges = vehicle_route["edges"]
	  dict_edge_deparr[vehicle_id]= vehicle_edges
 departed_ids = traci.simulation.getDepartedIDList() 
 #arrived_ids = traci.simulation.getArrivedIDList() 
 for road in edgeallgraph:
  list_all.append(traci.edge.getLastStepVehicleIDs(road))
 for v in list_all:
  source = traci.vehicle.getRoadID(v)
  route =  traci.vehicle.getRoute(v)
  if source == destination:
   arrived_ids.append(v)
   
 for road in graph.nodes_iter():
  if road.startswith(":"):
   for successor_road in graph.successors_iter(road):
     graph.edge[road][successor_road]["predict"]=0
  else:
     edge_road = net.getEdge(road)
     N_Lane = edge_road.getLaneNumber()
     logging.debug("N_Lane[edge]::::(%s)" % (N_Lane))
     C_i=0
     X_arrived_i = 0
     X_departed_i = 0
     
     for depart in departed_ids:
	  logging.debug("depart::::(%s)" % (depart))
	  route = traci.vehicle.getRoute(depart)
	  initialpos= route[0]
	  if initialpos == road :
	    X_departed_i +=1
	  else:
	    X_departed_i += 0
	  
     for arrive in arrived_ids:
	  logging.debug("arrive::::(%s)" % (arrive))
	  
	  route= dict_edge_deparr[arrive] 
	  destination= route[-1]
	  if destination == road :
	   X_arrived_i +=1
	  else:
	    X_arrived_i += 0
     number_vehicles = traci.edge.getLastStepVehicleNumber(road)
     Lenght_Lane = float(traci.lane.getLength(road.encode("ascii") + '_' + '0'))
     
     if Lenght_Lane > 8:
      C_i = ((Lenght_Lane *  N_Lane) / 7.5) 
     else:	 
      C_i = 0
     
     print(list(bfs_edges(graph, road, reverse=True, L= 1)))
     
     Totaln=0
     Q_i_in=0
     dict_numVehicle_for_edge={}
     if len(visit_bfs) > 1:
	  for e in visit_bfs:
	   n=0
	   numberV_edge_v=0
	   dict_numVehicle_for_edge[e]=0
	   if e==road: continue
	   if e.startswith(":"): continue
	   numberV_edge_v = traci.edge.getLastStepVehicleNumber(e)
	   Vehicle_ids = traci.edge.getLastStepVehicleIDs(e)
	   for v in Vehicle_ids:
	    route = traci.vehicle.getRoute(v)
	    currentpos = traci.vehicle.getRoadID(v)
	    logging.debug("currentpos::::(%s)" % (currentpos))
	    if currentpos != route[-1]:
	      next_road = (route.index(currentpos)) + 1
	      logging.debug("next_road::::(%s)" % (next_road))
	      if route[next_road] == road:
	         n += 1
	   dict_numVehicle_for_edge[e]= n
	   Totaln += numberV_edge_v
	  nextNodeID = net.getEdge(road).getToNode().getID()
	  logging.debug("nextNodeID::::(%s)" % (nextNodeID))
	  
	  logging.debug("roadroad::::(%s)" % (road))
	  logging.debug("visit_bfs::::(%s)" % (visit_bfs))
	  if Totaln != 0 :
	   for edge in visit_bfs:
	    if edge==road: continue
	    if edge.startswith(":"): continue
	    numberV_edge = traci.edge.getLastStepVehicleNumber(edge)
	    edge_nei = net.getEdge(edge)
	    TLS = edge_nei.getTLS()
	    time = edge_nei.getLength() / edge_nei.getSpeed()
	    if TLS is not None:
		 
             tlane = graph.edge[edge][road]["TLane"]
             flane = graph.edge[edge][road]["FLane"]
             TLSID= TLS.getID()
             links = traci.trafficlights.getControlledLinks(TLSID)
             remaningdur = (traci.trafficlights.getNextSwitch(TLSID)- traci.simulation.getCurrentTime()) /1000
             state = traci.trafficlights.getRedYellowGreenState(TLSID)
             dict_State ={}
             i = 0
             for sta in state:
		      dict_State[i] = sta
		      i += 1
		      logging.debug("sta: %s" % sta)
             for conn in links:
		      indicate = links.index(conn)
		      logging.debug("indicate: %s" % indicate)
		      if (edge + '_' + flane)== conn[0]:
		       if (road + '_' + tlane)== conn[1]:
			    if dict_State[indicate] == 'G':
				 Q_i_in +=  (dict_numVehicle_for_edge[edge] / Totaln) *  (remaningdur / graph.edge[edge][road]["TTg"])#numberV_edge * (dict_numVehicle_for_edge[edge] / Totaln) *  (remaningdur / graph.edge[edge][road]["TTg"])
             
	    else:
		 Q_i_in += (dict_numVehicle_for_edge[edge] / Totaln)
	    
	  else:
	   Q_i_in = 0
	   
     else:
	  Q_i_in = 0
      
     ###############################################################
     print(list(bfs_edges(graph, road, reverse=False, L= 1)))
     nn = 0
     Totalnn = 0
     Q_i_out = 0
     dict_numVehicle_for_next_road={}
	 
     listOutfromgoing = net.getEdge(road.encode("ascii")).getToNode().getIncoming()
     logging.debug("listOutfromgoing: %s" % listOutfromgoing)
     EdgeId_Outfromgoing=[]
     for edgelist in listOutfromgoing:
        list_edgelist=[]
        list_edgelist.append(str(edgelist))
        data = list_edgelist[0].split('id=')[1]
        EdgeId_Outfromgoing.append( ast.literal_eval(data.split(' ')[0]))
        logging.debug("EdgeIdEdgeId: %s" % EdgeId_Outfromgoing)
		   	 
     Vehicle_ids= traci.edge.getLastStepVehicleIDs(road)
     for edge in visit_bfs:
	   dict_numVehicle_for_next_road[edge] =0
     
     for v in Vehicle_ids:
	   route= traci.vehicle.getRoute(v)
	   currentpos = traci.vehicle.getRoadID(v)
	  
	   if currentpos != route[-1]:
	    next_road= (route.index(currentpos)) + 1
	    if route[next_road] in visit_bfs:
		 dict_numVehicle_for_next_road[route[next_road]] += 1
                 
     for edge in EdgeId_Outfromgoing:
	     Totalnn += traci.edge.getLastStepVehicleNumber(edge)
	      
     TLS = edge_road.getTLS()
     if  TLS is not None:
       TLSID= TLS.getID()
       lanes = traci.trafficlights.getControlledLanes(TLSID)
       links = traci.trafficlights.getControlledLinks(TLSID)
       logging.debug("TLSID::::(%s)" % (TLSID))
       logging.debug("road::::(%s)" % (road))
       logging.debug("laneslanes::::(%s)" % (lanes))
       logging.debug("links::::(%s)" % (links))
       phaseDuration = traci.trafficlights.getPhaseDuration(TLSID)
       phase = traci.trafficlights.getPhase(TLSID)
       state = traci.trafficlights.getRedYellowGreenState(TLSID)
       logging.debug("state::::(%s)" % (state))
       logging.debug("phase::::(%s)" % (phase))
       logging.debug("phaseDuration::::(%s)" % (phaseDuration))
       getSwitch = traci.trafficlights.getNextSwitch(TLSID)
       logging.debug("getSwitch::::(%s)" % (getSwitch))
       remaningdur = (traci.trafficlights.getNextSwitch(TLSID)- traci.simulation.getCurrentTime()) /1000

       logging.debug("remaningdur::::(%s)" % (remaningdur))
       dict_State ={}
       i = 0
       for sta in state:
		dict_State[i] = sta
		i += 1
		logging.debug("sta: %s" % sta)
     time = edge_road.getLength() / edge_road.getSpeed()  
     for edge in visit_bfs:
	   if edge.startswith(":"): continue
	   if edge==road:continue  
	   if Totalnn !=0 :
	     if TLS is not None:
		  flane = graph.edge[road][edge]["FLane"]
		  tlane = graph.edge[road][edge]["TLane"]
		  
		  for conn in links:
		   indicate = links.index(conn)
		   logging.debug("indicate: %s" % indicate)
		   if (road + '_' + flane) == conn[0]:
		    if (edge + '_' + tlane) == conn[1]:
			 if dict_State[indicate] == 'G':
			  Q_i_out += (dict_numVehicle_for_next_road[edge] / Totalnn) * (remaningdur / graph.edge[road][edge]["TTg"]) #number_vehicles * (dict_numVehicle_for_next_road[edge] / Totalnn) * (remaningdur / graph.edge[road][edge]["TTg"]) 
			      
	     else:
		  Q_i_out += (dict_numVehicle_for_next_road[edge] / Totalnn)#number_vehicles * (dict_numVehicle_for_next_road[edge] / Totalnn) #* (4./time)
	   else:
	      Q_i_out =0
	 
     X_i_calculated_next_k = max ((number_vehicles +  Q_i_in + X_departed_i - Q_i_out - X_arrived_i), 0)
     
     for successor_road in graph.successors_iter(road):
        if C_i != 0 :
		 x = X_i_calculated_next_k / C_i
		 if x > 1 :
		  x= 1
		 
		 graph.edge[road][successor_road]["predict"] = x
        else:
         graph.edge[road][successor_road]["predict"] = 0
        logging.debug("predictpredictpredictpredict: %s" % graph.edge[road][successor_road]["predict"])
        logging.debug("X_i_calculated_next_k: %s" % X_i_calculated_next_k)
        logging.debug("number_vehicles: %s" % number_vehicles)
        logging.debug("Q_i_in: %s" % Q_i_in)
        logging.debug("X_departed_i: %s" % X_departed_i)
        logging.debug("Q_i_out: %s" % Q_i_out)
        logging.debug("X_arrived_i: %s" % X_arrived_i)
        logging.debug("C_i: %s" % C_i)

        list_predict.append(graph.edge[road][successor_road]["predict"])
        d= graph.edge[road][successor_road]["predict"]
        print("roadtest: {0}".format(road))
        print ("{0}w6 id={1}{2}{3} {4}{5}" .format('<','"',d,'"','/','>'))

  