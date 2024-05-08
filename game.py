""" Main module containing logic for Em8eddings game."""

import numpy as np
import json
import random

def find_closest_indices(indices, target_index, N):
    """ Finds N closest words to target_index by proximity in embeddings space. """
    # Extract coordinates of target_index
    target_coords = indices[target_index]
    # Compute distances between target_index and all other indices
    distances = np.linalg.norm(indices - target_coords, axis=1)
    # Sort indices based on distances and get the N closest ones
    closest_indices = distances.argsort()[:N]
    return closest_indices


class Game():
    """ Class containing logic for the game. """
    def __init__(self):
        """ Initialises class. Sets list of words, embeddings, and hints, as well as data necessary to show start screen."""
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
                'show_string': f'{self.start_text.split(" ")[i]}',
                'hint': "",
                'len': len(f'Neighbour {i}'),
                'locked': False
            } for i in range(8)]


    def load_files(self):
        """ Loads data from data/ directory, includding embeddings and the list of words."""
        # Open files
        coords_file = open('data/filtered_embeddings.txt','r')
        word_file = open('data/wordlist.txt','r')
        word_data_file = open('data/word_data.json','r')
        hints_file = open('data/hints.json','r')
        word_data = json.load(word_data_file)

        # Load data
        hints = json.load(hints_file)
        nounlist = word_file.read().split('\n')[:-1]
        coords = coords_file.read().split('\n')[:-1]
        coords = [c.split(' ') for c in coords]
        coords = np.array([[float(x) for x in c] for c in coords])

        # Close files
        word_file.close()
        coords_file.close()
        word_data_file.close()
        hints_file.close()
        return nounlist, coords, word_data, hints


    def get_gamedata(self):
        """ Fetches data about the game to send to the front-end web UI."""
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
        """ Get how much time the player has per word, based on number of rounds played."""
        if self.rounds_played < 3:
            return 90
        elif self.rounds_played < 6:
            return 60
        elif self.rounds_played < 9:
            return 45
        else:
            return 30


    def start_game(self):
        """ Initialises the game by choosing a center word, targets, and setting scores to 0."""
        self.state = 'started'
        self.rounds_played = 0
        self.score = 0
        self.targets_hit = 0
        self.guessed_words = []
        self.select_word()
        self.get_targets()


    def select_word(self, selected_word = None):
        """ Selects a new word to go in the centre. If selected_word is None, chooses randomly.
            Otherwise, chooses the guessed neighbour.

            TODO: Break up into separate methods
        """
        if selected_word is not None:
            self.selected_word = selected_word
        else:
            self.selected_word = random.randint(0, self.num_words-1)

        # Append selected word to already guessed words, so it can't be a future neighbour
        self.guessed_words.append(self.selected_word)

        # If target is reached, reward player and get a new target
        if selected_word is not None:
            if selected_word in self.targets:
                # Increase score for player
                self.targets_hit += 1
                self.score += (100 * self.targets_hit)

                # Get a new target
                attempts = 0
                while True:
                    attempts += 1
                    new_target = random.randint(0, self.num_words-1)
                    if new_target not in self.targets and new_target not in self.guessed_words or attempts > 100:
                        break
                
                # If can't find a new target, give up
                if attempts > 100:
                    self.targets.remove(selected_word)
                else:
                    self.targets[self.targets.index(selected_word)] = new_target

        # Fetch new neighbours
        closest_indices = find_closest_indices(self.coords, self.selected_word, 9)[1:]
        for i in range(8):
            self.neighbours[i]['word_id'] = closest_indices[i]
            self.neighbours[i]['word_string'] = self.nounlist[closest_indices[i]]
            self.neighbours[i]['show_string'] = len(self.nounlist[closest_indices[i]]) * '_ '
            self.neighbours[i]['len'] = len(self.nounlist[closest_indices[i]])
            self.neighbours[i]['locked'] = self.neighbours[i]['word_id'] in self.guessed_words

        # Fetch new hints
        self.get_hints()

    
    def get_targets(self):
        """ Generates targets at the start of game."""
        while True:
            targets = [random.randint(0, self.num_words-1) for i in range(5)]
            if self.selected_word not in targets and len(targets) == len(set(targets)):
                break
        self.targets = targets


    def get_hints(self):
        """ Randomly choose hints for each neighbouring word. """
        # Three options
        hint_options = ['medium', 'hard', 'phonetics']
        for neighbour in self.neighbours:
            # Choose at random
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
        
            # Additionally, 1/3 chance of some letters in the word to be shown
            if random.random() < (1/3):
                # Based on length
                if len(neighbour['word_string']) > 5:
                    neighbour['show_string'] = neighbour['word_string'][:2] + '_ '*(len(neighbour['word_string'])-2)
                else:
                    neighbour['show_string'] = neighbour['word_string'][:1] + '_ '*(len(neighbour['word_string'])-1)

    def check_answer(self, textbox_id, textbox_data):
        """ Check if a user given guess is correct"""
        # If so, reward the player and move words.
        if self.neighbours[textbox_id]['word_string'] == textbox_data:
            print('Correct Guess')
            self.select_word(self.neighbours[textbox_id]['word_id'])
            self.rounds_played += 1
            self.score += 10
            return True
        else:
            print(f'Incorrect!, your guess was {textbox_data}, but the answer was {self.neighbours[textbox_id]["word_string"]}')
            return False
