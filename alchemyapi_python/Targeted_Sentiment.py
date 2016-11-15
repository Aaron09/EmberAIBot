import json
from watson_developer_cloud import AlchemyLanguageV1

txt = 'I cant meet may 7th but id love to meet on may 8th'

with open('api_key.txt', 'r') as file:
  api_key = file.read()


alchemy_language = AlchemyLanguageV1(api_key=api_key)
print(json.dumps(
  alchemy_language.targeted_sentiment(
    text=txt, targets=['may 7th', 'may 8th']),
  indent=2))


response = alchemy_language.targeted_sentiment(text = txt, targets=['may 7th', 'may 8th'])

if response['status'] == 'OK':
    print('## Response Object ##')
    #print(json.dumps(response, indent=4))
    for target in response['results']:
    	print (str(target['text']), float(target['sentiment']['score']))
    #print('score: ', response.get("results"))
else:
    print('Error in targeted sentiment analysis call: ',
          response['statusInfo'])
