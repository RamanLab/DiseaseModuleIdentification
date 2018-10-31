'''inputs : weighted graph as edgelist,
            community file,,
            output file name''' 

import sys
import networkx as nx
from collections import defaultdict

#construct graph
G = nx.read_edgelist(sys.argv[1], delimiter='\t', create_using=nx.Graph(), nodetype=int, data=(('weight',float),))

#read community file and remove nodes of smaller community
communities = map(lambda l: l.rstrip().split("\t"), open(sys.argv[2],'r').readlines())
communities = {int(l[0]) : map(int,l[2:]) for l in communities if len(l) > 4}

#shorten the community by keeping nodesw whose out_degree to indegree ratio is greater than 1
with open(sys.argv[3],'w') as f:
    for community_id,i in enumerate(communities.keys()):
        if len(communities[i])>100:
            ncc = nx.number_connected_components(G.subgraph(communities[i]))
            if ncc != 1:
                print ncc
                continue
            indeg = G.subgraph(communities[i]).degree(communities[i])
            out_in_ratio = {x:1.0*(G.degree(x)-indeg[x])/indeg[x] for x in communities[i]}
            newcore = sorted([j for j in communities[i] if out_in_ratio[j] < 1], key = lambda x: out_in_ratio[x])[:60]
            f.write('\t'.join(map(str, [community_id+1,1]+newcore)) +'\n')
        else:
            f.write('\t'.join(map(str, [community_id+1,1]+communities[i])) +'\n')

