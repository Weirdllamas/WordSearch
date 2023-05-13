import customtkinter as ctk


def display_words():
    for word in words:
        add_word(word)
    if len(words) == 0:
        feedback.set("Number of Words: 0")


def delete_words_in_scrollable_frame(word):
    for child in scrollable_frame.winfo_children():
        if isinstance(child, ctk.CTkFrame):
            child.destroy()
    words.remove(word)
    display_words()


def add_word(word):
    global feedback
    if not word.isalpha():
        feedback_label.configure(text_color="red", font=ctk.CTkFont(size=20))
        feedback.set("Words must be composed of letters!")
        words.remove(word)
        return
    word_frame = ctk.CTkFrame(scrollable_frame)
    word_frame.pack(fill='x', pady=5)
    label = ctk.CTkLabel(word_frame, text=word)
    label.pack(side='left')
    delete_button = ctk.CTkButton(word_frame, text='Remove Word', command=lambda: delete_words_in_scrollable_frame(word))
    delete_button.pack(side='right')
    feedback.set("Number of Words: " + str(len(words)))
    feedback_label.configure(text_color="white", font=ctk.CTkFont(size=15))


def key_pressed(event):
    if event.keysym == 'Return':
        word = word_entry.get().split(' ', 1)[0]
        word = word.upper()

        try:
            words.append(word)
            add_word(word)
        except NameError:
            pass
        word_entry.delete(0, 'end')


words = []
root = ctk.CTk()
root.geometry('800x500')
root.title("Word Search")
root.bind('<Key>', key_pressed)

title_label = ctk.CTkLabel(root, text="Word Search Generator", font=ctk.CTkFont(size=30, weight='bold'))
title_label.pack(padx=10, pady=(40, 20))

scrollable_frame = ctk.CTkScrollableFrame(root, width=500, height=300)
scrollable_frame.pack()

word_entry = ctk.CTkEntry(scrollable_frame, placeholder_text='Enter Words Here')
word_entry.pack(fill='x')

feedback = ctk.StringVar()
feedback.set("Number of Words: 0")
feedback_label = ctk.CTkLabel(root, textvariable=feedback, font=ctk.CTkFont(size=15))
feedback_label.pack()

root.mainloop()
