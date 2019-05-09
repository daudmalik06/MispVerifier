# MispVerifier
python script to check the value in misp warning list depending on the type of list (hostname, cidr, string, substring)

Pythonic way to work with the warning lists defined there: https://github.com/MISP/misp-warninglists

# Installation
pip install -r requirements.txt



# to search for an entity in warning lists

python search.py warningListFolder stringToSearch

> warningListFolder will be downloaded from https://github.com/MISP/misp-warninglists

e.g:    
  
    python search.py ../misp-warninglists/lists youtube.com

# Enabled Warning lists
If you want to consider only few warning list you can do it by saving their names in **enabledLists.json**, to see the format please check **enabledLists.json.example** file.
