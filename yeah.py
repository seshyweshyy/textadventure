import os
from random import randint
import sys
from typing import List, Dict, Optional

#classes

class Item:
    #represents an item the player can carry or find.
    def __init__(self, name: str, description: str, usable: bool = False):
        self.name = name
        self.description = description
        self.usable = usable

    def __str__(self):
        return f"{self.name}: {self.description}"


class Entity:
    #Rrepresents a living or sentient thing in the world (player, animals, NPCs).
    def __init__(self, name: str, description: str, hostile: bool = False):
        self.name = name
        self.description = description
        self.hostile = hostile
        self.alive = True

    def interact(self, player: "Player", action: str) -> None:
        #Default interaction; override in subclasses or instances.
        print(f"{self.name} doesn't respond to that.")


class Player(Entity):
    #player entity with inventory and simple methods.
    def __init__(self, name: str = "Traveler"):
        super().__init__(name, "A determined treasure seeker.", hostile=False)
        self.inventory: Dict[str, Item] = {}

    def add_item(self, item: Item) -> None:
        self.inventory[item.name.lower()] = item
        print(f"You picked up: {item.name}.")

    def has_item(self, item_name: str) -> bool:
        return item_name.lower() in self.inventory

    def remove_item(self, item_name: str) -> Optional[Item]:
        return self.inventory.pop(item_name.lower(), None)

    def list_inventory(self) -> None:
        if not self.inventory:
            print("Your inventory is empty.")
            return
        print("Inventory:")
        for item in self.inventory.values():
            print(f"- {item.name}: {item.description}")


class Location:
    #represents a location with description, items, entities, and exits.
    def __init__(self, name: str, description: str):
        #initializes a location with name and description; sets up empty dictionaries for items, entities, and exits
        self.name = name
        self.description = description
        self.items: Dict[str, Item] = {}
        self.entities: Dict[str, Entity] = {}
        self.exits: Dict[str, "Location"] = {}

    def add_item(self, item: Item) -> None:
        #adds an item to the location, stored by its lowercase name as a key
        self.items[item.name.lower()] = item

    def remove_item(self, item_name: str) -> Optional[Item]:
        #removes and returns an item from the location by name; returns None if not found
        return self.items.pop(item_name.lower(), None)

    def add_entity(self, entity: Entity) -> None:
        #adds an entity (NPC, creature) to the location, stored by its lowercase name as a key
        self.entities[entity.name.lower()] = entity

    def describe(self) -> None:
        #displays the location's name, description, items present, and entities present
        print(f"\n{self.name}")
        print(self.description)
        if self.items:
            print("You notice:")
            # prints each item with its name and description
            for item in self.items.values():
                print(f"- {item.name}: {item.description}")
        if self.entities:
            # prints each entity with its name and description
            for ent in self.entities.values():
                print(f"- {ent.name}: {ent.description}")

    def get_exit_names(self) -> List[str]:
        #returns a list of all available exit directions from this location
        return list(self.exits.keys())

    def connect(self, direction: str, other: "Location") -> None:
        #connects this location to another location in a given direction; stores it in the exits dictionary
        self.exits[direction.lower()] = other


#world setup

