#!/usr/bin/env python3
#
# getwww.py <url> - return text contents of URL
#
import sys
import requests
if len( sys.argv ) != 2: die( 'usage: getwww.py <url>', '' )
r = requests.get( sys.argv[1] )
print(r.text)
