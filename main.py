#!/usr/bin/env python3

# Arsh Chauhan
# main.py: Main program to integrate mzxml_parser and handle_csv. Made for a particular workflow
# 06/16/2017
# Last Edited: 06/16/2017
# MIT License (2017)

import mzxml_parser
import handle_csv

def colate_scan_info(mzxml_file,scans_file):
	scan_nums = handle_csv.read_scans_list(scans_file)
	results = []
	for scan in scan_nums:
		current_scan ={}
		mz,mz_intensity = mzxml_parser.get_peaks(mzxml_file,scan)
		current_scan['scan'] = scan
		current_scan['peaks'] = mz
		peptides = handle_csv.get_peptide('real.csv',[scan])
		current_scan['peptides'] = peptides[0]['peptide'] #list (size 1) of dicts
		results.append(current_scan)
	return results

if __name__ == '__main__':
	collated_data = colate_scan_info('real.mzXML','scan_list.csv')
	print(collated_data)
