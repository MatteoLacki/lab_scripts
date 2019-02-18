import argparse

from source import dump_params_to_jsons, iter_output_path


p = argparse.ArgumentParser(description="Dump parameters from xml files into jsons.")
p.add_argument("folder", help="Folder to be searched for results.")
p.add_argument( "-r", "--recursive",
                action='store_const',
                const=True,
                default=False,
                help="Show all verbosely.")
p.add_argument( "-v", "--verbose",
                action='store_const',
                const=True,
                default=False,
                help="Show all verbosely.")
a = p.parse_args()
# fp = "/home/matteo/Projects/lab_scripts/projectizer2/data"

file_paths = iter_output_path(a.folder) if a.recursive else [a.folder]
dump_params_to_jsons(file_paths, a.verbose)
