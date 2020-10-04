#!/usr/bin/env python3
#
# run <subject> [question_cnt]
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

def min( a, b ):
    return a if a < b else b

def prompt( s, default='' ):
    def_str = '' if default == '' else (' [' + default + ']')
    ans = input( s + def_str + ': ' )
    ans = re.sub( r'^\s+', '', ans )
    ans = re.sub( r'\s+$', '', ans )
    if ans == '': ans = default 
    return ans

#-----------------------------------------------------------------------
# read in <subject>.txt file
#-----------------------------------------------------------------------
if len( sys.argv ) < 2: die( 'usage: run <subject> [question_cnt]', '' )
filename = sys.argv[1] + '.txt'
question_cnt = int(sys.argv[2]) if len( sys.argv ) >= 3 else 20
Q = open( filename, 'r' )
all_questions = []
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
    if answer == '': die( 'question on line ' + line_num + ' is not followed by a non-blank answer on the next line' )
    line_num += 1

    all_questions.append( question )
    all_questions.append( answer )
Q.close()

#-----------------------------------------------------------------------
# keep trying to run a new test
#-----------------------------------------------------------------------
random.seed( time.time() )

all_question_cnt = len( all_questions ) >> 1
if all_question_cnt == 0: die( 'no questions found in ' + filename )
question_cnt = min( question_cnt, all_question_cnt )

while True:
    #-----------------------------------------------------------------------
    # choose questions
    #-----------------------------------------------------------------------
    curr_questions = []
    asked = {}
    for i in range( question_cnt ):
        while True:
            ii = rand_n( all_question_cnt )
            if ii not in asked: break
        asked[ii] = True
        curr_questions.append( ii )

    #-----------------------------------------------------------------------
    # keep trying to ask questions that haven't been answered correctly
    #-----------------------------------------------------------------------
    while len( curr_questions ) != 0:
        for i in range( 100 ): print()
        curr_question_cnt = len( curr_questions )
        correct_cnt = 0
        missed_questions = []
        while len( curr_questions ) != 0:
            ii = curr_questions.pop( 0 )
            q = all_questions[ii*2]
            a = all_questions[ii*2+1]
            a_lc = a.lower()

            ua = prompt( '\n' + q ).lower()
            if ua == a_lc: 
                correct_cnt += 1
            else:
                print( 'Wrong!  ' + a )
                missed_questions.append( ii )
        pct = int( 100.0 * correct_cnt / curr_question_cnt + 0.5 )
        print( '\nYou got ' + str(correct_cnt) + ' out of ' + str(curr_question_cnt) + ' questions correct (' + str(pct) + '%)' ) 
        if len( missed_questions ) != 0 and prompt( '\nRetry missed questions?', 'y' ) == 'y': 
            curr_questions = missed_questions
    if prompt( '\nPlay again?', 'y' ) != 'y': break 

print( '\nGoodbye!\n' )
sys.exit( 0 )
