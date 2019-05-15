from lib import WarningList
import sys
import json
import os
from glob import glob
import validators
import tldextract

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
    domain = tldextract.extract(stringToSearch)
    currentDomain = domain.domain + '.' + domain.suffix
    if domain.subdomain == 'www':
        # remove www. from hostname
        stringToSearch = currentDomain

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

tmpSearchString = stringToSearch
matches = []
for warninglist in lists:
    if allListsEnabled:
        enabledLists.append(warninglist['name'])
    if warninglist['name'] in enabledLists:
        if 'Alexa' in warninglist['name'] and iocType == 'hostname':
            # only for alexa top list we'll check domain name only
            stringToSearch = currentDomain
        tmp = WarningList(warninglist, True)
        if tmp.slowSearch(stringToSearch, iocType):
            matches.append(warninglist['name'])
        # reset the string to search
        stringToSearch = tmpSearchString
if len(matches) != 0:
    print json.dumps(matches)
