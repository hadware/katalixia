import pickle
import random

from voxpopuli import Voice, PhonemeList
from typing import Union, Dict, List
from random import randint


class TreeNode:

    def __init__(self):
        self.children = dict() # type:Dict[str,TreeNode]
        self.leaves = list() # type:List[Leaf]

    def __getitem__(self, item):
        return self.children[item]

    def insert(self, leaf: 'Leaf', current_pho_index):
        try:
            leaf_current_pho = leaf.phonemes[-current_pho_index].name
        except IndexError: # if this leaf has "no more" phonems to unstack, it's stored on this node's leaves
            self.leaves.append(leaf)
            return

        if leaf_current_pho not in self.children:
            self.children[leaf_current_pho] = leaf
        else:
            current_child = self.children[leaf_current_pho]

            if isinstance(current_child, Leaf): # creating the new node
                new_node = TreeNode()
                new_node.insert(current_child, current_pho_index + 1)
                new_node.insert(leaf, current_pho_index + 1)
                self.children[leaf_current_pho] = new_node

            elif isinstance(current_child, TreeNode):
                current_child.insert(leaf, current_pho_index + 1)

    def find_random(self):
        if self.leaves and randint(0,1):
            return random.choice(self.leaves).text

        else:
            rnd_child = random.choice(list(self.children.values()))
            if isinstance(rnd_child, Leaf):
                return rnd_child.text
            else:
                return rnd_child.find_random()

    def find(self, phoneme_list: PhonemeList):
        if not phoneme_list:
            return self.find_random()
        else:
            current_pho = phoneme_list.pop().name
            if current_pho in self.children:
                current_child = self.children[current_pho]
                if isinstance(current_child, Leaf):
                    return current_child.text
                else:
                    return current_child.find(phoneme_list)

    def to_dict(self):
        return { "children" : {pho: child.to_dict() for pho, child in self.children.items()},
                 "leaves" : [leaf.text for leaf in self.leaves]}


class RhymeTree(TreeNode):

    def __init__(self, rhyming_lang="fr"):
        super().__init__()
        self.voice = Voice(lang=rhyming_lang)
        self.children = dict() # type:Dict[str,Union[TreeNode, Leaf]]

    def insert_rhyme(self, rhyme_string):
        new_leaf = Leaf.from_string(rhyme_string.strip(), self.voice)
        self.insert(new_leaf, 1)

    def find_rhyme(self, string):
        string_phonemes = Leaf.clean_silences(self.voice.to_phonemes(string))
        current_pho = string_phonemes.pop()
        if current_pho.name not in self.children:
            return None
        else:
            return self.children[current_pho.name].find(string_phonemes)

    @classmethod
    def from_pickle(cls, pickle_filepath):
        with open(pickle_filepath, "rb") as picklefile:
            return pickle.load(picklefile)

    @classmethod
    def from_text_file(cls, textfile_filepath, separator=None):
        separator = separator if separator is not None else "\n"
        with open(textfile_filepath) as file:
            all_strings = file.read().split(separator)

        return cls.from_word_list(all_strings)

    @classmethod
    def from_word_list(cls, input_list):
        tree = cls()
        for string in input_list:
            tree.insert_rhyme(string)

        return tree

    def to_dict(self):
        return { pho : child.to_dict() for pho, child in self.children.items()}


class Leaf:

    def __init__(self, string, phonemic_form):
        self.text = string
        self.phonemes = phonemic_form # type:PhonemeList

    @staticmethod
    def clean_silences(phoneme_list):
        while phoneme_list[-1].name == "_":
            phoneme_list.pop()
        return phoneme_list

    @classmethod
    def from_string(cls, string, voxpopuli_voice):
        return cls(string, cls.clean_silences(voxpopuli_voice.to_phonemes(string)))

    def to_dict(self):
        return self.text