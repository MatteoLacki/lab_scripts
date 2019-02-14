from pathlib import Path
import re
import json
import os


def read_line(path, n):
	"""Read a line in a file.

	Args:
		f (str or pathlib.Path): Path to the csv with data.
		n (int): number of line to output.
	"""
	with open(path, "r") as f:
		for i in range(n+1):
			x = f.readline()
	return x


def parse_stats(path):
	"""Parse the _stat.csv file in the output of the pipeline.

	Args:
		f (str or pathlib.Path): Path to the folder with csv.
	"""
	x = ('stat:sample','stat:mode','stat:queries','stat:peptides','stat:proteins')
	y = read_line(path, 1).replace('\n','').split(",")[1:]
	yield from zip(x,y)


def parse_xml_params(path, prefix=""):
	"""A quicker XML parser.

	Args:
		path (str or pathlib.Path): path to the xml file.
		prefix (str): prefix to the name of the parameter.
	Yields:
		tuples (parameter, value).
	"""
	with open(path, 'r') as f:
		for l in f:
			if "PARAM NAME" in l:
				w = l.split('"')
				k = w[1]
				v = w[3]
				try:
					v = v.replace(',','.')
					v = float(v)
				except ValueError:
					pass
				yield "{}{}".format(prefix, k), v
			if "</PARAMS>" in l:
				break


def parse_folder(f):
	"""Parse the contents of a folder.

	Only if the folder contains one of files matching the patter,
	will it ever output anything. Matches include:
		*_Apex3D.xml
		*_Pep3D_Spectrum.xml
		*_workflow.xml

	Args:
		f (str or pathlib.Path): Path to the folder with data.
	"""
	f = Path(f)
	for prefix, suffix in (("apex:","*_Apex3D.xml"),
						   ("spec:","*_Pep3D_Spectrum.xml"),
						   ("work:","*_workflow.xml")):
		for file in f.glob(suffix):
			for param in parse_xml_params(file, prefix):
				yield param


def get_sampleSetNo_rawFileNo(f):
	"""Get sample set and raw file numbers of a folder with data.

	Args:
		f (str or pathlib.Path): Path to the folder with data.
	"""
	f = Path(f)
	return f.parent.name, f.name


sample_set = re.compile("20\d+-\d+")
raw_file = re.compile("\d+_\d+")


def iter_output_path(fp):
	"""Iterate over paths that match the pattern containing xmls.

	Args:
		fp (str or path): path to where to recursively look into.
	Yields:
		A sequence of paths to the folders with data.
	"""
	for r, _, _ in os.walk(fp):
		sampleSetNo, rawFileNo = get_sampleSetNo_rawFileNo(r)
		if raw_file.search(rawFileNo) and sample_set.search(sampleSetNo):
			yield Path(r)


def dump_params_to_jsons(fp, verbose=True):
	if verbose:
		print("Searching for files in {}".format(fp))
	for p in iter_output_path(fp):
		param_dict = dict(parse_folder(p))
		if param_dict:
			try:
				with (p/"params.json").open('w') as h:
					json.dump(param_dict, h, indent=3)
				if verbose:
					print("Dumped {}.".format(p))
			except Exception as e:
				print(e)
				print(p)
	if verbose:
		print('Thank you for patience.')