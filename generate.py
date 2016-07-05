from random import randint

st = ['dslam', 'olt']
pt = ['start', 'stop']

time = 0
for i in xrange(10000):
	time += 0.00001
	cust_id = 880030000+randint(0,3000)
	service_type = st[randint(0,1)] #0 = dslam , 1 = olt
	node = randint(0,100)
	rack = randint(0,10)
	card = randint(0,10)
	port = randint	(0,5)
	onu_id = randint(0,200)
	packet_type = pt[randint(0,1)] #0 = start, 1 = stop
	status = 0 #0 = start
	if packet_type == 'stop':
		status = 2 #1 = user-request, 2 = loss-carries
	print str(time)+","+str(cust_id)+","+str(service_type)+","+str(node)+","+str(rack)+","+str(card)+","+str(port)+","+str(onu_id)+","+str(packet_type)+","+str(status)

