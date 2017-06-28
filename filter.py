#!/usr/bin/env python3
##

from handle_csv import write_to_csv
import csv
import os
import pathlib

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

if __name__ == '__main__':
	#sort_by_peptide('remaining_psm.csv')
	min_fdr('results/peptides')
	write_to_csv('min_fdr',min_fdr('results/peptides'))


