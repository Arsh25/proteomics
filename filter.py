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

def filter_by_rsc(rsc_file,output_file):
	base_path = os.path.dirname(os.path.realpath(__file__))
	keep_list = []
	with open(rsc_file,'r') as full_file:
		protein_list = []
		reader = csv.DictReader(full_file)
		for entry in reader:
				protein_list.append(entry['Protein'])
		full_file.seek(0)
		for entry in reader:
			if entry['Entry'] in protein_list and entry['Entry'] != "":
				keep_list.append({'INF Rsc':entry['INF Rsc'],'Protein':entry['Entry'],'FDR':entry['FDR']})
	#print(keep_list)
	os.chdir(base_path)
	with open('results/'+output_file,'a') as output_file:
		writer = csv.DictWriter(output_file,fieldnames=['INF Rsc','Protein','FDR'])
		writer.writeheader()
		writer.writerows(keep_list)

def peptide_sublist(full_file,sublist_file,results_file):
	return_list = []
	peptide_sublist = []
	sublist_peptides = []
	fieldnames = []
	with open(sublist_file,'r') as sublist:
		reader = csv.DictReader(sublist)
		for entry in reader:
			sublist_peptides.append(entry['GG-modified peptide'])
			peptide_sublist.append(entry)
			
	with open(full_file,'r') as full_list:
		reader = csv.DictReader(full_list)
		fieldnames = reader.fieldnames
		for entry in reader:
			if entry['GG-modified peptide'] in sublist_peptides:
				for peptide in peptide_sublist:
					if peptide['GG-modified peptide'] == entry['GG-modified peptide']:
						entry['Protein Accession number'] = peptide['Protein Accession number']
				return_list.append(entry)

	base_path = os.path.dirname(os.path.realpath(__file__))
	os.chdir(base_path+'/results')
	with open(results_file,'a') as results:
		fieldnames.append('Protein Accession number')
		writer = csv.DictWriter(results,fieldnames)
		writer.writeheader()
		writer.writerows(return_list)

def omit_Ubproteins(full_file,to_remove_file,results_file):
	keep_list = []
	remove_list = []
	fieldnamesv = []
	with open(to_remove_file,'r') as to_remove:
		reader = csv.DictReader(to_remove)
		for protein in reader:
			remove_list.append(protein['Ub proteins'])
	
	with open(full_file,'r') as full_list:
		reader = csv.DictReader(full_list)
		fieldnames = reader.fieldnames
		for entry in reader:
			if entry['Protein'] not in remove_list:
				keep_list.append(entry)
	
	base_path = os.path.dirname(os.path.realpath(__file__))
	os.chdir(base_path+'/results')
	with open(results_file,'a') as results:
		writer = csv.DictWriter(results,fieldnames)
		writer.writeheader()
		writer.writerows(keep_list)

# Remove entries created by "filter_by_peaks" from main file
def remove_peptides(to_remove_file,output_file):
	remove_peptide_list = []
	check_psm_list = []
	fieldnames = []
	with open(to_remove_file,'r') as remove_list:
		remove_reader = csv.DictReader(remove_list)
		remove_list = list(remove_reader)
	for psm in remove_list:
		del psm['peak']
		spectra_set = psm['spectra_set']
		psm['spectra_set'] = spectra_set[:spectra_set.find('.mzXML')]

	with open(main_file,'r') as main_file:
		main_reader = csv.DictReader(main_file)
		fieldnames = main_reader.fieldnames
		for psm in main_reader:
			cur_psm = {'scan':psm['start_scan'],'spectra_set':psm['spectra_set']}
			if cur_psm in remove_list:
				if psm['peptide'] not in remove_peptide_list:
					remove_peptide_list.append(psm['peptide'])
				
	base_path = os.path.dirname(os.path.realpath(__file__))
	with open('results/'+output_file,'a') as output:
		writer = csv.DictWriter(output,fieldnames=['peptide'])
		writer.writeheader()
		print("WRITING CSV FILE")
		for peptide in remove_peptide_list:
			writer.writerow({'peptide':peptide})

if __name__ == '__main__':
	#sort_by_peptide('remaining_psm.csv')
	#min_fdr('results/peptides')
	#write_to_csv('min_fdr',min_fdr('results/peptides'))
	parser = argparse.ArgumentParser(description='Various functions to filter results')
	parser.add_argument('--pfilter',type=str,help='check scans from this results \
						folder for peaks between 259.50 and 260.77',)
	parser.add_argument('--peptide_check',type=str,help='Find peptides occuring in file created by pfilter')
	args = parser.parse_args()
	#filter_by_peaks(args.pfilter,259.50,260.77)
	#remove_peptides('results/all_do_not_check.csv','results/Mothership.csv','remove_peptides.csv')
	#filter_by_rsc('sheetforRSC.csv','rsc_filtered.csv')
	#peptide_sublist('peptide_full.csv','peptide_sublist.csv','GG_filtered.csv')
	omit_Ubproteins('Workbook1.csv','things to omit.csv','Ub_proteins_keep.csv')