def build_world(player: Player) -> Dict[str, Location]:
    #locations
    crossroads = Location(
        "Crossroads",
        "You stand at a crossroads deep in the forest. Paths lead left, right, and straight ahead."
    )
    cave = Location(
        "Dark Cave",
        "A dark cave, barely lit, smelling of mystery and mild danger."
    )
    meadow = Location(
        "Sunny Meadow",
        "A sunny meadow, suspiciously peaceful."
    )
    river_bank = Location(
        "Overgrown Path",
        "An overgrown path that opens onto a wide, fast-moving river."
    )
    cabin = Location(
        "Cozy Cabin",
        "A small cabin with a warm fireplace. Someone left a note on the door."
    )
    castle = Location(
        "Old Castle Ruins",
        "Mossy stones and broken towers. A place that hints at old secrets."
    )

    #connect locations
    crossroads.connect("left", cave)
    crossroads.connect("right", meadow)
    crossroads.connect("straight", river_bank)
    river_bank.connect("follow", cabin)
    river_bank.connect("cross", None)  
    cave.connect("deeper", castle)  

    #items
    treasure = Item("Treasure Chest", "A glimmering chest filled with riches.", usable=False)
    prank_rocks = Item("Bag of Rocks", "A heavy bag full of ordinary rocks. Not treasure.", usable=False)
    map_item = Item("Map", "A crumpled map showing a route to treasure.", usable=True)
    hat = Item("Nice Hat", "A very nice hat. Stylish and useful for shade.", usable=False)
    rusty_key = Item("Rusty Key", "An old key with a worn handle. It looks like it belongs to something locked.", usable=True)

    #place items
    cave.add_item(prank_rocks)
    cave.add_item(map_item)
    castle.add_item(treasure)
    castle.add_item(hat)
    castle.add_item(rusty_key)
    cabin.add_item(treasure)  #alternate treasure location if player follows river

    #entities
    bear = Entity("Bear", "A large bear blocking the path, looking mildly annoyed.", hostile=False)

    #bear interaction 
    def bear_interact(self_entity: Entity, player_entity: Player, action: str) -> str:
        action = action.lower()
        if "run" in action:
            print("\nYou bolt. Impressive hustle. You escape the bear but drop your map in a panic.")
            if player_entity.has_item("map"):
                player_entity.remove_item("map")
                print("Your map is gone.")
            print("You wander the forest for three days before accepting your fate.")
            print("You lose. Maybe next time don't drop the map.")
            sys.exit(0)
        elif "approach" in action or "calm" in action or "talk" in action:
            print("\nYou walk up slowly, hands out, speaking in a calm voice like a reasonable person.")
            print("The bear sniffs you, decides you're fine, and wanders off to reveal a hidden trail.")
            meadow.connect("hidden trail", cabin)
            print("A hidden trail is revealed to the east.")
            return "trail"
        elif "fight" in action or "battle" in action or "attack" in action:
            number = randint(1, 10)
            print("\nYou fight the bear. Daring.")
            if number <= 5:
                print("Perhaps not the greatest idea, however.")
                print("The bear mauls you. What did you really expect?")
                print("Game over. You lose.")
                sys.exit(0)
            elif number == 8:
                print("It's impressed by your effort and lets you live.")
                print("It wanders off to reveal a hidden trail.")
                meadow.connect("hidden trail", cabin)
                print("A hidden trail is revealed to the east.")
                return "trail"
            else:
                print("Not the wisest choice, yet by some stroke of luck, you win.")
                meadow.connect("hidden trail", cabin)
                print("A hidden trail is revealed to the east.")
                return "trail"
        else:
            print("The bear is waiting. Try 'run', 'fight', or 'approach'.")
            return "wait"

    #custom interact method
    bear.interact = lambda player, action: bear_interact(bear, player, action)

    meadow.add_entity(bear)

    # world dictionary
    world = {
        "crossroads": crossroads,
        "cave": cave,
        "meadow": meadow,
        "river_bank": river_bank,
        "cabin": cabin,
        "castle": castle
    }
    return world


#game flow

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

INTRO_MESSAGES = [
    "Welcome to the Forest of Choices!",
    "You are a traveler searching for a lost treasure.",
    "Choose carefully, because every decision matters.",
    "(Or don't. We'll see how that works out for you.)",
]

def show_intro():
    for message in INTRO_MESSAGES:
        print(message)

def prompt_choice(prompt: str) -> str:
    try:
        return input(prompt).strip().lower()
    except (EOFError, KeyboardInterrupt):
        print("\nGoodbye.")
        sys.exit(0)

