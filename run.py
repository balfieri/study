#!/usr/bin/env python3
#
# run.py <subject> [options]
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

def max( a, b ):
    return a if a > b else b

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
if len( sys.argv ) < 2: die( 'usage: run.py <subject> [options]', '' )
filename = sys.argv[1] + '.txt'
question_cnt = int(sys.argv[2]) if len( sys.argv ) >= 3 else 20
skip_prompts = len(sys.argv) >= 4
skip_pause_sec = int(sys.argv[3]) if skip_prompts else 0
file_start_pct = int(sys.argv[4]) if len(sys.argv) >= 5 else 0
file_end_pct   = int(sys.argv[5]) if len(sys.argv) >= 6 else 100
if file_start_pct < 0 or file_end_pct < 0: die( 'file_start_pct and file_end_pct must be >= 0' )
if file_end_pct > 100: die( 'file_end_pct must be <= 100' )
if file_start_pct >= file_end_pct: die( 'file_start_pct must be < file_end_pct' )
acronyms_only  = int(sys.argv[6]) if len(sys.argv) >= 7 else 0

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

    if acronyms_only == 0 or (re.match( r'^[A-Z0-9\s]+$', question ) and len(question) >= acronyms_only):
        all_questions.append( question )
        all_questions.append( answer )
Q.close()

#-----------------------------------------------------------------------
# keep trying to run a new test
#-----------------------------------------------------------------------
random.seed( time.time() )

all_question_cnt = len( all_questions ) >> 1
if all_question_cnt == 0: die( 'no questions found in ' + filename )
all_question_first = int(file_start_pct*all_question_cnt/100.0)
all_question_last  = min(int(file_end_pct*all_question_cnt/100.0), all_question_cnt-1)
all_question_used_cnt = all_question_last - all_question_first + 1

if question_cnt == 0: 
    question_cnt = all_question_used_cnt
else:
    question_cnt = min( question_cnt, all_question_used_cnt )
    question_cnt = max( 1, question_cnt )
print( f'Number of questions in the file is {all_question_cnt}, using questions {all_question_first}..{all_question_last}, asking {question_cnt} questions\n' )        

while True:
    #-----------------------------------------------------------------------
    # choose questions
    #-----------------------------------------------------------------------
    curr_questions = []
    asked = {}
    for i in range( question_cnt ):
        while True:
            ii = all_question_first + rand_n( all_question_used_cnt )
            if ii not in asked: break
        asked[ii] = True
        curr_questions.append( ii )

    #-----------------------------------------------------------------------
    # keep trying to ask questions that haven't been answered correctly
    #-----------------------------------------------------------------------
    while True:
        curr_question_cnt = len( curr_questions )
        correct_cnt = 0
        missed_questions = []
        while len( curr_questions ) != 0:
            ii = curr_questions.pop( 0 )
            q = all_questions[ii*2]
            a = all_questions[ii*2+1]
            a_lc = a.lower()

            if skip_prompts:
                for i in range(2):
                    s = q if i == 0 else a
                    print( s + (':' if i == 0 else '\n') )
                    pause_sec = skip_pause_sec if len(s) <= 40 else int(skip_pause_sec * len(s) / 40)   # more time for long strings
                    time.sleep( pause_sec )
            else:
                ua_lc = prompt( '\n' + q ).lower()
                if ua_lc == a_lc: 
                    correct_cnt += 1
                else:
                    prefix = 'Wrong!  ' if ua_lc != '' else ''
                    print( prefix + a )
                    missed_questions.append( ii )
        if skip_prompts: break
        pct = int( 100.0 * correct_cnt / curr_question_cnt + 0.5 )
        print( '\nYou got ' + str(correct_cnt) + ' out of ' + str(curr_question_cnt) + ' questions correct (' + str(pct) + '%)' ) 
        if len( missed_questions ) == 0 or prompt( '\nRetry missed questions?', 'y' ) != 'y': break
        curr_questions = missed_questions
        for i in range( 100 ): print()
    if skip_prompts or prompt( '\nPlay again?', 'y' ) != 'y': break 

print( '\nGoodbye!\n' )
sys.exit( 0 )
