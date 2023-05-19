import customtkinter as ctk
import generator
import solver

#Defining Constants for colour pallete
DARK_BLUE = "#3d5a80"
MEDIUM_BLUE = "#98c1d9"
LIGHT_BLUE = "#e0fbfc"
ORANGE = "#ee6c4d"
GREY = "#293241"

COLOUR_LIST = ('#e6194B', '#3cb44b', '#ffe119', '#4363d8', '#f58231', '#911eb4', '#42d4f4', '#f032e6', '#bfef45', '#fabed4', '#469990', '#dcbeff', '#9A6324', '#fffac8', '#800000', '#aaffc3', '#808000', '#ffd8b1', '#000075', '#a9a9a9', '#ffffff', '#000000')


#From Internet (Jeremy Cantrell)
def hex_to_rgb(value):
    """Return (red, green, blue) for the color given as #rrggbb."""
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))


#From Internet (Jeremy Cantrell)
def rgb_to_hex(rgb):
    """Return color as #rrggbb for the given color values."""
    return '#%02x%02x%02x' % (int(rgb[0]), int(rgb[1]), int(rgb[2]))


def colour_blend(rgb1, rgb2):
    return ((rgb1[0]+rgb2[0]) // 2, (rgb1[1]+rgb2[1]) // 2, (rgb1[2]+rgb2[2]) // 2)  


def check_word_validity(word):
    word = word.upper()
    word_entry.delete(0, 'end')
    if not word.isalpha():
        feedback_label.configure(text_color="red", font=ctk.CTkFont(size=20))
        feedback.set("Words must be composed of letters!")
        return False
    if word in ' '.join(words) and len(words) > 0:
        feedback_label.configure(text_color="red", font=ctk.CTkFont(size=20))
        feedback.set("No substrings allowed!")
        return False
    if len(word) < 3:
        feedback_label.configure(text_color="red", font=ctk.CTkFont(size=20))
        feedback.set("Words must be at least 3 letters!")
        return False
    try:
        words.append(word)
        add_word(word)
    except NameError:
        pass


def populate_words():
    amount = number_of_words_slider.get() - len(words)
    size = word_search_size_slider.get()
    word_list = generator.generate_words(amount, size)
    for word in word_list:
        check_word_validity(word)


#Display all words in scrollable frame
def display_words():
    for word in words:
        add_word(word)
    if len(words) == 0:
        feedback.set("Number of Words: 0")
        feedback_label.configure(text_color="white", font=ctk.CTkFont(size=15))


#Delete all the words in the scrollable frame
def delete_words_in_scrollable_frame(word):
    for child in scrollable_frame.winfo_children():
        if isinstance(child, ctk.CTkFrame):
            child.destroy()
    words.remove(word)
    display_words()


#Add word to scrollable frame. Creates a sub-frame that contains the word and its delete button. (Sub-Frame helpful for packing and delete button referencing word)
def add_word(word):
    global feedback
    word_frame = ctk.CTkFrame(scrollable_frame)
    word_frame.pack(fill='x', pady=5)
    label = ctk.CTkLabel(word_frame, text=word)
    label.pack(side='left')
    delete_button = ctk.CTkButton(word_frame, text='Remove Word', command=lambda: delete_words_in_scrollable_frame(word), fg_color=DARK_BLUE, hover_color=ORANGE)
    delete_button.pack(side='right')
    feedback.set("Number of Words: " + str(len(words)))
    feedback_label.configure(text_color="white", font=ctk.CTkFont(size=15))


#Key Pressed Event. If it is "ENTER", run the word thorugh a series of checks and then add it 
def key_pressed(event):
    if event.keysym == 'Return':
        word = word_entry.get().split(' ', 1)[0]
        check_word_validity(word)


def size_scalar_event(value):
    word_search_size_label.configure(text=int(value))
    number_of_words_slider.set(value**2 // 9)
    number_of_words_scalar_event(value**2 // 9)


def number_of_words_scalar_event(value):
    number_of_words_label.configure(text=int(value))
    

def clear_frame():
    for widget in root.winfo_children():
       widget.destroy()


def solve_word_search_on_screen(word_search):
    solved_cube = solver.solve_word_search(word_search)
    clear_frame()
    generate_play_word_search_gui(solved_cube)


def generate_play_word_search_gui(word_search):
    title_label = ctk.CTkLabel(root, text="Play!", font=ctk.CTkFont(size=30, weight='bold'), text_color=LIGHT_BLUE)
    title_label.pack(padx=10, pady=(40, 20))

    words_and_button_frame = ctk.CTkFrame(root)
    words_and_button_frame.pack(fill='x', pady=5)

    board_box = ctk.CTkFrame(words_and_button_frame, width=400, height=400, fg_color='white')
    board_box.pack(side='left', padx=10)

    board = word_search.cube

    word_placement = word_search.word_placement
    fill_in_squares = {}
    solved_words = []
    if word_placement:
        for word_num, word in enumerate(word_placement):
            word_colour = COLOUR_LIST[word_num]
            solved_words.append(word[2])
            for i in range(len(word[2])):
                if str(word[0][0] + i * word[1][0]) +  str(word[0][1] + i * word[1][1]) in fill_in_squares:
                    colour = rgb_to_hex(colour_blend(hex_to_rgb(word_colour), hex_to_rgb(fill_in_squares[str(word[0][0] + i * word[1][0]) +  str(word[0][1] + i * word[1][1])])))
                    fill_in_squares[str(word[0][0] + i * word[1][0]) +  str(word[0][1] + i * word[1][1])] = colour
                else:
                    fill_in_squares[str(word[0][0] + i * word[1][0]) +  str(word[0][1] + i * word[1][1])] = word_colour


    for row_num, row in enumerate(board):
        board_box.rowconfigure(row_num, weight=1)
        for column_num, letter in enumerate(row):
            board_box.columnconfigure(column_num, weight=1)
            letter_label = ctk.CTkLabel(board_box, text=letter, width=400 / len(row), height=400 / len(row), text_color='black')
            letter_label.grid(row=row_num, column=column_num)
            if str(row_num) + str(column_num) in fill_in_squares:
                letter_label.configure(bg_color=fill_in_squares[str(row_num) + str(column_num)])
    
    solve_button = ctk.CTkButton(words_and_button_frame, text='Solve!', hover_color=ORANGE, fg_color=DARK_BLUE, 
                                     command=lambda: solve_word_search_on_screen(word_search))
    solve_button.pack(anchor='center', pady=30, padx=30)

    word_list_scrollable_frame = ctk.CTkScrollableFrame(words_and_button_frame)
    word_list_scrollable_frame.pack(anchor='center', pady=30, padx=30)

    for word in sorted(word_search.words):
        label = ctk.CTkLabel(word_list_scrollable_frame, text=word)
        label.pack()
        if solved_words and word in solved_words:
            label.configure(text_color=ORANGE)


def play_word_search(size, words):
    clear_frame()
    active_word_search = generator.generate_word_search(int(size), words)
    generate_play_word_search_gui(active_word_search)


#Generates Word Search GUI
def generate_word_search_gui():
    generate_button.destroy()
    global word_entry
    global words
    global scrollable_frame
    global feedback_label
    global feedback
    global word_search_size_label
    global word_search_size_slider
    global number_of_words_label
    global number_of_words_slider
    words = []
    title_label.configure(text="Word Search Generator", font=ctk.CTkFont(size=30, weight='bold'))

    words_and_button_frame = ctk.CTkFrame(root)
    words_and_button_frame.pack(fill='x', pady=5)

    scrollable_frame = ctk.CTkScrollableFrame(words_and_button_frame, width=500, height=300)
    scrollable_frame.pack(side='left', padx=(20, 0))
    
    fill_rest_button = ctk.CTkButton(words_and_button_frame, text='Auto-Generate Rest of Words', hover_color=ORANGE, fg_color=DARK_BLUE, 
                                     command=populate_words)
    fill_rest_button.pack(anchor='center', pady=30, padx=30)

    word_search_size_descriptor = ctk.CTkLabel(words_and_button_frame, text='Size', text_color=LIGHT_BLUE)
    word_search_size_descriptor.pack(anchor='center', pady=0, padx=30)

    word_search_size_label = ctk.CTkLabel(words_and_button_frame, text='', text_color=LIGHT_BLUE)
    word_search_size_label.pack(anchor='center', pady=0, padx=30)

    word_search_size_slider = ctk.CTkSlider(words_and_button_frame, from_=5, to=15, number_of_steps=10, command=size_scalar_event)
    word_search_size_slider.pack(padx=5, pady=5)

    number_of_words_descriptor = ctk.CTkLabel(words_and_button_frame, text='Recommended Number of Words', text_color=LIGHT_BLUE)
    number_of_words_descriptor.pack(anchor='center', pady=(30, 0), padx=30)

    number_of_words_label = ctk.CTkLabel(words_and_button_frame, text='', text_color=LIGHT_BLUE)
    number_of_words_label.pack(anchor='center', pady=0, padx=30)

    number_of_words_slider = ctk.CTkSlider(words_and_button_frame, from_=2, to=25, number_of_steps=23, command=number_of_words_scalar_event)
    number_of_words_slider.pack(padx=5, pady=5)

    word_entry = ctk.CTkEntry(scrollable_frame, placeholder_text='Enter Words Here')
    word_entry.pack(fill='x')

    feedback = ctk.StringVar()
    feedback.set("Number of Words: 0")
    feedback_label = ctk.CTkLabel(root, textvariable=feedback, font=ctk.CTkFont(size=15))
    feedback_label.pack(anchor='w', padx=(200, 0))

    go_button = ctk.CTkButton(root, text='Generate!', hover_color=ORANGE, fg_color=DARK_BLUE, command=lambda: play_word_search(word_search_size_slider.get(), words))
    go_button.pack(anchor='se', pady=0, padx=10)


root = ctk.CTk()
root.geometry('800x500')
root.title("Word Search")
root.bind('<Key>', key_pressed)

#Title Page
title_label = ctk.CTkLabel(root, text="Word Search", font=ctk.CTkFont(size=40, weight='bold'), text_color=LIGHT_BLUE)
title_label.pack(padx=10, pady=(40, 20))
generate_button = ctk.CTkButton(root, text='Generate', command=lambda: generate_word_search_gui(), height=50, width=100, fg_color=DARK_BLUE)
generate_button.pack(pady=(50, 0))

root.mainloop()
