import sqlite3 as sqll
import random
import string
import time
import os

# GLOBALS
dumpFilePath = './journaldump/'

# DATA STRUCTURES
lstEbox = set()
lstJournalOps = [ ('_INS',datInserts), ('_DEL',datDeletions), ('_UPD',datUpdates) ]

# GET EboxList
lstEboxFiles = [dir for dir in os.walk('.').next()[1] if dir.startswith('E') is True]
for eboxfile in lstEboxFiles:
	lstEbox.add(eboxfile)

# APPEND TO OP-TABLES
for operation in lstJournalOps:
	

#inserts
datInserts = []
for ebox in lstEbox:
	with open( dumpFilePath + ebox + '_INS', 'r' ) as filereader:
		tablename, values = filereader.readline().split['|']
		datInserts.append((tablename, values))

#deletions
datDeletions = []
for ebox in lstEbox:
	with open( dumpFilePath + ebox + '_DEL', 'r' ) as filereader:
		tablename, values = filereader.readline().split['|']
		datDeletions.append((tablename, values))



# READ FROM JOURNAL FILES
