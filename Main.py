import time, os
from collections import defaultdict
import MySQLdb
from DB import *

buffers = ""
where = 0
list_splitter = {}
list_splitter2 = {}

def resetBuffer():
	global buffers
	buffers = ""

def groupBy(all_packet, list_of_key):
	group = {}
	group = defaultdict(lambda: [], group)
	group_ans = {}
	group_ans = defaultdict(lambda: [], group_ans)
	number = len(list_of_key[0].split(" "))

	for packet in all_packet:
		if number == 6:
			key = packet[3]+" "+packet[4]+" "+packet[5]+" "+packet[6]+" "+list_splitter[packet[1]]+" "+list_splitter2[packet[1]]
			if key in list_of_key:
				group[key].append(packet)
		elif number == 5:
			key = packet[3]+" "+packet[4]+" "+packet[5]+" "+packet[6]+" "+list_splitter[packet[1]]
			if key in list_of_key:
				group[key].append(packet)
		else:
			key = " ".join([packet[i+3] for i in xrange(number)])

			if key in list_of_key:
				group[key].append(packet)

	for k,v in group.iteritems():
		if len(group[k]) > 1:
			group_ans[k] = group[k]

	return group_ans

def checkAlarmOlt(olt_packet):
	s_olt_packet = [[],[]]
	alarm = {'start':{}, 'stop':{}}

	for packet in olt_packet:
		if packet[8] == "start":
			s_olt_packet[0].append(packet)
		elif packet[8] == "stop":
			s_olt_packet[1].append(packet)

	for index in xrange(len(s_olt_packet)):

		key = []
		for packet in s_olt_packet[index]:
			k = packet[3]+" "+packet[4]+" "+packet[5]+" "+packet[6]+" "+list_splitter[packet[1]]+" "+list_splitter2[packet[1]]
			if not k in key:
				key.append(k)
		for i in xrange(5,0,-1):
			# 1 port = 1 splitter L1
			if i == 4: continue
			if len(key) == 0: break
			predict_alarm = groupBy(s_olt_packet[index], key)
			key = []
			count_key = {}
			count_key = defaultdict(lambda: [0,""], count_key)
			for k,v in predict_alarm.iteritems():
				#print " ".join([k.split(" ")[x] for x in xrange(i)])
				count_key[" ".join([k.split(" ")[x] for x in xrange(i)])][0] += 1
				count_key[" ".join([k.split(" ")[x] for x in xrange(i)])][1] = k
			for k,v in count_key.iteritems():
				if v[0] > 1:
					key.append(k)
					#print k
				elif v[0] == 1:
					if index == 0:
						alarm["start"][v[1]] = predict_alarm[v[1]]
					elif index == 1:
						alarm["stop"][v[1]] = predict_alarm[v[1]]
						
			if i == 1 and len(key) != 0:
				if index == 0:
					#print groupBy(s_olt_packet[index], key)
					alarm["start"].update(groupBy(s_olt_packet[index], key))
				elif index == 1:
					pass
					alarm["stop"].update(groupBy(s_olt_packet[index], key))

	return alarm


def checkAlarmDslam(dslam_packet):
	s_dslam_packet = [[],[]]
	alarm = {'start':{}, 'stop':{}}

	for packet in dslam_packet:
		if packet[8] == "start":
			s_dslam_packet[0].append(packet)
		elif packet[8] == "stop":
			s_dslam_packet[1].append(packet)

	for index in xrange(len(s_dslam_packet)):

		key = []
		for packet in s_dslam_packet[index]:
			k = packet[3]+" "+packet[4]+" "+packet[5]+" "+packet[6]
			if not k in key:
				key.append(k)
		for i in xrange(3,0,-1):
			# 1 port = 1 splitter L1
			if len(key) == 0: break
			predict_alarm = groupBy(s_dslam_packet[index], key)
			key = []
			count_key = {}
			count_key = defaultdict(lambda: [0,""], count_key)
			for k,v in predict_alarm.iteritems():
				#print " ".join([k.split(" ")[x] for x in xrange(i)])
				count_key[" ".join([k.split(" ")[x] for x in xrange(i)])][0] += 1
				count_key[" ".join([k.split(" ")[x] for x in xrange(i)])][1] = k
			for k,v in count_key.iteritems():
				if v[0] > 1:
					key.append(k)
					#print k
				elif v[0] == 1:
					if index == 0:
						alarm["start"][v[1]] = predict_alarm[v[1]]
					elif index == 1:
						alarm["stop"][v[1]] = predict_alarm[v[1]]
						
			if i == 1 and len(key) != 0:
				if index == 0:
					#print groupBy(s_dslam_packet[index], key)
					alarm["start"].update(groupBy(s_dslam_packet[index], key))
				elif index == 1:
					pass
					alarm["stop"].update(groupBy(s_dslam_packet[index], key))

	return alarm

def processLog():
	global buffers

	packet_all = buffers.split("\n")
	packet_all = filter(lambda s: s if len(s)>0 else None, packet_all)
	packet_all = map(lambda s: s.split(","), packet_all)

	resetBuffer()

	dslam_packet = []
	olt_packet = []

	for packet in packet_all:
		if packet[2] == "dslam":
			dslam_packet.append(packet)
		elif packet[2] == "olt":
			olt_packet.append(packet)

	#processDB(checkAlarmOlt(olt_packet), checkAlarmDslam(dslam_packet))


def readLogRadius():

	global buffers
	global where

	filename = 'radius.log'
	file = open(filename,'r')

	while 1:
		where = file.tell()
		line = file.readline()
		buffers += line
		#print line
		if not line:
			file.seek(where)
			print 'wait'
			processLog()
			time.sleep(5)

def readLogSplitter():

	global list_splitter

	f = open('splitter.in','r')
	lists = f.read().split("\n")
	for l in lists:
		if l == "": continue
		cust_id,splitter_id,splitter_id2 = l.split(" ")
		list_splitter[cust_id] = splitter_id
		list_splitter2[cust_id] = splitter_id2


def Main():
	readLogSplitter()
	readLogRadius()


Main()