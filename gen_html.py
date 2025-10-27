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
if len( sys.argv ) < 1: die( 'usage: gen_html.py [options]', '' )
subjects_s = ''
title = 'All Lists'
other_lang = 'English'
other_lang_code = 'en-US'
other_lang_voice = 'Samantha'

i = 1
while i < len( sys.argv ):
    arg = sys.argv[i]
    i += 1
    if   arg == '-subjects':
        subjects_s = sys.argv[i]
    elif arg == '-title': 
        title = sys.argv[i]
    elif arg == '-other_lang':
        other_lang = sys.argv[i]
    elif arg == '-other_lang_code':
        other_lang_code = sys.argv[i]
    elif arg == '-other_lang_voice':
        other_lang_voice = sys.argv[i]
    else:
        die( f'unknown option: {arg}' )
    i += 1

if subjects_s == '': die( 'no -subjects' )

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
        question = re.sub( r'^\{[\w,]+\}\s*', '', question )
        if '"' in question: die( f'double-quote not allowed at {filename}:{line_num}: {question}' )
        if len(question) == 0 or question[0] == '#': continue

        line_num += 1
        answer = Q.readline()
        answer = re.sub( r'^\s+', '', answer )
        answer = re.sub( r'\s+$', '', answer )
        if answer == '': die( f'question at {filename}:{line_num} is not followed by a non-blank answer on the next line: {question}' )
        if '"' in answer: die( f'double-quote not allowed at {filename}:{line_num}: {answer}' )
        line_num += 1

        phrases_s += f'        [ "{question}", "{answer}", true, false ],\n'

    Q.close()

# need to create a loop here
is_english_only = other_lang == 'English'

is_advanced  = re.match( r'.*_advanced', subjects_s ) != None
is_basic     = re.match( r'.*_basic',    subjects_s ) != None
eng_speed    = 1.25 if is_advanced else 1.00
oth_speed    = 1    if is_advanced or is_english_only else 0.8 if is_basic else 0.9
eng_speed100 = str(eng_speed * 100)
oth_speed100 = str(oth_speed * 100)
eng_speed    = str(eng_speed)
oth_speed    = str(oth_speed)
eng_name     = 'Question' if is_english_only else 'English'
oth_name     = 'Answer'   if is_english_only else other_lang
eng_lang     = '\'en-US\''
oth_lang     = f'\'{other_lang_code}\''
eng_voice    = '\'Samantha\''
oth_voice    = f'\'{other_lang_voice}\''
eng_first    = '\'Question First\'' if is_english_only else '\'English First\''
oth_first    = '\'Answer First\''   if is_english_only else f'\'{other_lang} First\''
eng_prefix   = '\'Question: \' + '  if is_english_only else ''
oth_prefix   = '\'Answer: \' + '    if is_english_only else ''
delay_after  = '2'  if is_basic    else '0'

