#!/usr/bin/env python3

# Arsh Chauhan
# main.py: Main program to integrate mzxml_parser and handle_csv. Made for a particular workflow
# 06/16/2017
# Last Edited: 06/16/2017
# MIT License (2017)

import mzxml_parser
import handle_csv
import csv
import pathlib

def colate_scan_info(mzxml_file,scans_file):
	scan_nums = handle_csv.read_scans_list(scans_file)
	results = []
	for scan in scan_nums:
		current_scan ={}
		mz,mz_intensity = mzxml_parser.get_peaks(mzxml_file,scan)
		current_scan['scan'] = scan
		current_scan['peaks'] = mz
		peptides = handle_csv.get_peptide('real.csv',[scan])
		current_scan['peptide'] = peptides[0]['peptide'] #list (size 1) of dicts
		results.append(current_scan)
	return results

def write_csv_files(scan_results):
	pathlib.Path('results').mkdir(parents=True,exist_ok=True)
	field_names=['peptide','peaks']
	for scan in scan_results:
		with open('results/'+str(scan['scan'])+'.csv','w') as csv_file:
			csv_writer = csv.DictWriter(csv_file,fieldnames=field_names,dialect='excel')
			csv_writer.writeheader()
			csv_writer.writerow({'peptide':scan['peptide']})
			for peak in zip(scan['peaks']):# Write each peak in new row
				csv_writer.writerow({'peaks':peak[0]})


if __name__ == '__main__':
	collated_data = colate_scan_info('real.mzXML','scan_list.csv')
	write_csv_files(collated_data)
