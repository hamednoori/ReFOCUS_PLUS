def choose_route(paths_and_weights, possible_paths, k, max_weight,begin_of_cycle,graph,source, destination,net, temperature=1):  
    route = None
    highest_choice_prob = 0
    N=0
    list_choice_prob=[]
    dict_choice_prob={}
    sys.stdout = open('h.txt','wt')
    for edge in edgeallgraph:
	     N += dict_footprint[edge]         
    if N==0:
	   route = nx.dijkstra_path(graph, source, destination,"weight")
	   for e in route:
	     dict_footprint[e] = dict_footprint[e] + 1
             logging.debug("dict_footprint::::(%d)" % (dict_footprint[e]))
    else:
	  for path in possible_paths:
                divefN= 0
		for edge in path:
		  ni = dict_footprint[edge]
		  fci=0.0
		  print("ni:{0}" .format(ni))
		  Lenght_Lane = traci.lane.getLength(edge + '_' + '0')
		  max_speed_Lane = float(traci.lane.getMaxSpeed(edge + '_' + '0'))
		  edge_road = net.getEdge(edge)
		  N_Lane = edge_road.getLaneNumber()
		  fci = Decimal(ni * (Decimal(Decimal(avgLengthall) / Decimal(Decimal(Lenght_Lane) * Decimal(N_Lane))) * Decimal(Decimal(avgSpeedall) / Decimal(max_speed_Lane))))
		  print("fci:{0}" .format(fci))
		  logging.debug("fci::::(%d)" % (fci))
		  logging.debug("N::::(%d)" % (N))
		  if fci==0 : continue
		  divefN += Decimal(Decimal(Decimal(fci) / N) * Decimal(math.log(Decimal(fci) / N)))
		  print("divefN:{0}" .format(divefN))
		Entropyk = Decimal(divefN)
		print("Entropyk:{0}" .format(Entropyk))
		choice_prob = Decimal(math.exp(Entropyk))
		print("choice_prob:{0}" .format(choice_prob))
		list_choice_prob.append(choice_prob)
		dict_choice_prob[choice_prob]= path
	  print("route:{0}" .format(route))
	  min_choice_prob = min(list_choice_prob)
	  route = dict_choice_prob[min_choice_prob]
	  for edge in route:
	     dict_footprint[edge]+=1
    return route	
	
	    	

   
	
 