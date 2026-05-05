import os
import sys

def clear_terminal():
    # 'nt' is for Windows, 'posix' is for macOS and Linux
    os.system('cls' if os.name == 'nt' else 'clear')

def show_intro():
    print("Welcome to the Forest of Choices!")
    print("You are a traveler searching for a lost treasure.")
    print("Choose carefully, because every decision matters.")
    print()

def play_game():
    print("You find yourself at a crossroads in the forest.")
    print("Do you want to go left towards the dark cave, or right towards the sunny meadow?")
    choice = input("Type 'left' or 'right': ").strip().lower()
    if  'left' in choice:
        print("You venture into the dark cave and find a hidden treasure chest!")
        print("Congratulations, you win!")
    elif 'right' in choice:
        print("You walk into the sunny meadow and encounter a wild animal.")
        print("Unfortunately, you are not prepared and lose the game.")
    else:
        print("Invalid choice. Please type 'left' or 'right'.")
        play_game()

if __name__ == "__main__":
    clear_terminal()
    show_intro()
    play_game()