html_s = '''<!DOCTYPE html>
<html>
  <head>
    <meta charset="UTF-8">
    <title>''' + title + '''</title>
  </head>
  <style type="text/css">
    #english-text-box {
      height: 1em;
      width: 500px;
      border: 1px solid #ccc;
      font-size: 20px;
    }
    #other-text-box {
      height: 1em;
      width: 500px;
      border: 1px solid #ccc;
      font-size: 20px;
    }
  </style>
  <body>
    <h1>''' + title + '''</h1>
    <p>
    <h3><a href="https://www.imustcook.com/crossword">[return to lists]</a></h3>
    </p>
    <form>
        <label for="english-text-box">''' + eng_name + ''' filter:</label>
        <input type="text" id="english-text-box" name="english-text-box">
    </form>
    <p>
    <form>
        <label for="other-text-box">''' + oth_name + ''' filter:</label>
        <input type="text" id="other-text-box" name="other-text-box">
    </form>
    </p>
    <button id="button_play_randomly" title="Start/stop randomized playback of list entries" style="font-size:20px;border-radius:15px;padding:5px 10px" onclick="start_stop_play_randomly()">Play Randomly</button>
    <button id="button_play_in_order" title="Start/stop in-order playback of list entries" style="font-size:20px;border-radius:15px;padding:5px 10px" onclick="start_stop_play_in_order()">Play In Order</button>
    <button id="button_mute" title="Mute/unmute voices" style="font-size:20px;border-radius:15px;padding:5px 10px" onclick="mute_unmute()">Mute</button>
    <button id="button_show_all" title="Show all entries" style="font-size:20px;border-radius:15px;padding:5px 10px" onclick="show_all()">Show All</button>
    <button id="button_first" title="Show ''' + other_lang + '''/English translation first" style="font-size:20px;border-radius:15px;padding:5px 10px" onclick="which_first()">''' + oth_name + ''' First</button>
    <p style="font-size:18px">
    ''' + eng_name + ''' Speed: <input type="range" min="25" max="125" value="''' + eng_speed100 + '''" class="slider" id="slider_en" oninput="update_slider_en(this.value)">
    <span id="slider_en_value">''' + eng_speed + '''</span>
    ''' + oth_name + ''' Speed: <input type="range" min="25" max="125" value="''' + oth_speed100 + '''" class="slider" id="slider_it" oninput="update_slider_it(this.value)">
    <span id="slider_it_value">''' + oth_speed + '''</span>
    </p>
    <p style="font-size:18px">
    Extra Delay Between ''' + eng_name + ''' and ''' + oth_name + ''' (secs): <input type="range" min="0" max="10" value="0" class="slider" id="slider_extra_delay_between" oninput="update_slider_extra_delay_between(this.value)">
    <span id="slider_extra_delay_between_value">0</span>
    </p>
    <p style="font-size:18px">
    Extra Delay After ''' + eng_name + ''' and ''' + oth_name + ''' (secs): <input type="range" min="0" max="10" value="''' + delay_after + '''" class="slider" id="slider_extra_delay_after" oninput="update_slider_extra_delay_after(this.value)">
    <span id="slider_extra_delay_after_value">''' + delay_after + '''</span>
    </p>

    <p><pre id="log" style="font-size:24px"></pre></p>
    
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
    <script>
      var in_playback = false;
      const phrases = [
''' + phrases_s + '''
          ];
      
      var log_s = ""

      var english_filter = "";
      var other_filter = "";

      var in_order = false;
      var in_order_i = 0;
      var english_first = true;
      var speech_enabled = true;
      var timeout_id = 0;
      var extra_delay_between_sec = 0;
      var extra_delay_after_sec = ''' + delay_after + ''';
      var did_between_delay = false;
      var did_second = false;

      var msg_en = new SpeechSynthesisUtterance("");
      var msg_ot = new SpeechSynthesisUtterance("");

      msg_en.lang = ''' + eng_lang + ''';
      msg_ot.lang = ''' + oth_lang + ''';

      msg_en.voice = window.speechSynthesis.getVoices().find(voice => voice.name === ''' + eng_voice + ''' );
      msg_ot.voice = window.speechSynthesis.getVoices().find(voice => voice.name === ''' + oth_voice + ''' );

      msg_en.rate = ''' + eng_speed + ''';
      msg_ot.rate = ''' + oth_speed + ''';

      msg_en.onend = continue_playback; 
      msg_ot.onend = continue_playback; 

      // don't submit when user hits newline in form
      $(document).ready(function(){
          $('form').on('keyup keypress', function(e) {
              var keyCode = e.keyCode || e.which;
              if (keyCode === 13) { 
                  e.preventDefault();
                  return false;
              }
          });
      });

      window.speechSynthesis.addEventListener('voiceschanged', () => {
          msg_en.voice = window.speechSynthesis.getVoices().find(voice => voice.name === ''' + eng_voice + ''' );
          msg_ot.voice = window.speechSynthesis.getVoices().find(voice => voice.name === ''' + oth_voice + ''' );
      });

      function clear_log() {
          log_s = "";
          document.getElementById("log").textContent = log_s;
      }

      function stop_playback() {
          if ( in_playback ) {
              window.speechSynthesis.cancel();
              document.getElementById('button_play_randomly').innerHTML = 'Play Randomly';
              document.getElementById('button_play_in_order').innerHTML = 'Play In Order';
              in_playback = false;
          }
      }

      function apply_filters() {
          if ( document.getElementById("english-text-box").value == english_filter &&
               document.getElementById("other-text-box").value == other_filter ) {
              // no changes in filters, so no need to re-apply them
              return;
          }             

          clear_log();
          english_filter = document.getElementById("english-text-box").value;
          other_filter = document.getElementById("other-text-box").value;
          var english_regex = new RegExp( english_filter );
          var other_regex = new RegExp( other_filter );
          for( idx = 0; idx < phrases.length; idx++ ) {
              phrase = phrases[idx];
              phrase[2] = (english_filter == "" || english_regex.test( phrase[0] )) &&
                          (other_filter == "" || other_regex.test( phrase[1] ));
          }
      }

      function show_all() {
          stop_playback();
          apply_filters();
          log_s = "";
          for( idx = 0; idx < phrases.length; idx++ ) {
              phrase = phrases[idx];
              if ( phrase[2] ) {
                  if ( english_first ) {
                      log_s += phrase[0] + "\\n" + phrase[1] + "\\n\\n";
                  } else {
                      log_s += phrase[1] + "\\n" + phrase[0] + "\\n\\n";
                  }
              }
              document.getElementById("log").textContent = log_s;
          }
      }

      function getNextPhrase() {
          if ( in_order ) {
              for( ;; )
              {
                  if ( in_order_i >= phrases.length ) return null;
                  if ( !phrases[in_order_i][2] || phrases[in_order_i][3] ) {
                      in_order_i++;
                      continue;
                  }
                  phrases[in_order_i][3] = true; // not necessary, but for consistency
                  return phrases[in_order_i++];
              }
          } else {
              idx_first = Math.floor(Math.random() * phrases.length);
              idx = idx_first;
              while( !phrases[idx][2] || phrases[idx][3] ) { // already did this one
                  idx++;
                  if ( idx == phrases.length ) idx = 0;
                  if ( idx == idx_first ) {
                      // did them all => mark all undone and return none
                      for( var i = 0; i < phrases.length; i++ )
                      {
                          phrases[i][3] = false;  
                      }
                      return null;
                  }
              }
              phrases[idx][3] = true;
              return phrases[idx];
          }
      }
      
      function playback() {
          if ( !in_playback ) return;
          apply_filters();

          const phrase = getNextPhrase();
          if ( !phrase ) {
              log_s = "Done showing all matching entries!\\n\\n" + log_s;
              document.getElementById("log").textContent = log_s;
              stop_playback();
          }

          msg_en.text = ''' + eng_prefix + '''phrase[0];
          msg_ot.text = ''' + oth_prefix + '''phrase[1];

          if ( log_s.length > 1000000 ) log_s.slice( 0, 1000000 );
          if ( english_first ) {
              log_s = phrase[0] + "\\n" + phrase[1] + "\\n\\n" + log_s;
          } else {
              log_s = phrase[1] + "\\n" + phrase[0] + "\\n\\n" + log_s;
          }
          document.getElementById("log").textContent = log_s;

          did_between_delay = false;
          did_second = false;
          if ( speech_enabled ) {
              if ( english_first ) {
                  window.speechSynthesis.speak(msg_en);
              } else {
                  window.speechSynthesis.speak(msg_ot);
              }
          } else {
              timeout_id = setTimeout( playback, 3000 + extra_delay_after_sec*1000 );
          }
      }

      function continue_playback() {
          if ( !in_playback ) return;

          // do we need to insert a delay between languages?
          //
          if ( !did_between_delay ) {
              did_between_delay = true;
              if ( extra_delay_between_sec > 0 ) {
                  delay = extra_delay_between_sec*1000;
                  timeout_id = setTimeout( continue_playback, delay );
                  return;
              }
          }

          // do we need to start the second voice?
          //
          if ( !did_second ) {
              did_second = true;
              if ( english_first ) {
                  window.speechSynthesis.speak(msg_ot);
              } else {
                  window.speechSynthesis.speak(msg_en);
              }
              return;
          }

          // add non-zero delay after the second voice, which help
          // keep iOS devices from falling asleep,
          // then go back to playback
          //
          delay = extra_delay_after_sec*1000;
          if ( delay == 0 ) delay = 250; 
          timeout_id = setTimeout( playback, delay );
      }

      function start_stop_play_randomly() {
          if ( in_playback && !in_order ) {
              stop_playback();
          } else {
              if ( in_playback ) stop_playback();
              in_order = false;
              document.getElementById('button_play_randomly').innerHTML = 'Stop';
              in_playback = true; 
              playback()
          }
      }

      function start_stop_play_in_order() {
          if ( in_playback && in_order ) {
              stop_playback();
          } else {
              if ( in_playback ) stop_playback();
              in_order = true;
              in_order_i = 0;
              document.getElementById('button_play_in_order').innerHTML = 'Stop';
              in_playback = true; 
              playback()
          }
      }

      function mute_unmute() {
          if ( speech_enabled ) {
              document.getElementById('button_mute').innerHTML = 'Unmute';
              speech_enabled = false;
              if ( in_playback ) {
                  window.speechSynthesis.cancel();
                  playback();
              }
          } else {
              if ( timeout_id ) clearTimeout( timeout_id );
              document.getElementById('button_mute').innerHTML = 'Mute';
              speech_enabled = true;
              playback();
          }
      }

      function which_first() {
          window.speechSynthesis.cancel();
          if ( english_first ) {
              document.getElementById('button_first').innerHTML = ''' + eng_first + ''';
              english_first = false;
          } else {
              document.getElementById('button_first').innerHTML = ''' + oth_first + ''';
              english_first = true;
          }
          playback();
      }

      function update_slider_en( value ) {
          value = value / 100.0;
          document.getElementById('slider_en_value').innerText = value;
          msg_en.rate = value;
      }

      function update_slider_it( value ) {
          value = value / 100.0;
          document.getElementById('slider_it_value').innerText = value;
          msg_ot.rate = value;
      }

      function update_slider_extra_delay_between( value ) {
          document.getElementById('slider_extra_delay_between_value').innerText = value;
          extra_delay_between_sec = value;
      }

      function update_slider_extra_delay_after( value ) {
          document.getElementById('slider_extra_delay_after_value').innerText = value;
          extra_delay_after_sec = value;
      }

      window.onbeforeunload = function(event) {
          window.speechSynthesis.cancel();
      };

    </script>
  </body>
</html>
'''

print( html_s )
