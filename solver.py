import numpy as np

_end = "_end_"
directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]


class WordSearch:

    def __init__(self, size):
        self.cube = np.zeros((size, size), dtype=str)
        self.words = []
        self.word_placement = {}


def create_trie(words):
    root = dict()
    for word in words:
        current_dict = root
        for letter in word:
            current_dict = current_dict.setdefault(letter, {})
        current_dict[_end] = _end
    return root


def in_trie(trie, word_search_array, row: int, column: int):
    base_r = row
    base_c = column
    current_dict = trie
    if word_search_array[row, column] in current_dict:
        for direction in directions:
            word = word_search_array[base_r, base_c]
            row = base_r
            column = base_c
            current_dict = trie[word]
            row += direction[0]
            column += direction[1]
            while (0 <= row < word_search_array.shape[0]) and (0 <= column < word_search_array.shape[1]):
                if word_search_array[row, column] not in current_dict:
                    break
                current_dict = current_dict[word_search_array[row, column]]
                word += word_search_array[row, column]
                row += direction[0]
                column += direction[1]

            if _end in current_dict:
                return True, direction, word

    return False, None, None


def solve_word_search(word_search: WordSearch):
    shape = word_search.cube.shape
    word_search_array = word_search.cube
    trie = create_trie(word_search.words)

    for row in range(int(shape[0])):
        for column in range(int(shape[1])):
            repeat = True
            while repeat:
                data = in_trie(trie, word_search_array, row, column)
                if data[0]:
                    direction = data[1]
                    word = data[2]
                    word_search.word_placement[word] = [[row + i * direction[0], column + i * direction[1]] for i in range(len(word))]
                    word_search.words.remove(word)
                    trie = create_trie(word_search.words)
                    repeat = True

                else:
                    repeat = False
    word_search.words = [word for word in word_search.word_placement]
    return word_search
