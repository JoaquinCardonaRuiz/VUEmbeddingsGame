""" Generate filtered embeddings for the game.

This script takes a file with tagged embeddings, and a list of nouns, and generates two new files:

    - wordlist.txt has a list of every noun from the list which had an embedding.
    - filtered_embeddings.txt has the embeddings for every word in wordlist.txt, in the same order.

Only run to generate filtered_embeddings.txt.
"""

# List of common nouns
filter_file = open('data/filterlist.txt','r')
# Embeddings
embeddings_file = open('data/embeddings.txt','r', encoding='utf8')

# Resulting words found in common nouns that have embeddings
word_list = open('data/wordlist.txt','w')

# Resulting filtered embeddings
output_file = open('data/filtered_embeddings.txt','w')

nounlist = filter_file.read().split('\n')[:-1]
found = []

i=0
# For every embedding, we check if it's on the filter file 
for line in embeddings_file:
    line_list = line.split(' ')
    word = line_list[0].split('_')[0]
    tag = line_list[0].split('_')[1]
    coords = line_list[1:]

    # If it is, we find the NOUN embeddings for it
    # And write the resulting embeddings to our filtered file
    if word in nounlist and tag == 'NOUN':
        found.append(word)
        output_file.write(' '.join((coords)))
        word_list.write(f'{word}\n')
        i+=1

filter_file.close()
embeddings_file.close()
output_file.close()
word_list.close()