from __future__ import print_function
from alchemyapi import AlchemyAPI
import json

demo_text = "Yep, Sent this to Ryan but my availability from now till then is Monday 11/7 7am-10am (PST) Tuesday 11/8 12:15pm-5pm (PST) Wednesday 11/9 1:15pm-onwards (PST) Thursday 11/10 1:15pm -onwards (PST) Friday 11/11 1:15pm-onwards (PST) Monday 11/14 7am-10am (PST) Tuesday 11/15 12:15pm-5pm (PST) Wednesday 11/16 1:15pm-onwards (PST) Thursday 11/17 1:00pm -3pm (PST) Friday 11/18 11:00 am) - 1pm (PST) Sorry for making this hard on you. Thanks so much"

# Create the AlchemyAPI Object
alchemyapi = AlchemyAPI()


response = alchemyapi.entities('text', demo_text, {'sentiment': 1})

for entity in response['entities']:
        print('text: ', entity['text'].encode('utf-8'))
        print('type: ', entity['type'])
        print('relevance: ', entity['relevance'])
        print('sentiment: ', entity['sentiment']['type'])
        if 'score' in entity['sentiment']:
            print('sentiment score: ' + entity['sentiment']['score'])
        print('')