import sys
from glob import glob

in_pattern, out_path = sys.argv[1:3]

def read_line(path, n):
	with open(path, "r") as f:
		for i in range(n+1):
			x = f.readline()
	return x

with open(out_path, "w+") as f:
	f.write("file,sample,mode,queries,peptides,proteins\n")
with open(out_path, "a+") as f:
	for path in glob(in_pattern):
		f.write(read_line(path,1)) 
		
print("Results saved to {}".format(out_path))