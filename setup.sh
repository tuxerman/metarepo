#!/bin/bash

mkdir journaldump
mkdir logs

echo 'Creating blank databases for testing..'

cd cloudserver
sqlite3 cloudserver.db < cloudServerTableCreator.sqlite3

cd ../ebox
sqlite3 E12019.db < tableCreator.sql
sqlite3 E20010.db < tableCreator.sql
sqlite3 E40063.db < tableCreator.sql
sqlite3 E12001.db < tableCreator.sql

echo 'Done.'