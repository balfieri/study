#!/usr/bin/env python3
#
# run <subject>
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
if len( sys.argv ) != 2: die( 'usage: run <subject>', '' )
filename = sys.argv[1] + '.txt'
Q = open( filename, 'r' )
questions = []
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

    questions.append( question )
    questions.append( answer )
Q.close()

#-----------------------------------------------------------------------
# keep trying to run a new test
#-----------------------------------------------------------------------
random.seed( time.time() )

question_cnt = len( questions ) >> 1
if question_cnt == 0: die( 'no questions found in ' + filename )

while True:
    #-----------------------------------------------------------------------
    # choose questions
    #-----------------------------------------------------------------------
    count = int( prompt( '\nNumber of questions', str(min( question_cnt, 20 )) ) )
    count = min( count, question_cnt )

    which = []
    asked = {}
    for i in range( count ):
        while True:
            ii = rand_n( question_cnt )
            if ii not in asked: break
        asked[ii] = True
        which.append( ii )

    #-----------------------------------------------------------------------
    # keep trying to test questions that haven't been answered correctly
    #-----------------------------------------------------------------------
    while len( which ) != 0:
        for i in range( 100 ): print()
        correct_cnt = 0
        count = len( which )
        missed = []
        while len( which ) != 0:
            ii = which.pop( 0 )
            q = questions[ii*2]
            a = questions[ii*2+1]
            a_lc = a.lower()

            ua = prompt( '\n' + q ).lower()
            if ua == a_lc: 
                correct_cnt += 1
            else:
                print( 'Wrong!  ' + a )
                missed.append( ii )
        pct = int( 100.0 * correct_cnt / count + 0.5 )
        print( '\nYou got ' + str(correct_cnt) + ' out of ' + str(count) + ' questions correct (' + str(pct) + '%)' ) 
        if len( missed ) != 0 and prompt( '\nRetry missed questions?', 'y' ) == 'y': 
            which = missed
    if prompt( '\nPlay again?', 'y' ) != 'y': break 

print( '\nGoodbye!\n' )
sys.exit( 0 )
