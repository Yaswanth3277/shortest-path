import sys

# Code for uninformed search - Uniform Search Cost Algorithm
def ucs():
    nodes_expanded = 0
    nodes_generated = 1
    nodes_popped = 1
    closed = []
    dest_node = False
    goal_index = locations.index(goal)
    fringe = [{"current": locations.index(source), "total_cost": 0, "parent": None}] # Adding the first node to the fringe
    while len(fringe)>0: # checking for the chile nodes in the graph
        if fringe[0]["current"] == goal_index: # if the present node is the goal node then break
            closed.append({"node": fringe[0]["current"], "parent": fringe[0]["parent"]})
            dest_node = fringe[0]
            break
        elif check_visited(fringe[0]["current"], closed): # if it is not the goal node then check if its already visited if it is already visited then pop it
            del fringe[0]
            nodes_popped = nodes_popped + 1
            continue
        else: # if the node is not present then add its children nodes to the fringe
            nodes_expanded = nodes_expanded + 1
            closed.append({"node":fringe[0]["current"], "parent":fringe[0]["parent"]})
            for values in range(len(route_distance[fringe[0]["current"]])):
                if route_distance[fringe[0]["current"]][values] > 0:
                    fringe.append({"current": values, "total_cost": fringe[0]["total_cost"] + route_distance[fringe[0]["current"]][values], "parent": fringe[0]["current"]})
                    nodes_generated = nodes_generated + 1
            del fringe[0]
            nodes_popped = nodes_popped + 1
            if len(fringe) > 1:# once the children nodes are added to the fringe pop the parent node and then sort the remaining nodes in the fringe
                for nodes in range(0, len(fringe)-1):
                    s_node = nodes
                    for node in range(nodes+1, len(fringe)):
                        small_node = fringe[s_node]["total_cost"]
                        next_node = fringe[node]["total_cost"]
                        if small_node > next_node:
                            s_node = node
                    temp = fringe[s_node]
                    fringe[s_node] = fringe[nodes]
                    fringe[nodes] = temp
    print("nodes popped: " + str(nodes_popped))# print all the values
    print("expanded nodes: " + str(nodes_expanded))
    print("generated nodes: " + str(nodes_generated))

    routes(dest_node, closed)
    return

# code for Informed Search - A star algorithm
def astar():
    nodes_expanded = 0
    nodes_generated = 1
    nodes_popped = 1
    closed_nodes = []
    dest_node = False
    goals_index = locations.index(goal)
    fringe = [{"current": locations.index(source), "total_cost": 0, "heuristics": heuristicss[locations.index(source)], "parent": None}] # Adding the first node to the fringe
    while len(fringe) > 0:# checking for the chile nodes in the graph
        if fringe[0]["current"] == goals_index:# if the present node is the goal node then break
            closed_nodes.append({"node": fringe[0]["current"], "parent": fringe[0]["parent"]})
            dest_node = fringe[0]
            break
        elif check_visited(fringe[0]["current"], closed_nodes):# if it is not the goal node then check if its already visited if it is already visited then pop it
            del fringe[0]
            nodes_popped = nodes_popped + 1
            continue
        else:# if the node is not present then add its children nodes to the fringe
            nodes_expanded = nodes_expanded + 1
            closed_nodes.append({"node": fringe[0]["current"], "parent": fringe[0]["parent"]})
            for values in range(len(route_distance[fringe[0]["current"]])):
                if route_distance[fringe[0]["current"]][values] > 0:
                    fringe.append({"current": values,
                                   "total_cost": fringe[0]["total_cost"] + route_distance[fringe[0]["current"]][values], "heuristics": heuristicss[values],
                                   "parent": fringe[0]["current"]})
                    nodes_generated = nodes_generated + 1
            del fringe[0]
            nodes_popped = nodes_popped + 1
            if len(fringe) > 1:# once the children nodes are added to the fringe pop the parent node and then sort the remaining nodes in the fringe
                for nodes in range(0, len(fringe) - 1):
                    s_node = nodes
                    for node in range(nodes + 1, len(fringe)):
                        small_node = fringe[s_node]["total_cost"]
                        next_node = fringe[node]["total_cost"]
                        small_node += fringe[s_node]["heuristics"]
                        next_node += fringe[node]["heuristics"]
                        if small_node > next_node:
                            s_node = node
                    temp = fringe[s_node]
                    fringe[s_node] = fringe[nodes]
                    fringe[nodes] = temp
    print("nodes popped: " + str(nodes_popped))
    print("expanded nodes: " + str(nodes_expanded))
    print("generated nodes: " + str(nodes_generated))

    routes(dest_node, closed_nodes)
    return


def routes(destination, nodes): # once we reach the destination we use this to find the path and distance
    directions = []
    def check_path(goal, goal_node):
        if goal is not None:
            for node in goal_node:
                if node["node"] == goal:
                    directions.append(goal)
                    check_path(node["parent"], goal_node)

    if destination:
        print("distance:"+ str(destination["total_cost"])+".0 km")
        print("route:")
        check_path(destination["current"], nodes)
        directions.reverse()
        for values in range(0, len(directions)-1):
            print(locations[directions[values]]+ "to"+locations[directions[values+1]]+","+str(route_distance[directions[values]][directions[values+1]])+".0 km")

    else:
        print("distance: infinity")
        print("route:")
        print("none")
    return


def check_visited(current, closed):# this function is used to check if the node is already visited or is it a new one
    for node in closed:
        if current == node["node"]:
            return True
    return False


def heuristics(files): # Opens the heuristics file and adds the values into a list
    heuristics_data = open(files, "r").read().split("\n")
    for rt in heuristics_data:
        if rt == "END OF INPUT":
            break
        else:
            heu_values = rt.split(" ")
            heuristicss[locations.index(heu_values[0])] = int(heu_values[1])
    return

# Opens the input file and traverses through the data
if len(sys.argv) >= 4:
    locations = []
    route_distance = []
    input_data = open(sys.argv[1], "r").read().split("\n")
    source = sys.argv[2]
    goal = sys.argv[3]

    for route in input_data:
        if route == "END OF INPUT":
            break
        else:
            area1, area2, distance = route.strip().split(" ") # split the data
            if area1 in locations:
                pass
            else:
                locations.append(area1)

            if area2 in locations:
                pass
            else:
                locations.append(area2)

    locations.sort()

    for values in range(len(locations)):# used to create an identity matrix
        route_distance.append([])
        for value in range(len(locations)):
            route_distance[values].append(-1)
        route_distance[values][values] = 0

    for route in input_data:# update the values in the matrix that has a path
        if route == "END OF INPUT":
            break
        else:
            area1, area2, distance = route.strip().split(" ")
            route_distance[locations.index(area1)][locations.index(area2)] = int(distance)
            route_distance[locations.index(area2)][locations.index(area1)] = int(distance)

    if len(sys.argv)== 4:
        ucs()
    elif len(sys.argv) == 5:
        heuristicss = [0] * len(locations)
        heuristics(sys.argv[4])
        astar()
    else:
        print("Not Found")