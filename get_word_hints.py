import requests
import json
import groq


def generate_response(prompt, client):
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

    


with open('wordlist.txt','r') as word_file:
    nounlist = word_file.read().split('\n')[:-1]

with open('llm_template.txt','r') as template_file:
    template = template_file.read()

with open('credentials.txt','r') as creds_file:
    key = creds_file.read()

with open('hints.json','r') as hints_file:
    hints_dict = json.load(hints_file)

for word in nounlist:
    print(f'Selected word: {word}')
    if word not in hints_dict.keys():
        print(f'Fetching hints for {word}')
        hints = generate_response(template.replace('{word}',word), client=groq.Groq(api_key=key))
        hints = hints.replace('\n',' ')
        if hints != "Error":
            print(f'Hints for {word} successful.')
            hints_dict[word] = hints
            with open('hints.json','w') as hints_file:
                json.dump(hints_dict,hints_file)
            print(f'Hints for {word} written to file.')
        else:
            print(f'Hints for {word} error.')
    else:
        print(f'{word} already has hints.')
with open('hints.json','w') as hints_file:
    json.dump(hints_dict,hints_file,indent=4)