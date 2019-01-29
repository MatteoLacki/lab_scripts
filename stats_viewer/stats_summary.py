import sys
import os
from os.path import join, split
from glob import glob, iglob
import xml.etree.ElementTree as ET
import pandas as pd

# folder_path = "/home/matteo/Projects/lab_scripts/data/RES"
folder_path, csv_path = sys.argv[1:3]


def read_line(path, n):
	with open(path, "r") as f:
		for i in range(n+1):
			x = f.readline()
	return x

def parse_stats(path):
	"""Parse the _stat.csv file in the output of the pipeline."""
	x = ('sample','mode','queries','peptides','proteins')
	y = read_line(path, 1).replace('\n','').split(",")[1:]
	yield from zip(x,y)

def parse_xml_params(path):
	tree = ET.parse(path)
	root = tree.getroot()
	for p in root.find('PARAMS'):
		yield p.attrib['NAME'], p.attrib['VALUE']

output_names = ('stats.csv', 'Apex3D.xml', 'workflow.xml')
parsers = dict(zip(output_names, (parse_stats, parse_xml_params, parse_xml_params)))

def parse_files(files, search=output_names):
	return {s: f for f in files for s in search if s in f}

def iter_paths(folder_path):
	for folder in iglob(join(folder_path,"*","*")):
		sample_set_no, raw_file_no = split(folder)
		_, sample_set_no = split(sample_set_no)
		files = parse_files(os.listdir(folder))
		row = {'sample_set_no': sample_set_no, 'raw_file_no': raw_file_no}
		for f in files:
			try:
				for param, value in parsers[f](join(folder,files[f])):
					row[param] = value
			except FileNotFoundError as e:
				print(e)
		yield row

data_frame = pd.DataFrame(iter_paths(folder_path))
data_frame.to_csv(path_or_buf=csv_path, index=False)