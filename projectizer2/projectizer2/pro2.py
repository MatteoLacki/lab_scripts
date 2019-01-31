import sys
import os
import re

from parsers import parsers, get_sampleSetNo_rawFileNo, get_parse


verbose = True
folder_path, csv_path = sys.argv[1:3]
# folder_path = "/home/matteo/Projects/lab_scripts/projectizer2/data/2018-061"
# csv_path = "/home/matteo/Projects/lab_scripts/projectizer2/tests/project2.csv"


glob(os.path.join(folder_path, ""))

os.listdir(folder_path)
it = os.walk(folder_path)
root, dirs, files = next(it)




sn_pattern = re.compile("\d+-\d+")
rf_pattern = re.compile("(S|T)\d+_\d+")
file_patterns = re.compile("")

folder_pattern = re.compile("\d+-\d+/.\d+_\d+") # windows? linux = /
bool(folder_pattern.search(root))
look_for = ("_Pep3D_Spectrum.csv", "_workflow.xml")

for f in files:
	for p in look_for:


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
		ss, rf = row['sample_set_no'], row['raw_file_no'] = get_sampleSetNo_rawFileNo(root)
		for file in files:
			row.update(parse(root, file))
		yield row
		if verbose:
			print("Finished sample set {} and raw file {}.".format(ss, rf))

parse = get_parse(parsers)
outputs = iter_outputs(folder_path, parsers.keys())
# root = "/home/matteo/Projects/lab_scripts/data/RES/2017-121/T180126_40"
# file = "T180126_40_Apex3D.xml"
# list(parse(root,path))
data_frame = pd.DataFrame(get_rows(outputs, parse))
data_frame.to_csv(path_or_buf=csv_path, index=False)
