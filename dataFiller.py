import sqlite3 as sqll
import random
import string
import time
import os
import sys
import requests

'''
TUNING PARAMETERS AT EBOX SIDE:
	Inter-commit time
	How often journal-files are being written

'''

# GLOBALS ########################################
DBPATH = 'ebox.db'
EBOXID = ''

lstUid = []
lstAppId = []
lstDevId = []


# journalising lists
# TODO: How to journalise only after a commit
jrnOperations = []

# RANDOM ID GENERATORS 
def generateUid():
	return 'U' + str( int(random.uniform(10000,99999)) )

def generateAppId():
	return 'A' + str( int(random.uniform(10000,99999)) )

def generateDevId():
	return random.choice(['DT', 'DP']) + str( int(random.uniform(10000,99999)) )	
	

# CLEAR ALL TABLES IN DB
def clearAllTables():
	#TODO HANDLE JOURNALISING HERE
	try:
		con = sqll.connect(DBPATH)
		cur = con.cursor() 
		cur.execute("DELETE FROM apps");
		cur.execute("DELETE FROM uids");
		cur.execute("DELETE FROM uidToAppUsage");
		cur.execute("DELETE FROM uidToDevices");
		cur.execute("DELETE FROM sqlite_sequence WHERE name='uidToDevices'")
	except sqll.Error, e:
		if con:
			con.rollback()	
		print "SQLite Error %s:" % e.args[0]
		return
	finally:
		if con:
			con.commit()
			con.close() 


# INSERT <COUNT> NUMBER OF UIDS
def genInsertUids(count):
	try:
		con = sqll.connect(DBPATH)
		cur = con.cursor()   

		for i in range(count):
			#new Uid
			newUid = generateUid()
			while newUid in lstUid:
				newUid = generateUid()
			
			#new DevId
			newDevId = generateDevId()
			while newDevId in lstDevId:
				newDevId = generateDevId()

			#add to global list
			lstUid.append(newUid)
			lstDevId.append(newDevId)

			#insert into Uid table
			cur.execute( "INSERT INTO uids VALUES ('%s')" %(newUid) )
			jrnOperations.append("INS|uids|('%s')" %(newUid))

			#check if the pair exists before inserting (uid, dev_id), 
			tmpQuery = cur.execute("SELECT count(*) from uidToDevices where id ='%s' AND device_id ='%s'" %(newUid, newDevId))
			if tmpQuery.fetchall()[0][0] == 0:
				cur.execute( "INSERT INTO uidToDevices VALUES (NULL, '%s', '%s')" %(newUid, newDevId) )
				jrnOperations.append("INS|uidToDevices|(NULL, '%s', '%s')" %(newUid, newDevId))

		#write out		
		con.commit()
	
	except sqll.Error, e:
		if con:
			con.rollback()	
		print "SQLite Error in genInsertUids! %s:" % e.args[0]
		return
		
	finally:
		if con:
			con.commit()
			con.close() 


# INSERT <COUNT> NUMBER OF APP IDS
def genInsertAppIds(count):
	try:
		con = sqll.connect(DBPATH)
		cur = con.cursor()   

		for i in range(count):
			#new appId business
			newAppId = generateAppId()
			while newAppId in lstAppId:
				newAppId = generateAppId()

			lstAppId.append(newAppId)
			cur.execute( "INSERT INTO apps VALUES ('%s')" %(newAppId) )
			jrnOperations.append("INS|apps|('%s')" %(newAppId))
		con.commit()
	
	except sqll.Error, e:
		if con:
			con.rollback()	
		print "SQLite Error in genInsertAppIds! %s:" % e.args[0]
		return
		
	finally:
		if con:
			con.commit()
			con.close() 


# GENERATE APP USAGE
def genInsertAppUsage(count, commits = 1):
	commitCheckNumber = count/commits

	print "About to insert %s app usage data points, committing every %s" %(count, count/commits)

	try:
		con = sqll.connect(DBPATH)
		cur = con.cursor() 

		### TODO!! get correct Device-Ids, etc from table
		for i in range(count):
			uid = lstUid[int(random.uniform(0,len(lstUid)))]
			appId = lstAppId[int(random.uniform(0,len(lstAppId)))]
			usageStamp = time.strftime('%Y-%m-%d %H:%M:%S')
			# Random usage durations
			duration = "%s:%s:%s" %( int(random.uniform(0,10)), int(random.uniform(0,60)), int(random.uniform(0,60)) )
			tf = random.choice('TF')
			appSign = '/appsigns/' + appId

			#insert into DB
			cur.execute( "INSERT INTO uidToAppUsage VALUES (NULL, '%s', '%s', datetime('%s'), time('%s'), '%s', '%s')" %(uid, appId, usageStamp, duration, tf, appSign) )
			jrnOperations.append( "INS|uidToAppUsage|(NULL, '%s', '%s', datetime('%s'), time('%s'), '%s', '%s')" %(uid, appId, usageStamp, duration, tf, appSign) )

			if (i % commitCheckNumber) == 0:
				print 'Committing...'
				con.commit()

	except sqll.Error, e:
		if con:
			con.rollback()	
		print "SQLite Error in genInsertAppUsage! %s:" % e.args[0]
		return
	
	finally:
		if con:
			con.commit()
			con.close() 

