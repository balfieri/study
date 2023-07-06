#!/usr/bin/env python3
#
# run.py <subjects> [options]
#
import sys
import time
import random
import string
import re
import subprocess

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

def say( text, voice, rate ):
    with open( '/tmp/say.txt', 'w' ) as file:
        file.write( text )
    cmd( f'say -v {voice} -r {rate} -f /tmp/say.txt', False )

#-----------------------------------------------------------------------
# process command line args
#-----------------------------------------------------------------------
if len( sys.argv ) < 2: die( 'usage: run.py <subjects> [options]', '' )
subjects = sys.argv[1].split( ',' )
question_cnt = 20
skip_prompts = 0
skip_pause_sec = -1
start_pct = 0
end_pct = 100
acronyms_only = 0
categories_s = ''
have_categories_s = 0
speak = False
question_voice = 'Samantha'
answer_voice = 'Alice'
question_rate  = 180
answer_rate  = 160
i = 2
while i < len( sys.argv ):
    arg = sys.argv[i]
    i += 1
    if   arg == '-q':           
        question_cnt = int(sys.argv[i])
        i += 1
    elif arg == '-ps':          
        skip_pause_sec = int(sys.argv[i])
        skip_prompts = 1
        i += 1
    elif arg == '-start_pct':
        start_pct = int(sys.argv[i])
        if start_pct < 0 or end_pct < 0: die( 'start_pct and end_pct must be >= 0' )
        i += 1
    elif arg == '-end_pct':
        end_pct = int(sys.argv[i])
        if end_pct > 100: die( 'end_pct must be <= 100' )
        i += 1
    elif arg == '-acronyms_only':
        acronyms_only = int(sys.argv[i])
        i += 1
    elif arg == '-cat':
        categories_s = sys.argv[i]
        have_categories_s = 1
        i += 1
    elif arg == '-s':
        speak = int(sys.argv[i])
        i += 1
    elif arg == '-av':
        answer_voice = sys.argv[i]
        i += 1
    elif arg == '-ar':
        answer_rate = int(sys.argv[i])
        i += 1
    else:
        die( f'unknown option: {arg}' )

if start_pct >= end_pct: die( 'start_pct must be < end_pct' )

if not have_categories_s: 
    print()
    categories_s = prompt( 'Categories (separated by spaces, leave blank for all)' )
categories = categories_s.split( ' ' )
if len(categories) == 1 and categories[0] == '': categories = []

#-----------------------------------------------------------------------
# read in <subject>.txt files
#-----------------------------------------------------------------------
all_questions = []
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

        if re.match( r'^\{', question ):
            m = re.match( r'^\{(\S+)\}\s+(.*)', question )
            if not m: die( f'ill-formed categories on line {line_num}: {question}' )
            cats_s = m.group( 1 )
            question = m.group( 2 )
            if len(categories) > 0:
                cats = cats_s.split( ',' )
                found_one = False
                for category in categories:
                    for cat in cats:
                        if cat == category: found_one = True
                if not found_one: continue

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
all_question_first = int(start_pct*all_question_cnt/100.0)
all_question_last  = min(int(end_pct*all_question_cnt/100.0), all_question_cnt-1)
all_question_used_cnt = all_question_last - all_question_first + 1

if question_cnt == 0: 
    question_cnt = all_question_used_cnt
else:
    question_cnt = min( question_cnt, all_question_used_cnt )
    question_cnt = max( 1, question_cnt )
print()
print( f'Number of questions in the file matching the category is {all_question_cnt}, using questions {all_question_first}..{all_question_last}, asking {question_cnt} questions\n' )        

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
                    if i == 0:
                        print( s + ':' )
                    else:
                        ss = s.split( '; ' )
                        for s in ss: print( s )
                        print()
                    pause_sec = skip_pause_sec if len(s) <= 40 else int(skip_pause_sec * len(s) / 40)   # more time for long strings
                    if skip_pause_sec > 0: time.sleep( pause_sec )
            else:
                ua_lc = prompt( '\n' + q ).lower()
                if ua_lc == a_lc: 
                    correct_cnt += 1
                else:
                    ss = a.split( '; ' )
                    for s in ss: print( s )
                    missed_questions.append( ii )
            if speak:
                say( q, question_voice, question_rate )
                say( a, answer_voice,   answer_rate )

        if skip_prompts: break
        pct = int( 100.0 * correct_cnt / curr_question_cnt + 0.5 )
        print( '\nYou got ' + str(correct_cnt) + ' out of ' + str(curr_question_cnt) + ' questions correct (' + str(pct) + '%)' ) 
        if len( missed_questions ) == 0 or prompt( '\nRetry missed questions?', 'y' ) != 'y': break
        curr_questions = missed_questions
        for i in range( 100 ): print()
    if not skip_prompts and prompt( '\nPlay again?', 'y' ) != 'y': break 

print( '\nGoodbye!\n' )
sys.exit( 0 )
