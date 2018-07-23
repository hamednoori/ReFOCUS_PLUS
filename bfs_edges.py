def bfs_edges(G, source, reverse=False, L=0):#BFSMAXDEPTH program
    if reverse : 
        neighbors = G.predecessors_iter
    else:
        neighbors = G.successors_iter
     visited = set([source])
    del visit_bfs[:]
    visit_bfs.append(source)
    queue = deque([(source, neighbors(source), 0)])
    while queue: 
        parent, children, v = queue[0]
        q= children
        front= queue.popleft()
        level = front[2]
        if level >= L:
		      break
        level +=1
        for child in children:  
            if child not in visited:
                yield parent, child
                visited.add(child)
                visit_bfs.append(child)
                queue.append((child, neighbors(child), level))
