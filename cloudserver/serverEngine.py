import sqlite3 as sqll
import random
import string
import time
import os
import sys

# GLOBALS
DUMPFILEPATH = './journaldump/'
DBPATH = 'cloudserver.db'
PENDINGOPS = './pendingops'

# DATA STRUCTURES
lstEbox = set()
lstOps = []

###########################################################################################
# GENERAL SQL COMMAND FUNCTION
def ExecuteSQL(cmd):
	try:
		con = sqll.connect(DBPATH)
		cur = con.cursor()
		
		query = cur.execute(cmd)
		return query.fetchall()
	except sqll.Error, e:
		if con:
			con.rollback()	
		print "SQLite Error %s:" % e.args[0]
		return
	finally:
		if con:
			con.commit()
			con.close()


# CLEAR ALL TABLES
def clearAllTables():
	#TODO HANDLE JOURNALISING HERE
	try:
		con = sqll.connect(DBPATH)
		cur = con.cursor() 
		cur.execute("DELETE FROM apps");
		cur.execute("DELETE FROM eboxes");
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


# GET EboxList
def updateEboxList():		
	lstEboxFiles = [filename[:-4] for filename in os.listdir(DUMPFILEPATH) if filename.startswith('E') is True]
	print lstEboxFiles
	for eboxfile in lstEboxFiles:
		print 'Adding:', eboxfile
		lstEbox.add(eboxfile)
	updateEboxTable()

# UPDATE EBOX ID TABLE
def updateEboxTable():
	for ebox in lstEbox:
		try:
			# open DB connection
			con = sqll.connect(DBPATH)
			cur = con.cursor()
			tmpQuery = cur.execute( "SELECT count(*) FROM eboxes WHERE id = '%s'" %(ebox))
			if tmpQuery.fetchall()[0][0] == 0:
				insQuery = "INSERT INTO eboxes VALUES ('%s')" %(ebox)
				cur.execute( insQuery )
		except sqll.Error, e:
			if con:
				con.rollback()		
			print "SQLite Error in updateEboxTable! %s:\nQuery: " % (e.args[0], insQuery)
		finally:
			if con:
				con.commit()
				con.close()


# APPEND TO OP-TABLES
def readToOpTable():
	for ebox in lstEbox:
		with open( DUMPFILEPATH + ebox + '.log', 'r' ) as filereader:
			for line in filereader:
				op, tablename, values = line.split('|')
				
				#modify for insertion into specific tables 
				if op == 'INS':
					# For app usage, add eboxid in the end of values list
					# INS|uidToAppUsage|(NULL, 'U22896', 'A68575', datetime('2014-04-27 03:20:50'), time('7:45:51'), 'T', '/appsigns/A68575')
					if tablename == 'uidToAppUsage':
						values = values[:-2] + ",'%s')" %(ebox)
					
					# For uids, add (eboxid, uid) pair to eboxestouids table
					elif tablename == 'uids':
						lstOps.append( (op, 'eboxesToUids', "(NULL, '%s', %s)" %(ebox, values[1:-2])) )
					
					# For appids, add (eboxid, app_id pair to eboxestoappids table
					elif tablename == 'apps':
						lstOps.append( (op, 'eboxesToApps', "(NULL, '%s', %s)" %(ebox, values[1:-2])) )
					lstOps.append((op, tablename, values))

				#modify for insertion into specific tables 
				# DEL|apps|id = 'A30017'
				elif op == 'DEL':
					# For app usage, add eboxid in the end of values list
					if tablename == 'uidToAppUsage':
						values = values + " and eboxid = '%s'" %(ebox)
					
					# For uids, add (eboxid, uid) pair to eboxestouids table
					elif tablename == 'uids':
						lstOps.append( (op, 'eboxesToUids', "eboxid = '%s' and %s" %(ebox, values)) )
					
					# For appids, add (eboxid, app_id pair to eboxestoappids table
					elif tablename == 'apps':
						lstOps.append( (op, 'eboxesToApps', "eboxid = '%s' and %s" %(ebox, values)) )
					lstOps.append((op, tablename, values))

		os.remove( DUMPFILEPATH + ebox + '.log')
		#TODO: commit to DB here?

def updateDB(commits = 1):
	successfulOps = 0

	# open DB connection
	con = sqll.connect(DBPATH)
	cur = con.cursor() 

	index = 0
	commitEvery = len(lstOps)/commits
	if commitEvery < 1:
		commitEvery = len(lstOps)

	print 'Have to update db with %s transactions, committing every %s.' %(len(lstOps), commitEvery)

	for (op, tablename, values) in lstOps:
		try:
			if op == 'INS':
				# INS|uidToAppUsage|(NULL, 'U22896', 'A68575', datetime('2014-04-27 03:20:50'), time('7:45:51'), 'T', '/appsigns/A68575')
				cur.execute( 'INSERT INTO %s VALUES %s' %(tablename, values) )
			elif op == 'UPD':
				pass
			elif op == 'DEL':
				# DEL|apps|id = 'A30017'
				cur.execute( 'DELETE from %s WHERE %s' %(tablename, values) )

			successfulOps += 1

		except sqll.IntegrityError, e:
			print 'IntegrityError trying to insert %s into %s. Ignoring.' %(values, tablename)

		except sqll.Error, e:
			if con:
				con.rollback()		
			print "SQLite Error in updateDB! %s:" % e.args[0]
			print 'INSERT INTO %s VALUES %s' %(tablename, values)

		finally:
			index += 1
			if index % commitEvery == 0:
				print 'Committing..'
				con.commit()

	if con:
		con.close()


# THE WORKS
def main(commits):
	#keep looping for ever
	while (True):
		updateEboxList()
		readToOpTable()
		updateDB(commits)

		#wait for a while
		time.sleep(300)

if __name__ == '__main__':
	clearAllTables()
	if len(sys.argv) > 1 and sys.argv[1] != '':
		commits = int(sys.argv[1].split(',')[0])
		main(int(commits))
	else:
		main(10) #default number of commits