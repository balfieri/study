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

filename = 'words.out'

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

def match( s, pattern ): 
    return re.compile( pattern ).match( s )

W = open( filename, 'r' )
with open( filename ) as file:
    for line in file:
        m = match( line, r'\d+\s+(\S+)\s+\d+\s+(\S+)\s+\d+\s+(\S+)\s+\d+\s+(\S+)\s+\d+\s+(\S+)' )
        if m:
            words = [m.group(1), m.group(2), m.group(3), m.group(4), m.group(5)]
            for word in words:
                cmd( f'./grit.py {word}', True, True )
        else:
            die( f'bad line: {line}' )
