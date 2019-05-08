from lib import WarningList
import sys
import json
import os
from glob import glob

if len(sys.argv) < 4:
  print("arguments are missing")
  print "search.py pathToWarningLists stringToSearch IOC_TYPE"
  print "search.py ../misp-warninglists/lists/ google.com domain"
  sys.exit()


listPath = os.path.abspath(sys.argv[1])
stringToSearch = sys.argv[2].strip()
iocType = sys.argv[3]

if iocType == 'url':
    sys.exit()

if iocType == 'domain' or iocType == 'hostname':
    iocType = 'hostname'
if iocType == 'ip':
    iocType = 'cidr'


enabledListsFile = os.path.abspath('./enabledLists.json')
enabledListsFileExists = os.path.isfile(enabledListsFile)

enabledLists = []
if enabledListsFileExists:
    enabledLists = open(enabledListsFile).read()
    enabledLists = json.loads(enabledLists)

allListsEnabled = False
if len(enabledLists) == 0:
    # no file present for enabled list means have to consider all the list
    allListsEnabled = True

lists = []
warninglists = {}
for warninglist_file in glob(os.path.join(listPath, '*', 'list.json')):
    with open(warninglist_file, 'r') as f:
        lists.append(json.load(f))

matches = []
for warninglist in lists:
    if allListsEnabled:
        enabledLists.append(warninglist['name'])
    if warninglist['name'] in enabledLists:
        tmp = WarningList(warninglist, True)
        if tmp.slowSearch(stringToSearch, iocType):
            matches.append(warninglist['name'])
if len(matches) != 0:
    print json.dumps(matches)
