import MySQLdb

def updateStart(position, customer, service_type):
	db = MySQLdb.connect(host='localhost',
					user='root',
					passwd='1q2w3e4r',
					db='Alarm')

	cur = db.cursor()
	try:
		cur.execute("""update Alarm set result=%s where position=%s and service_type=%s and result='0'""", (1, position, service_type))
		db.commit()
		print "[MESSAGE] : Update (position = "+str(position)+", service_type = "+str(service_type)+", result = 1)"
	except:
		db.rollback()

	db.close()

def writeAlarm(position, customer, service_type):
	db = MySQLdb.connect(host='localhost',
					user='root',
					passwd='1q2w3e4r',
					db='Alarm')

	cur = db.cursor()
	try:
		cur.execute("""insert into Alarm (position, service_type, result) values (%s, %s, %s)""", (position, service_type, 0))
		db.commit()
		cur = db.cursor()
		cur.execute("""select alarm_id from Alarm where position=%s and service_type=%s and result=%s order by time desc limit 1""", (position, service_type, 0))
		this_alarm_id = cur.fetchall()[0][0]
		for cust in customer:
			cur.execute("""insert into Alarm_Cust (cust_id, alarm_id) values (%s, %s)""", (cust[1], this_alarm_id))
		db.commit()
		print "[MESSAGE] : Insert (position = "+str(position)+", service_type = "+str(service_type)+", result = 0)"
	except:
		db.rollback()

	db.close()

def processDB(olt_alarm, dslam_alarm):
	for packet_type, alarm in olt_alarm.iteritems():
		if packet_type == "start":
			for position, customer in alarm.iteritems():
				updateStart(position, customer, 'olt')
		elif packet_type == "stop":
			for position, customer in alarm.iteritems():
				writeAlarm(position, customer, 'olt')
	
	for packet_type, alarm in dslam_alarm.iteritems():
		if packet_type == "start":
			for position, customer in alarm.iteritems():
				updateStart(position, customer, 'dslam')
		elif packet_type == "stop":
			for position, customer in alarm.iteritems():
				writeAlarm(position, customer, 'dslam')
	