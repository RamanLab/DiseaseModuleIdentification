'''
	input : Network Number
'''

import networkx as nx
import sys
import random
from collections import defaultdict
import itertools
from sklearn.metrics import jaccard_similarity_score
import community

net = sys.argv[1]
# Load the graph
G = nx.read_edgelist('../sc1/'+net+'.txt', delimiter='\t', create_using=nx.Graph(), nodetype=int, data=(('weight',float),))

# Randomly remove 1% of edges 100 times
k = int(len(G.edges())*0.01)
node_com = defaultdict(lambda: [0]*100)
for i in range(100):
	print i
	g = nx.Graph(G)
	remove = random.sample(g.edges(),k)
	g.remove_edges_from(remove)
	# Clustering on all the network
	modpartit = community.best_partition(g,resolution = 0.1)
	# make a vector of size 100
	for node,com in modpartit.items():
		node_com[node][i] = com

print "Computing similarity..."
Sim_G = nx.Graph()
Sim_G.add_nodes_from(G)
# make a similarity graph by finding jaccard similarity
for node1, node2 in itertools.combinations(node_com, 2):
	js = jaccard_similarity_score(node_com[node1], node_com[node2])
	if js > 0.5:
		Sim_G.add_edge(node1, node2, weight=js)
print len(Sim_G.edges())

# Clustering on similarity graph
partit = community.best_partition(Sim_G,resolution = 0.1)
comm = defaultdict(list)
for node, com in partit.items():
	comm[com].append(node)
with open('../sc1_submit/core_check/'+net+'_perturbation.txt','w') as f:
	for com , nodes in comm.items():
		f.write('\t'.join(map(lambda x: str(x), [com,1]+nodes))+'\n')
