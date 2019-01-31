from os.path import join, split
import xml.etree.ElementTree as ET

def read_line(path, n):
	"""Read a line in a file."""
	with open(path, "r") as f:
		for i in range(n+1):
			x = f.readline()
	return x


def parse_stats(path):
	"""Parse the _stat.csv file in the output of the pipeline."""
	x = ('stat:sample','stat:mode','stat:queries','stat:peptides','stat:proteins')
	y = read_line(path, 1).replace('\n','').split(",")[1:]
	yield from zip(x,y)


# def make_xml_parser(col_prefix=""):
# 	def parse_xml_params(path):
# 		tree = ET.parse(path)
# 		root = tree.getroot()
# 		for p in root.find('PARAMS'):
# 			yield ":".join((col_prefix, p.attrib['NAME'])), p.attrib['VALUE']
# 	return parse_xml_params


def make_xml_parser(col_prefix=""):
	def parse_xml_params(path):
		"""Hopefully a quicker XML parser."""
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
					yield "{}:{}".format(col_prefix, k), v 
				if "</PARAMS>" in l:
					break
	return parse_xml_params



def get_parse(parsers):
	def parse(root, file):
		for pattern, parser in parsers.items():
			if pattern in file:
				yield from parsers[pattern](join(root,file))
	return parse

def get_sampleSetNo_rawFileNo(root):
	"""Extract sample set and raw file numbers from a folder that contains data."""
	sample_set_no, raw_file_no = split(root)
	_, sample_set_no = split(sample_set_no)
	return sample_set_no, raw_file_no


parsers = {'_stats.csv':parse_stats,
		   '_Apex3D.xml':make_xml_parser("apex"),
		   '_Pep3D_Spectrum.xml':make_xml_parser("spec"),
		   '_workflow.xml':make_xml_parser("work")}
