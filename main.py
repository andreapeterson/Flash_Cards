import tkinter as tk
import pandas as pd
import random

# Making dictionary from csv
try:
    df = pd.read_csv("data/words_to_study.csv")
except FileNotFoundError:
    df = pd.read_csv("data/spanish_words.csv")
finally:
    df_dict = df.to_dict(orient="records")

# Constants
BACKGROUND_COLOR = "#B1DDC6"

# FUNCTIONS
current_card = {}

known_words = []


def next_card():
    global current_card, flip_timer
    if len(df_dict) != 0:
        window.after_cancel(flip_timer)
        current_card = random.choice(df_dict)
        canvas1.itemconfig(canvas_text1, text=["Spanish"], fill="black")
        canvas1.itemconfig(canvas_text2, text=current_card["Spanish"], fill="black")
        canvas1.itemconfig(canvas1_image, image=flash_card_front)
        flip_timer = window.after(3000, func=flip_card)
    else:
        window.after_cancel(flip_timer)
        canvas1.itemconfig(canvas_text1, text="Well done!", fill="black")
        canvas1.itemconfig(canvas_text2, text="You have gone through the whole deck. Close the window and run this program again to study the ones you missed.", fill="black", font=("Arial", 10, "bold"))
        canvas1.create_text(400, 200, text="If your words_to_study.csv is empty, delete both files if you wish to study all cards again.", fill="black", font=("Arial", 10, "bold"))


def flip_card():
    canvas1.itemconfig(canvas1_image, image=flash_card_back)
    canvas1.itemconfig(canvas_text1, fill="white", text="English")
    canvas1.itemconfig(canvas_text2, fill="white", text=current_card["English"])


def known_cards():
    next_card()
    known_words.append(current_card)
    if current_card in df_dict:
        df_dict.remove(current_card)
    new_data1 = pd.DataFrame(df_dict)
    new_data1.to_csv("data/words_to_study.csv", index=False)
    new_data2 = pd.DataFrame(known_words)
    new_data2.to_csv("data/words_you_rock_at.csv", index=False)


# Window and background set up
window = tk.Tk()
window.title("My Flashcards")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=flip_card)

canvas1 = tk.Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
flash_card_front = tk.PhotoImage(file="images/card_front.png")
flash_card_back = tk.PhotoImage(file="images/card_back.png")
canvas1_image = canvas1.create_image(400, 263, image=flash_card_front)
canvas1.grid(column=0, row=0, columnspan=2)
canvas_text1 = canvas1.create_text(400, 150, text="", fill="black", font=("Arial", 40, "italic"))
canvas_text2 = canvas1.create_text(400, 263, text="", fill="black", font=("Arial", 60, "bold"))

# Buttons
x_pic = tk.PhotoImage(file="images/wrong.png")
no_button = tk.Button(command=next_card, image=x_pic, highlightthickness=0, borderwidth=0)
no_button.grid(column=0, row=1)

check_pic = tk.PhotoImage(file="images/right.png")
yes_button = tk.Button(command=known_cards, image=check_pic, highlightthickness=0, borderwidth=0)
yes_button.grid(column=1, row=1)

next_card()
window.mainloop()
