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
title = 'All Lists'

i = 1
while i < len( sys.argv ):
    arg = sys.argv[i]
    i += 1
    if   arg == '-subjects':
        subjects_s = sys.argv[i]
        i += 1
    elif arg == '-title': 
        title = sys.argv[i]
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

        phrases_s += f'        [ "{question}", "{answer}", false ],\n'

    Q.close()

html_s = '''<!DOCTYPE html>
<html>
  <head>
    <meta charset="UTF-8">
    <title>''' + title + '''</title>
  </head>
  <body>
    <h1>''' + title + '''</h1>
    <button id="button_randomize" title="Start/stop randomized playback of list entries" style="font-size:20px;border-radius:15px;padding:5px 10px" onclick="start_stop()">Randomize</button>
    <button id="button_mute" title="Mute/unmute voices" style="font-size:20px;border-radius:15px;padding:5px 10px" onclick="mute_unmute()">Mute</button>
    <button id="button_first" title="Show Italian/English translation first" style="font-size:20px;border-radius:15px;padding:5px 10px" onclick="which_first()">Italian First</button>
    <p style="font-size:18px">
    English Rate: <input type="range" min="25" max="125" value="80" class="slider" id="slider_en" oninput="update_slider_en(this.value)">
    <span id="slider_en_value">0.8</span>
    Italian Rate: <input type="range" min="25" max="125" value="80" class="slider" id="slider_it" oninput="update_slider_it(this.value)">
    <span id="slider_it_value">0.8</span>
    </p>

    <p><pre id="log" style="font-size:24px"></pre></p>
    
    <script>
      var in_randomization = false;
      const phrases = [
''' + phrases_s + '''
          ];
      
      var log_s = ""

      var english_first = true;
      var speech_enabled = true;
      var quiet_timeout_id = 0;

      var msg_en = new SpeechSynthesisUtterance("");
      var msg_it = new SpeechSynthesisUtterance("");

      msg_en.lang = 'en-US';
      msg_it.lang = 'it-IT';

      msg_en.rate = 0.8;
      msg_it.rate = 0.8;

      msg_it.onend = randomize; // continue loop


      window.speechSynthesis.addEventListener('voiceschanged', () => {
          msg_en.voice = window.speechSynthesis.getVoices().find(voice => voice.name === 'Samantha' );
          msg_it.voice = window.speechSynthesis.getVoices().find(voice => voice.name === 'Alice' );
      });

      function getRandomPhrase() {
          idx_first = Math.floor(Math.random() * phrases.length);
          idx = idx_first;
          while( phrases[idx][2] ) { // already did this one
              idx++;
              if ( idx == phrases.length ) idx = 0;
              if ( idx == idx_first ) {
                  // did them all => mark all undone
                  for( var i = 0; i < phrases.length; i++ )
                  {
                      phrases[i][2] = false;  
                  }
              }
          }
          phrases[idx][2] = true;
          return phrases[idx];
      }
      
      function randomize() {
          if ( !in_randomization ) return;

          const phrase = getRandomPhrase();

          msg_en.text = phrase[0];
          msg_it.text = phrase[1];

          if ( log_s.length > 1000000 ) log_s.slice( 0, 1000000 );
          if ( english_first ) {
              log_s = phrase[0] + "\\n" + phrase[1] + "\\n\\n" + log_s;
          } else {
              log_s = phrase[1] + "\\n" + phrase[0] + "\\n\\n" + log_s;
          }
          document.getElementById("log").textContent = log_s;

          if ( speech_enabled ) {
              if ( english_first ) {
                  window.speechSynthesis.speak(msg_en);
                  window.speechSynthesis.speak(msg_it);
              } else {
                  window.speechSynthesis.speak(msg_it);
                  window.speechSynthesis.speak(msg_en);
              }
          } else {
              quiet_timeout_id = setTimeout( randomize, 3000 );
          }
      }

      function start_stop() {
          if ( in_randomization ) {
              window.speechSynthesis.cancel();
              document.getElementById('button_randomize').innerHTML = 'Randomize';
              in_randomization = false;
          } else {
              document.getElementById('button_randomize').innerHTML = 'Stop';
              in_randomization = true; 
              randomize()
          }
      }

      function mute_unmute() {
          if ( speech_enabled ) {
              document.getElementById('button_mute').innerHTML = 'Unmute';
              speech_enabled = false;
              if ( in_randomization ) {
                  window.speechSynthesis.cancel();
                  randomize();
              }
          } else {
              if ( quiet_timeout_id ) clearTimeout( quiet_timeout_id );
              document.getElementById('button_mute').innerHTML = 'Mute';
              speech_enabled = true;
              randomize();
          }
      }

      function which_first() {
          window.speechSynthesis.cancel();
          if ( english_first ) {
              document.getElementById('button_first').innerHTML = 'English First';
              english_first = false;
              msg_en.onend = randomize; // continue loop
              msg_it.onend = null;
          } else {
              document.getElementById('button_first').innerHTML = 'Italian First';
              english_first = true;
              msg_en.onend = null;
              msg_it.onend = randomize; // continue loop
          }
          randomize();
      }

      function update_slider_en( value ) {
          value = value / 100.0;
          document.getElementById('slider_en_value').innerText = value;
          msg_en.rate = value;
      }

      function update_slider_it( value ) {
          value = value / 100.0;
          document.getElementById('slider_it_value').innerText = value;
          msg_it.rate = value;
      }

      window.onbeforeunload = function(event) {
          window.speechSynthesis.cancel();
      };

    </script>
  </body>
</html>
'''

print( html_s )
