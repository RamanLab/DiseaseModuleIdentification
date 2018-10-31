import networkx as nx 
import sys
import copy
from collections import defaultdict
import gzip

__MIN = 0.0000001

def conductance(G, S):
	if len(S.nodes())==0 or len(S.nodes())==1:
		return 0
	else:
		num_cut_edges = len(nx.edge_boundary(G, S)) *1.0
		volume_S = sum(G.degree(S).values()) *1.0
		return num_cut_edges / volume_S

#Reading network
net=sys.argv[1]
G = nx.read_edgelist("sc1/original/"+net+".txt", data=(('weight',float),), create_using=nx.Graph())
sub_id=sys.argv[2]
comm={}

postfix = {	'1': '.1_ppi_anonym_v2.txt.gz', '2': '.2_ppi_anonym_v2.txt.gz', '3':'.3_signal_anonym_directed_v3.txt.gz' ,'4':'.4_coexpr_anonym_v2.txt.gz' ,'5':'.5_cancer_anonym_v2.txt.gz' ,'6':'.6_homology_anonym_v2.txt.gz' }
#Reading node id of All Community from submission file and creating genelist with community no.
geneList = defaultdict(list)
line=map(lambda x: x.rstrip().split('\t'),gzip.open("ToEval/"+net+"/"+net+'.'+sub_id+postfix[net],'r').readlines())
for l in line:
	comm[l[0]] =[]
	for i in range(2,len(l)):
		geneList[l[i]].append(l[0])

# creating community list with non-overlapping part
undecidedGene=[]
for gene in geneList:
	if len(geneList[gene])==1:
		comm[geneList[gene][0]].append(gene)
	else:
		undecidedGene.append(gene)

cond={}
# computing conductance of community
for c in comm:
	S = G.subgraph(comm[c])
	cond[c]=conductance(G,S)
#print "conductance",cond

newcomm={}
# find community for undecidedGene with max increase in conductance 
for ug in undecidedGene:
	maxinc=0
	newcomm[ug]=geneList[ug][0]
	for c in geneList[ug]:
		temp=copy.deepcopy(comm[c])
		temp.append(ug)
		S = G.subgraph(temp)
		temp_cond=conductance(G,S)
		inc=cond[c]-temp_cond
		if inc>=maxinc:
			maxinc=inc
			newcomm[ug]=c
	#cond[newcomm[ug]]=maxinc
# print "new community ",newcomm
#print len(newcomm)
#print len(undecidedGene)

# assign undecidedGenes to best community with max increase in conductance
for g in newcomm:
	c=newcomm[g]
	comm[c].append(g)
score = 0
for c in comm.keys():
	S = G.subgraph(comm[c])
	cond[c]=conductance(G,S)
	score=score+cond[c]
modif=True
new_score=score
while modif:
	cur_score = new_score
	modif = False
	# find community for undecidedGene with max increase in conductance 
	for ug in undecidedGene:
		maxinc=0
		# removing from the assigned community
		com=newcomm[ug]
		comm[com].remove(ug)
		cond[com]=conductance(G,G.subgraph(comm[com]))
		best_com=com
		for c in geneList[ug]:
			temp=copy.deepcopy(comm[c])
			temp.append(ug)
			S = G.subgraph(temp)
			temp_cond=conductance(G,S)
			inc=cond[c]-temp_cond
			if inc>maxinc:
				maxinc=inc
				best_com=c
		newcomm[ug]=best_com
		# insert undecidedGenes to best community with max increase in conductance
		comm[best_com].append(ug)
		cond[best_com]=conductance(G,G.subgraph(comm[best_com]))
		if best_com != com:
			# print "modified"
			modif  =  True
	# print "new community ",newcomm
	#computing conductance of whole graph
	new_score=0
	for c in comm.keys():
		new_score=new_score+cond[c]
	if (cur_score - new_score) < __MIN:
		print "no conducatnce increase",str(cur_score)+"\t"+str(new_score)
		break

# writing communities to file
with gzip.open("ToEval/"+net+"/"+net+'.'+sub_id+'_O2NO'+postfix[net],'w') as f:
	for count, community in enumerate(comm):
		if len(comm[community])>2 and len(comm[community])<101:
			f.write("\t".join([str(count),'1']+comm[community])+'\n')
