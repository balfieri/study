#!/usr/bin/env python3
#
# grit.py <string> - search for string in existing definitions
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

#-----------------------------------------------------------------------
# process command line args
#-----------------------------------------------------------------------
if len( sys.argv ) < 2: die( 'usage: grit.py <string> [options]', '' )
string = sys.argv[1]
subjects_s = 'italian_basic,italian_advanced,italian_expressions_common,italian_expressions_other,american_expressions_get,american_expressions_favorite,italian_vulgar,italian_passato_remoto,italian_tongue_twisters'
search_question = True
search_answer = True
out_file = ''
i = 2
while i < len( sys.argv ):
    arg = sys.argv[i]
    i += 1
    if   arg == '-subjects':
        subjects_s = sys.argv[i]
        i += 1
    elif arg == '-q':
        search_question = int(sys.argv[i])
        i += 1
    elif arg == '-a':
        search_answer = int(sys.argv[i])
        i += 1
    else:
        die( f'unknown option: {arg}' )

#-----------------------------------------------------------------------
# read in <subject>.txt files
#-----------------------------------------------------------------------
subjects = subjects_s.split( ',' )
for subject in subjects:
    filename = subject + '.txt'
    Q = open( filename, 'r' )
    line_num = 0
    while True:
        question = Q.readline()
        if question == '': break
        line_num += 1
        ques_line_num = line_num
        question = re.sub( r'^\s+', '', question )
        question = re.sub( r'\s+$', '', question )
        if len(question) == 0 or question[0] == '#': continue

        answer = Q.readline()
        answer = re.sub( r'^\s+', '', answer )
        answer = re.sub( r'\s+$', '', answer )
        if answer == '': die( f'question at {filename}:{line_num} is not followed by a non-blank answer on the next line: {question}' )
        line_num += 1

        if (search_question and match( question, f'.*{string}' )) or (search_answer and match( answer, f'.*{string}' )):
            print()
            print( f'{filename}:{ques_line_num}:    {question}' )
            print( f'{filename}:{line_num}:    {answer}' )

    Q.close()

