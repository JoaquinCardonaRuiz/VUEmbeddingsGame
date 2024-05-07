import json
from wiktionaryparser import WiktionaryParser

word_file = open('wordlist.txt','r')
nounlist = word_file.read().split('\n')[:-1]
parser = WiktionaryParser()

num_words = len(nounlist)
failed = []

word_data = {}
for i,noun in enumerate(nounlist):
    print(f'Processed {i}/{num_words} words ({round(100*(i/num_words),2)}%)',end='\r')
    try:
        data = parser.fetch(noun)
    except:
        failed.append(noun)
    try:
        word_data[noun] = data[0]
    except IndexError:
        word_data[noun] = None
        failed.append(noun)

with open("word_data.json",'w', encoding='utf8') as output_file:
    output_file.write(json.dumps(word_data, indent=4))