class Game:
    """Main game controller that manages game state and player interactions."""
    def __init__(self, player_name: str = "Traveler"):
        self.player = Player(player_name)
        self.world = build_world(self.player)
        self.current_location = self.world["crossroads"]
        self.is_running = True
        self.moves = 0

    def show_help(self) -> None:
        """Display available commands."""
        print("\n--- Available Commands ---")
        print("look          - Examine the current location in detail")
        print("go <direction> - Move in a direction (north, south, east, west, left, right, etc.)")
        print("take <item>   - Pick up an item")
        print("inventory     - Show your inventory")
        print("use <item>    - Use an item")
        print("interact <target> - Interact with an entity")
        print("exits         - Show available exits")
        print("help          - Show this help message")
        print("quit          - Exit the game")

    def parse_command(self, user_input: str) -> None:
        """Parse and execute player commands."""
        if not user_input:
            return

        parts = user_input.split(maxsplit=1)
        command = parts[0].lower()
        arg = parts[1].lower() if len(parts) > 1 else ""

        if command == "look":
            self.current_location.describe()
        elif command == "go":
            self.move(arg)
        elif command == "take":
            self.take_item(arg)
        elif command == "inventory":
            self.player.list_inventory()
        elif command == "use":
            self.use_item(arg)
        elif command == "interact":
            self.interact(arg)
        elif command == "exits":
            self.show_exits()
        elif command == "help":
            self.show_help()
        elif command == "quit":
            print("You gave up. Goodbye.")
            self.is_running = False
        else:
            print(f"Unknown command: '{command}'. Type 'help' for available commands.")

    def move(self, direction: str) -> None:
        """Move player in a direction."""
        if not direction:
            print("Move in which direction? (try: go left, go right, go straight, etc.)")
            return

        # Check available exits
        available = self.current_location.exits
        if direction in available:
            next_location = available[direction]
            if next_location is None:
                print("You can't go that way.")
                return
            self.current_location = next_location
            self.moves += 1
            self.current_location.describe()
        else:
            print(f"You can't go {direction} from here.")
            print(f"Available exits: {', '.join(available.keys())}")

    def take_item(self, item_name: str) -> None:
        """Player takes an item from the location."""
        if not item_name:
            print("Take what? (try: take treasure, take map, etc.)")
            return

        item = self.current_location.remove_item(item_name)
        if item:
            self.player.add_item(item)
        else:
            print(f"There's no '{item_name}' here.")

    def use_item(self, item_name: str) -> None:
        """Player uses an item."""
        if not item_name:
            print("Use what? (try: use map, use key, etc.)")
            return

        if self.player.has_item(item_name):
            item = self.player.inventory[item_name]
            if item.usable:
                print(f"You used the {item.name}. {item.description}")
            else:
                print(f"The {item.name} isn't useful right now.")
        else:
            print(f"You don't have a '{item_name}'.")

    def interact(self, target_name: str) -> None:
        """Player interacts with an entity."""
        if not target_name:
            print("Interact with what? (try: interact bear, interact npc, etc.)")
            return

        target = self.current_location.entities.get(target_name)
        if target:
            action = prompt_choice(f"How do you interact with the {target.name}? ")
            target.interact(self.player, action)
        else:
            print(f"There's no '{target_name}' here to interact with.")

    def show_exits(self) -> None:
        """Display available exits."""
        exits = self.current_location.get_exit_names()
        if exits:
            print(f"Exits: {', '.join(exits)}")
        else:
            print("There are no exits from here.")

    def check_win_condition(self) -> bool:
        """Check if player has won."""
        if self.player.has_item("treasure chest"):
            print("\n=== YOU WIN! ===")
            print(f"You found the treasure in {self.moves} moves!")
            return True
        return False

    def run(self) -> None:
        """Main game loop."""
        clear_terminal()
        show_intro()
        print(f"\nWelcome, {self.player.name}!\n")

        self.current_location.describe()
        self.show_exits()

        while self.is_running:
            try:
                if self.check_win_condition():
                    self.is_running = False
                    break

                user_input = prompt_choice("\n> ")
                self.parse_command(user_input)
            except KeyboardInterrupt:
                print("\n\nGame interrupted.")
                self.is_running = False


def main():
    """Entry point for the game."""
    print("Welcome to the Text Adventure!")
    player_name = input("What is your name, traveler? ").strip() or "Traveler"
    game = Game(player_name)
    game.run()


if __name__ == "__main__":
    main()