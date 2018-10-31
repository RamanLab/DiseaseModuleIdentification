'''input: (run from outside src)
		Network
		Submission Id
'''

import sys
from collections import defaultdict
import itertools
import community
import networkx as nx

net = sys.argv[1]
sub_id = sys.argv[2]
power = 1e-4 # Power for seed node

def conductance(G, S):
    num_cut_edges = len(list(nx.edge_boundary(G, S))) *1.0
    volume_S = sum(dict(G.degree(S)).values()) *1.0
    return num_cut_edges / volume_S

#Reading the network
G = nx.read_edgelist('sc1/'+net+'.txt', delimiter='\t', create_using=nx.Graph(), nodetype=int, data=(('weight',float),))

#Reading Enriched files to find out community number
enriched_path = "enriched_files/"+sub_id+"_enrichedModules_gwas_set_all.txt"
commNo_diseases = map(lambda l: l.rstrip().split("\t"), open(enriched_path,'r').readlines())
comms = [int(commNo_diseases[i][0]) for i in range(2,len(commNo_diseases))]
disease = [commNo_diseases[i][1:] for i in range(2,len(commNo_diseases))]
commNo_diseases={u:v for u,v in zip(comms,disease)}

#Reading node id of Enriched Community from submission file and creating gene2com with community no.
submit_path = "sc1_submit/diseaseSeedExpansion/"+sub_id
communities = map(lambda l: l.rstrip().split("\t"), open(submit_path,'r').readlines())
communities = {int(l[0]) : map(int,l[2:]) for l in communities if int(l[0]) in comms}

mod = {}
cond = {}
for com, nodes in communities.items():
	part = {n:(1 if n in nodes else 0) for n in G.nodes()}
	# Find modularity of that group
	mod[com] = community.modularity(part,G)[1][1]
	cond[com] = conductance(G,nodes)

# writing modularity and conductance to file
with open("SeedExpansionAnalysis/"+sub_id+'_CommNo_Mod_Cond_Disease.tsv','w') as f:
	f.write('CommNo\tModularity\tConductance\t#Disease\tDisease\n')
	for com in communities:
		f.write('\t'.join([str(com),str(mod[com]),str(cond[com]),str(len(commNo_diseases[com]))])+'\t'+','.join(commNo_diseases[com])+'\n')

# writing conductance to file
with open("SeedExpansionAnalysis/"+sub_id+'_Conductance_Enriched.tsv','w') as f:
	f.write('Network\tConductance\n')
	for com in communities:
		f.write(net+'\t'+str(cond[com])+'\n')

# writing modularity to file
with open("SeedExpansionAnalysis/"+sub_id+'_Modularity_Enriched.tsv','w') as f:
	f.write('Network\tModularity\n')
	for com in communities:
		f.write(net+'\t'+str(mod[com])+'\n')