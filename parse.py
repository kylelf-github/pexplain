
#from array import array
import re
import sys

#def main (argv): 

def print_costs(cost_at_node,node,cost_children,total_cost):

	pctcost_node=round(100*float(cost_at_node[node])/float(total_cost),2)

	print("node delta %"),
	pctcost_node_delta=round(100*(float(cost_at_node[node])-(float(cost_children[node])))/float(total_cost),2)
	print(pctcost_node_delta),

	print("node cost"),
	print(cost_at_node[node]),

	print("child cost"),
	print(cost_children[node]),

	print("node delta cost"),
	print(round(float(cost_at_node[node])-float(cost_children[node]),2)),

	print("node %"),
	print(pctcost_node)

def node_costs():
	i=1

def main (): 
	debug=0
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
        file = open(filename,"r")
	lines = file.readlines()
	file.close()

        node_cnt=0
        cost_at_node={}
        depth_at_node={}
        cost_children={}
        buffer={}
	buffer_child={}
	# noden_child, don't really need this, adding for debugging, it's the node # of a direct child of parent
	noden_child={}
	children={}
	temp_buffer=""

	# look for patterns
	for line in lines:
		#print("line: "),
		#print(line)

		# look for nodes
		# depth equals -1, even though divided by 6
		depth = line.find ("  ->")/6 
		#print("depth 1",depth)
		
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

			# get indent spaces
			indents=line.split("->")[0]

			# get cost
			# split after first .., take right, split on blanks, take first string
			cost=line.split("..")[1].split()[0]

        		node_cnt+=1

        		cost_at_node[node_cnt]=cost
        		depth_at_node[node_cnt]=depth

		temp_buffer=temp_buffer+line
	buffer[node_cnt]=temp_buffer

	# loop through nodes
	# calculate costs of nodes direct children
	parent=1
	while parent <= node_cnt:
		cost_children[parent]=0
		child=parent+1
		children[parent]=0
		# how many children (not grand children does node have?)
		nchildren=0
		if debug > 1:
			print ("parent "),
			print (buffer[parent])
		while child <= node_cnt:
			# if current child is same depth as first child of parent, add the cost
			if debug > 3:
				print ("parent depth "),
				print (parent),
				print ("child "),
				print (child),
				print ("depth"),
				print (depth_at_node[child]),
				print (buffer[child])

			if int(depth_at_node[child]) == int(depth_at_node[parent])+1:
				cost_children[parent]+=float(cost_at_node[child])
				# get buffers for direct children
				buffer_child[parent,nchildren]=buffer[child]
				noden_child[parent,nchildren]=child
				children[parent]+=1
				nchildren+=1
			# if the child is at the parents depth, exit out of loop as we are no longer looking at children
			# if we don't find any children at parents depth, we have to go to the very end of file
			if depth_at_node[child] ==  depth_at_node[parent]:
				child=node_cnt
			child+=1
		parent+=1;


	# loop through nodes
	#  look for expensive Filters  ( >= 10% )
	#  look for expensive Hash Joins ( >= 10% )
	#  look for expensive Nested Loops ( >= 10% )
	parent=1
	while parent < node_cnt-1:
		pctcost_node=round(100*float(cost_at_node[parent])/float(total_cost),2)
		if pctcost_node >= 10.0 :
			print("---------") 
			print("parent node"), 
			print(parent), 
			print("depth at parent "), 
			print(depth_at_node[parent])
			cdepth=0
			while cdepth <= depth_at_node[parent]:
				print("    "),
				cdepth+=1
			print(">>"),
			pctcost_node_delta=round(100*(float(cost_at_node[parent])-(float(cost_children[parent])))/float(total_cost),2)
			# cost_at_node is a dictonary
			# cost_children is a dictonary
			# cost_children is a dictonary
			print_costs(cost_at_node,parent,cost_children,total_cost)
			print(buffer[parent])
                	if  re.search(r"[\n\r]  *Filter",buffer[parent]):
                        	print("Filter")
				if pctcost_node_delta > 10.0 :
					print("missing index")
                	# there are other types of Hash but not sure these rules apply, I don't see them applying for no
                	#if  re.search(r"[\n\r]*  *->  Hash",buffer[parent]):
                	if  re.search(r"[\n\r]*  *->  Hash Join",buffer[parent]):
                		i=0
                		print("#children :"),
                		print(children[parent])
				print("- vvvvv --")
                		while i < children[parent]:
					print("parent node "),
					print(parent),
					print("child # "),
					print(i)
					child_node=noden_child[parent,i]
					print_costs(cost_at_node,child_node,cost_children,total_cost)
					print(buffer_child[parent,i])
					i+=1
				print("- ^^^^^ --")
				tempcost=0
			        cost_node_A=float(cost_at_node[parent+1])-(float(cost_children[parent+1]))
			        cost_node_B1=float(cost_at_node[parent+2])-(float(cost_children[parent+2]))
			        cost_node_B2=float(cost_at_node[parent+3])-(float(cost_children[parent+3]))
			        pctcost_node_B=round(100*(cost_node_B1+cost_node_B2)/float(total_cost),2)
			        pctcost_node_A=round(100*(cost_node_A)/float(total_cost),2)
                		#if  re.search(r"[\n\r]*  *->  Seq Scan",buffer_child[parent,0]):
                		#if  re.search(r"[\n\r]*  *->  Seq Scan",buffer_child[parent,0]):
				if  re.search(r"[\n\r]*  *->  Seq Scan",buffer[parent+1]):
					if pctcost_node_A >= 10.0  and pctcost_node_A >= pctcost_node_B:
						print("******************** Hash Join missing Join index 1111")
						tempcost = pctcost_node_delta
				#noden_child[parent,nchildren]=child
                		#if  re.search(r"[\n\r]*  *->  Seq Scan",buffer[parent+3]) :
				childn=noden_child[parent,1]
                		if  re.search(r"[\n\r]*  *->  Seq Scan",buffer[childn]) :
					print("******************** Hash Join missing second Join index ")
					print_costs(cost_at_node,parent,cost_children,total_cost)
					print(buffer[parent+3])
					#if pctcost_node_delta >= 10.0 and pctcost_node_delta > tempcost:
					if pctcost_node_B >= 10.0 and pctcost_node_B >= pctcost_node_A:
						print("******************** Hash Join missing Join index 222")
						print(buffer[parent+3])
                	if  re.search(r"[\n\r]*  *->  Nested Loop",buffer[parent]):
                		i=0
                		print("#children :"),
                		print(children[parent])
				print("- vvvvv --")
                		while i < children[parent]:
					print("parent node "),
					print(parent),
					print("child # "),
					print(i)
					child_node=noden_child[parent,i]
					print_costs(cost_at_node,child_node,cost_children,total_cost)
					print(buffer_child[parent,i])
					i+=1
				print("- ^^^^^ --")
				tempcost=0
			        cost_node_A=float(cost_at_node[parent+1])-(float(cost_children[parent+1]))
				if cost_children.has_key(parent+2):
			        	cost_node_B1=float(cost_at_node[parent+2])-(float(cost_children[parent+2]))
				else:
			        	cost_node_B1=0
				if cost_at_node.has_key(parent+3):
				        cost_node_B2=float(cost_at_node[parent+3])-(float(cost_children[parent+3]))
				else:
				        cost_node_B2=0
			        pctcost_node_B=round(100*(cost_node_B1+cost_node_B2)/float(total_cost),2)
			        pctcost_node_A=round(100*(cost_node_A)/float(total_cost),2)
                		#if  re.search(r"[\n\r]*  *->  Seq Scan",buffer[parent+1]):
                		if  re.search(r"[\n\r]*  *->  Seq Scan",buffer_child[parent,0]):
					if pctcost_node_A >= 10.0  and pctcost_node_A >= pctcost_node_B:
						print("******************** Nested Loops missing Join index 1111")
						tempcost = pctcost_node_delta
                		if  re.search(r"[\n\r]*  *->  Seq Scan",buffer_child[parent,1]) :
					print("******************** Nested Loops missing second Join index ")
					print_costs(cost_at_node,parent,cost_children,total_cost)
					print(buffer[parent+2])
					#if pctcost_node_delta >= 10.0 and pctcost_node_delta > tempcost:
					# in nested, loops, even if second node is cheap, if total nested looops is expenisive
					#  means that second node is excuted alot, so is we can optimize it we should
					if pctcost_node_B >= 0.0 and pctcost_node_B >= pctcost_node_A:
						print("******************** Nested Loops missing Join index 222")
						#print(buffer[parent+2])
						print(buffer_child[parent,1])

		parent+=1;

main()
