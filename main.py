import csv
from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"

# FUNCTIONALITY

# # set variables and methods

to_learn = {}

try:
	data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
	original_data = pandas.read_csv("data/french_words.csv")
	to_learn = original_data.to_dict(orient="records")
else:
	to_learn = data.to_dict(orient="records")

current_card = {}


# #get the card to generate random words when buttons are pressed


def next_card():
	global current_card, swap_timer
	window.after_cancel(swap_timer)
	current_card = random.choice(to_learn)
	canvas.itemconfig(card_title, text="French", fill="black")
	canvas.itemconfig(card_text, text=current_card["French"], fill="black")
	canvas.itemconfig(card_image, image=card_front_image)
	swap_timer = window.after(3000, change_card)


def known_card():
	to_learn.remove(current_card)
	print(len(to_learn))
	data = pandas.DataFrame(to_learn)
	data.to_csv("data/words_to_learn.csv", index=False)
	next_card()



def change_card():
	canvas.itemconfig(card_image, image=card_back_image)
	canvas.itemconfig(card_text, text=current_card["English"], fill="white")
	canvas.itemconfig(card_title, text="English", fill="white")


# SETTING UP THE INTERFACE

# #Window
window = Tk()
window.title("Learn French")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

swap_timer = window.after(5000, change_card)

# #set up the required images
card_front_image = PhotoImage(file="./images/card_front.png")
card_back_image = PhotoImage(file="./images/card_back.png")
check_mark_image = PhotoImage(file="./images/right.png")
x_mark_image = PhotoImage(file="./images/wrong.png")

# #canvas
canvas = Canvas(width=800, height=526, highlightthickness=0, background=BACKGROUND_COLOR)
card_image = canvas.create_image(400, 263, image=card_front_image)
card_title = canvas.create_text(400,150, text="Language", font=("Ariel", 40, "italic"))
card_text = canvas.create_text(400,263, text="Word", font=("Ariel", 60, "bold"))
canvas.grid(row=0, column=0, columnspan=2)

# #buttons
check_button = Button(image=check_mark_image, highlightthickness=0, command=next_card)
check_button.grid(row=1, column=0)
x_button = Button(image=x_mark_image, highlightthickness=0, command=known_card)
x_button.grid(row=1, column=1)

next_card()


window.mainloop()