import os
import sys

# messages to be used in the game, stored in a list for better organisation and easier maintenance
messages = [
# intro
"Welcome to the Forest of Choices!",
"You are a traveler searching for a lost treasure.",
"Choose carefully, because every decision matters.",
"(Or don't. We'll see how that works out for you.)",
# play game
"\nYou find yourself at a crossroads deep in the forest.",
"To the left: a dark cave, barely lit, smelling of mystery and mild danger.",
"To the right: a sunny meadow, suspiciously peaceful.",
"Straight ahead: an overgrown path leading somewhere unknown.",
# cave path - setup
"\nYou creep into the dark cave. It smells like regret and wet stone.",
"By the faint glow ahead, you spot a glimmering treasure chest.",
"There's a locked chest right in front of you, and a narrow tunnel going deeper.",
# cave path - go deeper (win)
"\nBold. You crawl deeper and find the mother lode — gold, jewels, a very nice hat.",
"You haul it all out and live comfortably ever after. Nice work.",
"You win!",
# cave path - grab (lose)
"\nYou snatch a heavy bag in a hurry. Impressive speed, truly.",
"Less impressive: it's a bag of rocks someone left as a prank. Classic.",
"You lose. The rocks were not worth it.",
# meadow path - setup
"\nYou stroll into the sunny meadow. Very scenic. Very peaceful.",
"A large bear is blocking the path, looking mildly annoyed at your presence.",
# meadow path - run (lose)
"\nYou bolt. Impressive hustle. You escape the bear but drop your map in a panic.",
"You wander the forest for three days before accepting your fate.",
"You lose. Maybe next time don't drop the map.",
# meadow path - approach (win)
"\nYou walk up slowly, hands out, speaking in a calm voice like a reasonable person.",
"The bear sniffs you, decides you're fine, and wanders off to reveal a hidden trail.",
"The trail leads straight to the treasure. The bear was a test. You passed.",
"You win!",
# river path - setup
"\nThe overgrown path opens onto a wide river. Cool, refreshing, and fast-moving.",
"You could wade across, or follow the bank upstream where you see a curl of smoke.",
# river path - cross (lose)
"\nYou wade in confidently. The current, unbothered by your confidence, sweeps you away.",
"You wash up downstream, treasureless and damp.",
"You lose. Rivers don't negotiate.",
# river path - follow (win)
"\nSmart call. You follow the bank and find a cozy cabin with a note on the door.",
"The note says: 'Treasure is yours. I retired. — The previous adventurer.'",
"Inside: the treasure, plus a warm fireplace. You earned this.",
"You win!",
]



def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

# function to print a range of messages from the list, for better organisation
def pmessages(start, end):
    for message in messages[start:end]:
        print(message)

def show_intro():
    pmessages(0, 4)

def cave_path():
    pmessages(8, 11)
    choice = input("Do you 'grab' what you can reach, or 'go deeper'? ").strip().lower()

    if 'deeper' in choice or 'go' in choice:
        pmessages(11, 14)
    elif 'grab' in choice:
        pmessages(14, 17)
    else:
        print("That's not really an option here. Try 'grab' or 'go deeper'.")
        cave_path()

def meadow_path():
    pmessages(17, 19)
    print()
    choice = input("Do you 'run' or 'approach' the bear carefully? ").strip().lower()

    if 'run' in choice:
        pmessages(19, 22)
    elif 'approach' in choice:
        pmessages(22, 26)
    else:
        print("The bear is waiting. Try 'run' or 'approach'.")
        meadow_path()

def castle_path():
    print()


def river_path():
    pmessages(26, 28)
    print()
    choice = input("Do you 'cross' the river or 'follow' it upstream? ").strip().lower()

    if 'cross' in choice:
        pmessages(28, 31)
    elif 'follow' in choice or 'upstream' in choice:
        pmessages(31, 35)
    else:
        print("You need to pick a direction. Try 'cross' or 'follow'.")
        river_path()

def play_game():
    pmessages(4, 8)
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
