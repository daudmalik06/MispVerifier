from lib import WarningList
import sys
import json
import os
from glob import glob

if len(sys.argv) < 3:
  print("arguments are missing")
  print "search.py pathToWarningLists stringToSearch"
  sys.exit()

stringToSearch = sys.argv[2]
listPath = os.path.abspath(sys.argv[1])

lists = []
warninglists = {}
for warninglist_file in glob(os.path.join(listPath, '*', 'list.json')):
    with open(warninglist_file, 'r') as f:
        lists.append(json.load(f))

matches = []
for warninglist in lists:
    tmp = WarningList(warninglist, True)
    if tmp.slowSearch(stringToSearch):
        matches.append(warninglist['name'])

print json.dumps(matches)
