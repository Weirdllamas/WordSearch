import customtkinter as ctk

#Defining Constants for colour pallete
DARK_BLUE = "#3d5a80"
MEDIUM_BLUE = "#98c1d9"
LIGHT_BLUE = "#e0fbfc"
ORANGE = "#ee6c4d"
GREY = "#293241"


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
        word = word.upper()
        word_entry.delete(0, 'end')
        if not word.isalpha():
            feedback_label.configure(text_color="red", font=ctk.CTkFont(size=20))
            feedback.set("Words must be composed of letters!")
            return
        if word in ' '.join(words) and len(words) > 1:
            feedback_label.configure(text_color="red", font=ctk.CTkFont(size=20))
            feedback.set("No substrings allowed!")
            return
        if len(word) < 3:
            feedback_label.configure(text_color="red", font=ctk.CTkFont(size=20))
            feedback.set("Words must be at least 3 letters!")
            return
        try:
            words.append(word)
            add_word(word)
        except NameError:
            pass


root = ctk.CTk()
root.geometry('800x500')
root.title("Word Search")
root.bind('<Key>', key_pressed)


#Generates Word Search GUI
def generate_word_search_gui():
    generate_button.destroy()
    global word_entry
    global words
    global scrollable_frame
    global feedback_label
    global feedback
    words = []
    title_label.configure(text="Word Search Generator", font=ctk.CTkFont(size=30, weight='bold'))

    scrollable_frame = ctk.CTkScrollableFrame(root, width=500, height=300)
    scrollable_frame.pack(anchor='w', padx=20)

    word_entry = ctk.CTkEntry(scrollable_frame, placeholder_text='Enter Words Here')
    word_entry.pack(fill='x')

    feedback = ctk.StringVar()
    feedback.set("Number of Words: 0")
    feedback_label = ctk.CTkLabel(root, textvariable=feedback, font=ctk.CTkFont(size=15))
    feedback_label.pack(anchor='w', padx=(200, 0))

    go_button = ctk.CTkButton(root, text='Generate!', hover_color=ORANGE, fg_color=DARK_BLUE)
    go_button.pack(anchor='se', pady=0, padx=10)


#Title Page
title_label = ctk.CTkLabel(root, text="Word Search", font=ctk.CTkFont(size=40, weight='bold'), text_color=LIGHT_BLUE)
title_label.pack(padx=10, pady=(40, 20))
generate_button = ctk.CTkButton(root, text='Generate', command=lambda: generate_word_search_gui(), height=50, width=100, fg_color=DARK_BLUE)
generate_button.pack(pady=(50, 0))

root.mainloop()
