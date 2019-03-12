from pathlib import Path

fp = Path("/home/matteo/Projects/lab_scripts/projectizer2/data/2018-061")


f = fp


paths = ["/home/matteo/Projects/lab_scripts/projectizer2/data/2018-061/S180826_20",
 "/home/matteo/Projects/lab_scripts/projectizer2/data/2018-061/S180826_21",
 "/home/matteo/Projects/lab_scripts/projectizer2/data/2018-061/S180826_22"]

paths = [Path(p) for p in paths]
p = paths[0]
p = paths[1]







