#!/usr/bin/env python3
#
# gen_html.py - generate .html for doing searches on lists and for playing back randomed
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

i = 1
while i < len( sys.argv ):
    arg = sys.argv[i]
    i += 1
    if   arg == '-subjects':
        subjects_s = sys.argv[i]
        i += 1
    else:
        die( f'unknown option: {arg}' )

#-----------------------------------------------------------------------
# read in <subject>.txt files
#-----------------------------------------------------------------------
subjects = subjects_s.split( ',' )
phrases_s = ''
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

        phrases_s += f'        [ "{question}", "{answer}" ],\n'

    Q.close()

html_s = '''<!DOCTYPE html>
<html>
  <head>
    <meta charset="UTF-8">
    <title>Italian Phrases</title>
  </head>
  <body>
    <h1>Italian Phrases</h1>
    <p id="phrase_en"></p>
    <p id="phrase_it"></p>
    <button onclick="randomize()">Randomize</button>
    
    <script>
      const phrases = [
'''
html_s += phrases_s
html_s += '''        ];
      
      function getRandomPhrase() {
        return phrases[Math.floor(Math.random() * phrases.length)];
      }
      
      function randomize() {
          const phrase = getRandomPhrase();
          msg_en = new SpeechSynthesisUtterance(phrase[0]);
          msg_it = new SpeechSynthesisUtterance(phrase[1]);

          msg_en.lang = 'en-US';
          msg_it.lang = 'it-IT';

          msg_en.voice = window.speechSynthesis.getVoices().find(voice => voice.name === 'Samantha' );
          msg_it.voice = window.speechSynthesis.getVoices().find(voice => voice.name === 'Alice' );
          msg_it.onend = randomize; // continue loop

          document.getElementById("phrase_en").textContent = phrase[0]
          document.getElementById("phrase_it").textContent = phrase[1]

          window.speechSynthesis.speak(msg_en);
          window.speechSynthesis.speak(msg_it);
      }
    </script>
  </body>
</html>
'''

print( html_s )
