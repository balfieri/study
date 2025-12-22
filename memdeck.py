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

#-----------------------------------------------------------------------
# process command line args
#-----------------------------------------------------------------------
if len( sys.argv ) < 1: die( 'usage: memdeck.py [options]', '' )
json_filename = 'mydeck.json'
do_print_deck = False
do_forward = True
do_reverse = True
i = 1
while i < len( sys.argv ):
    arg = sys.argv[i]
    i += 1
    if   arg == '-json':
        json_filename = sys.argv[i]
    elif arg == '-pd':
        do_print_deck = int(sys.argv[i])
    elif arg == '-f':
        do_forward = int(sys.argv[i])
    elif arg == '-r':
        do_reverse = int(sys.argv[i])
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

if do_print_deck: print( deck )
deck_len = len( deck )
if deck_len != 52: die( f'deck does not have 52 cards, got {deck_len}: {deck}' )

#-----------------------------------------------------------------------
# forward
#-----------------------------------------------------------------------
if do_forward:
    print( '\nTell me the cards in forward order:\n' )
    i = 0
    while i < 52:
        ans = input( f'{i}: ' )
        ans = ans.rstrip()
        if ans != deck[i]: print( f'*{deck[i]}' )
        i += 1

#-----------------------------------------------------------------------
# reverse
#-----------------------------------------------------------------------
if do_reverse:
    print( '\nTell me the cards in reverse order:\n' )
    i = 51
    while i >= 0:
        ans = input( f'{i}: ' )
        ans = ans.rstrip()
        if ans != deck[i]: print( f'*{deck[i]}' )
        i -= 1
