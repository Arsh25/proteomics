#!/usr/bin/env python3

# Arsh Chauhan
# scan_parser.py: Parse peaks information for a given scan from an Mzxml file
# 07/02/2017
# Last Edited: 07/02/2017

import sqlite3

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
		db_conn.rollback()
	db_conn.commit()


