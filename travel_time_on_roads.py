def travel_time_on_roads(graph,time, begin_of_cycle):
    Lenght_Lane = 0
    max_speed_Lane = 0
    travel_time = 0
    avespeed = 0
    maxLenght = 0
    mul_max = 0
    mean = 0
    Vmax = 0
    vmaxlane = 0.0
    Vmax = max(edgListspeed) 
    maxLenght = max(edgListLength)
    mul_max= float(maxLenght * Vmax)
    maxtraveltime = 0.0
    for road in graph.nodes_iter():
        travel_time = traci.edge.getAdaptedTraveltime(road.encode("ascii"), time)
        travel_timenon = traci.edge.getAdaptedTraveltime(road.encode("ascii"), time)
        logging.debug("AdaptedTraveltime::::(%s)" % (travel_time))
        vmaxlane = traci.lane.getMaxSpeed(road.encode("ascii") + '_' + '0')
        dict_fc[road]= traci.edge.getLastStepVehicleNumber(road.encode("ascii"))
        logging.debug("maxLenght :::: (%s)" % maxLenght)
        if travel_time <= 0:
            Lenght_Lane = float(traci.lane.getLength(road.encode("ascii") + '_' + '0')) 
            Vcurrent = traci.edge.getLastStepMeanSpeed(road.encode("ascii"))
            logging.debug("Vcurrent::::(%s)" % (Vcurrent))
            logging.debug("Lenght::::(%s)" % (Lenght_Lane ))
            logging.debug("Vmaxlane :::: (%s)" % vmaxlane)
            travel_timenon = traci.edge.getTraveltime(road.encode("ascii"))
            travel_time = float((Lenght_Lane) / ((Vcurrent + vmaxlane)* maxLenght) )
        for successor_road in graph.successors_iter(road):
            if begin_of_cycle:
                graph.edge[road][successor_road]["weight"] = travel_time
                graph.edge[road][successor_road]["TTg"] = travel_timenon
            else:
                t = float((graph.edge[road][successor_road]["weight"]) + (travel_time)) / 2 #### t!=0
                Vcurrent = traci.edge.getLastStepMeanSpeed(road.encode("ascii"))
                t = t if t > 0 else travel_time
                graph.edge[road][successor_road]["weight"] = t
                tt = float((graph.edge[road][successor_road]["TTg"]) + (travel_time)) / 2
                tt = tt if tt > 0 else travel_timenon
                graph.edge[road][successor_road]["TTg"] = tt
                logging.debug("travel_timenotbegin:::(%s)" % (t))
                logging.debug("Vcurrent:::-340581875#0(%s)" % (road.encode("ascii")))
                logging.debug("Road:::-340581875#0(%s)" % (Vcurrent))
            listtraveltime.append(graph.edge[road][successor_road]["weight"])
            d = graph.edge[road][successor_road]["weight"]
            print("roadtest: {0}".format(road))
            print ("{0}w1 id={1}{2}{3} {4}{5}" .format('<','"',d,'"','/','>'))

			
			
		
