import networkx as nx
import sys
import gzip

# grpah of all the diseases
G=nx.Graph()
#gene={}
for sub_id in range(1,182):
	predLea=open("Enriched/1."+str(sub_id)+"_enrichedModules_gwas_set_leaderboard.txt",'r')
	predTest=open("Enriched/1."+str(sub_id)+"_enrichedModules_gwas_set_final.txt",'r')
	comm=[]
	cnt=0
	for line in predLea:
		if cnt<2:
			cnt=cnt+1
			continue
		l=line.rstrip().split("\t")
		#print l[0]
		comm.append(int(l[0]))
		for i in range(1,len(l)):
			for j in range(i+1,len(l)):
				wt=G.get_edge_data(l[i],l[j],{'weight':0})
				G.add_edge(l[i],l[j],weight=wt['weight']+1)
	predLea.close()
	cnt =0
	for line in predTest:
		if cnt<2:
			cnt=cnt+1
			continue
		l=line.rstrip().split("\t")
		if int(l[0]) not in comm:
			for i in range(1,len(l)):
				for j in range(i+1,len(l)):
					wt=G.get_edge_data(l[i],l[j],{'weight':0})
					G.add_edge(l[i],l[j],weight=wt['weight']+1)
	predTest.close()
nx.write_edgelist(G,'Disease.net',data=['weight'])