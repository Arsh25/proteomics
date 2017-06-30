#!/usr/bin/env python3
##

from handle_csv import write_to_csv
import csv
import os
import pathlib
import argparse

def sort_by_peptide(filename):
	pathlib.Path('results/peptides').mkdir(parents=True,exist_ok=True)
	os.chdir('results/')
	with open(filename,'r') as master_file:
		csv_reader = csv.DictReader(master_file,dialect='excel')
		fieldnames = ['spectra_set','start_scan','precursor_neutral_mass','calc_neutral_pep_mass',\
					'peptide','mods','protein','estfdr']
		os.chdir('peptides/')
		peptides_seen = []
		for psm in csv_reader:
			with open(psm['peptide']+'.csv','a') as peptide_file:
				peptide_csv = csv.DictWriter(peptide_file,dialect='excel',fieldnames=fieldnames)
				if psm['peptide'] not in peptides_seen: # only write headers the first time we see this peptide
					peptide_csv.writeheader()
				peptides_seen.append(psm['peptide'])
				peptide_csv.writerow({'spectra_set':psm['spectra_set'],'start_scan':psm['start_scan'],\
							'precursor_neutral_mass':psm['precursor_neutral_mass'],\
							'calc_neutral_pep_mass':psm['calc_neutral_pep_mass'],\
							'peptide':psm['peptide'],'mods':psm['mods'],'protein':psm['protein'],\
							'estfdr':psm['estfdr']})

def min_fdr(folder):
	min_fdr = []
	for file in os.listdir(folder):
		with open(folder+'/'+file,'r') as peptide_file:
			fieldnames = ['spectra_set','start_scan','precursor_neutral_mass','calc_neutral_pep_mass',\
					'peptide','mods','protein','estfdr']
			reader = csv.DictReader(peptide_file,dialect='excel',fieldnames=fieldnames)
			# for k in reader:
			# 	print(k['estfdr'])
			reader = sorted(reader, key=lambda k: k['estfdr'])
			min_fdr.append(reader[0])
	return min_fdr

def filter_by_peaks(results_dir,min_val,max_val):
	min_val = str(min_val)
	max_val = str(max_val)
	fieldnames = ['spectra_set','scan,precursor_neutral_mass','calc_neutral_pep_mass',\
				'peptide','mods','protein','estfdr','peaks']
	base_path = os.path.dirname(os.path.realpath(__file__))
	good_psm_list =[]
	for file in os.listdir(results_dir):
		if file.find('.zip') != 0:
			print("Processing: " +file)
			with open(results_dir+"/"+file,'r') as results_file:
				dialect = csv.Sniffer().sniff(results_file.read(1024))
				results_file.seek(0)
				reader = csv.DictReader(results_file,dialect=dialect)
				spectra_set = ""
				scan = ""
				for row in reader:
					if row['spectra_set'] != "":
						spectra_set = row['spectra_set']
					if row['scan'] != "":
						scan = row['scan']
					if row['peaks'] >= min_val and row['peaks'] <= max_val:
			 			good_psm = {}
			 			good_psm['spectra_set'] = spectra_set
			 			good_psm['scan'] = scan
			 			good_psm['peak'] = row['peaks']
			 			good_psm_list.append(good_psm)
	os.chdir(base_path+"/results")
	with open('do_not_check.csv','a') as output_file:
		writer = csv.DictWriter(output_file,fieldnames=['spectra_set','scan','peak'])
		writer.writeheader()
		for spectra_set in good_psm_list:
			writer.writerow(spectra_set)

if __name__ == '__main__':
	#sort_by_peptide('remaining_psm.csv')
	#min_fdr('results/peptides')
	#write_to_csv('min_fdr',min_fdr('results/peptides'))
	parser = argparse.ArgumentParser(description='Various functions to filter results')
	parser.add_argument('--pfilter',type=str,help='check scans from this results \
						folder for peaks between 259.50 and 260.77',)
	args = parser.parse_args()
	filter_by_peaks(args.pfilter,259.50,260.77)

