import MySQLdb
import datetime

db = MySQLdb.connect(host='localhost',
				user='root',
				passwd='1q2w3e4r',
				db='Alarm')

cur = db.cursor()
cur.execute("""insert into alarms (node, rack, card, port, s1, s2, service_type, time_updated, result) 
	values (%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
	(1,1,1,1,1,1,'dslam',datetime.datetime.now(),0))
db.commit()