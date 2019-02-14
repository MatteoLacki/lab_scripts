import argparse

from source import dump_params_to_jsons


p = argparse.ArgumentParser(description="Dump parameters from xml files into jsons.")
p.add_argument("folder", help="Folder to be searched for results.")
p.add_argument( "-v", "--verbose",
                action='store_const',
                const=True,
                default=False,
                help="Show all verbosely.")
a = p.parse_args()

# fp = "/home/matteo/Projects/lab_scripts/projectizer2/data"
# dump_params_to_jsons(fp, True)
dump_params_to_jsons(a.folder, a.verbose)