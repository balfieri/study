#!/usr/bin/env python3
#
# fix.py <subject> - quick script to munge various input formats into the canonical format
#
import sys
import time
import random
import string
import re

def die( msg, prefix='ERROR: ' ):
    print( prefix + msg )
    sys.exit( 1 )

def match( s, pattern ): 
    return re.compile( pattern ).match( s )

def subst( s, pattern, subst ):
    return re.sub( pattern, subst, s )

if len( sys.argv ) != 2: die( 'usage: fix.py <subject>' )
subject = sys.argv[1]
filename = subject + '.txt'
file = open( filename, 'r' )
lines = file.readlines()
file.close()
line_num = 0
for line in lines:
    line_num += 1
    line = re.sub( r'^\s+', '', line )
    line = re.sub( r'\s+$', '', line )
    if line == '': continue
    m = match( line, r'^(.*) = (.*)$' )
    if not m: die( "bad input: " + line )
    answer = m.group( 1 )
    answer = answer[0].lower() + answer[1:]
    question = m.group( 2 )
    question = question[0].lower() + question[1:]
    print( question )
    print( answer )
    print()
