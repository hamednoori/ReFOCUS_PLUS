def prediction_area_RSU(subgraph_g,graph, edgelist, net):
 list=[]
 list_all=[]
 veh_num=0
 # Input  
 f = open("...\\PATH\\Your.rou.xml", 'r')
 data = f.read()
 soup = BeautifulSoup(data)
 f.close()
 dict_edge_deparr={}
 X_arrived_area = 0
 Q_i_out = 0
 for vehicle_tag in soup.findAll("vehicle"):
	  vehicle_id = vehicle_tag["id"]
	  vehicle_route = vehicle_tag.find("route")
	  vehicle_edges = vehicle_route["edges"]
	  dict_edge_deparr[vehicle_id]= vehicle_edges 
 C_i=0
 for road in  edgelist: # Total Vehicle Number in Area
  edge_road = net.getEdge(road)
  N_Lane = edge_road.getLaneNumber()
  
  Lenght_Lane = float(traci.lane.getLength(road.encode("ascii") + '_' + '0'))
  if Lenght_Lane > 8:
   C_i += ((Lenght_Lane *  N_Lane) / 7.5) 
  else:
   C_i += 0
  list.append(traci.edge.getLastStepVehicleIDs(road)) 
  veh_num = veh_num + (traci.edge.getLastStepVehicleNumber(road))
 for v in list:
  route =  traci.vehicle.getRoute(v) 
  source = traci.vehicle.getRoadID(v)
  
  if source == destination: 
   X_arrived_area = X_arrived_area + 1 # Total Vehicle Number arrived in next time
  else:
   next_road = (route.index(source)) + 1
   if next_road not in edgelist: 
    Q_i_out = out + 1 # Total Vehicle Number out in next time
 departed_ids = traci.simulation.getDepartedIDList() 
 X_departed_area = 0
 for road in edgelist:
  for depart in departed_ids: # Total Vehicle Number departed in next time
   route = traci.vehicle.getRoute(depart)
   initialpos= route[0]
   if initialpos == road :
    X_departed_area +=1
   else:
    X_departed_area +=0
 for road in edgeallgraph:# all current vehicles in the road network
  list_all.append(traci.edge.getLastStepVehicleIDs(road))
 Q_i_in = 0
 for v in list_all: # Total Vehicle Number input in next time
  if v not in list:
   route =  traci.vehicle.getRoute(v) 
   source = traci.vehicle.getRoadID(v)
   if source != destination:  
    next_road = (route.index(source)) + 1
    if next_road  in edgelist: 
	 Q_i_in += 1 
	 
 for road in  subgraph_g.nodes_iter():
  if road.startswith(":"):
  for successor_road in subgraph_g.successors_iter(road):
   graph.edge[road][successor_road]["predictArea"]=0
  else:
   graph.edge[road][successor_road]["predictArea"] = max ((veh_num +  Q_i_in + X_departed_area - Q_i_out - X_arrived_area), 0)
   
 
 
 
 
 
 
  
	  
     
      
     