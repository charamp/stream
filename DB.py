import MySQLdb

def updateStart(position, customer, service_type, time):

	list_position = [""]*6
	split_position = position.split(" ")
	for i in xrange(6):
		if i < len(split_position):
			list_position[i] = split_position[i]
		else:
			list_position[i] = ""
	node,rack,card,port,s1,s2 = list_position

	db = MySQLdb.connect(host='localhost',
					user='root',
					passwd='1q2w3e4r',
					db='Alarm')

	cur = db.cursor()
	try:
		if len(split_position) == 6:
			cur.execute("""update alarms set result=%s where node=%s and rack=%s and card=%s and port=%s and s1=%s and s2=%s and service_type=%s and result=%s 
				order by time_updated desc""",
				(1, node, rack, card, port ,s1, s2, service_type, 0))
		elif len(split_position) == 5:
			cur.execute("""update alarms set result=%s where node=%s and rack=%s and card=%s and port=%s and s1=%s and service_type=%s and result=%s 
				order by time_updated desc""",
				(1, node, rack, card, port ,s1, service_type, 0))
		elif len(split_position) == 4:
			cur.execute("""update alarms set result=%s where node=%s and rack=%s and card=%s and port=%s and service_type=%s and result=%s 
				order by time_updated desc""",
				(1, node, rack, card, port, service_type, 0))
		elif len(split_position) == 3:
			cur.execute("""update alarms set result=%s where node=%s and rack=%s and card=%s and service_type=%s and result=%s 
				order by time_updated desc""",
				(1, node, rack, card, service_type, 0))
		elif len(split_position) == 2:
			cur.execute("""update alarms set result=%s where node=%s and rack=%s and service_type=%s and result=%s 
				order by time_updated desc""",
				(1, node, rack, service_type, 0))
		elif len(split_position) == 1:
			cur.execute("""update alarms set result=%s where node=%s and service_type=%s and result=%s 
				order by time_updated desc""",
				(1, node, service_type, 0))

		db.commit()
		#print "[MESSAGE] : Update (position = "+str(position)+", service_type = "+str(service_type)+", result = 1)"
	except:
		db.rollback()

	db.close()

def writeAlarm(position, customer, service_type, time):

	list_position = [""]*6
	split_position = position.split(" ")
	for i in xrange(6):
		if i < len(split_position):
			list_position[i] = split_position[i]
		else:
			list_position[i] = ""
	node,rack,card,port,s1,s2 = list_position

	db = MySQLdb.connect(host='localhost',
					user='root',
					passwd='1q2w3e4r',
					db='Alarm')

	cur = db.cursor()
	try:
		cur.execute("""select alarm_id from alarms where node=%s and rack=%s and card=%s and port=%s and s1=%s and s2=%s and service_type=%s and result=%s 
			order by time_updated desc limit 1""", 
			(node, rack, card, port, s1, s2, service_type, 0))

		if len(cur.fetchall()) != 0:
			cur.execute("""update alarms set time_updated=%s where node=%s and rack=%s and card=%s and port=%s and s1=%s and s2=%s and service_type=%s and result=%s 
				order by time_updated desc limit 1""",
				(time, node, rack, card, port, s1, s2, service_type, 0))
			db.commit()
			cur = db.cursor()
			cur.execute("""select alarm_id from alarms where node=%s and rack=%s and card=%s and port=%s and s1=%s and s2=%s and service_type=%s and result=%s 
				order by time_updated desc limit 1""", 
				(node, rack, card, port, s1, s2, service_type, 0))
			this_alarm_id = cur.fetchall()[0][0]
			cur.execute("""select cust_id from alarm_custs where id=%s""", (this_alarm_id))
			list_cust_id = []
			for record in cur.fetchall():
				list_cust_id.append(record[1])
			for cust in customer:
				if not cust[1] in list_cust_id:
					cur.execute("""insert into alarm_custs (cust_id, alarm_id, time_updated) values (%s, %s, %s)""", (cust[1], this_alarm_id, time))
			db.commit()
			#print "[MESSAGE] : Insert (position = "+str(position)+", service_type = "+str(service_type)+", result = 0)"
		else:
			cur.execute("""insert into alarms (node, rack, card, port, s1, s2, service_type, time_updated, result) 
				values (%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
				(node, rack, card, port, s1, s2, service_type, time, 0))
			db.commit()

			cur = db.cursor()
			cur.execute("""select alarm_id from alarms where node=%s and rack=%s and card=%s and port=%s and s1=%s and s2=%s and service_type=%s and result=%s 
				order by time_updated desc limit 1""",
				(node, rack, card, port, s1, s2, service_type, 0))
			this_alarm_id = cur.fetchall()[0][0]
			for cust in customer:
				cur.execute("""insert into alarm_custs (cust_id, alarm_id, time_updated) values (%s, %s, %s)""", (cust[1], this_alarm_id, time))
			db.commit()
			#print "[MESSAGE] : Insert (position = "+str(position)+", service_type = "+str(service_type)+", result = 0)"
	except:
		db.rollback()

	db.close()

def processDB(olt_alarm, dslam_alarm):
	list_position = []
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
	