import os
from random import randint
import sys
from typing import List, Dict, Optional

#classes

class Item:
    #Represents an item the player can carry or find.
    def __init__(self, name: str, description: str, usable: bool = False):
        self.name = name
        self.description = description
        self.usable = usable

    def __str__(self):
        return f"{self.name}: {self.description}"


class Entity:
    #Represents a living or sentient thing in the world (player, animals, NPCs).
    def __init__(self, name: str, description: str, hostile: bool = False):
        self.name = name
        self.description = description
        self.hostile = hostile
        self.alive = True

    def interact(self, player: "Player", action: str) -> None:
        #Default interaction; override in subclasses or instances.
        print(f"{self.name} doesn't respond to that.")


class Player(Entity):
    #Player entity with inventory and simple methods.
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
    #Represents a location with description, items, entities, and exits.
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.items: Dict[str, Item] = {}
        self.entities: Dict[str, Entity] = {}
        self.exits: Dict[str, "Location"] = {}

    def add_item(self, item: Item) -> None:
        self.items[item.name.lower()] = item

    def remove_item(self, item_name: str) -> Optional[Item]:
        return self.items.pop(item_name.lower(), None)

    def add_entity(self, entity: Entity) -> None:
        self.entities[entity.name.lower()] = entity

    def describe(self) -> None:
        print(f"\n{self.name}")
        print(self.description)
        if self.items:
            print("You notice:")
            for item in self.items.values():
                print(f"- {item.name}: {item.description}")
        if self.entities:
            for ent in self.entities.values():
                print(f"- {ent.name}: {ent.description}")

    def get_exit_names(self) -> List[str]:
        return list(self.exits.keys())

    def connect(self, direction: str, other: "Location") -> None:
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
    river_bank.connect("cross", None)  # crossing is a risky action handled in logic
    cave.connect("deeper", castle)  # deeper cave leads to castle ruins in this version

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

def cave_sequence(player: Player, location: Location, world: Dict[str, Location]) -> None:
    location.describe()
    print("There's a locked chest right in front of you, and a narrow tunnel going deeper.")
    choice = prompt_choice("Do you 'grab' what you can reach, or 'go deeper'? ")

    if 'deeper' in choice or 'go' in choice:
        # Move to castle (deeper)
        deeper = location.exits.get("deeper")
        if deeper:
            num = randint(1, 10)
            if num <= 3:
                castle_sequence(player, deeper, world)
            else:
                print("\nBold. You crawl deeper and find the mother lode — gold, jewels, a very nice hat.")
                # Transfer items from deeper location to player (simulate hauling out)
                if deeper.items:
                    for item_name in list(deeper.items.keys()):
                        item = deeper.remove_item(item_name)
                        if item:
                            player.add_item(item)
                print("You haul it all out and live comfortably ever after. Nice work.")
                print("You win!")
                sys.exit(0)
        else:
            print("The tunnel collapses. You're stuck. You lose.")
            sys.exit(0)
    elif 'grab' in choice:
        # Grab nearest item (bag of rocks or map)
        if location.items:
            # Prefer map if present
            if 'map' in location.items:
                item = location.remove_item('map')
                player.add_item(item)
                print("\nYou snatch the map in a hurry. Good call — this might help later.")
            else:
                # pick a random item (prank rocks)
                item = location.remove_item(next(iter(location.items)))
                player.add_item(item)
                if item.name.lower() == "bag of rocks":
                    print("\nLess impressive: it's a bag of rocks someone left as a prank. Classic.")
                    print("You lose. The rocks were not worth it.")
                    sys.exit(0)
        else:
            print("There's nothing reachable to grab.")
            cave_sequence(player, location, world)
    else:
        print("That's not really an option here. Try 'grab' or 'go deeper'.")
        cave_sequence(player, location, world)


def meadow_sequence(player: Player, location: Location, world: Dict[str, Location]) -> None:
    location.describe()
    choice = prompt_choice("Do you 'run', 'fight', or 'approach' the bear carefully? ")

    bear = location.entities.get("bear")
    if not bear: 
        print("The meadow is empty now.")
        return

    if 'run' in choice:
        bear.interact(player, "run")
    elif 'fight' in choice or 'battle' in choice or 'attack' in choice:
        result = bear.interact(player, "fight")
        if result == "trail":
            hidden_trail_sequence(player, world)
    elif 'approach' in choice or 'calm' in choice:
        result = bear.interact(player, "approach")
        if result == "trail":
            hidden_trail_sequence(player, world)
    elif 'follow' in choice or 'hidden' in choice or 'trail' in choice:
        if "hidden trail" in location.exits:
            hidden_trail_sequence(player, world)
        else:
            print("The bear still blocks the path.")
            meadow_sequence(player, location, world)
    else:
        print("The bear is waiting. Try 'run', 'fight', or 'approach'.")
        meadow_sequence(player, location, world)


