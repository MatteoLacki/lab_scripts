import sys
import os
from os.path import join
import pandas as pd

from parsers import parsers, get_sampleSetNo_rawFileNo, get_parse


folder_path, csv_path = sys.argv[1:3]
# folder_path = "/home/matteo/Projects/lab_scripts/data/RES"
# csv_path = "test.csv"


def iter_outputs(folder_path, file_patterns):
	"""Iterate over all folders containing the results from output.

	Args:
		folder_path (str): Path to the root of the folder-tree being search.
		file_patterns (tuple): These strings should be present in the names of files that qualify to be parsed.
	"""
	for root, dirs, files in os.walk(folder_path):
		if files:
			files_str = "|".join(files)
			if any(fn in files_str for fn in file_patterns):
				yield root, files


def get_rows(outputs, parse):
	for root, files in outputs:
		row = {}
		row['sample_set_no'], row['raw_file_no'] = get_sampleSetNo_rawFileNo(root)
		for file in files:
			row.update(parse(root, file))
		yield row

parse = get_parse(parsers)
outputs = iter_outputs(folder_path, parsers.keys())
# root = "/home/matteo/Projects/lab_scripts/data/RES/2017-121/T180126_40"
# file = "T180126_40_Apex3D.xml"
# list(parse(root,path))
data_frame = pd.DataFrame(get_rows(outputs, parse))
data_frame.to_csv(path_or_buf=csv_path, index=False)
