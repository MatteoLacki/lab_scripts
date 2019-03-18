import argparse

from source import dump_params_to_jsons, iter_input_folders


p = argparse.ArgumentParser(description="Dump parameters from xml files into jsons.")
p.add_argument( "folders",
                nargs="+",
                help="Folder(s) to be searched for results.")
p.add_argument( "-r", "--recursive",
                action='store_const',
                const=True,
                default=False,
                help="Parse files recursively within the submitted folders?")
p.add_argument( "-v", "--verbose",
                action='store_const',
                const=True,
                default=False,
                help="Show all verbosely.")
a = p.parse_args()
if a.verbose:
    print(a.folders)
file_paths = iter_input_folders(a.folders, a.recursive)
dump_params_to_jsons(file_paths, a.verbose)
