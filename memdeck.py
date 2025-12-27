#!/usr/bin/env python3
#
# mydeck.py - help memorize a deck of cards
#
import sys
import json
import random
import time

def die( msg, prefix='ERROR: ' ):
    print( prefix + msg )
    if die_with_exception: 
        raise AssertionError
    else:
        sys.exit( 1 )

def clear():
    for i in range(100): print()

def pretty_suit( s ):
    if s == 's': return '♠️'
    if s == 'h': return '♥️ '
    if s == 'd': return '♦️'
    if s == 'c': return ' '
    die( f'bad suit character: {s}' )
    return ''

def pretty_card( c ):
    s = c[-1]
    ps = pretty_suit( s )
    pc = c[:-1] + ps
    return pc

def deck_print( deck, i, j ):
    print()
    tot = 0
    c = 0
    while i <= j:
        if c == 0: 
            print( f'{i:2d}: ', end='' )
        else:
            print( '  ', end='' )
        card = deck[i]
        pcard = pretty_card( card )
        print( f'{pcard:3s}', end='' )
        tot += 1
        c += 1
        if c == 4 or (tot % 13) == 0:
            print()
            if (tot % 13) == 0: print()
            c = 0
        i += 1

def rand_n( n ):
    return int( random.random() * n )

def input_int( prompt, v0, v1 ):
    while True:
        s = input( prompt )
        try:
            i = int(s)
            if i >= v0 and i <= v1: return i;
        except:
            pass
        print( f'Enter a valid integer in the range {v0} .. {v1}' )

#-----------------------------------------------------------------------
# process command line args
#-----------------------------------------------------------------------
if len( sys.argv ) < 1: die( 'usage: memdeck.py [options]', '' )
json_filename = 'mydeck.json'
do_print_deck = False
fwd_i_begin = 52
fwd_i_last  = 51
rev_i_begin = 0
rev_i_last  = -1
rand_card_cnt = 0
rand_qnum_cnt = 0
rand_cnum_cnt = 0
deck_end = 52
i = 1
while i < len( sys.argv ):
    arg = sys.argv[i]
    i += 1
    if   arg == '-json':
        json_filename = sys.argv[i]
    elif arg == '-pd':
        do_print_deck = int(sys.argv[i])
    elif arg == '-fb':
        fwd_i_begin = int(sys.argv[i])
    elif arg == '-fl':
        fwd_i_last = int(sys.argv[i])
    elif arg == '-fq': 
        q = int(sys.argv[i])
        fwd_i_begin = 13*q + 0
        fwd_i_last  = 13*q + 12
    elif arg == '-rb':
        rev_i_begin = int(sys.argv[i])
    elif arg == '-rl':
        rev_i_last = int(sys.argv[i])
    elif arg == '-rq': 
        q = int(sys.argv[i])
        rev_i_begin = 13*q + 12
        rev_i_last  = 13*q + 0
    elif arg == '-randc':
        rand_card_cnt = int(sys.argv[i])
    elif arg == '-randq':
        rand_qnum_cnt = int(sys.argv[i])
    elif arg == '-randn':
        rand_cnum_cnt = int(sys.argv[i])
    elif arg == '-de':
        deck_end = int(sys.argv[i])
    else:
        die( 'unknown arg: {arg}' )
    i += 1

random.seed( time.time() )

#-----------------------------------------------------------------------
# read in deck from private .json file
#-----------------------------------------------------------------------
with open( json_filename, 'r', encoding='utf-8' ) as f:
    data = json.load( f )
    deck = data['deck']

if do_print_deck: deck_print( deck, 0, 51 )
deck_len = len( deck )
if deck_len != 52: die( f'deck does not have 52 cards, got {deck_len}: {deck}' )

#-----------------------------------------------------------------------
# forward
#-----------------------------------------------------------------------
if fwd_i_begin <= fwd_i_last:
    missed = 1
    while missed != 0:
        input( '\nhit any key to continue' )
        clear()
        missed = 0
        print( '\nTell me the cards in forward order:\n' )
        i = fwd_i_begin
        while i <= fwd_i_last:
            ans = input( f'{i}: ' )
            ans = ans.rstrip()
            if ans != deck[i]: 
                missed += 1
                print( f'> {deck[i]}' )
            i += 1
        deck_print( deck, fwd_i_begin, fwd_i_last )

#-----------------------------------------------------------------------
# reverse
#-----------------------------------------------------------------------
if rev_i_last >= rev_i_begin:
    missed = 1
    while missed != 0:
        input( '\nhit any key to continue' )
        clear()
        missed = 0
        print( '\nTell me the cards in reverse order:\n' )
        i = rev_i_last
        while i >= rev_i_begin:
            ans = input( f'{i}: ' )
            ans = ans.rstrip()
            if ans != deck[i]: 
                missed += 1
                print( f'> {deck[i]}' )
            i -= 1
        deck_print( deck, rev_i_begin, rev_i_last )

#-----------------------------------------------------------------------
# random card
#-----------------------------------------------------------------------
if rand_card_cnt != 0:
    input( '\nhit any key to continue' )
    clear()
    print( '\nTell me the cards at these random indexes:\n' )
    for r in range(rand_card_cnt):
        i = rand_n( deck_end )
        ans = input( f'{i}: ' )
        ans = ans.rstrip()
        if ans != deck[i]: 
            print( f'> {deck[i]}' )

#-----------------------------------------------------------------------
# random card num
#-----------------------------------------------------------------------
if rand_cnum_cnt != 0:
    input( '\nhit any key to continue' )
    clear()
    print( '\nTell me the indexes of these random cards:\n' )
    for r in range(rand_cnum_cnt):
        i = rand_n( deck_end )
        card = deck[i]
        ii = input_int( f'{card}: ', 0, 51 )
        if ii != i:
            print( f'> {i}' )

#-----------------------------------------------------------------------
# random quadrant num
#-----------------------------------------------------------------------
if rand_qnum_cnt != 0:
    input( '\nhit any key to continue' )
    clear()
    print( '\nTell me the quandrant of these random cards:\n' )
    for r in range(rand_qnum_cnt):
        i = rand_n( deck_end )
        q = int( i / 13 )
        card = deck[i]
        qq = input_int( f'{card}: ', 0, 3 )
        if qq != q:
            qi = i % 13
            qr = int(qi/4)
            qc = qi % 4
            print( f'> {q} ({i}, r{qr}, c{qc})' )
