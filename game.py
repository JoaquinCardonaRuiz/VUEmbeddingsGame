import numpy as np
import json
import matplotlib.pyplot as plt
from blessed import Terminal
from math_utils import calculate_octant, find_closest_indices, directions
import random

class Game():
    def __init__(self):
        self.nounlist, self.coords, self.word_data, self.hints = self.load_files()
        self.filtered_words = [1741,3139,1812,1937,3399,3558,4081]
        self.num_words = len(self.nounlist)
        self.state = "not_started"
        self.start_text = 'Guess the word by its most similar neighbours.'
        self.selected_word = None
        self.neighbours = [
            {
                'word_id': i,
                'word_string' : f'Neighbour {i}',
                'show_string': f'{self.start_text.split(' ')[i]}',
                'hint': "",
                'len': len(f'Neighbour {i}')
            } for i in range(8)]

    def load_files(self):
        coords_file = open('filtered_embeddings.txt','r')
        word_file = open('wordlist.txt','r')
        word_data_file = open('word_data.json','r')
        hints_file = open('hints.json','r')
        word_data = json.load(word_data_file)
        hints = json.load(hints_file)
        nounlist = word_file.read().split('\n')[:-1]
        coords = coords_file.read().split('\n')[:-1]
        coords = [c.split(' ') for c in coords]
        coords = np.array([[float(x) for x in c] for c in coords])
        word_file.close()
        coords_file.close()
        word_data_file.close()
        hints_file.close()
        return nounlist, coords, word_data, hints

    def get_gamedata(self):
        if self.state == "started":
            return {
                "state": self.state,
                "selected_word": self.nounlist[self.selected_word],
                "neighbours": self.neighbours,
                "time": self.get_time(),
                "score": self.score,
                "targets": ', '.join([self.nounlist[target] for target in self.targets])
            }
        else:
            return {
                "state": self.state,
                "selected_word": "Em8eddings",
                "neighbours": self.neighbours,
                "time": 0
            }

    def get_time(self):
        if self.rounds_played < 3:
            return 90
        elif self.rounds_played < 6:
            return 60
        elif self.rounds_played < 9:
            return 45
        else:
            return 30

    def start_game(self):
        self.state = 'started'
        self.rounds_played = 0
        self.score = 0
        self.targets_hit = 0
        self.guessed_words = []
        self.select_word()
        self.get_targets()
        
    def select_word(self, selected_word = None):
        if selected_word:
            self.selected_word = selected_word
        else:
            self.selected_word = random.randint(0, self.num_words-1)
        self.guessed_words.append(self.selected_word)

        if selected_word:
            if selected_word in self.targets:
                self.targets_hit += 1
                score += (100 * self.targets_hit)
                while True:
                    new_target = random.randint(0, self.num_words-1)
                    if new_target not in self.targets and new_target not in self.guessed_words:
                        break
                self.targets[self.targets.index(selected_word)] = new_target

        closest_indices = find_closest_indices(self.coords, self.selected_word, 9)[1:]
        for i in range(8):
            self.neighbours[i]['word_id'] = closest_indices[i]
            self.neighbours[i]['word_string'] = self.nounlist[closest_indices[i]]
            self.neighbours[i]['show_string'] = len(self.nounlist[closest_indices[i]]) * '_ '
            self.neighbours[i]['len'] = len(self.nounlist[closest_indices[i]])
        self.get_hints()

    
    def get_targets(self):
        while True:
            targets = [random.randint(0, self.num_words-1) for i in range(5)]
            if self.selected_word not in targets and len(targets) == len(set(targets)):
                break
        self.targets = targets


    def get_hints(self):
        hint_options = ['medium', 'hard', 'phonetics']
        for neighbour in self.neighbours:
            hint_type = random.choice(hint_options)
            if hint_type == 'medium':
                neighbour['hint'] = self.hints[neighbour['word_string']]['Medium']
            elif hint_type == 'hard':
                neighbour['hint'] = self.hints[neighbour['word_string']]['Hard']
            elif hint_type == 'phonetics':
                try:
                    neighbour['hint'] = 'IPA' + self.word_data[neighbour['word_string']]['pronunciations']['text'][0].split('IPA')[1]
                except IndexError:
                    neighbour['hint'] = neighbour['hint'] = self.hints[neighbour['word_string']]['Hard']
            else:
                neighbour['hint'] = 'None'
        
            if random.random() < (1/3):
                if len(neighbour['word_string']) > 5:
                    neighbour['show_string'] = neighbour['word_string'][:2] + '_ '*(len(neighbour['word_string'])-2)
                else:
                    neighbour['show_string'] = neighbour['word_string'][:1] + '_ '*(len(neighbour['word_string'])-1)

    def check_answer(self, textbox_id, textbox_data):
        if self.neighbours[textbox_id]['word_string'] == textbox_data:
            print('Correct Guess')
            self.select_word(self.neighbours[textbox_id]['word_id'])
            self.rounds_played += 1
            self.score += 10
            return True
        else:
            print(f'Incorrect!, your guess was {textbox_data}, but the answer was {self.neighbours[textbox_id]['word_string']}')
            return False
