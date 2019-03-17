from oscar import *
import gzip
import csv
import sys
import datetime
import pytz


localfiles = "data/"

if len(sys.argv) > 1:
    ecos = sys.argv[1:]
else:
    ecos = "Atom Bioconductor Cargo CocoaPods CPAN CRAN Go Hackage Hex Lua Maven NPM NuGet Packagist Pypi Rubygems Stackage Eclipse".split(" ")

def projects(eco): return "data/common/%s-repos.txt" % (eco,)

def interesting(filename):
    end = filename.split("/")[-1]
    if len(end) < len(filename): return None
    if end[-2:]=="md" or end[-3:] == "txt" or end[-4:]=="json" or \
       end[-3:] == "xml" or "." not in end or end[-4:]=="toml" or \
       end[-2:] == "ac" or end[-3:] == "yml":
        return end
    else:
        return None

epoch = datetime.datetime(1970,1,1,0,0,0,0,pytz.UTC)

for eco in ecos:
    seen = set()
    csvf = csv.writer(open(localfiles + "authact.%s.e.csv" % (eco,), "w"))
    csvf.writerow("author,eco,package,epoch,tz,core,files".split(","))
    print "\n", eco
    for project in open(projects(eco)).readlines():
        prj = project.strip()
        print prj
        for sha in Project(prj).commit_shas:
            if sha not in seen:
                try:
                    commit = Commit(sha)
                    author = commit.author
                    when = int((commit.authored_at - epoch).total_seconds())
                    tz = commit.authored_at.strftime("%z")

                    # Specific list of files not implemented right now
                    files = "" #";".join([i for i in [interesting(fn) for fn in commit.tree.files.keys()] if i is not None])

                    csvf.writerow([author,eco,prj,when,tz,1,files])
                    seen.add(sha)
                except Exception, e:
                    print "Error", type(e), e
                    pass
