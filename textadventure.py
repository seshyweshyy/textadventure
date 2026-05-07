import os
import sys

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def show_intro():
    print("Welcome to the Forest of Choices!")
    print("You are a traveler searching for a lost treasure.")
    print("Choose carefully, because every decision matters.")
    print("(Or don't. We'll see how that works out for you.)")
    print()

def cave_path():
    print()
    print("You creep into the dark cave. It smells like regret and wet stone.")
    print("By the faint glow ahead, you spot a glimmering treasure chest.")
    print("There's a locked chest right in front of you, and a narrow tunnel going deeper.")
    print()
    choice = input("Do you 'grab' what you can reach, or 'go deeper'? ").strip().lower()

    if 'deeper' in choice or 'go' in choice:
        print()
        print("Bold. You crawl deeper and find the mother lode — gold, jewels, a very nice hat.")
        print("You haul it all out and live comfortably ever after. Nice work.")
        print("You win!")
    elif 'grab' in choice:
        print()
        print("You snatch a heavy bag in a hurry. Impressive speed, truly.")
        print("Less impressive: it's a bag of rocks someone left as a prank. Classic.")
        print("You lose. The rocks were not worth it.")
    else:
        print("That's not really an option here. Try 'grab' or 'go deeper'.")
        cave_path()

def meadow_path():
    print()
    print("You stroll into the sunny meadow. Very scenic. Very peaceful.")
    print("A large bear is blocking the path, looking mildly annoyed at your presence.")
    print()
    choice = input("Do you 'run' or 'approach' the bear carefully? ").strip().lower()

    if 'run' in choice:
        print()
        print("You bolt. Impressive hustle. You escape the bear but drop your map in a panic.")
        print("You wander the forest for three days before accepting your fate.")
        print("You lose. Maybe next time don't drop the map.")
    elif 'approach' in choice:
        print()
        print("You walk up slowly, hands out, speaking in a calm voice like a reasonable person.")
        print("The bear sniffs you, decides you're fine, and wanders off to reveal a hidden trail.")
        print("The trail leads straight to the treasure. The bear was a test. You passed.")
        print("You win!")
    else:
        print("The bear is waiting. Try 'run' or 'approach'.")
        meadow_path()

def river_path():
    print()
    print("The overgrown path opens onto a wide river. Cool, refreshing, and fast-moving.")
    print("You could wade across, or follow the bank upstream where you see a curl of smoke.")
    print()
    choice = input("Do you 'cross' the river or 'follow' it upstream? ").strip().lower()

    if 'cross' in choice:
        print()
        print("You wade in confidently. The current, unbothered by your confidence, sweeps you away.")
        print("You wash up downstream, treasureless and damp.")
        print("You lose. Rivers don't negotiate.")
    elif 'follow' in choice or 'upstream' in choice:
        print()
        print("Smart call. You follow the bank and find a cozy cabin with a note on the door.")
        print("The note says: 'Treasure is yours. I retired. — The previous adventurer.'")
        print("Inside: the treasure, plus a warm fireplace. You earned this.")
        print("You win!")
    else:
        print("You need to pick a direction. Try 'cross' or 'follow'.")
        river_path()

def play_game():
    print("You find yourself at a crossroads deep in the forest.")
    print("To the left: a dark cave, barely lit, smelling of mystery and mild danger.")
    print("To the right: a sunny meadow, suspiciously peaceful.")
    print("Straight ahead: an overgrown path leading somewhere unknown.")
    print()
    choice = input("Which way do you go? (left / right / straight) ").strip().lower()

    if 'left' in choice:
        cave_path()
    elif 'right' in choice:
        meadow_path()
    elif 'straight' in choice or 'ahead' in choice or 'forward' in choice:
        river_path()
    else:
        print("Left, right, or straight. Three options. You've got this.")
        play_game()

if __name__ == "__main__":
    clear_terminal()
    show_intro()
    play_game()
