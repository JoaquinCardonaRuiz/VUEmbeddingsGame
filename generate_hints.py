""" Generate hints using the Llama3 LLM

This script takes a list of words, a prompt template, and credentials to access Llama3.
It iterates through every word, filling in the prompt template and sending it to Llama3 to generate
hints for the game.

It outputs the file hints.json, a dictionary in which the key is the word, and the value is hints for it.

Only run to generate hints.jsons. Credentials not included in git.

"""

import json
import groq


def generate_response(prompt, client):
    """ Send prompt to Llama 3"""
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],

            model="llama3-8b-8192",
            temperature=0.7,
            max_tokens=75
            )
    except groq.InternalServerError:
        return "Error"

    return chat_completion.choices[0].message.content

    

# List of words
with open('data/wordlist.txt','r') as word_file:
    nounlist = word_file.read().split('\n')[:-1]

# Prompt template to fill
with open('data/llm_template.txt','r') as template_file:
    template = template_file.read()

# Credentials for Llama3
with open('credentials.txt','r') as creds_file:
    key = creds_file.read()

# Output file, we read it in case this script has been run before
# but not all queries were successful, so we fill the gaps.
# If this script is ran for the first time, it will be an empty dict.
with open('data/hints.json','r') as hints_file:
    hints_dict = json.load(hints_file)

# Iterate through every word
for word in nounlist:
    print(f'Selected word: {word}')
    # If the word does not already have hints, we generate them
    if word not in hints_dict.keys():
        print(f'Fetching hints for {word}')
        hints = generate_response(template.replace('{word}',word), client=groq.Groq(api_key=key))
        hints = hints.replace('\n',' ')
        # If the query was successful, we save it to file
        if hints != "Error":
            print(f'Hints for {word} successful.')
            hints_dict[word] = hints
            with open('data/hints.json','w') as hints_file:
                json.dump(hints_dict,hints_file)
            print(f'Hints for {word} written to file.')
        else:
            print(f'Hints for {word} error.')
    else:
        print(f'{word} already has hints.')


with open('data/hints.json','w') as hints_file:
    json.dump(hints_dict,hints_file,indent=4)