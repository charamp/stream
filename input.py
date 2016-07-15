import re

pre = ['O', 'F', 'D']

f = open('20160714_0700.act', 'r')
data = f.read().split("\n")
for x in data:
	if x == '': continue
	tmp = x.split(",")
	if tmp[3][1:-1] == "Stop" or tmp[3][1:-1] == "Start":

		match = ""
		for char in pre:
			
			m = re.search(r''+char+'\w*_\w*_\w*_\w*\s.*:', x)
			if m != None:
				match = m.group()[0:-1]

		if match == "": continue

		position = match.split()
		if len(position) == 3: continue
		if len(tmp[6][1:-1]) > 10: continue
		time = tmp[0][1:-1]+" "+tmp[1][1:-1]
		cust_id = tmp[6][1:-1]
		service_type = "dslam" if position[0][0] == "D" else "olt"
		node = position[0]
		rack,card,port = position[1].split("/")
		onu_id = ""
		packet_type = tmp[3][1:-1] 
		status = 0
		if packet_type == 'Stop': status = 2
		print str(time)+","+str(cust_id)+","+str(service_type)+","+str(node)+","+str(rack)+","+str(card)+","+str(port)+","+str(onu_id)+","+str(packet_type)+","+str(status)



		#print detail[0][i:len(detail[0]-1)]