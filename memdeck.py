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

# read in deck from private .json file
#
with open( 'mydeck.json', 'r', encoding='utf-8' ) as f:
    data = json.load( f )
    deck = data['deck']

#print( deck )
deck_len = len( deck )
if deck_len != 52: die( f'deck does not have 52 cards, got {deck_len}: {deck}' )

# forward direction
#
print( '\nTell me the cards in forward order:\n' )
i = 0
for c in deck:
    ans = input( f'{i}: ' )
    ans = ans.rstrip()
    if ans != deck[i]: print( f'*{deck[i]}' )
    i += 1
