def build_road_graph(network, net):                
    f = open("...\\PATH\\Your.net.xml", 'r')
    data = f.read()
    soup = BeautifulSoup(data)
    f.close()
    sys.stdout = open('RSU.txt','wt')
    edges_length={}
    numberlane = {}
    mul=0
    for edge_tag in soup.findAll("edge"):
	  edge_id = edge_tag["id"]
 	  lane_tag = edge_tag.find("lane")
	  edge_length = float(lane_tag["length"])
	  edge_speed = float(lane_tag["speed"])
	  edges_length[edge_id] = edge_length
	  edgListLength.append(edge_length)
	  edgListspeed.append(edge_speed)
	  edgeallsgraph.append(edge_id)
	  lane_tagall= edge_tag.findAll("lane")
	  laneid=[]
	  number_of_lane[edge_id]=0
	  for lane in lane_tagall:
	   laneid.append(lane["id"])
	   laneallgraph.append(lane["id"])
	   dict_lane[edge_id]= laneid
	   number_of_lane[edge_id]= number_of_lane[edge_id] + 1  
    graph = nx.DiGraph() 
    for edg_tag in soup.findAll("edge"):
	 edg_id = edg_tag["id"]
 	 if edg_id.startswith(":") : continue
	 edgeallgraph.append(edg_id)
    for connection_tag in soup.findAll("connection"):
        source_edge = connection_tag["from"]        
        dest_edge = connection_tag["to"]
        if source_edge.startswith(":") or dest_edge.startswith(":"):
		 graph.add_edge(source_edge.encode("ascii"), dest_edge.encode("ascii"), length=edges_length[source_edge], TTg=0, weight=0 , TT=0, Counter=0)
        else:
         edge_net = net.getEdge(source_edge)
         nextEdge = net.getEdge(dest_edge)
         connection = str(edge_net.getOutgoing()[nextEdge][0])
         FromLane = connection.split(' ')[3]
         s,fromLane = FromLane.split("fromLane=")
         logging.debug("connection::::(%s)" % (connection))
         logging.debug("FromLaneFromLaneFromLane::::(%s)" % (fromLane))
         ToLane = connection.split(' ')[4]
         s,toLane = ToLane.split("toLane=")
         logging.debug("ToLaneToLane::::(%s)" % (toLane))
         graph.add_edge(source_edge.encode("ascii"), dest_edge.encode("ascii"), length= edges_length[source_edge], FLane = fromLane, TLane = toLane, TTg=0, weight=0 ,predict=0, TT=0, Counter=0,predictArea=0)
        
    
    return graph