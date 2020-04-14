
from array import array

def main (): 
	# read file
	file = open("plans/01CD.p","r")
	lines = file.readlines()
	file.close()

	# look for patterns
	buffer=""
	buffers=0
	printbuf=0;
        costdict={}
        nodes={}
	for line in lines:
		# look for nodes
		# depth equals -1, even though divided by 6
		depth = line.find ("  ->")/6 
		
		#  extract cost from line
		costs = line.find ("cost")
		if costs != -1 & depth == -1 :
			total_cost=line.split("..")[1].split()[0]
			print("first cost ", total_cost)
			ccost=total_cost

		# if "->" 
		if depth != -1:
			buffers=buffers+1
			# split after first (
			operation=line.split("(")[0]

			prevcost=ccost

			# split after first .., take right, split on blanks, take first string
			ccost=line.split("..")[1].split()[0]
			costdict[buffers]=ccost
			print("costdict[",buffers,"]")

			if buffers > 1:
				print("costdelta=",costdict[buffers-1],"-",ccost)
				costdelta=float(costdict[buffers-1])-float(ccost)
				print("costdelta ", round(costdelta,2));

			# percentage cost
			pctcost=round(100*float(ccost)/float(total_cost),2)
			if pctcost > 10.0 :
				print(depth,ccost, round(100*float(ccost)/float(total_cost),2))
				print(buffer)
				nodes[buffers]=buffer
				maxbuffer=buffers
				print("nodes ",maxbuffer)
				buffer=""
		buffer=buffer + line

        start=1
	while start <= maxbuffer:
		if start < maxbuffer:
			nodecost=float(costdict[start])-float(costdict[start+1])
			print("nodecost ",round(nodecost,2))
		else:
			print("nodecost ",costdict[start])
		print nodes[start]
		start += 1;

main()
