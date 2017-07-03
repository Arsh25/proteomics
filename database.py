#!/usr/bin/env python3

# Arsh Chauhan
# scan_parser.py: Parse peaks information for a given scan from an Mzxml file
# 07/02/2017
# Last Edited: 07/02/2017

import sqlite3
import os

def log_error(error,database):
	base_dir = os.getcwd()
	os.chdir(os.getcwd()+'/logs')
	with open(database+'errors.log','a') as log:
		log.write(error+'\n')
	os.chdir(base_dir)

def create_database(database):
	database = database[:database.find('.mzXML')]

	table_scans = """ CREATE TABLE IF NOT EXISTS scans (
						number INTEGER PRIMARY KEY,
						peaks TEXT);"""
	try:
		db_conn = sqlite3.connect(database+'.sqlite')
		db_conn.execute(table_scans)
		db_conn.commit()
	except sqlite3.OperationalError as e:
		print (e)
		db_conn.rollback()

def add_scan(database,scan,RAM=False):
	database = database[:database.find('.mzXML')]
	db_conn = sqlite3.connect(database+'.sqlite')
	cursor = db_conn.cursor()
	try:
		if RAM:
			for entry in scan:
				cursor.execute("INSERT INTO scans(number,peaks) VALUES (?,?)",(entry['num'],entry['peaks']))
		else:
			cursor.execute("INSERT INTO scans(number,peaks) VALUES (?,?)",(scan['num'],scan['peaks']))
	except sqlite3.IntegrityError as e:
		pass
	db_conn.commit()

def connect_to_db(database):
	database = database[:database.find('.mzXML')]
	print(database)
	db_conn = sqlite3.connect(database+'.sqlite')
	return db_conn

def get_peaks(database,scan):
	db_conn = connect_to_db(database)
	cursor = db_conn.cursor()
	encoded_peak=""
	try:
		current_peak = cursor.execute("SELECT peaks from scans WHERE number = (?)",(scan,))
		encoded_peak = current_peak.fetchone()[0]
	except sqlite3.Error as e:
		log_error(str(scan) +": " + str(e),database)
	except TypeError as e:
		log_error(str(scan) +": " + str(e),database)
	return encoded_peak


