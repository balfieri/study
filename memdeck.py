#!/usr/bin/env python3
#
# mydeck.py - help me memorize a deck of cards
#
import json

# read in mydeck from private .json file
#
with open( 'mydeck.json', 'r', encoding='utf-8' ) as f:
    data = json.load( f )
    deck = data['deck']

print( deck )
