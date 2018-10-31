'''inputs : weighted graph as edgelist,
            community file,
            resolution for community detection algorithm,
            output file name'''  

import networkx as nx
import community
import sys
#construct graph
G = nx.read_edgelist(sys.argv[1], delimiter='\t', create_using=nx.Graph(), nodetype=int, data=(('weight',float),))
#print G.edges(data=True)

#read community file and remove nodes of smaller community
count = 1
comms = {}
comm_file = open(sys.argv[2],'r')
for line in comm_file:
    l = line.rstrip().split("\t")
    comm = [int (l[i]) for i in range(2,len(l))]
    if len(comm) >=3 and len(comm)<=100:  #removes nodes belonging to perfect community from network
        comms[count] = comm
        count += 1
        G.remove_nodes_from(comm)

#modularity maximization on the remaining graph
parameter=sys.argv[3]
###Modularity
modpartit = community.best_partition(G,resolution=float(parameter))
print 
modularit, mod = community.modularity(modpartit,G)
print "Modularity score:",round(modularit,2)
comm = {}
for i in modpartit.keys():
#    print i,"\t",modpartit[i]
    if comm.has_key(modpartit[i]):
        comm[modpartit[i]].append(i)
    else:
        comm[modpartit[i]]=[i]
for _,val in comm.iteritems():
    comms[count] = val
    count += 1

#writing community to file
output_file_name = sys.argv[4]
output_file = open(output_file_name,'w')
#output_file.write(str("Modularity score: ")+str(round(modularit,2))+"\n")
for key, value in comms.iteritems() :
    output_file.write(str(key)+"\t1")
    for elem in value:
        output_file.write("\t"+str(elem))
    output_file.write("\n")
output_file.close()