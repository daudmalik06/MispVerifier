from lib import WarningList
import sys
import json
import os
from glob import glob
import validators

if len(sys.argv) < 3:
  print("arguments are missing")
  print "search.py pathToWarningLists stringToSearch"
  print "search.py ../misp-warninglists/lists/ google.com"
  sys.exit()


listPath = os.path.abspath(sys.argv[1])
stringToSearch = sys.argv[2].strip()
root_dir = os.path.dirname(os.path.realpath(__file__))

iocType = ''
if validators.domain(stringToSearch):
    iocType = 'hostname'

if validators.ipv4(stringToSearch):
    iocType = 'cidr'

enabledListsFile = os.path.abspath(root_dir + '/enabledLists.json')
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
