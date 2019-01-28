# Make the header for the csv.
find -name '*stats.csv' -print -quit | xargs sed -n 1p > res.csv
# Append all the entires to the csv.
find -name '*stats.csv' -print0 | xargs -0 -n 1 sed -n 2p >> res.csv
