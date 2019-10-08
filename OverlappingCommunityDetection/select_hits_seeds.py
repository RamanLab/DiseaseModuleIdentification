'''
accepts 3 arguments 
arg1: graph file name in which graph is written in edge list format 
arg2: number of seed nodes required
arg3: output file name to store seed nodes
'''

import sys
import networkx as nx
import numpy as np
import scipy.io
from copy import deepcopy
from operator import itemgetter
from collections import OrderedDict

def getSeedsFromAuth(a,G,num_seeds):
    seeds = list()
    a = OrderedDict(a)
    is_seed = dict()
    for node,score in a.iteritems():
        nbrSeedCnt = 0
        for nbr in G.neighbors(node):
            for nbrnbr in G.neighbors(nbr):
                nbrSeedCnt += is_seed.get(nbr,0)
        if nbrSeedCnt == 0:
            seeds.append([float(node)])
            is_seed[node] = 1
        if len(seeds) == num_seeds:
            break
    return seeds

def select_seeds(G,num_seeds):
    G_biconn_core = deepcopy(G)
    G_dir = G_biconn_core

    h,a = nx.hits(G_dir,max_iter=200,tol=0.0001,nstart=G_dir.degree(G_dir.nodes()))
    print "HITS done."
    a_sorted = sorted(a.iteritems(),key=itemgetter(1),reverse=True)
    seeds = getSeedsFromAuth(a_sorted,G,num_seeds)
    print "Seeds Computed"
    return seeds

def __main():
    data_set_path = sys.argv[1]
    num_seeds = int(sys.argv[2])
    G = nx.read_edgelist(data_set_path,data=(('weight',float),))
    seeds = select_seeds(G,num_seeds)
    with open(sys.argv[3],'w') as f:
        for seed in seeds:
            for s in seed:
                f.write(str(int(s)))
            f.write('\n')

if __name__ == "__main__":
    __main()
