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
import time

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
def get_batch_peaks(mzxml_file,minfdr_file,experiment,RAM=False):
	#scan_nums = handle_csv.read_scans_list(scans_file)
	fieldnames = ['spectra_set','start_scan','precursor_neutral_mass','calc_neutral_pep_mass','peptide','mods','protein','estfdr']
	spectra_set = experiment
	min_fdr_list = []
	base_path = os.path.dirname(os.path.realpath(__file__))
	with open(minfdr_file,'r') as min_fdr:
		reader = csv.DictReader(min_fdr,fieldnames=fieldnames)
		min_fdr_list = list(reader)
	os.chdir(base_path)
	pathlib.Path(base_path+'/results/'+spectra_set).mkdir(parents=True,exist_ok=True)
	loop_iter=0
	total_scans = len(min_fdr_list)
	for peptide in min_fdr_list:
		print ("Iterations left: "+str(total_scans-loop_iter))
		print(peptide['start_scan'])
		results = []
		current_scan ={}
		scan = int(peptide['start_scan'])
		if scan is None:
			print ("NONE")
			print(peptide)
		mz,mz_intensity = mzxml_parser.get_peaks(mzxml_file,scan)
		current_scan['scan'] = peptide['start_scan']
		current_scan['precursor_neutral_mass']=peptide['precursor_neutral_mass']
		current_scan['peptide']=peptide['peptide']
		current_scan['calc_neutral_pep_mass']=peptide['calc_neutral_pep_mass']
		current_scan['mods']=peptide['mods']
		current_scan['protein']=peptide['protein']
		current_scan['estfdr']=peptide['estfdr']
		current_scan['peaks'] = mz
		current_scan['spectra_set'] = spectra_set
		results.append(current_scan)
		print("WRITING CSV FILE FOR "+ str(scan))
		write_csv_files(experiment,results)
		print("DONE WRITING CSV FILE")
		os.chdir(base_path)
		loop_iter += 1
		
def write_csv_files(experiment,scan_results,peaks=True):
	pathlib.Path('results/'+experiment).mkdir(parents=True,exist_ok=True)
	field_names=['spectra_set','scan','precursor_neutral_mass','calc_neutral_pep_mass','peptide','mods','protein','estfdr','peaks']
	base_path = os.path.dirname(os.path.realpath(__file__))
	for scan in scan_results:
		os.chdir(base_path+'/results/'+experiment)
		print(os.getcwd())
		with open(str(scan['scan'])+'.csv','w') as csv_file:
			csv_writer = csv.DictWriter(csv_file,fieldnames=field_names,dialect='excel')
			csv_writer.writeheader()
			csv_writer.writerow({'spectra_set':scan['spectra_set'],'mods':scan['mods'],\
				'scan':scan['scan'],'precursor_neutral_mass':scan['precursor_neutral_mass'],\
				'calc_neutral_pep_mass':scan['calc_neutral_pep_mass'],'peptide':scan['peptide'],\
				'protein':scan['protein'],'estfdr':scan['estfdr']})
			if peaks:
				for peak in zip(scan['peaks']):# Write each peak in new row
					csv_writer.writerow({'peaks':peak[0]})

def mzxml_to_db(mzxml_file,experiment):
	mzxml_parser.file_to_object(mzxml_file,experiment,True)

if __name__ == '__main__':

	parser = argparse.ArgumentParser(description='Colate peptide and mz informarion from various files.')
	parser.add_argument('--infile',type=str,help='Raw file converted \
						to mzXML with 32 bit precision and no zlib compression',
						default='sample.mzXML')
	parser.add_argument('--scans',type=str,help='csv file with scan numbers to match'
	 					,default='scan_list.csv')
	parser.add_argument('--name',type=str,help='Experiment name. Results will be \
						stored in results/name. Default is --infile')
	parser.add_argument('--minfdr',type=str,help='csv file with minfdr vales from this experiment')
	args = parser.parse_args()
	#collated_data = colate_scan_info(args.infile,args.scans)
	if args.name is None: #Check to see if --name was passed
		args.name = args.infile
	get_batch_peaks(args.infile,args.minfdr,args.name)
	#write_csv_files(args.name,collated_data)
	#mzxml_to_db(args.infile,args.name)
	print ("time for "+ args.infile +":" + str(time.process_time()/60) + " minutes")
