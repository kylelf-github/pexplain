

def main (): 
	# read file
	file = open("plans/01CD.p","r")
	lines = file.readlines()
	file.close()

	# look for patterns
	buffer=""
	printbuf=0;
	for line in lines:
		# look for nodes
		depth = line.find ("  ->")/6 
		# depth equals -1, even though divided by 6
		# print("depth ", depth)
		costs = line.find ("cost")
		if costs != -1 & depth == -1 :
			total_cost=line.split("..")[1].split()[0]
			print("first cost ", total_cost)
			ccost=total_cost
		# if "->" 
		if depth != -1:
			# split after first (
			operation=line.split("(")[0]

			pcost=ccost

			# split after first .., take right, split on blanks, take first string
			ccost=line.split("..")[1].split()[0]

			# percentage cost
			pctcost=round(100*float(ccost)/float(total_cost),2)
			if pctcost > 10.0 :
				print(depth,ccost, round(100*float(ccost)/float(total_cost),2))
				#print(depth,operation,ccost, round(100*float(ccost)/float(total_cost),2))
				#print(line,)
				#print(buffer)
				#printbuf=1;
				#if printbuf == 1:
				#print(" -----vvvvvv--------- " )
				print(buffer)
				#printbuf=0;
				buffer=""
				#print(" -----^^^^^^--------- " )
		buffer=buffer + line
	# display results

main()
