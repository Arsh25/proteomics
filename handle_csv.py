#!/usr/bin/env python3

# Arsh Chauhan
# handle_csv.py: Handle data from csv exported from <insert program here>
# 06/16/2017
# Last Edited: 06/16/2017
# MIT License (2017)

import csv

# get_peptide
# filename: csv file with scan information
# 		scan_list: list of valid scan numbers
# returns:
# 		peptides: dict containg all peptides where key == scan number
def get_peptide(file_name,scan_list):
	with open(file_name,'r') as csv_file:
		csv_reader = csv.DictReader(csv_file,dialect='excel')
		peptides = []
		for row in csv_reader:
		 	if int(row['start_scan']) in scan_list:
		 		peptides.append({'scan':row['start_scan'],'peptide':row['peptide']}) 
		 	if len(peptides) == len(scan_list): # Found all, return
		 		return peptides
		return peptides

# read_scan_list
# scan_list: csv file with scan numbers
# returns:
# 		scan_nums: list of all scan numbers in scan_list
def read_scans_list(scan_list):
	with open(scan_list,'r') as scan_list:
		dialect = csv.Sniffer().sniff(scan_list.read(1024))
		scan_list.seek(0)
		csv_reader = csv.reader(scan_list,dialect)
		scan_nums = list(csv_reader)
		scan_nums = [int(i) for i in scan_nums[0]] #Convert to a list of int
		return scan_nums

if __name__ == '__main__':
	scan_nums = read_scans_list('scan_list.csv')
	scan_nums.sort()
	peptides = get_peptide('real.csv',scan_nums)
	print(peptides)