def hidden_trail_sequence(player: Player, world: Dict[str, Location]) -> None:
    cabin = world.get("cabin")
    if not cabin:
        print("The hidden trail disappears into the forest and leads nowhere.")
        return

    follow = prompt_choice("Do you follow the hidden trail? (yes/no) ")
    if 'yes' in follow or 'y' in follow:
        print("\nYou follow the hidden trail.")
        print("A cozy cabin appears, warm and welcoming.")
        cabin.describe()
        if cabin.items:
            for item_name in list(cabin.items.keys()):
                item = cabin.remove_item(item_name)
                if item:
                    player.add_item(item)
            print("Inside: the treasure, plus a warm fireplace. You earned this.")
            print("You win!")
            sys.exit(0)
        else:
            print("The cabin is empty. You find nothing more here.")
    else:
        print("You decide not to follow the trail right now.")


def river_sequence(player: Player, location: Location, world: Dict[str, Location]) -> None:
    location.describe()
    print("You could wade across, or follow the bank upstream where you see a curl of smoke.")
    choice = prompt_choice("Do you 'cross' the river or 'follow' it upstream? ")

    if 'cross' in choice:
        print("\nYou wade in confidently. The current, unbothered by your confidence, sweeps you away.")
        print("You wash up downstream, treasureless and damp.")
        print("You lose. Rivers don't negotiate.")
        sys.exit(0)
    elif 'follow' in choice or 'upstream' in choice:
        # Move to cabin
        cabin = world.get("cabin")
        if cabin:
            print("\nSmart call. You follow the bank and find a cozy cabin with a note on the door.")
            cabin.describe()
            if cabin.items:
                for item_name in list(cabin.items.keys()):
                    item = cabin.remove_item(item_name)
                    if item:
                        player.add_item(item)
                print("Inside: the treasure, plus a warm fireplace. You earned this.")
                print("You win!")
                sys.exit(0)
        else:
            print("You follow the river but find nothing of interest.")
            river_sequence(player, location, world)
    else:
        print("You need to pick a direction. Try 'cross' or 'follow'.")
        river_sequence(player, location, world)


def castle_sequence(player: Player, location: Location, world: Dict[str, Location]) -> None:
    location.describe()
    print("The castle ruins are quiet. A locked chest sits beneath a collapsed arch.")
    print("You can try to open the chest, but it looks like it might be trapped.")
    choice = prompt_choice("Do you want to try to open the chest or explore deeper into the ruins? ")
    if 'open' in choice or 'chest' in choice:
        if player.has_item("rusty key"):
            print("\nYou turn the key and the chest clicks open.")
            if location.items:
                for item_name in list(location.items.keys()):
                    item = location.remove_item(item_name)
                    if item:
                        player.add_item(item)
                print("You gather the spoils from the ruins and find a very nice hat among the loot.")
                print("You win!")
                sys.exit(0)
            else:
                print("The chest is empty. Someone beat you to it.")
                sys.exit(0)
        else:
            chance = randint(1, 10)
            if chance <= 4:
                print("\nThe chest is locked tight and refuses to budge. There must be a key hidden deeper in the ruins.")
                castle_sequence(player, location, world)
            else:
                print("\nYou manage to pry the chest open despite the lock.")
                if location.items:
                    for item_name in list(location.items.keys()):
                        item = location.remove_item(item_name)
                        if item:
                            player.add_item(item)
                    print("You gather the spoils from the ruins and find a very nice hat among the loot.")
                    print("You win!")
                    sys.exit(0)
                else:
                    print("The chest is empty. Someone beat you to it.")
                    sys.exit(0)
    elif 'explore' in choice or 'deeper' in choice:
        key = location.remove_item("rusty key")
        if key:
            player.add_item(key)
            print("\nYou search the ruined corridors and find a rusty key tucked under a fallen stone.")
            print("This looks like it could open the chest.")
        else:
            print("\nYou explore further, but the ruins offer no new secrets right now.")
        castle_sequence(player, location, world)
    else:
        print("That's not a good choice here. Try 'open' or 'explore deeper'.")
        castle_sequence(player, location, world)


#main game loop

def play_game():
    clear_terminal()
    show_intro()
    player = Player()
    world = build_world(player)
    current = world["crossroads"]

    #show crossroads description
    current.describe()
    while True:
        choice = prompt_choice("\nWhich way do you go? (left / right / straight / inventory / quit) ")

        if 'left' in choice:
            cave_sequence(player, world["cave"], world)
        elif 'right' in choice:
            meadow_sequence(player, world["meadow"], world)
        elif 'straight' in choice or 'ahead' in choice or 'forward' in choice:
            river_sequence(player, world["river_bank"], world)
        elif 'inventory' in choice or 'inv' in choice:
            player.list_inventory()
        elif 'quit' in choice or 'exit' in choice:
            print("You leave the forest for now. Adventure awaits another day.")
            sys.exit(0)
        elif 'back' in choice:
            print("You're already at the crossroads. There's no going back from here.")
        else:
            print("Left, right, or straight. You can also type 'inventory' or 'quit'.")


if __name__ == "__main__":
    play_game()
