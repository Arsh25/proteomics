#!/usr/bin/env python3

# Arsh Chauhan
# scan_parser.py: Parse peaks information for a given scan from an Mzxml file
# 06/13/2017
# Last Edited: 06/15/2017
# MIT License (2017)

import base64
import struct
import csv
import database
import os

def file_to_object(mzxml_file,database_name,RAM=False,debug=False):
	scans_obj = []
	database.create_database(database_name)
	with open (mzxml_file,'r') as scan_file:
		seen_peak_open = False
		seen_peak_close = False
		peaks = ""
		current_scan = {}
		for line in scan_file:
			if line.find('<scan num=') != -1: #found scan                                  #
				current_scan['num'] = int(line[line.find("=")+2:-2]) #scan num
			if line.find('<peaks') != -1:
				seen_peak_open = True
			if line.find('>') != -1 and seen_peak_open:
				peaks += line[line.find('>')+1:].strip()
			if line.find('</peaks>') != -1 and seen_peak_open:
				peaks += line[:line.find('</peaks>')]
				current_scan['peaks'] = peaks[:peaks.find('</peaks> ')]
				scans_obj.append(current_scan)
				seen_peak_open = False
				seen_peak_close = True
			if debug and seen_peak_close:
				print(current_scan)
				#handle_peak(current_scan['peaks'])
			if not RAM and not debug and seen_peak_close:
				database.add_scan(database_name,current_scan)
			if RAM and not debug and seen_peak_close:
				scans_obj.append(current_scan)
			if seen_peak_close and line.find('</scan>') != -1:
				current_scan = {}
				peaks = ""
				seen_peak_close = False
	if RAM:
		database.add_scan(database_name,scans_obj,True)



def handle_peak(encoded_peaks):
	peaks = base64.b64decode(encoded_peaks)
	mz_list,intensity_list = parse_peaks(peaks)

	for mz in mz_list:
		print(mz)

def find_scan(file_name,scan_num):
	with open (file_name,'r') as scan_file:
		if scan_file is None:
			print (file_name)
		peaks = ""
		precursor_charge = ""
		for line in scan_file:
			if line.find("<scan") != -1:
				current_scan = line[line.find("=")+2:-2]
				if current_scan == str(scan_num):
					while(True):
						try:
							next_line = scan_file.readline()
							previous_line = next_line
							if next_line.find('<precursorMz') !=-1:
								end_tag = next_line.find('>')
								precursor_charge = next_line[end_tag+1:next_line.find('</precursorMz>')]
							elif next_line.find('<peaks') !=-1:
								output = ""
								while(True):
									next_line = scan_file.readline()
									output += next_line
									if next_line.find(">") != -1:
										peaks = output[:output.find("<")]
										return peaks,precursor_charge
						except:
							print ("Could not handle scan: "+current_scan)
							break

def find_scan_RAM(file_name,current_scan):
	with open (file_name,'r') as scan_file:
		if scan_file is None:
			print (file_name)
		peaks = ""
		precursor_charge = ""
		memory_file = []
		for line in scan_file:
			memory_file.append(line)
		for i in range(0,len(memory_file)):
			line = memory_file[i]
			if line.find("<scan") != -1:
				current_scan = line[line.find("=")+2:-2]
				if str(scan) == current_scan:
					while(True):
						next_line = memory_file[i+1]
						previous_line = next_line
						if next_line.find('<precursorMz') !=-1:
							end_tag = next_line.find('>')
							precursor_charge = next_line[end_tag+1:next_line.find('</precursorMz>')]
						elif next_line.find('<peaks') !=-1:
							output = ""
							while(True):
								next_line = memory_file[i+2]
								output += next_line
								if next_line.find(">") != -1:
									peaks = output[:output.find("<")]
	return peaks,precursor_charge
									
def parse_peaks(peaks_decoded):
	#Based on code by Taejoon Kwon (https://code.google.com/archive/p/massspec-toolbox/)
	tmp_size = len(peaks_decoded)/4
	unpack_format1 = ">%dL" % tmp_size

	idx = 0
	mz_list = []
	intensity_list = []
	for tmp in struct.unpack(unpack_format1,peaks_decoded):
		tmp_i = struct.pack("I",tmp)
		tmp_f = struct.unpack("f",tmp_i)[0]
		if( idx % 2 == 0 ):
			mz_list.append( float(tmp_f) )
		else:
			intensity_list.append( float(tmp_f) )
		idx += 1
	return mz_list,intensity_list

def get_peaks(db_file,scan,RAM=False):
	os.chdir(os.getcwd())
	encoded_peaks = database.get_peaks(db_file,scan)

	peaks = base64.b64decode(encoded_peaks)
	mz_list,intensity_list= parse_peaks(peaks)
	
	return mz_list,intensity_list

def write_to_csv(filename,data):
	with open(filename+'.csv','w',newline='') as csv_file:
		data_writer = csv.writer(csv_file,dialect='excel')
		data_writer.writerow(data)


if __name__ == '__main__':
	#data = find_scan("real.mzXML",5000)	
		#mz_list,intensity_list,precursor_charge = get_peaks('160108_C812-1_a.mzXML',21822)
	# peaks,precursor_charge = find_scan('160108_C812-1_a.mzXML',21822)
	# print (precursor_charge)
	#print (peaks)
	# print('{0:15} | {1:2}'.format("        mz","mz intensity"))
	# for mz,intensity in zip(mz_list,intensity_list):
	# 	print('{0:15f} | {1:2f}'.format(mz,intensity))

	# print("GENERATING csv file. Open output.csv after termination")
	# write_to_csv("output",mz_list)
	file_to_object('/media/arsh/ResearchRazzle/converted/160108_C812-1_a.mzXML','test',False,False)