#!/usr/bin/env python3
#
# puz.py <subjects> [options]
#
# This program generates a random crossword puzzle in .puz format from 
# questions taken from one or more subject files.
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

#-----------------------------------------------------------------------
# process command line args
#-----------------------------------------------------------------------
if len( sys.argv ) < 2: die( 'usage: puz.py <subjects> [options]', '' )
subjects = sys.argv[1].split( ',' )
side = 15
reverse = False
seed = time.time()
attempts = 10000
larger_cutoff = 6
out_file = ''
i = 2
while i < len( sys.argv ):
    arg = sys.argv[i]
    i += 1
    if   arg == '-side':           
        side = int(sys.argv[i])
        i += 1
    elif arg == '-reverse':          
        reverse = int(sys.argv[i]) == 1
        i += 1
    elif arg == '-out_file':
        out_file = sys.argv[i]
        i += 1
    elif arg == '-seed':
        seed = int(sys.argv[i])
        i += 1
    elif arg == '-attempts':
        attempts = int(sys.argv[i])
        i += 1
    elif arg == '-larger_cutoff':
        larger_cutoff = int(sys.argv[i])
        i += 1
    else:
        die( f'unknown option: {arg}' )

if out_file == '': die( 'must supply -out_file <file>' )
random.seed( seed )

#-----------------------------------------------------------------------
# Read in <subject>.txt files.
#-----------------------------------------------------------------------
entries = []
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
        answer = answer.lower()
        if answer == '': die( f'question on line {line_num} is not followed by a non-blank answer on the next line: {question}' )
        line_num += 1

        if reverse:
            tmp = question
            question = answer
            answer = tmp

        entries.append( [question, answer] )
    Q.close()

#-----------------------------------------------------------------------
# Pull out all interesting answer words and put them into an array, 
# with a reference back to the original question.
#-----------------------------------------------------------------------
def pick_words( a ):
    words = []
    word = ''
    word_pos = 0
    in_parens = False
    for i in range(len(a)):
        ch = a[i]
        if ch == ' ' or ch == '\t' or ch == '\'' or ch == '’' or ch == '/' or ch == '(' or ch == ')' or ch == '!' or ch == '?' or ch == '.' or ch == ',' or ch == '-':
            if word != '': 
                if not in_parens: words.append( [word, word_pos] )
                word = ''
            if ch == '(':
                if in_parens: die( 'cannot support nested parens' )
                in_parens = True
            if ch == ')':
                if not in_parens: die( 'no matching right paren' )
                in_parens = False
        elif not in_parens:
            if word == '': word_pos = i
            word += ch.lower()

    if word != '': words.append( [word, word_pos] )
    return words

# 1 and 2-letter words are already excluded
# these are common words with more then 3 letters to excluded
common_words = { 'avere': 1, 
                 'averla': 1,
                 'averlo': 1,
                 'averle': 1,
                 'averli': 1,
                 'aver': 1,
                 'essere': 1, 
                 'esserla': 1, 
                 'esserlo': 1, 
                 'esserle': 1, 
                 'esserli': 1, 
                 'stare': 1,
                 'stai': 1,
                 'stiamo': 1,
                 'state': 1,
                 'stanno': 1,
                 'fare': 1, 
                 'farla': 1,
                 'farlo': 1,
                 'farle': 1,
                 'farli': 1,
                 'farsi': 1,
                 'dare': 1,
                 'come': 1,
                 'così': 1,
                 'sono': 1, 
                 'miei': 1,
                 'tuoi': 1,
                 'suoi': 1,
                 'vuoi': 1,
                 'dall': 1,
                 'dalla': 1,
                 'dagli': 1, 
                 'dalle': 1, 
                 'dell': 1,
                 'della': 1,
                 'degli': 1, 
                 'delle': 1, 
                 'nell': 1,
                 'nella': 1,
                 'negli': 1, 
                 'nelle': 1, 
                 'sull': 1,
                 'sugli': 1,
                 'sulla': 1,
                 'sulle': 1,
                 'all': 1,
                 'alla': 1,
                 'alle': 1,
                 'agli': 1,
                 'cosa': 1,
               }

words = []
for entry in entries:
    question = entry[0]
    answers = entry[1]
    aa = answers.split( '; ' )
    for a in aa:
        ww = pick_words( a )
        for w in ww:
            if len( w[0] ) > 3 and not w[0] in common_words:
                words.append( [w, a, entry] )
                #print( w[0] )
word_cnt = len(words)

#-----------------------------------------------------------------------
# Generate the puzzle from the data structure using this simple algorithm:
#
#     for some number attempts:
#         pick a random word from the list (pick only longer words during first half)
#         if the word is already in the grid: continue
#         for each across/down location of the word:
#             score the placement of the word in that location
#         if score > 0:
#             add the word to one of the locations with the best score found
#-----------------------------------------------------------------------
def print_grid():
    for y in range(side):
        for x in range(side):
            print( f'{grid[x][y]} ', end='' )
        print()

grid = []
for x in range(side):
    grid.append( [] )
    for y in range(side):
        grid[x].append( '-' )

words_used = {}
attempts_div2 = attempts >> 1
for i in range(attempts):
    wi = rand_n( word_cnt )
    info = words[wi]
    w = info[0]
    word = w[0]
    if i < attempts_div2 and len(word) < larger_cutoff: continue
    pos = w[1]
    if word in words_used: continue

    best_words = []
    best_score = 0
    word_len = len(word)
    for x in range(side):
        for y in range(side):
            if (x + word_len) <= side:
                # score across
                score = 2 if y == 0 or y == (side-1) else 1 
                for ci in range(word_len):
                    if (ci == 0 and x > 0 and grid[x-1][y] != '-') or \
                       (ci == (word_len-1) and (x+ci+1) < side and grid[x+ci+1][y] != '-'): 
                        score = 0
                        break
                    c  = word[ci]
                    gc = grid[x+ci][y]
                    if c == gc:
                        score += 1
                    elif gc != '-' or \
                         (y > 0 and grid[x+ci][y-1] != '-') or \
                         (y < (side-1) and grid[x+ci][y+1] != '-'):
                        score = 0
                        break
                if score != 0 and score >= best_score:
                    if score > best_score:
                        best_score = score
                        best_words = []
                    best_words.append( [word, pos, x, y, True, info ] )

            if (y + word_len) <= side:
                # score down
                score = 2 if x == 0 or x == (side-1) else 1 
                for ci in range(word_len):
                    if (ci == 0 and y > 0 and grid[x][y-1] != '-') or \
                       (ci == (word_len-1) and (y+ci+1) < side and grid[x][y+ci+1] != '-'):
                        score = 0
                        break
                    c  = word[ci]
                    gc = grid[x][y+ci]
                    if c == gc:
                        score += 1
                    elif gc != '-' or \
                         (x > 0 and grid[x-1][y+ci] != '-') or \
                         (x < (side-1) and grid[x+1][y+ci] != '-'):
                        score = 0
                        break
                if score != 0 and score >= best_score:
                    if score > best_score:
                        best_score = score
                        best_words = []
                    best_words.append( [word, pos, x, y, False, info] )
    if best_score > 0: 
        bi = rand_n( len(best_words) )
        best   = best_words[bi]
        word   = best[0]
        pos    = best[1]
        x      = best[2]
        y      = best[3]
        across = best[4]
        info   = best[5]
        words_used[word] = best
        for ci in range(word_len):
            if across:
                grid[x+ci][y] = word[ci]
            else:
                grid[x][y+ci] = word[ci]
        #print( f'\n{word}: best_score={best_score}' )
        #print_grid()
print()
print_grid()
