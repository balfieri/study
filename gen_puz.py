#!/usr/bin/env python3
#
# gen_puz.py - generates crossword puzzles for all interesting categories
#
import sys
import os
import os.path
import subprocess
import time
import string
import re

subjects = [ 'italian_advanced',
             'italian_basic',
             'italian_expressions',
             'italian_slang',
             'italian_vulgar' ]

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
side = 15
count = 10

i = 2
while i < len( sys.argv ):
    arg = sys.argv[i]
    i += 1
    if   arg == '-side':           
        side = int(sys.argv[i])
        i += 1
    elif arg == '-count':
        count = int(sys.argv[i])
        i += 1
    else:
        die( f'unknown option: {arg}' )

#-----------------------------------------------------------------------
# Generate the individual puzzles.
#-----------------------------------------------------------------------
seed = 1000000
for subject in subjects:
    for reverse in range(2):
        for i in range(count):
            title = f'{subject}_s{seed}_r{reverse}'
            cmd( f'./puz.py {subject} -side {side} -seed {seed} -reverse {reverse} -title {title} > www/{title}.html' )
            seed += 1
