import MySQLdb

def updateStart(position, customer, service_type, time):
	db = MySQLdb.connect(host='localhost',
					user='root',
					passwd='1q2w3e4r',
					db='Alarm')

	cur = db.cursor()
	try:
		cur.execute("""update alarms set result=%s where position=%s and service_type=%s and result=%s order by time_updated desc limit 1""", (1, position, service_type, 0))
		db.commit()
		print "[MESSAGE] : Update (position = "+str(position)+", service_type = "+str(service_type)+", result = 1)"
	except:
		db.rollback()

	db.close()

def writeAlarm(position, customer, service_type, time):
	db = MySQLdb.connect(host='localhost',
					user='root',
					passwd='1q2w3e4r',
					db='Alarm')

	cur = db.cursor()
	try:
		cur.execute("""select alarm_id from alarms where position=%s and service_type=%s and result=%s order by time_updated desc limit 1""", (position, service_type, 0))
		if len(cur.fetchall()) != 0:
			cur.execute("""update alarms set time_updated=%s where position=%s and service_type=%s and result=%s order by time_updated desc limit 1""", (time, position, service_type, 0))
			db.commit()
			cur = db.cursor()
			cur.execute("""select alarm_id from alarms where position=%s and service_type=%s and result=%s order by time_updated desc limit 1""", (position, service_type, 0))
			this_alarm_id = cur.fetchall()[0][0]
			cur.execute("""select cust_id from alarm_custs where id=%s""", (this_alarm_id))
			list_cust_id = []
			for record in cur.fetchall():
				list_cust_id.append(record[1])
			for cust in customer:
				if not cust[1] in list_cust_id:
					cur.execute("""insert into alarm_custs (cust_id, alarm_id, time_updated) valurs (%s, %s, %s)""", cust[1], this_alarm_id, time)
			db.commit()
			print "[MESSAGE] : Insert (position = "+str(position)+", service_type = "+str(service_type)+", result = 0)"
		else:
			cur.execute("""insert into alarms (position, service_type, time_updated, result) values (%s, %s, %s, %s)""", (position, service_type, time, 0))
			db.commit()
			cur = db.cursor()
			cur.execute("""select alarm_id from alarms where position=%s and service_type=%s and result=%s order by time_updated desc limit 1""", (position, service_type, 0))
			this_alarm_id = cur.fetchall()[0][0]
			for cust in customer:
				cur.execute("""insert into alarm_custs (cust_id, alarm_id, time_updated) values (%s, %s, %s)""", (cust[1], this_alarm_id, time))
			db.commit()
			print "[MESSAGE] : Insert (position = "+str(position)+", service_type = "+str(service_type)+", result = 0)"
	except:
		db.rollback()

	db.close()

def processDB(olt_alarm, dslam_alarm):
	for packet_type, alarm in olt_alarm.iteritems():
		if packet_type == "start":
			for position, customer in alarm.iteritems():
				updateStart(position, customer, 'olt', customer[0][0])
		elif packet_type == "stop":
			for position, customer in alarm.iteritems():
				writeAlarm(position, customer, 'olt', customer[0][0])
	
	for packet_type, alarm in dslam_alarm.iteritems():
		if packet_type == "start":
			for position, customer in alarm.iteritems():
				updateStart(position, customer, 'dslam', customer[0][0])
		elif packet_type == "stop":
			for position, customer in alarm.iteritems():
				writeAlarm(position, customer, 'dslam', customer[0][0])
	