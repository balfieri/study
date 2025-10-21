#!/usr/bin/env python3
#
# grit_words.py - grit words on one page of www.top10000words.com that are in words.out
#
import sys
import time
import random
import string
import os
import os.path
import subprocess
import re

def die( msg, prefix='ERROR: ' ):
    print( prefix + msg )
    sys.exit( 1 )

cmd_en = True

#-----------------------------------------------------------------------
# process command line args
#-----------------------------------------------------------------------
subjects_s = ''
filename = 'words.out'
one_per_line = False

i = 1
while i < len( sys.argv ):
    arg = sys.argv[i]
    i += 1
    if   arg == '-subjects':
        subjects_s = sys.argv[i]
    elif arg == '-one_per_line':           
        one_per_line = int(sys.argv[i])
    elif arg == '-file':
        filename = sys.argv[i]
    else:
        die( f'unknown option: {arg}' )
    i += 1

if subjects_s == '': die( f'no -subjects' )

def cmd( c, echo=True, echo_stdout=False, can_die=True ):  
    if echo: print( c )
    if cmd_en:
        info = subprocess.run( c, shell=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT )
        if echo_stdout: print( info.stdout )
        if can_die and info.returncode != 0: die( f'command failed: {c}' )
        return info.stdout
    else:
        return ''

def match( s, pattern ): 
    return re.compile( pattern ).match( s )

W = open( filename, 'r' )
with open( filename ) as file:
    for line in file:
        if one_per_line:
            m = match( line, r'(.+)$' )
            if m:
                s = m.group(1)
                print( f':{s}' )
                cmd( f'./grit.py -subjects {subjects_s} \"{s}\"', False, True )
            else:
                die( f'bad line: {line}' )
        else:
            # from www.top10000words.com
            m = match( line, r'\d+\s+(\S+)\s+\d+\s+(\S+)\s+\d+\s+(\S+)\s+\d+\s+(\S+)\s+\d+\s+(\S+)' )
            if m:
                words = [m.group(1), m.group(2), m.group(3), m.group(4), m.group(5)]
                for word in words:
                    print( f':{word}' )
                    cmd( f'./grit.py -subjects {subjects_s} \"{word}\"', False, True )
            else:
                die( f'bad line: {line}' )
