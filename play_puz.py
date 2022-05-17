#!/usr/bin/env python3
#
# play_puz.py - generate one puzzle and play it right now
#
import sys
import os
import os.path
import subprocess
import time
import string
import re
import datetime

def die( msg, prefix='ERROR: ' ):
    print( prefix + msg )
    sys.exit( 1 )

cmd_en = True

def cmd( c, echo=True, echo_stdout=False, can_die=True ):  
    if echo: print( c )
    if cmd_en:
        info = subprocess.run( c, shell=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT )
        if echo_stdout: print( info.stdout )
        if can_die and info.returncode != 0: die( f'command failed: {c}' )
        return info.stdout
    else:
        return ''

#-----------------------------------------------------------------------
# process command line args
#-----------------------------------------------------------------------
subject = 'italian_advanced'
side = 15
seed = int( time.time() )
reverse = 0

i = 1
while i < len( sys.argv ):
    arg = sys.argv[i]
    i += 1
    if   arg == '-subject':
        subject = sys.argv[i]
        i += 1
    elif arg == '-side':           
        side = int(sys.argv[i])
        i += 1
    elif arg == '-seed':
        seed = int(sys.argv[i])
        i += 1
    elif arg == '-reverse':
        reverse = int(sys.argv[i])
        i += 1
    else:
        die( f'unknown option: {arg}' )

cmd( f'./gen_puz.py {subject} -side {side} -seed {seed} -reverse {reverse} > www/one.html' )
cmd( f'open -a Safari www/one.html' )
