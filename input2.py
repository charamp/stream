import re
from collections import defaultdict
import time, os
import datetime

buffers = ""
prefix = ['O', 'D']
current_log_name = ""
isNewLog = True

def convertStringToDateTime(dt):
	date,time = dt.split(" ")
	mo,d,y = date.split("/")
	h,mi,s = time.split(":")

	return datetime.datetime(int(y), int(mo), int(d), int(h), int(mi), int(s), 0)

def checkTimeNow():
	now = datetime.datetime.now()
	y = now.year
	m = now.month
	d = now.day
	return False

def generateLogName(time):
	m = "0"+str(time.month) if time.month < 10 else str(time.month)
	d = "0"+str(time.day) if time.day < 10 else str(time.day)
	log_name = str(time.year)+m+d+"_"+str(time.hour)+"00.act"
	return log_name

def logInputReadjustment(data):
	result = []
	raw_log = data.split("\n")
	for line in raw_log:
		if line == "": continue
		column = line.split(",")

		if column[3][1:-1] == "Stop" or column[3][1:-1] == "Start":

			if len(str(column[21][1:-1])) > 2:
				if column[22][1:-1] != "2": continue
			else:
				if column[21][1:-1] != "2": continue

			match = ""
			for character in prefix:
				m = re.search(r''+character+'\w*_\w*_\w*_\w*\s.*:', line)
				if m != None:
					match = m.group()[0:-1]	
			if match == "": continue
			position = match.split()
			if len(column[6][1:-1]) > 10: continue

			time = convertStringToDateTime(column[0][1:-1]+" "+column[1][1:-1])
			cust_id = column[6][1:-1]
			service_type = "dslam" if position[0][0] == "D" else "olt"
			node = position[0]
			rack,card,port = position[1].split("/")
			onu_id = ""
			packet_type = column[3][1:-1]
			status = 0
			if packet_type == "Stop": status = 2
	
			result.append([time,str(cust_id),str(service_type),str(node),str(rack),str(card),str(port),str(onu_id),str(packet_type),str(status)])

	return result

def readLogSplitter():
	splitter_list = {}
	splitter_list = defaultdict(lambda: ["", ""], splitter_list)
	f = open('OLT_SPLITTER_DETAIL_DATA_TABLE.csv', 'r')
	raw_splitter = f.read().split("\n")
	for line in raw_splitter:
		if line == "": continue
		column = line.split(",")
		match = ""
		m = re.search(r'P[0-9][0-9]_SP.*"', column[1])
		if m != None:
			match = m.group()[0:-1]
		if match == "": continue
		unit_name_splitter = match.split("_")
		splitter_list[column[3][1:-1]][0] = unit_name_splitter[0][1:len(unit_name_splitter[0])]
		splitter_list[column[3][1:-1]][1] = unit_name_splitter[2]
	return splitter_list

#print readLogSplitter()["8800093698"]
"""
for k,v in readLogSplitter().iteritems():
	if len(v[2]) != 1:
		print str(k)+"=>"+str(v)
"""
"""
def readLogRadius():

	global buffers
	global isNewLog

	while 1:
		if isNewLog:
			isNewLog = False
			#current_log_name = generateLogName(datetime.datetime.now())
			#print current_log_name
			f = open('20160714_0700.act','r')
			#f = open(current_log_name, 'r')
			all_line_first = f.read()
			buffers += all_line_first
		while 1:
			line = f.readline()
			buffers += line
			if not line:
				processLog(logInputReadjustment(buffers))
				buffers = ""
				if checkTimeNow():
					isNewLog = True
				print "wait"
				time.sleep(5)

readLogRadius()
"""


"""
file = open('20160714_0700.act','r')
read_first = file.read()
where = file.tell()
buffers += line
while 1:
	where = file.tell()
	line = file.readline()
	buffers += line
	if not line:
		file.seek(where)
		print 'wait'
		processLog()
		time.sleep(5)
"""