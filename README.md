
# Scripts for measuring the influence of migrating developers

These look to see how many developers work on projects in
different ecosystems (defined as projects that submit their
packages to language-specific repositories like NPM and CRAN).

Code assumes a file in data/common/<ecosystem>-repos.txt for 
each ecosystem of interest, listing all repositories in that
ecosystem using WoC's naming scheme for repository names.
Most of these lists we got from libraries.io.

## author-activity.py: collect author commits per ecosystem

Reads all commits for each project in an ecosystem
and writes authact.<ecosystem>.e.csv that has
author, ecosystem, package, and the date for each commit

Optional arguments: list of ecosystems; if omitted, uses a hard-coded list
ex: `author-activity.py NPM CRAN Go`

Sample output:
```
author,eco,package,epoch,tz,core,files
<email redacted>,Lua,mah0x211_lua-tointeger,1508289637.0,+0900,1,
<email redacted>,Lua,mah0x211_lua-tointeger,1508289514.0,+0900,1,
```

## Prepare a list of unique author ids committing in all ecosystems
Reads a bunch of authact files and creates a single
list of unique authors (authors.csv)

ex: `extract-authors.py authact.*.e.csv`

## Collect commits across all ecosystems, unifying author identities
Reads from authact files and author alias lookup dictionaries,
and writes a unified author activity file that summarizes
all of a person's activities over multiple ecosystems

The author map file should be a pickled dictionary mapping an
email address to a canonical email address for that person


ex: `substitute-authors.py authormap.dict.pickle authact*.csv`

Writes to unified.authors.csv.gz

Sample output:
```
author,package,epoch,eco
<redacted email>,mah0x211_lua-tointeger,1508289637.0,Lua
<redacted email>,mah0x211_lua-tointeger,1508289514.0,Lua
```

## Prepare tallies of influences from developer migration
Tally a measure of influence among pairs of ecosystems by
counting people who have migrated from one to another

ex: `tally-ecosystem-influences.py`

Sample output:
```
year,influence,proportion,raw_influence,raw_scale,commit_count
2016,Lua,6.560709534926016e-10,3061,42270547,110376
2016,Hex,9.05928449583639e-06,42267486,42270547,110376
2017,Lua,2.3208423734345453e-09,13421,48532270,119154
```


## Prepare package tallies of influences from developer migration
Tally a measure of influence from all other ecosystems on each
package in each ecosystem

Writes some pickled files (using pypi package dill) of
counts useful for later calculation: cmtcount.dill,
cmtcountp.dill, infl.dill

ex: `tally-package-influences.py unified.authors.csv.gz`

Sample output: graph_auth_pkgs_Lua.csv.gz:
```
year,repo,influence,proportion,raw_influence,raw_scale,commit_count_repo,commit_
count_eco,current_ecosystem_use
2017,stefano-m_lua-media_player,Lua,0.05,1200,1200,20,21498,2960,1
2017,stefano-m_lua-media_player,Hex,0.0,0,1200,20,21498,2960,1
2011,mkottman_luaspell,Lua,1.0,19,19,1,4681,9,1
```

Sample output: authtotals.csv.gz
```
author,year,ecosystem,commits
<email redacted>,2015,Lua,0
<email redacted>,2016,Hex,0
<email redacted>,2017,Hex,17
<email redacted>,2018,Hex,7
```

## Summarize migration influence for each pair of ecosystems
Reads the infl.dill file
Creates files for each ecosystem pair summarizing influence
from one to the other, listing the influence from a single
package to another ecosystem.

ex: `extract-specific-influence.py`
    
## Summarize migration influence on each ecosystem
Read from infl files and summarize over the destination, 
with and without normalization. 
Creates: infl_total and infl_normalized files

ex: `calc-net-influence.py`

## Files
data/common/<ecosystem>-repos.txt    List of repos for each ecosystem
