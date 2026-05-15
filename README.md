# yeah.py

A text-based adventure game set in a forest. You are a traveler. There is treasure. Find it.

---

## Requirements

- Python 3.8+
- No external dependencies. The standard library is sufficient for this level of chaos.

## Running the Game

```bash
python yeah.py
```

You will be asked for your name. You can press Enter to remain "Traveler", which is fine.

---

## How to Play

Type things. The game will try to understand you.

There are spoilers in this. Obviously.

You do not need to type exact commands. The parser accepts natural language variations:

| Intent | Accepted inputs |
|---|---|
| Move | `left`, `go left`, `move left`, `head left` |
| Pick up | `take map`, `grab map`, `get map`, `pick up map` |
| Examine | `look`, `examine`, `inspect`, `observe` |
| Inventory | `inventory`, `inv`, `bag`, `items` |
| Talk to NPC | `talk bear`, `speak sage`, `interact sage` |
| Search | `search`, `explore`, `investigate` |
| Exits | `exits`, `directions`, `where`, `paths` |
| Status | `status`, `stats`, `health`, `hp` |
| Use item | `use map`, `apply key`, `activate scroll` |
| Quit | `quit`, `exit`, `give up` |

Type `help` at any time for context-sensitive hints about what you can do in your current location.

---

## World Map

```
                  [Crossroads]
                 /      |      \
           [Cave]  [River Path]  [Meadow*]
              |         |
          [Castle]   [Cabin]

* The Meadow has a Bear. The Bear is blocking a hidden trail to the Cabin.
  Handle accordingly.
```

The goal is to find the **Treasure Chest**. There are two ways to reach it.

---

## Locations

**Crossroads** — Starting point. A Mysterious Sage is here. Ask them for a riddle.

**Dark Cave** — Contains a Map and a Bag of Rocks. The Bag of Rocks is not treasure, despite appearances.

**Old Castle Ruins** — Contains the Treasure Chest, a Nice Hat, a Rusty Key, a Magic Scroll, and a Mysterious Ring. This is where most items are.

**Sunny Meadow** — A Bear is here. It is mildly annoyed. You can run, fight, or approach it calmly. Two of these options end the game immediately.

**Overgrown Path** — A river. You can follow it to the Cabin or attempt to cross it. Attempting to cross it does not go well.

**Cozy Cabin** — Contains an alternate Treasure Chest. Reachable via the river path or the hidden trail unlocked by the Bear.

---

## Entities

### Bear
Located in the Sunny Meadow. Responds to:
- `run` — You escape. You also lose your map and eventually your will to continue.
- `approach` / `calm` / `talk` — The bear decides you are acceptable and leaves, revealing a hidden trail.
- `fight` / `attack` / `battle` — 50% chance of survival. The bear is not impressed either way.

### Mysterious Sage
Located at the Crossroads. Responds to:
- `riddle` / `ask` / `help` — Poses a riddle. Correct answers grant +15 Magic Power.

Incorrect answers are met with the correct answer and mild disappointment.

---

## Items

| Item | Location | Usable |
|---|---|---|
| Bag of Rocks | Cave | No |
| Map | Cave | Yes |
| Treasure Chest | Castle, Cabin | No (win condition) |
| Nice Hat | Castle | No |
| Rusty Key | Castle | Yes |
| Magic Scroll | Castle | Yes |
| Mysterious Ring | Castle | Yes |

"Usable" here means the game will acknowledge that you used it and read you its description. Manage your expectations.

---

## Player Stats

| Stat | Max | Notes |
|---|---|---|
| Health | 100 | Does not decrease through normal play |
| Stamina | 100 | Decorative |
| Magic Power | 50 | Gained by answering riddles (+15) or searching areas (+5, 30% chance) |

---

## Architecture

The code is structured around four classes:

- **`Item`** — A thing. Has a name, description, and a `usable` flag.
- **`Entity`** — A living thing. Has a name, description, and a default `interact()` method that does nothing useful. NPCs override this via lambda.
- **`Player`** — Subclass of `Entity`. Has inventory, health, stamina, and magic power.
- **`Location`** — A place. Holds items, entities, and exits (connections to other locations).
- **`Game`** — Controls game state, the main loop, and command parsing.

NPC behaviour is attached to entity instances at runtime using lambdas, rather than subclassing. This is unconventional but functional.

The command parser uses keyword sets rather than exact matching, which allows flexible natural-language input. Direction detection runs before command detection and takes priority, with an exception for `take` and `use` commands to prevent false positives.

---

## Limitations

- Magic Power has no gameplay effect beyond existing.
- The Nice Hat is not equippable. Our apologies.
- `river_bank.connect("cross", None)` — crossing the river is hardcoded to fail. I would not try it.
- Searching the same area repeatedly yields random results each time, including the possibility of gaining magic power indefinitely (up to the cap of 50).

---
 
## License

Unspecified. Use it however you like. Piracy is not theft.
