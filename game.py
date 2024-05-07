import numpy as np
from random import randint
import matplotlib.pyplot as plt
from blessed import Terminal
from math_utils import calculate_octant, find_closest_indices, directions

coords_file = open('filtered_embeddings.txt','r')
word_file = open('wordlist.txt','r')

nounlist = word_file.read().split('\n')[:-1]
coords = coords_file.read().split('\n')[:-1]
coords = [c.split(' ') for c in coords]
coords = np.array([[float(x) for x in c] for c in coords])

word_file.close()
coords_file.close()


num_words = len(nounlist)

selected_word = randint(0,num_words-1)

closest_indices = find_closest_indices(coords, selected_word, 25)[1:]

# term = Terminal()
# 
# print(term.home + term.clear + term.move_y(term.height // 4))
# print(term.black_on_darkkhaki(term.center('Road to Embeddings.')))
# print(term.move_y((term.height // 4) + 1))
# print(term.black_on_darkkhaki(term.center('A game about guessing semantically seeming words.')))
# print(term.move_y(term.height // 2))
# print(term.black_on_darkkhaki(term.center('Press any key to start.')))
# 
# with term.cbreak(), term.hidden_cursor():
#     inp = term.inkey()
# 
# print(term.move_down(2) + 'You pressed ' + term.bold(repr(inp)))

def get_stuff():
    stuff = [nounlist[selected_word], [nounlist[i] for i in closest_indices[:8]]]
    print(nounlist[selected_word])
    return stuff