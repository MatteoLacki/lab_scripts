"""
Prepare a csv input for ISOQuant.
It is a projectizer v. 2.0

Author: MatteoLacki
"""

import argparse
import json
from pathlib import Path

from source import dump_to_csv


p = argparse.ArgumentParser(description="Prepare a csv input file for ISOQuant. The files should include the necessary 'params.json' file.")
p.add_argument("folders",
    help="Folders to be included in the ISOQuant analysis.",
    nargs="+")
p.add_argument("-t", "--target",
               default=Path("./project.csv"),
               help="Path to the output csv file [default ./project.csv]")
p.add_argument( "-v", "--verbose",
                action='store_const',
                const=True,
                default=False,
                help="Show all verbosely.")
a = p.parse_args()
if a.verbose:
    print(a.__dict__)



def iter_rows(paths, header=True, verbose=False):
    """Iterate over all folders containing the results from output.

    Args:
        path (str): Path to the root of the folder-tree being search.
        file_patterns (tuple): These strings should be present in the names of files that qualify to be parsed.
    """
    if header:
        yield ("acquired_name", "peptide3d_xml", "iaDBs_xml", "sample_description")
    for p in paths:
        p = Path(p)
        with open(p/"params.json", 'r') as f:
            sample_desc = json.load(f)['work:SampleDescription']
        try:
            pep3dspec = next(p.glob("*_Pep3D_Spectrum.xml"))
        except StopIteration as e:
            print("Attention: File {} was not analysed as '*_Pep3D_Spectrum.xml' was (most likely) missing.".format(p.name))
            raise(e)
        try:
            workflow = next(p.glob("*_workflow.xml"))
        except RuntimeError as e:
            print("Attention: File {} was not analysed as '*_workflow.xml' was (most likely) missing.".format(p.name))
            raise(e)
        if verbose:
            print(p.name, pep3dspec, workflow, sample_desc)
        yield p.name, pep3dspec, workflow, sample_desc

try:
    dump_to_csv(iter_rows(a.folders, True, a.verbose), a.target)
    print("Thank you for using our services. Have a good day!")
except RuntimeError:
    print("WARNING: ERRORS ENCOUNTERED!!!")
