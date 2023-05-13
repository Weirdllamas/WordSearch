import random
import requests
import solver
from timeit import default_timer as timer
import string

word_site = "https://www.mit.edu/~ecprice/wordlist.10000"


def check_validity(board, word, direction, coordinate):
    row = coordinate[0]
    column = coordinate[1]
    x_max = board.shape[0]
    y_max = board.shape[1]

    if not (0 <= (row + (direction[0] * (len(word) - 1))) < x_max):
        return False
    if not (0 <= (column + (direction[1] * (len(word) - 1))) < y_max):
        return False

    for letter in word:
        if board[row, column] not in ('', letter):
            return False
        row += direction[0]
        column += direction[1]
    return True


def place_word(generating_word_search, word, free_coordinates):
    if len(free_coordinates) == 0:
        return None
    word_search = generating_word_search.cube
    while len(free_coordinates) > 0:
        coordinate = random.choice(free_coordinates)
        row, column = coordinate[0], coordinate[1]

        if word_search[row, column] in ('', word[0]):
            free_directions = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]
            while len(free_directions) > 0:
                direction = random.choice(free_directions)
                if not check_validity(word_search, word, direction, coordinate):
                    free_directions.remove(direction)
                    continue
                else:
                    for letter in word:
                        word_search[row, column] = letter
                        row += direction[0]
                        column += direction[1]
                    return word_search
            else:
                free_coordinates.remove(coordinate)
        else:
            free_coordinates.remove(coordinate)
    else:
        return None


def generate_word_search(size=15, words=None, store=0):
    global word_site
    n_of_attempts = 10
    while n_of_attempts > 0:
        generating_word_search = solver.WordSearch(size)

        if words:
            generating_word_search.words = words
        else:
            response = requests.get(word_site)
            words = response.content.splitlines()
            generating_word_search.words = random.sample(words, 24)

        free_coordinates = []
        for row in range(size):
            for column in range(size):
                free_coordinates.append([row, column])
        for word in words:
            data = place_word(generating_word_search, word, free_coordinates)
            if data is None:
                n_of_attempts -= 1
                break
            else:
                generating_word_search.cube = data
        else:
            place_random_letter(generating_word_search.cube)
            return generating_word_search


def place_random_letter(board):
    for row in range(board.shape[0]):
        for column in range(board.shape[1]):
            if board[row, column] == '':
                board[row, column] = random.choice(string.ascii_uppercase)
    return board


word_list1 = ["ARDEN", "HARMER", "MCKENNITT", "CLARK", "JEPSEN", "MCLACHLAN", "DION", "KRALL", "MITCHELL", "DOBSON",
              "KREVIAZUK", "MORISSETTE", "EDWARDS", "LANG", "MURRAY", "FABIAN", "LAVIGNE", "MYLES", "FEIST",
              "MARSHALL", "RYDER", "FURTADO", "MCDONALD", "TWAIN"]

word_list2 = ['DOG', 'CAT', 'BEAR', 'FISH']

start = timer()
unsolved = generate_word_search(size=15, words=word_list1)
end = timer()
print(end - start)
print(unsolved.cube)

solved = solver.solve_word_search(unsolved)
