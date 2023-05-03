#!/usr/bin/env python3
#
# talk.py - speak definitions using 'say' program
#
import sys
import subprocess
import time
import random
import string
import re

cmd_en = True

def die( msg, prefix='ERROR: ' ):
    print( prefix + msg )
    sys.exit( 1 )

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
if len( sys.argv ) < 1: die( 'usage: talk.py [options]', '' )
subjects_s = 'italian_basic,italian_advanced,italian_expressions_common,italian_expressions_other,american_expressions_get,american_expressions_favorite,italian_vulgar,italian_passato_remoto'
first = 0
english_voice = 'Samantha'
italian_voice = 'Alice'
english_rate  = 180
italian_rate  = 150

i = 1
while i < len( sys.argv ):
    arg = sys.argv[i]
    i += 1
    if   arg == '-subjects':
        subjects_s = sys.argv[i]
        i += 1
    elif arg == '-f': 
        first = int(sys.argv[i])
        i += 1
    else:
        die( f'unknown option: {arg}' )

#-----------------------------------------------------------------------
# read in <subject>.txt files
#-----------------------------------------------------------------------
def say( text, voice, rate ):
    with open( '/tmp/say.txt', 'w' ) as file:
        file.write( text )
    cmd( f'say -v {voice} -r {rate} -f /tmp/say.txt', False )

subjects = subjects_s.split( ',' )
cnt = 0
for subject in subjects:
    filename = subject + '.txt'
    Q = open( filename, 'r' )
    line_num = 0
    while True:
        question = Q.readline()
        if question == '': break
        question = re.sub( r'^\s+', '', question )
        question = re.sub( r'\s+$', '', question )
        if len(question) == 0 or question[0] == '#': continue

        line_num += 1
        answer = Q.readline()
        answer = re.sub( r'^\s+', '', answer )
        answer = re.sub( r'\s+$', '', answer )
        if answer == '': die( f'question at {filename}:{line_num} is not followed by a non-blank answer on the next line: {question}' )
        line_num += 1

        cnt += 1
        if cnt < first: continue

        say( question, english_voice, english_rate )
        say( answer,   italian_voice, italian_rate )

    Q.close()

