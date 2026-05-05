import sys


def show_intro():
    print("Welcome to the Forest of Choices!")
    print("You are a traveler searching for a lost treasure.")
    print("Choose carefully, because every decision matters.")
    print()


def get_choice(prompt, choices):
    while True:
        response = input(prompt).strip().lower()
        if response in choices:
            return response
        print(f"Please choose one of: {', '.join(choices)}")


def play_game():
    inventory = []
    location = "clearing"

    while True:
        if location == "clearing":
            print("You stand in a sunny clearing. Paths lead north and east.")
            choice = get_choice("Go north or east? (north/east/quit) ", ["north", "east", "quit"])
            if choice == "north":
                location = "river"
            elif choice == "east":
                location = "cabin"
            else:
                break

        elif location == "river":
            print("A gentle river flows here. The sound of water is calming.")
            if "rope" not in inventory:
                print("You see a coil of rope on the bank.")
            choice = get_choice("What do you do? (take rope/cross/return) ", ["take rope", "cross", "return", "quit"])
            if choice == "take rope":
                if "rope" in inventory:
                    print("You already took the rope.")
                else:
                    inventory.append("rope")
                    print("You pick up the rope.")
            elif choice == "cross":
                if "rope" in inventory:
                    print("You use the rope to secure yourself and cross safely.")
                    location = "cave"
                else:
                    print("The river is too wide to cross without something to help.")
            elif choice == "return":
                location = "clearing"
            else:
                break

        elif location == "cabin":
            print("You arrive at an old cabin. The door is unlocked.")
            choice = get_choice("Enter the cabin or return? (enter/return/quit) ", ["enter", "return", "quit"])
            if choice == "enter":
                print("Inside the cabin you find a lantern and a dusty map.")
                inventory.extend(item for item in ["lantern", "map"] if item not in inventory)
                print("You take the lantern and the map.")
                choice = get_choice("Go back to the clearing? (yes/no) ", ["yes", "no"])
                if choice == "yes":
                    location = "clearing"
                else:
                    print("You rest for a moment, then head back anyway.")
                    location = "clearing"
            elif choice == "return":
                location = "clearing"
            else:
                break

        elif location == "cave":
            print("A dark cave entrance appears on the other side of the river.")
            if "lantern" not in inventory:
                print("It is too dark to continue without a light.")
                choice = get_choice("Return to the river or go back? (return/back/quit) ", ["return", "back", "quit"])
                if choice == "return":
                    location = "river"
                elif choice == "back":
                    location = "river"
                else:
                    break
            else:
                print("Your lantern lights the path. You see a glittering chest deeper inside.")
                choice = get_choice("Open the chest or leave? (open/leave/quit) ", ["open", "leave", "quit"])
                if choice == "open":
                    if "map" in inventory:
                        print("Using the map, you find the correct chamber and open the chest safely.")
                        print("Congratulations! You discovered the lost treasure.")
                        break
                    else:
                        print("Without the map, you trigger a hidden trap and barely escape.")
                        print("You decide to go back and prepare better.")
                        location = "river"
                elif choice == "leave":
                    location = "river"
                else:
                    break

    print("Thank you for playing. Goodbye!")


if __name__ == "__main__":
    show_intro()
    play_game()
