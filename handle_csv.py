#!/usr/bin/env python3

# Arsh Chauhan
# handle_csv.py: Handle data from csv exported from <insert program here>
# 06/16/2017
# Last Edited: 06/29/2017
# MIT License (2017)

import csv
import pathlib
import os

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
		 		peptides.append({'scan':row['start_scan'],'peptide':row['peptide'],'precursor_mz':row['precursor_mz'],'mods':row['mods']}) 
		 	if len(peptides) == len(scan_list): # Found all, return
		 		return peptides
		return peptides

# read_scan_list
# scan_list: csv file with scan numbers
# returns:
# 		scan_nums: list of all scan numbers in scan_list
def read_scans_list(scan_list):
	with open(scan_list,'r') as scan_list:
		#dialect = csv.Sniffer().sniff(scan_list.read(1024))
		#scan_list.seek(0)
		csv_reader = csv.reader(scan_list)
		scan_nums = list(csv_reader)
		scan_nums = [int(i) for i in scan_nums[0]] #Convert to a list of int
		return scan_nums

def match_peptide_lists(all_info,to_do):
	with open(all_info,'r') as mothership_file, open(to_do,'r') as remaining:
		dialect_mothership = csv.Sniffer().sniff(mothership_file.read(1024))
		#dialect_remaining = csv.Sniffer().sniff(remaining.read(1024))
		mothership_fieldnames = ['spectra_set','start_scan','precursor_neutral_mass','calc_neutral_pep_mass','peptide','mods','protein','estfdr']
		mothership_reader = csv.DictReader(mothership_file,fieldnames=mothership_fieldnames)
		remaining_reader = csv.reader(remaining) 
		peptide_list = []
		remaining_psm = [] #psm: peptide spectram match
		for peptide in remaining_reader:
			peptide_list.append(peptide[0])
		for result in mothership_reader:
		# 	print(result)
		 	if result['peptide'] in peptide_list:
		  		remaining_psm.append(result)
		return remaining_psm
def write_to_csv(filename,data_list):
	pathlib.Path('results/').mkdir(parents=True,exist_ok=True)
	os.chdir('results/')
	extension = ""
	if filename.find(".") != -1:
		extension = filename[filename.find('.')+1:]
		if extension != 'csv':
			filename = filename+'.'+'csv'
	else:
		filename = filename+'.'+'csv'
	fieldnames = ['spectra_set','start_scan','precursor_neutral_mass','calc_neutral_pep_mass',\
					'peptide','mods','protein','estfdr']
	with open(filename,'w') as csv_file:
		writer = csv.DictWriter(csv_file,fieldnames=fieldnames)
		writer.writeheader()
		for row in data_list:
			writer.writerow({'spectra_set':row['spectra_set'],'start_scan':row['start_scan'],\
							'precursor_neutral_mass':row['precursor_neutral_mass'],\
							'calc_neutral_pep_mass':row['calc_neutral_pep_mass'],\
							'peptide':row['peptide'],'mods':row['mods'],'protein':row['protein'],\
							'estfdr':row['estfdr']})
# colate all files in folder into different files by spectra set
def colate_by_spectra_file(folder):
	base_path = os.path.dirname(os.path.realpath(__file__))
	pathlib.Path(base_path+"/results/spectra_collated").mkdir(parents=True,exist_ok=True)
	fieldnames = ['spectra_set','start_scan','precursor_neutral_mass','calc_neutral_pep_mass',\
					'peptide','mods','protein','estfdr']
	for file in os.listdir(folder):
		with open(folder+'/'+file,'r') as peptide_file:
			reader = csv.DictReader(peptide_file,fieldnames=fieldnames)
			for row in reader:
				with open(base_path+"/results/spectra_collated/"+row['spectra_set']+".csv",'a') as collated_file:
					writer = csv.DictWriter(collated_file,fieldnames=fieldnames)
					writer.writerow(row)

if __name__ == '__main__':
	# scan_nums = read_scans_list('scan_list.csv')
	# scan_nums.sort()
	# peptides = get_peptide('real.csv',scan_nums)
	# print(peptides)
	# remaining_psm = match_peptide_lists("Mothership.csv","correct peptide list.csv")
	# #print(remaining_psm)
	# print("WRITING CSV FILE")
	# write_to_csv("remaining_psm",remaining_psm)
	colate_by_spectra_file("results/peptides")