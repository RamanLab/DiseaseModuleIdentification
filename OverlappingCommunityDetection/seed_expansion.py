import networkx as nx
import sys
import argparse
from collections import defaultdict
import time
from multiprocessing import Pool
import numpy as np


INF = float('inf')

def pprgrow(args):
	seed,A,stopping,nruns,alpha,maxexpand,maxdeg,fast = args
	expandseq = [2.0,3.0,4.0,5.0,10.0,15.0]
	expands = list()
	curmod = 1.0
	while len(expands) < nruns:
		temp = [curmod*i for i in expandseq]
		for i in temp:
			expands.append(i)
		curmod *= 10.0

	expands = expands[:nruns]
	bestcond = INF
	bestset = list()
	bestexpand = 0.0
	bestceil = 0.0
	bestmceil = 0.0
	bestccnes = 0.0
	besttpr = 0.0
	bestfomd = 0.0
	bestmod = 0.0
	if fast==True:
		expands = [1000.0]
	for ei in xrange(len(expands)):
		if fast==True:
			curexpand = expands[ei]
		else:
			curexpand = expands[ei]*len(seed)+maxdeg
		assert len(seed)>0.0
		if curexpand > maxexpand:
			continue
		A_data, A_indices, A_indptr = np.array(A.data,dtype=long), np.array(A.indices,dtype=long), np.array(A.indptr,dtype=long)
		n_data, n_indices, n_indptr, n_seed = A_data.shape[0], A_indices.shape[0], A_indptr.shape[0], seed.shape[0]
		curset = np.array([-1]*A.shape[0],dtype=long)
		if stopping=='cond':
			import pprgrow_cy_cond
			cond=0.0
			pprgrow_cy_cond.pprgrow_min_cond_func(A_data,n_data,A_indices,n_indices,A_indptr,n_indptr,seed,n_seed,curset,cond,alpha,curexpand)
			curset = curset[curset!=-1]
			if cond < bestcond:
				bestcond = cond
				bestset = curset
				bestexpand = curexpand
		if stopping=='mod':
			import pprgrow_cy_mod
			mod=0.0
			pprgrow_cy_mod.pprgrow_max_mod_func(A_data,n_data,A_indices,n_indices,A_indptr,n_indptr,seed,n_seed,curset,mod,alpha,curexpand)
			curset = curset[curset!=-1]
			if mod > bestmod:
				bestmod = mod
				bestset = curset
				bestexpand = curexpand

	return curset


def growclusters(G,seeds,expansion,stopping,nworkers,nruns,alpha,maxexpand,fast):
	if maxexpand == INF:
		maxexpand = G.number_of_edges()*1.0

	seeds = [np.array(sorted(seed),dtype=long) for seed in seeds]
	n = G.number_of_nodes()
	ns = len(seeds)
	maxdeg = max([len(G[n]) for n in G])
	communities = list()

	# Convert graph to adjacency matrix
	A = nx.adjacency_matrix(G, nodelist=G)
	if nworkers==1:
		for i in xrange(ns):
			seed = seeds[i]
			if expansion=='ppr':
				curset = pprgrow((seed,A,stopping,nruns,alpha,maxexpand,maxdeg,fast))
			else:
				print 'Method not implemented yet'

			communities.append(curset)
			print 'Seed',i,'Done'

	else:
		print 'Initiating parallel seed expansion'
		slen = len(seeds)
		args = zip(seeds,[A]*slen,[stopping]*slen,[nruns]*slen,[alpha]*slen,\
			[maxexpand]*slen,[maxdeg]*slen,[fast]*slen)
		p = Pool(nworkers)
		if expansion=='ppr':
			communities = p.map(pprgrow, args)
	#	p.close()
	#	p.join()

	return communities


# TO DO: Write function to remove duplicate communities
def remove_duplicates(G, communities,delta):
	# Create node2com dictionary
	node2com = defaultdict(list)
	com_id = 0
	for comm in communities:
		for node in comm:
			node2com[node].append(com_id)
		com_id += 1

	deleted = dict()
	i = 0
	for i in xrange(len(communities)):
		comm = communities[i]
		if deleted.get(i,0) == 0:
			nbrnodes = nx.node_boundary(G, comm)
			for nbr in nbrnodes:
				nbrcomids = node2com[nbr]
				for nbrcomid in nbrcomids:
					if i!=nbrcomid and deleted.get(i,0)==0 and deleted.get(nbrcomid,0)==0:
						nbrcom = communities[nbrcomid]
						distance = 1.0 - (len(set(comm) & set(nbrcom))*1.0 / (min(len(comm),len(nbrcom))*1.0))

						if distance <= delta:
							# Near duplicate communities found.
							# Discard current community
							# Followed the idea of Lee et al. in GCE
							deleted[i] = 1
							for node in comm:
								node2com[node].remove(i)
	for i in xrange(len(communities)):
		if deleted.get(i,0)==1:
			communities[i] = []

	communities = filter(lambda c: c!=[], communities) # Discard empty communities
	return communities


def __main():
	parser = argparse.ArgumentParser()
	parser.add_argument('graph_file',type=str,help='Input Graph File Path')
	parser.add_argument('seed_file',type=str,help='Input Seeds File Path')
	parser.add_argument('--expansion',type=str,help='Seed expansion: PPR or VPPR',default='ppr')
	parser.add_argument('--stopping',type=str,help='Stopping criteria',default='mod')
	parser.add_argument('--nworkers',type=int,help='Number of Workers',default=1)
	parser.add_argument('--nruns',type=int,help='Maximum number of runs',default=13)
	parser.add_argument('--alpha',type=float,help='alpha value for Personalized PageRank expansion',default=0.99)
	parser.add_argument('--maxexpand',type=float,help='Maximum expansion allowed for approximate PPR',default=INF)
	parser.add_argument('--delta',type=float,help='Minimum distance parameter for near duplicate communities',default=0.0)
	parser.add_argument('--outfilepath',type=str,help='Path of output file \'community.dat\'',default='.')
	args = parser.parse_args()

	G = nx.read_edgelist(args.graph_file, nodetype=int, data=(('weight',float),), create_using=nx.Graph())
	temp=[n for n in range(max(G.nodes()))]
	G.add_nodes_from(temp)
	
	print "Graph Loaded"
	with open(args.seed_file,'r') as f:
		seeds = f.readlines()
		seeds = [x.strip() for x in seeds]
		seeds = [x.split() for x in seeds]
		seeds = [[int(y) for y in x if int(y) in G.nodes()] for x in seeds]
	print "Seeds Loaded\n"

	print "Initiating Seed Expansion------"
	communities = growclusters(G,seeds,args.expansion,args.stopping,args.nworkers,args.nruns,args.alpha,args.maxexpand,False)
	print "Seed Expansion Finished.\n"
	if args.delta >= 0.0:
		print "Initiating removal of near duplicate communities."
		communities = remove_duplicates(G,communities,args.delta)
		print "Duplicate communities removed\n"

	print "Writing communities to output file:"
	with open(args.outfilepath,'w') as f:
		for community_id,c in enumerate(communities):
			#print c
			f.write('\t'.join(map(str, [community_id+1,1]+c.tolist())) +'\n')
	
if __name__ == "__main__":
	__main()

