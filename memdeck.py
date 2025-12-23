#!/usr/bin/env python3
#
# mydeck.py - help memorize a deck of cards
#
import sys
import json

def die( msg, prefix='ERROR: ' ):
    print( prefix + msg )
    if die_with_exception: 
        raise AssertionError
    else:
        sys.exit( 1 )

def deck_print( deck, i, j ):
    tot = 0
    c = 0
    while i <= j:
        if c == 0: 
            print( f'{i:2d}: ', end='' )
        else:
            print( '  ', end='' )
        card = deck[i]
        print( f'{card:3s}', end='' )
        tot += 1
        c += 1
        if c == 4 or (tot % 13) == 0:
            print()
            if (tot % 13) == 0: print()
            c = 0
        i += 1

#-----------------------------------------------------------------------
# process command line args
#-----------------------------------------------------------------------
if len( sys.argv ) < 1: die( 'usage: memdeck.py [options]', '' )
json_filename = 'mydeck.json'
do_print_deck = False
fwd_i_begin = 0
fwd_i_last  = 52
rev_i_begin = 51
rev_i_last  = 0
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
    else:
        i -= 1
        break
    i += 1

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
    print( '\nTell me the cards in forward order:\n' )
    i = fwd_i_begin
    while i <= fwd_i_last:
        ans = input( f'{i}: ' )
        ans = ans.rstrip()
        if ans != deck[i]: print( f'*{deck[i]}' )
        i += 1

deck_print( deck, fwd_i_begin, fwd_i_last )

#-----------------------------------------------------------------------
# reverse
#-----------------------------------------------------------------------
if rev_i_last >= rev_i_begin:
    print( '\nTell me the cards in reverse order:\n' )
    i = rev_i_last
    while i >= rev_i_begin:
        ans = input( f'{i}: ' )
        ans = ans.rstrip()
        if ans != deck[i]: print( f'*{deck[i]}' )
        i -= 1
