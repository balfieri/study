#!/usr/bin/env python3
#
# gen_www.py - generates crossword puzzles for all interesting categories for website
#
import sys
import os
import os.path
import subprocess
import time
import string
import re
import datetime

subjects = [ [ 'all_lists',                     '#c095e3',      False ],
             [ 'italian_basic',                 '#a99887',      True ],
             [ 'italian_advanced',              '#53af8b',      True ],
             [ 'italian_passato_remoto',        '#929195',      False ],
             [ 'italian_expressions',           '#587a8f',      False ],
             [ 'american_expressions',          '#95dfe3',      False ],
             [ 'italian_tongue_twisters',       '#f69284',      False ],
             [ 'italian_vulgar',                '#95b8e3',      False ],
           ]

#unused colors

def die( msg, prefix='ERROR: ' ):
    print( prefix + msg )
    sys.exit( 1 )

cmd_en = True

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
side = 17
count = 15
today = datetime.date.today()
year = today.year - 2000
month = today.month
day = today.day
seed = year*10000 + month*100 + day
seed *= 10000
cw_en = True
gen_puzzles = False

i = 1
while i < len( sys.argv ):
    arg = sys.argv[i]
    i += 1
    if   arg == '-side':           
        side = int(sys.argv[i])
        i += 1
    elif arg == '-count':
        count = int(sys.argv[i])
        i += 1
    elif arg == '-seed':
        seed = int(sys.argv[i])
        i += 1
    elif arg == '-cmd_en':
        cmd_en = int(sys.argv[i])
        i += 1
    elif arg == '-cw_en':
        cw_en = int(sys.argv[i])
        i += 1
    elif arg == '-gen_puzzles':
        gen_puzzles = int(sys.argv[i])
        i += 1
    else:
        die( f'unknown option: {arg}' )

if cw_en: cmd( f'rm -f www/*.html' )
cmd( f'make gen_puz' )

s = ''
s += f'<html>\n'
s += f'<head>\n'
s += f'<style type="text/css">\n'
s += f'.rectangle {{\n'
s += f'  height: 30px;\n'
s += f'  width: 30px;\n'
s += f'  color:black;\n'
s += f'  background-color: rgb(0,0,255);\n'
s += f'  border-radius:10px;\n'
s += f'  display: flex;\n'
s += f'  justify-content:center;\n'
s += f'  align-items: center;\n'
s += f'  font-family: Arial;\n'
s += f'  font-size: 18px;\n'
s += f'  font-weight: bold;\n'
s += f'  float: left;\n'
s += f'  margin-right: 5px;\n'
s += f'  margin-bottom: 5px;\n'
s += f'}}\n'
s += f'#text-box {{' 
s += f'  height: 2em;' 
s += f'  width: 500px;'
s += f'  border: 1px solid #ccc;'
s += f'  overflow-y: scroll;' 
s += f'  font-size: 20px;'
s += f'}}\n'
s += f'</style>\n'
s += f'</head>\n'
and_crossword_puzzles = 'and Crossword Puzzles' if gen_puzzles else ''
s += f'<title>Italian-English Word Lists{and_crossword_puzzles}</title>\n'
s += f'<h1>Italian-English Word Lists{and_crossword_puzzles}</h1>\n'
s += f'<body>\n'
s += f'<p style="font-size:20px">Hear a phrase:</p>\n'
s += f'<p><pre><div id="text-box" contenteditable="true"></div></pre>\n'
s += f'<button id="button_italian_voice" title="Speak text using Italian voice" style="font-size:14px" onclick="speak_italian()">Italian Voice</button>\n'
s += f'<button id="button_english_voice" title="Speak text using English voice" style="font-size:14px" onclick="speak_english()">English Voice</button>\n'
s += f'<button id="button_repeat" title="Toggle repeat mode" style="font-size:14px" onclick="toggle_repeat()">Repeat</button></p>\n'
s += f'<p style="font-size:14px">\n'
s += f'Speed: <input type="range" min="25" max="125" value="90" class="slider" id="slider_speed" oninput="update_slider_speed(this.value)">\n'
s += f'<span id="slider_speed_value">0.9</span>\n'
s += f'<p style="font-size:20px">\n'
s += f'If that sounds wrong, check:\n'
s += f'<a href="https://it.forvo.com">Forvo Italian</a>,\n'
s += f'<a href="https://forvo.com">Forvo English</a>,\n'
s += f'<a href="https://dizionatore.it">Dizionatore.it</a></p>\n'
s += f'<p style="font-size:20px">\n'
s += f'For verb conjugations, see: <a href="https://italian-verbs.com">italian-verbs.com</a></p>\n'
s += f'<p style="font-size:22px">Click on a word list name (e.g., italian_basic) to hear randomized entries or search the list:</p>\n'
s += '''
<script>
  var rate = 0.9;
  var repeating = false;
  var timeout_id = 0;
  var delay = 1000;

  function speak_italian() {
      window.speechSynthesis.cancel();
      var msg = new SpeechSynthesisUtterance("");
      msg.lang = 'it-IT';
      msg.rate = rate;
      msg.text = document.getElementById("text-box").textContent;
      msg.onend = repeating ? delay_italian : 0;
      window.speechSynthesis.speak(msg);
  }

  function delay_italian() {
      timeout_id = setTimeout( speak_italian, delay );
  }

  function speak_english() {
      window.speechSynthesis.cancel();
      var msg = new SpeechSynthesisUtterance("");
      msg.lang = 'en-US';
      msg.rate = rate;
      msg.text = document.getElementById("text-box").textContent;
      msg.onend = repeating ? delay_english : 0; 
      window.speechSynthesis.speak(msg);
  }

  function delay_english() {
      timeout_id = setTimeout( speak_english, delay );
  }

  function toggle_repeat() {
      if ( repeating ) {
          window.speechSynthesis.cancel();
          document.getElementById('button_repeat').innerHTML = 'Repeat';
          repeating = false;
      } else {
          document.getElementById('button_repeat').innerHTML = 'No Repeat';
          repeating = true;
      }
  }

  function update_slider_speed( value ) {
      value = value / 100.0;
      document.getElementById('slider_speed_value').innerText = value;
      rate = value;
  }

</script>
'''

