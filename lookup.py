#!/usr/bin/env python3
#
# lookup.py <word> - look up word on treccani.it
#
import requests
r = requests.get('https://www.treccani.it/vocabolario/ricerca/rozzo/')
print(r.text)
