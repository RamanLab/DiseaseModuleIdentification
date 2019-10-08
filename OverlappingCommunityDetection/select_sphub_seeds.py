'''
accepts 3 arguments 
arg1: graph file name in which graph is written in edge list format 
arg2: number of seed nodes required
arg3: output file name to store seed nodes
'''
import sys
import networkx as nx
import numpy as np
from operator import itemgetter
import scipy.io

def select_seeds(G,num_seeds):
    seeds = list()
    mark = dict()
    deg = sorted(G.degree(G.nodes()).iteritems(),key=itemgetter(1),reverse=True)
    while len(seeds) < num_seeds and len(deg) > 0:
        node = deg[0][0]
        del deg[0]
        if mark.get(node,0) == 0:
            seeds.append([node])
            mark[node] = 1
            for nbr in G.neighbors(node):
                mark[nbr] = 1
    return seeds


def __main():
    data_set_path = sys.argv[1]
    num_seeds = int(sys.argv[2])
    G = nx.read_edgelist(data_set_path,delimiter='\t', create_using=nx.Graph(), nodetype=int,data=(('weight',float),))
    seeds = select_seeds(G,num_seeds)
    with open(sys.argv[3],'w') as f:
        for seed in seeds:
            for s in seed:
                f.write(str(s) + ' ')
            f.write('\n')

if __name__ == "__main__":
    __main()
