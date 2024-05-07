 
filter_file = open('filterlist.txt','r')
word_list = open('wordlist.txt','w')
embeddings_file = open('embeddings.txt','r', encoding='utf8')
output_file = open('filtered_embeddings.txt','w')

nounlist = filter_file.read().split('\n')[:-1]
found = []

i=0
for line in embeddings_file:
    line_list = line.split(' ')
    word = line_list[0].split('_')[0]
    tag = line_list[0].split('_')[1]
    coords = line_list[1:]
    if word in nounlist and tag == 'NOUN':
        found.append(word)
        output_file.write(' '.join((coords)))
        word_list.write(f'{word}\n')
        i+=1

filter_file.close()
embeddings_file.close()
output_file.close()
word_list.close()