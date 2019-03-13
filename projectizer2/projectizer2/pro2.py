import sys import os import re

from parsers import parsers, get_sampleSetNo_rawFileNo
from csv_tsv import write_rows

verbose = True
folder_path, csv_path = sys.argv[1:3]
folder_pattern = re.compile("\d+-\d+/.\d+_\d+") # windows? linux = /



def iter_outputs(folder_path, header=True):
    """Iterate over all folders containing the results from output.

    Args:
        folder_path (str): Path to the root of the folder-tree being search.
        file_patterns (tuple): These strings should be present in the names of files that qualify to be parsed.
    """
    file_patterns = ("_workflow.xml", "_Pep3D_Spectrum.xml")
    if header:
        yield ("acquired_name", "peptide3d_xml", "iaDBs_xml", "sample_description")
    for root, dirs, files in os.walk(folder_path):
        if folder_pattern.search(root):
            ss, rf = get_sampleSetNo_rawFileNo(root)
            r = {p: os.path.join(root,f) for f in files for p in file_patterns if p in f}
            yield rf, r[file_patterns[0]], r[file_patterns[1]], parse_xml_params(r[file_patterns[1]])

if __name__ == '__main__':
    write_rows(iter_outputs(folder_path), csv_path)


def test_outputs(os='mac'):
    if os is 'mac':
        csv_path = "/Users/matteo/Projects/lab_scripts/projectizer2/tests/project2.csv"
        folder_path = "/Users/matteo/Projects/lab_scripts/projectizer2/2018-061"
    if os is 'linux':
        folder_path = "/home/matteo/Projects/lab_scripts/projectizer2/data/2018-061"
        csv_path = "/home/matteo/Projects/lab_scripts/projectizer2/tests/project2.csv"
    write_rows(iter_outputs(folder_path), csv_path)
