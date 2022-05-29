#!/usr/bin/env python3
#
# find_dups.py <subject> - quick script to find duplicates 
#                          with various options for what to do
#
import sys
import time
import random
import string
import re

def die( msg, prefix='ERROR: ' ):
    print( prefix + msg )
    sys.exit( 1 )

#-----------------------------------------------------------------------
# process command line args
#-----------------------------------------------------------------------
if len( sys.argv ) < 2: die( 'usage: find_dups.py <subjects> [options]', '' )
subjects = sys.argv[1].split( ',' )
out_file = ''
i = 2
while i < len( sys.argv ):
    arg = sys.argv[i]
    i += 1
    if   arg == '-out':           
        out_file = sys.argv[i]
        i += 1
    else:
        die( f'unknown option: {arg}' )

#-----------------------------------------------------------------------
# read in <subject>.txt files
#-----------------------------------------------------------------------
uniques_s = ''
answer_to_question = {}
for subject in subjects:
    filename = subject + '.txt'
    Q = open( filename, 'r' )
    line_num = 0
    while True:
        question = Q.readline()
        if question == '': break
        line_num += 1
        question = re.sub( r'^\s+', '', question )
        question = re.sub( r'\s+$', '', question )
        if len(question) == 0 or question[0] == '#': continue

        answer = Q.readline()
        answer = re.sub( r'^\s+', '', answer )
        answer = re.sub( r'\s+$', '', answer )
        if answer == '': die( f'question on line {line_num} is not followed by a non-blank answer on the next line: {question}' )
        line_num += 1

        is_unique = True
        if answer in answer_to_question:
            prev_question = answer_to_question[answer]
            same_question = prev_question == question
            print( f'\n{answer}', end='' )     
            if question == prev_question:
                print( f' - and has same question, so can remove it' )
                is_unique = False
            else:
                print( f' - with different question:' )
                print( f'    old: {prev_question}' )
                print( f'    new: {question}' )
        else:
            answer_to_question[answer] = question

        if is_unique:
            uniques_s += f'{question}\n{answer}\n\n' 
    Q.close()

if out_file != '':
    print( f'\nWriting unique entries to {out_file}...\n' )
    file = open( out_file, 'w' )
    a = file.write( uniques_s )
    file.close()
