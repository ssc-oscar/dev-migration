import csv
import gzip
import sys
import pickle
# author,eco,package,epoch,tz,core,files
# sambadevi <t.otlik93@gmail.com>,Atom,sambadevi_atom-devrant,1496862886,+0200,1,

authormap = sys.argv[1]

unmask = pickle.load(open(authormap,"r"))
outp = csv.writer(gzip.open("data/unified.authors.csv.gz","wb"))
outp.writerow(["author","package","epoch","eco"])
for f in sys.argv[2:]:
    print f
    for row in csv.DictReader(open(f,"r")):
        try:
            row["author"] = unmask.get(row["author"].strip(),row["author"].strip())
        except Exception, e:
            print row["author"]
        outp.writerow([row["author"],row["package"],row["epoch"],row["eco"]])