#-----------------------------------------------------------------------
# Generate the individual lists and puzzles.
#-----------------------------------------------------------------------
all_s = ''
for subject_info in subjects:
    subject = subject_info[0]
    if subject != 'all_lists':
        if all_s != '': all_s += ','
        all_s += subject
    
is_first = True
for subject_info in subjects:
    subject   = subject_info[0]
    color     = subject_info[1]
    s += f'<section style="clear: left">\n'
    if gen_puzzles and not is_first: s += f'<br>\n'
    subjects_s = all_s if subject == 'all_lists' else subject
    entry_cnt = int( cmd( f'./gen_puz {subjects_s} -print_entry_cnt_and_exit 1' ) ) if cmd_en else 1
    cmd( f'./gen_html.py -subjects {subjects_s} -title {subject} > www/{subject}.html' ) 
    s += f'<h2><a href="{subject}.html">{subject}</a> ({entry_cnt} entries)</h2>'
    if gen_puzzles:
        if subject == 'all_lists': s += f'<p><b>Warning: includes italian_vulgar list</b></p>'
        for reverse in range(2):
            clue_lang = 'Italian' if reverse == 0 else 'English'
            start_pct = 85
            s += f'<section style="clear: left">\n'
            s += f'<b>{clue_lang} Crosswords:</b><br>'
            for i in range(count):
                title = f'{subject}_s{seed}_r{reverse}'
                if cw_en: cmd( f'./gen_puz {subjects_s} -side {side} -seed {seed} -reverse {reverse} -start_pct {start_pct} -title {title} > www/{title}.html' )
                seed += 1
                s += f'<a href="{title}.html"><div class="rectangle" style="background-color: {color}">{i}</div></a>\n'
    is_first = False

s += f'<section style="clear: left">\n'
s += '<br>\n'
s += '</body>\n'
s += '</html>\n'

file = open( "www/index.html", "w" )
a = file.write( s )
file.close()
