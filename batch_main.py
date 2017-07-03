#!/usr/bin/env python3

# Arsh Chauhan
# batch_main.py: Run main.py in batch mode
# 06/26/2017
# Last Edited: 06/27/2017
# MIT License (2017)
import subprocess
import os
from time import process_time

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

def run_main_parallel(directory,excluded_files):
	base_path = os.path.dirname(os.path.realpath(__file__))
	files = []
	i = 0
	for filename in os.listdir(directory):
		if filename not in excluded_files:
			files.append(filename)
	# print(int(len(files)/3))
	# while (i<len(files)):
	# 	print(i)
	# 	print(files[i][:files[i+0].find(".")]+".csv")
	# 	i=i+1
	
	while (i<(int(len(files)/3))):
		process_1 = subprocess.Popen(["./main.py","--infile",directory+"/"+files[i+0],\
					"--minfdr",files[i][:files[i+0].find(".")]+".csv","--name",files[i+0]])
		process_2 = subprocess.Popen(["./main.py","--infile",directory+"/"+files[i+1],\
		 			"--minfdr",files[i+1][:files[i+1].find(".")]+".csv","--name",files[i+1]])
		process_3 = subprocess.Popen(["./main.py","--infile",directory+"/"+files[i+2],\
		 			"--minfdr",files[i+2][:files[i+2].find(".")]+".csv","--name",files[i+2]])
		# # process_4 = subprocess.Popen(["./main.py","--infile",directory+"/"+files[i+0],\
		# #			"--minfdr",files[:files[i+0].find(".")]+".csv","--name",files[i+0]],shell=True)
		process_1.wait()
		process_2.wait()
		process_3.wait()
		# # process_4.wait()
		 
		if process_1.returncode != 0:
				with open('auto_run_parallel.log','a') as log:
					log.write('running for '+ files[i+0] + ' existed with ' + str(process_1.returncode) + '\n')
		if process_2.returncode != 0:
			with open('auto_run_parallel.log','a') as log:
				log.write('running for '+ files[i+1] + ' existed with ' + str(process_2.returncode) + '\n')
		if process_3.returncode != 0:
			with open('auto_run_parallel.log','a') as log:
				log.write('running for '+ files[i+2] + ' existed with ' + str(process_3.returncode) + '\n')
		# if process_4.returncode != 0:
		# 	with open('auto_run.log','a') as log:
		# 			log.write('running for '+ files[i+3] + ' existed with ' + str(process.returncode) + '\n')

		i=i+1
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

def mzxml_to_db(directory,excluded_files=[]):
	base_path = os.path.dirname(os.path.realpath(__file__))
	for filename in os.listdir(directory):
		if filename not in excluded_files:
			print("running "+filename)
			process = subprocess.run(["./main.py","--infile",directory+"/"+filename])
			if process.returncode != 0:
				with open('auto_run_db.log','a') as log:
					log.write('running for '+ filename + ' existed with ' + str(process.returncode) + '\n')



if __name__ == '__main__':
	confirm = input("Are you sure you want to run this batch job (Y/N?)")
	if confirm.lower() == "y":
		# completed_files = ['160108_C1021-2_a.mzXML','160108_C1021-2_c.mzXML','160108_C812-1_b.mzXML','160108_C812-1_c.mzXML','160108_C923-1_a.mzXML','160108_I122-1-K_a.mzXML']
		#run_main("/media/arsh/ResearchRazzle/converted",[])
		#run_main_parallel("/media/arsh/ResearchRazzle/converted",['160108_C1021-2_a.mzXML','160108_I122-1-K_a.mzXML','160108_C1021-2_c.mzXML'])
		#zip_results("results")
		#create_do_not_check_list("results")
		mzxml_to_db("/media/arsh/ResearchRazzle/converted",['160108_C812-1_a.mzXML'])
		print("Overall Time: "+process_time()/60 + "minutes")
	else:
		print("Exiting")