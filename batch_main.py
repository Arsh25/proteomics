#!/usr/bin/env python3

# Arsh Chauhan
# batch_main.py: Run main.py in batch mode
# 06/26/2017
# Last Edited: 06/27/2017
# MIT License (2017)
import subprocess
import os

def run_main(directory,excluded_files):
	base_path = os.path.dirname(os.path.realpath(__file__))
	for filename in os.listdir(directory):
		if filename not in excluded_files:
			print("running "+filename)
			process = subprocess.run(["./main.py","--infile",directory+"/"+filename,\
				"--minfdr",filename[:filename.find(".")]+".csv","--name",filename])
			if process.returncode != 0:
				with open('auto_run.log','a') as log:
					log.write('running for '+ filename + ' existed with ' + str(process.returncode) + '\n')

def zip_results(results_dir):
	for folder in os.walk(results_dir):
		if folder[0].find('.mzXML') != -1:
			experiment_name = folder[0].find('.mzXML')
			print ("zipping folder "+ folder[0])
			process = subprocess.run(["/usr/bin/zip","-r",folder[0][:experiment_name]+".zip",folder[0]+"/"])
			if process.returncode != 0:
				with open('auto_run.log','a') as log:
					log.write('zipping '+ folder[0] + ' existed with ' + str(process.returncode) + '\n')
def create_do_not_check_list(results_dir):
	for folder in os.walk(results_dir):
		if folder[0].find('.mzXML') != -1:
			print ("Processing results from "+ folder[0])
			process = subprocess.run(["./filter.py","--pfilter",folder[0]])
			if process.returncode != 0:
				with open('auto_run.log','a') as log:
					log.write('processing '+ folder[0] + ' existed with ' + str(process.returncode) + '\n')

if __name__ == '__main__':
	confirm = input("Are you sure you want to run this batch job (Y/N?)")
	if confirm.lower() == "y":
		# completed_files = ['160108_C1021-2_a.mzXML','160108_C1021-2_c.mzXML','160108_C812-1_b.mzXML','160108_C812-1_c.mzXML','160108_C923-1_a.mzXML','160108_I122-1-K_a.mzXML']
		# run_main("/media/arsh/ResearchRazzle/converted",completed_files)
		#zip_results("results")
		create_do_not_check_list("results")
	else:
		print("Exiting")