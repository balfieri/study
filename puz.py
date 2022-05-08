#!/usr/bin/env python3
#
# puz.py <subjects> [options]
#
# This program generates a random crossword puzzle in .puz format from 
# questions taken from one or more subject files.
#
import sys
import time
import random
import string
import re

def die( msg, prefix='ERROR: ' ):
    print( prefix + msg )
    sys.exit( 1 )

def rand_n( n ):
    return int( random.random() * n )

#-----------------------------------------------------------------------
# process command line args
#-----------------------------------------------------------------------
if len( sys.argv ) < 2: die( 'usage: puz.py <subjects> [options]', '' )
subjects = sys.argv[1].split( ',' )
side = 15
reverse = False
seed = time.time()
out_file = ''
i = 2
while i < len( sys.argv ):
    arg = sys.argv[i]
    i += 1
    if   arg == '-side':           
        side = int(sys.argv[i])
        i += 1
    elif arg == '-reverse':          
        reverse = int(sys.argv[i]) == 1
        i += 1
    elif arg == '-out_file':
        out_file = sys.argv[i]
        i += 1
    elif arg == '-seed':
        seed = int(sys.argv[i])
        i += 1
    else:
        die( f'unknown option: {arg}' )

if out_file == '': die( 'must supply -out_file <file>' )
random.seed( seed )

#-----------------------------------------------------------------------
# Read in <subject>.txt files.
#-----------------------------------------------------------------------
entries = []
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
        answer = answer.lower()
        if answer == '': die( f'question on line {line_num} is not followed by a non-blank answer on the next line: {question}' )
        line_num += 1

        if reverse:
            tmp = question
            question = answer
            answer = tmp

        entries.append( [question, answer] )
    Q.close()

#-----------------------------------------------------------------------
# Pull out all interesting answer words and put them into an array, 
# with a reference back to the original question.
#-----------------------------------------------------------------------
words = []
for entry in entries:
    question = entry[0]
    answers = entry[1]
    aa = answers.split( '; ' )
    for a in aa:
        ww = a.split()
        for w in ww:
            ww2 = w.split( '\'' )
            for w2 in ww2:
                w3 = re.sub( r'[\!\?]', '', w2 )
                if len( w3 ) > 3:
                    words.append( [w2, entry] )
                    print( w3 )

#-----------------------------------------------------------------------
# Generate the puzzle from the data structure using this simple algorithm:
#
#     for some number attempts:
#         pick a random word from the list
#         if the word is already in the grid: continue
#         for each across/down location of the word:
#             score the placement of the word in that location
#         if score > 0:
#             add the word to a location with the best score
#-----------------------------------------------------------------------
