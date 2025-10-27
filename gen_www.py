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

# these are used only for crosswords, which we no longer generate by default
# we cycle through these to change colors a little
colors = [ '#c095e3',
           '#a99887',
           '#53af8b',
           '#929195',
           '#587a8f',
           '#95dfe3',
           '#f69284',
           '#95b8e3',
          ]

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
name = ''
subjects_s = ''
other_lang = 'English'
other_lang_code = 'en-US'
other_lang_voice = 'Samantha'
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
    if   arg == '-name':
        name = sys.argv[i]
    elif arg == '-subjects':
        subjects_s = sys.argv[i]
    elif arg == '-other_lang':
        other_lang = sys.argv[i]
    elif arg == '-other_lang_code':
        other_lang_code = sys.argv[i]
    elif arg == '-other_lang_voice':
        other_lang_voice = sys.argv[i]
    elif arg == '-side':           
        side = int(sys.argv[i])
    elif arg == '-count':
        count = int(sys.argv[i])
    elif arg == '-seed':
        seed = int(sys.argv[i])
    elif arg == '-cmd_en':
        cmd_en = int(sys.argv[i])
    elif arg == '-cw_en':
        cw_en = int(sys.argv[i])
    elif arg == '-gen_puzzles':
        gen_puzzles = int(sys.argv[i])
    else:
        die( f'unknown option: {arg}' )
    i += 1

if name == '': die( f'no -name' )
Name = name.capitalize()
if subjects_s == '': die( f'no -name' )
subjects = subjects_s.split( ',' )
if gen_puzzles: cmd( f'make gen_puz' )

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
s += f'<title>{Name} Study Lists{and_crossword_puzzles}</title>\n'
s += f'<h1>{Name} Study Lists{and_crossword_puzzles}</h1>\n'
s += f'<body>\n'
s += f'<p>\n'
s += f'<h3><a href="https://www.imustcook.com">[back to imustcook.com]</a></h3>\n'
s += f'</p>\n'
if other_lang != 'English':
    s += f'<p style="font-size:20px">Hear a phrase:</p>\n'
    s += f'<p><pre><div id="text-box" contenteditable="true"></div></pre>\n'
    s += f'<button id="button_other_voice" title="Speak text using {Name} voice" style="font-size:14px" onclick="speak_other()">{Name} Voice</button>\n'
    s += f'<button id="button_english_voice" title="Speak text using English voice" style="font-size:14px" onclick="speak_english()">English Voice</button>\n'
    s += f'<button id="button_repeat" title="Toggle repeat mode" style="font-size:14px" onclick="toggle_repeat()">Repeat</button></p>\n'
    s += f'<p style="font-size:14px">\n'
    s += f'Speed: <input type="range" min="25" max="125" value="90" class="slider" id="slider_speed" oninput="update_slider_speed(this.value)">\n'
    s += f'<span id="slider_speed_value">0.9</span>\n'
    s += f'<p style="font-size:20px">\n'
    s += f'If that sounds wrong, check:\n'
    s += f'<a href="https://forvo.com">Forvo</a>,\n'
s += f'<p style="font-size:22px">Click on a study list name to hear randomized entries or search the list:</p>\n'
s += '''
<script>
  var rate = 0.9;
  var repeating = false;
  var timeout_id = 0;
  var delay = 1000;

  function speak_other() {
      window.speechSynthesis.cancel();
      var msg = new SpeechSynthesisUtterance("");
      msg.lang = ''' + '\'' + other_lang_code + '\'' + ''';
      msg.rate = rate;
      msg.text = document.getElementById("text-box").textContent;
      msg.onend = repeating ? delay_other : 0;
      window.speechSynthesis.speak(msg);
  }

  function delay_other() {
      timeout_id = setTimeout( speak_other, delay );
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
for subject in subjects:
    if subject != f'{name}_all_lists':
        if all_s != '': all_s += ','
        all_s += subject
    
is_first = True
color_i = 0
for subject in subjects:
    s += f'<section style="clear: left">\n'
    if gen_puzzles and not is_first: s += f'<br>\n'
    subjects_s = all_s if subject == f'{name}_all_lists' else subject
    entry_cnt = int( cmd( f'./gen_puz {subjects_s} -print_entry_cnt_and_exit 1' ) ) if cmd_en else 1
    cmd( f'./gen_html.py -subjects {subjects_s} -title {subject} -other_lang {other_lang} -other_lang_code {other_lang_code} -other_lang_voice {other_lang_voice} > www/{subject}.html' ) 
    s += f'<h2><a href="{subject}.html">{subject}</a> ({entry_cnt} entries)</h2>'
    if gen_puzzles:
        for reverse in range(2):
            clue_lang = Name if reverse == 0 else 'English'
            start_pct = 85
            s += f'<section style="clear: left">\n'
            s += f'<b>{clue_lang} Crosswords:</b><br>'
            for i in range(count):
                title = f'{subject}_s{seed}_r{reverse}'
                if cw_en: cmd( f'./gen_puz {subjects_s} -side {side} -seed {seed} -reverse {reverse} -start_pct {start_pct} -title {title} > www/{title}.html' )
                seed += 1
                s += f'<a href="{title}.html"><div class="rectangle" style="background-color: {color}">{i}</div></a>\n'
        color_i += 1
        if color_i == len( colors ): color_i = 0

    is_first = False

s += f'<section style="clear: left">\n'
s += '<br>\n'
s += '</body>\n'
s += '</html>\n'

file = open( f'www/{name}.html', "w" )
a = file.write( s )
file.close()
