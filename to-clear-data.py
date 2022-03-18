
readDir = "./data-collection.txt"
writeDir = "./clear-data-collection.txt"

outfile = open(writeDir,"w")
f = open(readDir,"r")
 
lines_seen = set()  # Build an unordered collection of unique elements.
 
for line in f:
    if line not in lines_seen:
        outfile.write(line)
        lines_seen.add(line)