# GENERATE APP USAGE DATA.
# NON-MODULO VERSION OF ABOVE FUNCTION: MARGINALLY FASTER
def genInsertAppUsageFast(count, commits = 1):
	try:
		con = sqll.connect(DBPATH)
		cur = con.cursor() 

		### TODO!! what if commits is not a factor of count? Find closest factor.
		print "About to insert %s app usage data points, committing every %s" %(count, count/commits)
		for j in range(commits):
			for i in range(count/commits):
				uid = lstUid[int(random.uniform(0,len(lstUid)))]
				appId = lstAppId[int(random.uniform(0,len(lstAppId)))]
				usageStamp = time.strftime('%Y-%m-%d %H:%M:%S')
				# Random usage durations
				duration = "%s:%s:%s" %( int(random.uniform(0,10)), int(random.uniform(0,60)), int(random.uniform(0,60)) )
				tf = random.choice('TF')
				appSign = '/appsigns/' + appId

				#insert into DB
				cur.execute( "INSERT INTO uidToAppUsage VALUES (NULL, '%s', '%s', datetime('%s'), time('%s'), '%s', '%s')" %(uid, appId, usageStamp, duration, tf, appSign) )
				jrnOperations.append( "INS|uidToAppUsage|(NULL, '%s', '%s', datetime('%s'), time('%s'), '%s', '%s')" %(uid, appId, usageStamp, duration, tf, appSign) )
			con.commit()
			print 'Committing..'

	except sqll.Error, e:
		if con:
			con.rollback()	
		print "SQLite Error in genInsertAppUsage! %s:" % e.args[0]
		return
	
	finally:
		if con:
			con.commit()
			con.close() 

# WRITE JOURNAL ENTRIES TO FILE
def writeJrnFiles():
	global jrnOperations
	with open( './journaldump/' + EBOXID + ".log", 'a') as fileInserts:
		for line in jrnOperations:
			fileInserts.write(line + '\n')
		jrnOperations = []

# REMOVE JOURNAL FILES
def delJournalFiles(eboxId):
	try:
		os.remove( './journaldump/' + eboxId + '.log')
	except OSError:
		pass
	os.system( 'touch ./journaldump/%s.log' %eboxId )


# REMOVE ENTRIES
def deleteFromTables(lstParams):
	con = sqll.connect(DBPATH)
	cur = con.cursor() 

	for (tablename, wherefield) in lstParams:
		try:
			cur.execute ("DELETE from %s WHERE %s" %(tablename,wherefield))
			jrnOperations.append("DEL|%s|%s" %(tablename, wherefield))
		except sqll.Error,e:
			print 'SQLite Error in deleteFromTables()!:', e.args[0]

	con.commit()

# MAKE HTTP REQUEST
def queryServer(url, apikey, params):
	#add API key
	params['apikey'] = apikey
	# make API call
	reqServer = requests.get(url, params=params)
	if reqServer.status_code == 200:
		jsnResponse = reqServer.json()
		return jsnResponse
	else:
		print 'HTTP not OK: Returned', reqServer.status_code
		return


# THE WORKS
def test1():
	global EBOXID
	global DBPATH
	global lstAppId

	for ebox in ['E12019', 'E20010', 'E12001', 'E40063']:
		EBOXID = ebox
		DBPATH = ebox + '.db'
		lstAppId = []
		delJournalFiles(ebox)
		clearAllTables()
		print 'Inserting UIDs...'
		genInsertUids(10)
		print 'Inserting AppIDs...'
		genInsertAppIds(100)
		print 'Inserting app usage stats...'
		genInsertAppUsageFast(1000)

		print 'deleting a few apps'
		lstDelApps = []
		for i in range(5):
			lstDelApps.append( ('apps', "id = '%s'" %lstAppId[i]) )
			# print lstAppId[i]
		deleteFromTables(lstDelApps)

		print 'Writing out to files...'
		writeJrnFiles()

def test2(uids, appids, usagepoints, commits):
	global EBOXID
	global DBPATH
	global lstAppId

	for ebox in ['E12019', 'E20010', 'E12001', 'E40063']:
		EBOXID = ebox
		DBPATH = ebox + '.db'
		print EBOXID
		# lstAppId = []
		delJournalFiles(ebox)
		clearAllTables()
		print 'Inserting UIDs...'
		genInsertUids(uids)
		print 'Inserting AppIDs...'
		genInsertAppIds(appids)
		print 'Inserting app usage stats...'
		genInsertAppUsage(usagepoints,commits)

		print 'deleting a few apps'
		lstDelApps = []
		for i in range(100):
			lstDelApps.append( ('apps', "id = '%s'" %lstAppId[i]) )
			# print lstAppId[i]
		deleteFromTables(lstDelApps)

		print 'Writing out to files...'
		writeJrnFiles()


if __name__ == '__main__':
	print sys.argv
	if len(sys.argv) > 1 and sys.argv[1] != '':
		uids = int(sys.argv[1].split(',')[0])
		appids = int(sys.argv[1].split(',')[1])
		usagepoints = int(sys.argv[1].split(',')[2])
		commits = int(sys.argv[1].split(',')[3])
		test2(uids, appids, usagepoints, commits)
	else:
		test1()


