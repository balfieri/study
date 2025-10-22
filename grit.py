#!/usr/bin/env python3
#
# grit.py <string> - search for string in existing definitions
#
import sys
import time
import random
import string
import re
import subprocess

# debugging flags
die_with_exception = False
cmd_en = True
cmd_force_echo_stdout = False

def die( msg, prefix='ERROR: ' ):
    print( prefix + msg )
    if die_with_exception: 
        raise AssertionError
    else:
        sys.exit( 1 )

def cmd( c, echo=True, echo_stdout=False, can_die=True, timeout=None ):  
    if echo: print( c, flush=True )
    if cmd_en:
        if echo_stdout or cmd_force_echo_stdout:
            info = subprocess.run( c, shell=True, text=True, timeout=timeout )
        else:
            info = subprocess.run( c, shell=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout )
        if can_die and info.returncode != 0: die( f'command failed: {c}' )
        return info.stdout
    else:
        return ''

def match( s, pattern ): 
    return re.compile( pattern ).match( s )

#-----------------------------------------------------------------------
# process command line args
#-----------------------------------------------------------------------
if len( sys.argv ) < 2: die( 'usage: grit.py [options] <string>', '' )
string = sys.argv[1]
subjects_s = ''
search_question = True
search_answer = True
speak = False
lookup_if_not_found = False
language = 'english'
voice = 'Samantha'
out_file = ''
i = 1
while i < len( sys.argv ):
    arg = sys.argv[i]
    i += 1
    if   arg == '-subjects':
        subjects_s = sys.argv[i]
    elif arg == '-l':
        language = sys.argv[i]
    elif arg == '-v':
        voice = sys.argv[i]
    elif arg == '-q':
        search_question = int(sys.argv[i])
    elif arg == '-a':
        search_answer = int(sys.argv[i])
    elif arg == '-s':
        speak = int(sys.argv[i])
    elif arg == '-lu':
        lookup_if_not_found = int(sys.argv[i])
    else:
        i -= 1
        break
    i += 1

if subjects_s == '': die( f'no -subjects' )
string = ' '.join( sys.argv[i:] )

#-----------------------------------------------------------------------
# read in <subject>.txt files
#-----------------------------------------------------------------------
subjects = subjects_s.split( ',' )
found = False
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
            if speak:
                cmd( f'say -v {voice} {answer}', echo=False )
            found = True

    Q.close()

if not found and lookup_if_not_found:
    print( f'Not found, looking up translation...' )
    cmd( f'gpt -c {language}_translations -i \"{string}\"', True, True )
