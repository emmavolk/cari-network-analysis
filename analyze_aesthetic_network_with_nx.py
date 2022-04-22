import json
import csv
import networkx as nx
import matplotlib.pyplot as plt

source_file = "cari_data.json"

G = nx.Graph()

nodelist = []
edgelist = []

#create the node and edge lists
with open(source_file, "r") as json_file:
    data = json.load(json_file)
    for aesthetic_category in data:
        aesthetic_id = aesthetic_category["ID"]
        nodelist.append(aesthetic_id)
        for similar_aesthetic in aesthetic_category["Similar_Aesthetics"]:
            edgelist.append([aesthetic_id, similar_aesthetic])

#construct the graph
G.add_nodes_from(nodelist)
G.add_edges_from(edgelist)

#removing node 58 because it's an isolate (unconnected to all other nodes), so it compromises the analysis
G.remove_node(58)

#draw the graph
nx.draw_spring(G, with_labels=True)

#calculate the diameter of the graph, ie the smallest path between opposite ends of the network
nx.diameter(G)

#calculate the density of the graph, ie # of actual connections divided by # of total possible connections
nx.density(G)

#return a list of bridges, ie edges whose removal would disconnect the graph
list(nx.bridges(G))

#return the degree centrality for each node, ie how many edges a node has
nx.degree_centrality(G)