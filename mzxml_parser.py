#!/usr/bin/env python3

# Arsh Chauhan
# scan_parser.py: Parse peaks information for a given scan from an Mzxml file
# 06/13/2017
# Last Edited: 06/15/2017
# MIT License (2017)

import base64
import struct
import csv

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

def find_scan_RAM(file_name,scan_nums_list):
	with open (file_name,'r') as scan_file:
		if scan_file is None:
			print (file_name)
		peaks = []
		precursor_charge = []
		memory_file = []
		for line in scan_file:
			memory_file.append(line)
		for scan in scan_nums_list:
			for line in memory_file:
				if line.find("<scan") != -1:
					current_scan = line[line.find("=")+2:-2]
					if str(scan) == current_scan:
						while(True):
							next_line = scan_file.readline()
							previous_line = next_line
							if next_line.find('<precursorMz') !=-1:
								end_tag = next_line.find('>')
								current_precursor_charge = next_line[end_tag+1:next_line.find('</precursorMz>')]
							elif next_line.find('<peaks') !=-1:
								output = ""
								while(True):
									next_line = scan_file.readline()
									output += next_line
									if next_line.find(">") != -1:
										current_peak = output[:output.find("<")]
										peaks.append(current_peak)
										precursor_charge.append(current_precursor_charge)
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

def get_peaks(mzxml_file,scan,RAM=False):
	scan_data,precursor_charge = find_scan(mzxml_file,scan)
	encoded_peaks = scan_data[scan_data.find(">")+1:]
	peaks = base64.b64decode(encoded_peaks)
	mz_list,intensity_list = parse_peaks(peaks)
	return mz_list,intensity_list,precursor_charge

def get_peaks_RAM(mzxml_file,scan_list):
	scan_data,precursor_charge = find_scan_RAM(mzxml_file,scan_list)
	all_mz = []
	for scan in scan_data:
		encoded_peaks = scan_data[scan_data.find(">")+1:]
		peaks = base64.b64decode(encoded_peaks)
		mz_list,intensity_list = parse_peaks(peaks)
		all_mz.append()
	return mz_list,intensity_list,precursor_charge

def write_to_csv(filename,data):
	with open(filename+'.csv','w',newline='') as csv_file:
		data_writer = csv.writer(csv_file,dialect='excel')
		data_writer.writerow(data)


if __name__ == '__main__':
	#data = find_scan("real.mzXML",5000)	
		#mz_list,intensity_list,precursor_charge = get_peaks('160108_C812-1_a.mzXML',21822)
	peaks,precursor_charge = find_scan('160108_C812-1_a.mzXML',21822)
	print (precursor_charge)
	print (peaks)
	# print('{0:15} | {1:2}'.format("        mz","mz intensity"))
	# for mz,intensity in zip(mz_list,intensity_list):
	# 	print('{0:15f} | {1:2f}'.format(mz,intensity))

	# print("GENERATING csv file. Open output.csv after termination")
	# write_to_csv("output",mz_list)
