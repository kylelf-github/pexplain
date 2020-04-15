
#from array import array
import re
import sys

#def main (argv): 
def main (): 
	n = len(sys.argv) 
	print("n",n )
	if n > 1 :
		#filename="plans/" + sys.argv[1]
		filename=sys.argv[1]
		print("filename ", filename)
	else:
		print("no file given")
		exit()
	# read file
	#file = open("plans/01CD.p","r")
	#file = open("plans/X5SA.p","r")
	file = open(filename,"r")
	lines = file.readlines()
	file.close()

	depthcnt={}

        node_cnt=0
        cost_at_node={}
        depth_at_node={}
        cost_children={}
        buffer={}
	temp_buffer=""

	# look for patterns
	for line in lines:
		# look for nodes
		# depth equals -1, even though divided by 6
		depth = line.find ("  ->")/6 
		#print("depth ",depth)
		
		#  extract cost from line
		costs = line.find ("cost")
		# total_cost
		if costs != -1 & depth == -1 :
			total_cost=line.split("..")[1].split()[0]
			print("first cost ", total_cost)
			cost=total_cost

		# if "->" 
		if depth != -1:
			buffer[node_cnt]=temp_buffer
			temp_buffer=""
			indents=line.split("->")[0]
			# cost
			# split after first .., take right, split on blanks, take first string
			cost=line.split("..")[1].split()[0]

			#print(node_cnt),
			#print(depth),
			#print(indents),
			#print("->"),
                        #print(cost),

			if depthcnt.has_key(depth):
				depthcnt[depth]+=1
			else:
				depthcnt[depth]=1

        		cost_at_node[node_cnt]=cost
        		depth_at_node[node_cnt]=depth
        		node_cnt+=1

                        #print(depthcnt[depth])
		temp_buffer=temp_buffer+line

	parent=0
	while parent < node_cnt:
		cost_children[parent]=0
		child=parent+1
		while child < node_cnt:
			if int(depth_at_node[child]) == int(depth_at_node[parent])+1:
				#print("    "),
				#print(parent),
				#print(cost_at_node[parent]),
				cost_children[parent]+=float(cost_at_node[child])
				#print(cost_children[parent]),
				#print(cost_at_node[child])
			if depth_at_node[child] ==  depth_at_node[parent]:
				child=node_cnt
			child+=1
		parent+=1;

	parent=0
	while parent < node_cnt:
		pctcost_node=round(100*float(cost_at_node[parent])/float(total_cost),2)
		if pctcost_node >= 10.0 :
			print(parent), 
			print(depth_at_node[parent])
			cdepth=0
			while cdepth <= depth_at_node[parent]:
				print("    "),
				cdepth+=1
			print("->"),
			print("node delta %"),
			pctcost_node_delta=round(100*(float(cost_at_node[parent])-(float(cost_children[parent])))/float(total_cost),2)
			print(pctcost_node_delta),
			print("node cost"),
			print(cost_at_node[parent]),
			print("child cost"),
			print(cost_children[parent]),
			print("node delta cost"),
			print(round(float(cost_at_node[parent])-float(cost_children[parent]),2)),
			print("node %"),
			print(pctcost_node)
			print(buffer[parent+1])
                	if  re.search(r"[\n\r]  *Filter",buffer[parent+1]):
                        	print("Filter")
				if pctcost_node_delta > 10.0 :
					print("missing index")
		parent+=1;

main()
