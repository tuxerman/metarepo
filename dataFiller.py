import sqlite3 as sqll
import random
import string
import time

'''
TUNING PARAMETERS AT EBOX SIDE:
	Inter-commit time
	How often journal-files are being written

'''

# GLOBALS ########################################
DBPATH = 'ebox.db'
lstUid = []
lstAppId = []
lstDevId = []

# journalising lists
# TODO: How to journalise only after a commit
jrnInserts = []
jrnUpdates = []
jrnDeletes = []


# RANDOM ID GENERATORS 
def generateUid():
	return 'U' + str( int(random.uniform(1000,9999)) )

def generateAppId():
	return 'A' + str( int(random.uniform(1000,9999)) )

def generateDevId():
	return random.choice(['DT', 'DP']) + str( int(random.uniform(1000,9999)) )	
	

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
			jrnInserts.append("uids|('%s')" %(newUid))

			#check if the pair exists before inserting (uid, dev_id), 
			tmpQuery = cur.execute("SELECT count(*) from uidToDevices where id ='%s' AND device_id ='%s'" %(newUid, newDevId))
			if tmpQuery.fetchall()[0][0] == 0:
				cur.execute( "INSERT INTO uidToDevices VALUES (NULL, '%s', '%s')" %(newUid, newDevId) )
				jrnInserts.append("uidToDevices|(NULL, '%s', '%s')" %(newUid, newDevId))

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
			jrnInserts.append("apps|('%s')" %(newAppId))
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
			jrnInserts.append( "uidToAppUsage|(NULL, '%s', '%s', datetime('%s'), time('%s'), '%s', '%s')" %(uid, appId, usageStamp, duration, tf, appSign) )

			if (i % commitCheckNumber) == 0:
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

# GENERATE APP USAGE
# NON-MODULO VERSION OF ABOVE FUNCTION
def genInsertAppUsageFast(count, commits = 1):
	try:
		con = sqll.connect(DBPATH)
		cur = con.cursor() 

		### TODO!! what if commits is not a factor of count? Find closest factor.
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
				jrnInserts.append( "uidToAppUsage|(NULL, '%s', '%s', datetime('%s'), time('%s'), '%s', '%s')" %(uid, appId, usageStamp, duration, tf, appSign) )
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

# WRITE JOURNAL ENTRIES TO FILE
def writeJrnFiles():
	with open("inserts.log", 'a') as fileInserts:
		for line in jrnInserts:
			fileInserts.write(line + '\n')

	with open("updates.log", 'a') as fileUpdates:
		for line in jrnUpdates:
			fileUpdates.write(line + '\n')

	with open("deletes.log", 'a') as fileDeletes:
		for line in jrnDeletes:
			fileDeletes.write(line + '\n')

# THE WORKS
def main():
	clearAllTables()
	genInsertUids(100)
	genInsertAppIds(200)
	genInsertAppUsageFast(20000,200)

	writeJrnFiles()

if __name__ == '__main__':
	main()