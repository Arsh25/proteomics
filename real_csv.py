#!/usr/bin/env python3

# Arsh Chauhan
# real_csv.py: Convert excel or google sheets "csv" into real csv
# 06/26/2017
# Last Edited: 06/26/2017
# MIT License (2017)
import csv
import argparse

def convert_actual_csv(filename,outfile):
	new_file=[]
	with open(filename,'r') as original:
		for line in original.read().splitlines():
			order = line.replace("\n",",")
			new_file.append(order)
	#print(new_file)
	with open(outfile,'w') as csv_file:
		writer = csv.writer(csv_file)
		writer.writerow(new_file)
if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Convert weird excel/google sheets exported csv to real csv')
	parser.add_argument('--infile',type=str,help='File to covert to csv. One entry per line')
	parser.add_argument('--outfile',type=str,help='Output file name. Default is infile')
	args = parser.parse_args()
	
	if args.outfile is None: #Check to see if --name was passed
		args.outfile = args.infile
	convert_actual_csv(infile,outfile)
