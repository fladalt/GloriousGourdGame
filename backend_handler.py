import os
import time
import random
from classes import Color

def timed_print(text, ms = 1000):
    """
    Input text and how long it should sleep after in ms
    """
    print(text)
    time.sleep(ms / 1000)

def slow_text(text, ms = 50):
    for i in range(len(text)-1):
        print(text[:i+1], end='\r')
        time.sleep(ms / 1000)
    print(text)

def estimate_damage(modifier, weapon):
    if modifier["Tag"] == "Mult":
        return weapon["Damage"] * modifier["Value"]
    elif modifier["Tag"] == "Add":
        return weapon["Damage"] + modifier["Value"]
    else:
        return weapon["Damage"]
    
def special_weapon(modifier, weapon):
    if modifier == "Gambling":
        return weapon["Damage"] * 0 if random.randint(0, 1) == 0 else 100
    elif modifier == "Shiny":
        return weapon["Damage"] * random.uniform(1, 2)
    elif modifier == "Rusty":
        return weapon["Damage"] * random.uniform(0.5, 1)
    elif modifier == "Thriving":
        return weapon["Damage"] + random.uniform(0, 5)
    elif modifier == "Moldy":
        return weapon["Damage"] - random.uniform(0, 5)
    elif modifier == "Demonic":
        return weapon["Damage"] + random.randint(-5, 5)
    else:
        return weapon["Damage"]
    
def defeated(pebbles):
    os.system("cls")
    print(r"""
  ____  _____    _  _____ _   _ 
 |  _ \| ____|  / \|_   _| | | |
 | | | |  _|   / _ \ | | | |_| |
 | |_| | |___ / ___ \| | |  _  |
 |____/|_____/_/   \_\_| |_| |_|
                                
""")
    time.sleep(1)
    slow_text("You have been defeated.")
    timed_print(f"+ {Color.PEBBLE}₲{pebbles}{Color.END}", 500)
    print(Color.ITALIC + Color.GRAY + "(Press 'enter' to continue)" + Color.END)
    input()