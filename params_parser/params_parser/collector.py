import argparse
from pathlib import Path
import json
import pandas as pd

p = argparse.ArgumentParser(description="Parse params.json's into one csv.")
p.add_argument("folder",
    help="Folder to be searched for 'params.json' files.")
p.add_argument("-t", "--target",
               default=Path("./all_params.csv"),
               help="Path to the output csv file [default ./all_params.csv]")
p.add_argument( "-v", "--verbose",
                action='store_const',
                const=True,
                default=False,
                help="Show all verbosely.")
a = p.parse_args()
if a.verbose:
    print(a.__dict__)

# path = Path("/home/matteo/Projects/lab_scripts/projectizer2/data/2018-061")
def parse_all_params(path, verbose=False):
    """Parse all jsons with params recursively under the given path.

    WE DO ASSUME that in that folder there will be no other files named
    like 'params.json'. Otherwisem write your own script.

    Args:
        path (str): Path where to search for params.json.
    Yields:
        dictionary with params from the xml files from Symphony Pipeline results.
    """
    path = Path(path)
    for f in path.glob("**/params.json"):
        with f.open('r') as g:
            yield json.load(g)
        if verbose:
            print("parsed {}".format(str(f)))

X = pd.DataFrame(parse_all_params(a.folder, a.verbose))
X.to_csv(path_or_buf=a.target, index=False)