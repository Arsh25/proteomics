#!/usr/bin/env python3

# Arsh Chauhan
# main.py: Main program to integrate mzxml_parser and handle_csv. Made for a particular workflow
# 06/16/2017
# Last Edited: 06/17/2017
# MIT License (2017)

import mzxml_parser
import handle_csv
import csv
import pathlib
import argparse
import os

def colate_scan_info(mzxml_file,scans_file):
	scan_nums = handle_csv.read_scans_list(scans_file)
	results = []
	for scan in scan_nums:
		current_scan ={}
		mz,mz_intensity,precursor_charge = mzxml_parser.get_peaks(mzxml_file,scan)
		current_scan['scan'] = scan
		current_scan['peaks'] = mz
		peptides = handle_csv.get_peptide('real.csv',[scan])
		current_scan['peptide'] = peptides[0]['peptide'] #list (size 1) of dicts
		current_scan['precursor_mz'] = peptides[0]['precursor_mz']
		current_scan['mods'] = peptides[0]['mods']
		results.append(current_scan)
	return results

def write_csv_files(experiment,scan_results,peaks=True):
	pathlib.Path('results/'+experiment).mkdir(parents=True,exist_ok=True)
	field_names=['peptide','mods','scan','peaks','precursor_mz']
	os.chdir('results/'+experiment)
	for scan in scan_results:
		with open(str(scan['scan'])+'.csv','w') as csv_file:
			csv_writer = csv.DictWriter(csv_file,fieldnames=field_names,dialect='excel')
			csv_writer.writeheader()
			csv_writer.writerow({'peptide':scan['peptide'],'mods':scan['mods'],'scan':scan['scan'],'precursor_mz':scan['precursor_mz']})
			if peaks:
				for peak in zip(scan['peaks']):# Write each peak in new row
					csv_writer.writerow({'peaks':peak[0]})


if __name__ == '__main__':

	parser = argparse.ArgumentParser(description='Colate peptide and mz informarion from various files.')
	parser.add_argument('--infile',type=str,help='Raw file converted \
						to mzXML with 32 bit precision and no zlib compression',
						default='sample.mzXML')
	parser.add_argument('--scans',type=str,help='csv file with scan numbers to match'
	 					,default='scan_list.csv')
	parser.add_argument('--name',type=str,help='Experiment name. Results will be \
						stored in results/name. Default is --infile')
	args = parser.parse_args()
	collated_data = colate_scan_info(args.infile,args.scans)
	if args.name is None: #Check to see if --name was passed
		args.name = args.infile
	write_csv_files(args.name,collated_data)
