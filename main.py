#==========================================================================================================
#==========================================================================================================
#
# A Lottory-Game Powered by the DRAND random values generator 
# we are using drand instead of randomfeedooooor's service due to the fact that they disconinued their
# support of the project, and it is no longer live.
#
# created by:
#   Almog Geva
#   Matan Brizman
#
#==========================================================================================================
#==========================================================================================================
#
# Requirements to run: (in cmd, run the following commands)
#       pip install tk
#       pip install requests
#
#==========================================================================================================
#==========================================================================================================


from operator import ne
from turtle import right
import requests
from typing import List
from math import floor,pow
import os

import tkinter as tk
import tkinter.messagebox
from tkinter import E, N, NE, filedialog, Text

NUMBER_OF_TABLES = 10
MAX_BET_VALUE = 30
UNIT_FOR_RELATIVE_LOCATION = 0.95

COLOR_DARK_BACK_GROUND = "#1d3557" #Dark blue 
COLOR_LIGHT_BACK_GROUND = "#a8dadc"
COLOR_LIGHT_WHITE = "#f1faee"
COLOR_RED = "#e63946"
COLOR_BLUE = "#457b9d"

ALL_FRAMES = []
ALL_COMPONENTS_MAP = {}



def get_random_value() -> str:
    url = "https://drand.cloudflare.com"
    request_path = "/public/latest"
    method = "GET"
    headers = {"Accept": "application/json"}
    response = requests.request(method, url + request_path, headers=headers)
    response.raise_for_status()

    result = response.json()
    randomness = result["randomness"]

    return randomness

def split_random(randomness : str) -> List[str]:
    segmentLength = floor(len(randomness) / NUMBER_OF_TABLES)
    if(segmentLength < 2):
        raise Exception("Number of tables is too big.")
    leftSegmentBorder = 0
    rightSegmentBorder = segmentLength
    segments = []
    for i in range(NUMBER_OF_TABLES):
        segments.append(randomness[leftSegmentBorder:rightSegmentBorder]) 
        leftSegmentBorder += segmentLength
        rightSegmentBorder += segmentLength

    return segments

def hex_to_int(value : str) -> int:
    return int(value, 16)

def parse_lottory_numbers(hexSegments : List[str]) -> List[int]:
    numbers = []
    for hex in hexSegments:
        numbers.append((hex_to_int(hex)%MAX_BET_VALUE)+1)

    return numbers

def get_lottory_numbers() -> List[int]:
    randomness = get_random_value()
    segmetns = split_random(randomness)
    lottoryWinningNumbers = parse_lottory_numbers(segmetns)

    return lottoryWinningNumbers

def create_frames(root : tk.Tk) -> List[tk.Frame]:
    allframes = []
    rely = UNIT_FOR_RELATIVE_LOCATION / NUMBER_OF_TABLES  
    relheight = UNIT_FOR_RELATIVE_LOCATION / (NUMBER_OF_TABLES+1)
    for i in range(NUMBER_OF_TABLES):
        frame = tk.Frame(root, bg=COLOR_LIGHT_WHITE)                
        frame.place(relwidth=0.9,relheight=relheight, relx=0.05, rely=(0.01 + rely*i))
        
        allframes.append(frame)

    return allframes

def add_radio_buttons_to_frame(frame : tk.Frame) -> List[tk.Radiobutton]:
    allbuttons = []
    variable = tk.IntVar()
    
    allbuttons.append(variable)
    maxcol = floor(MAX_BET_VALUE / 3)
    
    for i in range(MAX_BET_VALUE):
        button = tk.Radiobutton(frame,text=str(i+1),fg=COLOR_DARK_BACK_GROUND, bg=COLOR_LIGHT_WHITE ,variable=variable , value=i+1 , tristatevalue=0) 
        button.grid(row= floor(i/maxcol)  ,column= i%maxcol, sticky=N)
        
        allbuttons.append(button)

    variable.set(0)    
    label = tk.Label(frame,text="Result:TBD")
    label.grid(row=0,column=maxcol+2)
    allbuttons.append(label)

    return allbuttons

def add_radio_buttons_to_all_frames(frames : List[tk.Frame]):
    buttonToFrameMap = {}
    for frame in frames:
        allNewRadioButtons = add_radio_buttons_to_frame(frame)
        buttonToFrameMap[frame] = allNewRadioButtons

    return buttonToFrameMap

def get_winnint_amount(numberOfWins :int) -> int:
    return int(pow(10,numberOfWins))

def onclick_submit():
    
    lottorySubmittion = []
    for frame in ALL_FRAMES:
        lottorySubmittion.append(ALL_COMPONENTS_MAP[frame][0].get())

    if 0 in lottorySubmittion:
       tkinter.messagebox.showerror(message="Not All Values Were Selected")
    else:                
        lottoryWinningNumbers = get_lottory_numbers()
        for frame,entry in zip(ALL_FRAMES,lottoryWinningNumbers):
            ALL_COMPONENTS_MAP[frame][-1]['text'] = f"Result:{entry}"
        
        winCounter = 0
        for entry,winning in zip(lottorySubmittion,lottoryWinningNumbers):
            if(entry == winning):
                winCounter+=1
        
        tkinter.messagebox.showinfo(message=f"YOU WON {get_winnint_amount(winCounter)}$ !!!")
        
            


if __name__ == "__main__":
    
    root = tk.Tk()
    canvas = tk.Canvas(root, height=800,width=520,bg=COLOR_DARK_BACK_GROUND)
    canvas.pack()

    ALL_FRAMES = create_frames(root)
    ALL_COMPONENTS_MAP = add_radio_buttons_to_all_frames(ALL_FRAMES)

    submitBetButton = tk.Button(root, text="submit", padx=5,pady=5, bg=COLOR_DARK_BACK_GROUND,fg=COLOR_LIGHT_BACK_GROUND, command=onclick_submit)
    submitBetButton.pack()


    
   
    root.mainloop()