# %%
import time
import sys
import random

# %%
# All rooms, items and doors for game configuration
rooms = {
    'Foyer': {
        'description': 'A dimly lit entrance hall with a grand staircase. The air is thick with dust and the scent of decay. You hear a whisper in the darkness: "Three... Seven... Five..."',
        'items': ['Smelly Key']
    },
    'Library': {
        'description': 'Walls lined with ancient books. A cold draft chills you to the bone, and you feel like the books are watching you.\nA library filled with horrific human experiment tomes. One brightly colored spine stands out.' ,
        'items': ['Silver Key', 'Harry Potter Book']
    },
    'Dining Room': {
        'description': 'An elegant room with an old chandelier that sways slightly, casting eerie shadows on the walls.',
        'items': ['Bloody Hammer', 'Flashlight']
    },
    'Kitchen': {
        'description': 'A dark place filled with strange smells and the faint sound of scurrying rats. The shadows seem to move on their own.',
        'items': ['Wooden Box']
    },
    'Hidden Lab': {
        'description': 'A clandestine laboratory filled with disturbing equipment. The air smells of chemicals and decay.',
        'items': []
    },
    'Exit': {
        'description': "What could this be?",
        'items': []
    },
    'Gallery': {
        'description': 'A long, narrow room filled with eerie paintings. The eyes of the portraits seem to follow you as you move.',
        'items': []
    },
}


keys = {
    "Smelly Key": {         
        "name": "Smelly Key",
        "description": "A rusted key reeking of formaldehyde and rot. The stench is almost unbearable, quite disgusting.The engraving reads: LABORATORY ACCESS." 
    },
    "Silver Key": {
        "name": "Silver Key",
        "description": "A tarnished silver key, icy to the touch. Etched into it are the words: LIBRARY ARCHIVES."
    },
    "Main Door Key": {
        "name": "Main Door Key",
        "description": "A massive iron key, heavy and cold. Its teeth are shaped like screaming faces."
    }
}

items = {
    "Bloody Hammer": {
        "name": "Bloody Hammer",
        "description": "It's a bloody hammer!"
    },
    "Wooden Box": {
        "name": "Wooden Box",
        "description": "Some sort of wooden box."
    },
    "Harry Potter Book": {
        "name": "Harry Potter and the Philosopher's Stone",
        "description": "'Harry Potter and the Philosopher's Stone' seems wildly out of place among the grim scientific tomes. The cover feels unnaturally warm."
    },
    "Flashlight": {
        "name": "Flashlight",
        "description": "Makes light"
    }
}
doors = {
     "Squeaky Door": {
    "name":"Squeaky Door",
    "description": "Makes a lot of noise",
    "connections": ["Library", "Dining Room"],
    "locked": True,
    "key": "Silver Key"                          
    },
    "Wooden Door": {
    "name":"Wooden Door",
    "description": "A cracked wooden door. A foul, rotting stench seeps through the gaps.",
    "connections": ["Kitchen", "Dining Room"],
    "locked": True,
    "key": "Smelly Key"                           
    },
    "Bloody Door": {
        "name":"Bloody Door",
        "description": "A fancy door stained with dried blood, Pollock style!",
        "connections": ["Foyer", "Dining Room"],
        "locked": False,
        "key": None  
    },
    "Main Iron Door": {
        "name":"Main Iron Door",
        "description": "Big double iron door",
        "connections": ["Exit", "Foyer"],
        "locked": True,
        "key": "Main Door Key"
    },
    "Cracked Stone Archway": {
    "name": "Cracked Stone Archway",
    "description": "A hidden passage revealed behind the bookshelf, dripping with condensation.",
    "connections": ["Library", "Hidden Lab"],
    "locked": True,  # Initially locked
    "key": None
    },
    "Mystery Door": {
        "name": "Mystery Door",
        "description": "It is covered in ancient glyphs",
        "connections": ["Gallery", "Foyer"],
        "locked": True,
        "key": None # done with puzzle
    }
}

# %%
#helper functions
def print_slow(text, delay=0.01):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def timing(start_time, timer_duration):
    current_time = time.time()
    elapsed_time = current_time - start_time
    time_left = timer_duration - elapsed_time
    minutes = int(time_left // 60)
    remaining_seconds = int(time_left % 60)
    return minutes, remaining_seconds

def gameover():
    print_slow("The spirits of the haunted mansion have trapped you forever!")
    print("""
 _____                           _____                   
|  __ \                         |  _  |                  
| |  \/  __ _  _ __ ___    ___  | | | |__   __ ___  _ __ 
| | __  / _` || '_ ` _ \  / _ \ | | | |\ \ / // _ \| '__|
| |_\ \| (_| || | | | | ||  __/ \ \_/ / \ V /|  __/| |   
 \____/ \__,_||_| |_| |_| \___|  \___/   \_/  \___||_|                                                      
""")

# Add this function at the end
def display_outro(player, start_time, timer_duration):
    minutes, seconds = timing(start_time, timer_duration)
    
    print_slow(f"""
    \033[1mYou burst through the Main Iron Door into the moonlight!\033[0m
    
    The cold night air feels like freedom itself. As the door slams shut behind you, 
    the eerie wails of the mansion fade into the distance. You've escaped the Eclipsed Manor, 
    but its secrets will haunt your dreams forever... 
    
    \033[3m(Thank you for playing!)\033[0m
    
    \033[1mYou had {minutes} minutes and {seconds} seconds left to escape.\033[0m
    \033[1mYou made {player.moves} moves.\033[0m
    """)
    
def get_help():
    print("Everything written \033[3mitalic\033[0m is a command. You can for example use:")
    print(" - \033[3mQuit\033[0m: Exit the game.")
    print(" - \033[3mScout\033[0m: Look around the room.")
    print(" - \033[3mInventory\033[0m: Check your inventory.")
    print(" - \033[3mTime\033[0m: Check the remaining time.")

input_options = [ # for random choices for player input
"You hear a faint whisper. What will you do next?",
"A cold breeze sends shivers down your spine. Your next move?",
"The shadows seem to move. Decide your next action.",
"You feel like you're being watched. What will you do next?",
"A distant scream echoes through the halls. What's your next move?",
"The air grows colder. What will you do now?",
"You sense an eerie presence. Your next action?",
"A ghostly figure appears and vanishes. What do you do next?"
]

# Define the display_intro function
def display_intro():
         # Typographic ASCII Logo for "Escape from Eclipsed Manor"
    logo = r"""
▓█████  ▄████▄   ██▓     ██▓ ██▓███    ██████ ▓█████ ▓█████▄     ███▄ ▄███▓ ▄▄▄       ███▄    █  ▒█████   ██▀███  
▓█   ▀ ▒██▀ ▀█  ▓██▒    ▓██▒▓██░  ██▒▒██    ▒ ▓█   ▀ ▒██▀ ██▌   ▓██▒▀█▀ ██▒▒████▄     ██ ▀█   █ ▒██▒  ██▒▓██ ▒ ██▒
▒███   ▒▓█    ▄ ▒██░    ▒██▒▓██░ ██▓▒░ ▓██▄   ▒███   ░██   █▌   ▓██    ▓██░▒██  ▀█▄  ▓██  ▀█ ██▒▒██░  ██▒▓██ ░▄█ ▒
▒▓█  ▄ ▒▓▓▄ ▄██▒▒██░    ░██░▒██▄█▓▒ ▒  ▒   ██▒▒▓█  ▄ ░▓█▄   ▌   ▒██    ▒██ ░██▄▄▄▄██ ▓██▒  ▐▌██▒▒██   ██░▒██▀▀█▄  
░▒████▒▒ ▓███▀ ░░██████▒░██░▒██▒ ░  ░▒██████▒▒░▒████▒░▒████▓    ▒██▒   ░██▒ ▓█   ▓██▒▒██░   ▓██░░ ████▓▒░░██▓ ▒██▒
░░ ▒░ ░░ ░▒ ▒  ░░ ▒░▓  ░░▓  ▒▓▒░ ░  ░▒ ▒▓▒ ▒ ░░░ ▒░ ░ ▒▒▓  ▒    ░ ▒░   ░  ░ ▒▒   ▓▒█░░ ▒░   ▒ ▒ ░ ▒░▒░▒░ ░ ▒▓ ░▒▓░
 ░ ░  ░  ░  ▒   ░ ░ ▒  ░ ▒ ░░▒ ░     ░ ░▒  ░ ░ ░ ░  ░ ░ ▒  ▒    ░  ░      ░  ▒   ▒▒ ░░ ░░   ░ ▒░  ░ ▒ ▒░   ░▒ ░ ▒░
   ░   ░          ░ ░    ▒ ░░░       ░  ░  ░     ░    ░ ░  ░    ░      ░     ░   ▒      ░   ░ ░ ░ ░ ░ ▒    ░░   ░ 
   ░  ░░ ░          ░  ░ ░                 ░     ░  ░   ░              ░         ░  ░         ░     ░ ░     ░     
       ░                                              ░                                                           
    """
    # Intro Text
    intro_text = """
    You wake up with a pounding headache, your vision blurry. As your eyes adjust,
    you realize you're in a vast, dimly lit library. Towering shelves of ancient
    books surround you, their spines cracked and titles unreadable. The air is
    thick with dust and the faint smell of decay.

    A chill runs down your spine. You feel it—someone, or something, is watching
    you. The silence is broken only by the faint rustling of pages, though no
    breeze stirs the air.
    """
    # ASCII Art of a Bookshelf
    bookshelf = r"""
          ░▒▓████▓▒░      
       .-'~~≈≈≈≈~~`-.    
      /  _®_   _☠_   \   
  _/'¨¨¨¨¨¨¨¨¤¨¨¨¨¨¨¨¨`\_
 ( [«Flesh Synthesis 101»] )
 | [«Vivisection Journals»]|
 | [§§ Cranium Grafts §§ ]|
 | [«Blood Electrification»|
 | [≈≈ Neural Alchemy ≈≈ ]|
 | [☣ Soul Transference ☣]|
 | [«Cranial Recompositions» 
 | [†† Limb Hydraulics ††]|
 | [«Psyche Distillations»|
  \_[«Black Serum Formulas»
    \_¤_/          \_¤_/   
     |§|  cobwebbed |§|    
    /⌐¬\            /⌐¬\   
   {____}          {____}  
      ⌠▒░░▒⌡⌠▒░░▒⌡         
     ⌠▒☠░░░▒▒░░░☠▒⌡       
    """

    intro_text2 = """
    As you glance around, you notice some old scientific books on a nearby shelf.
    The titles are faded, but you can make out words like "Human Experiments"
    and "Dimensional Rifts." Suddenly, it hits you... you've heard stories about
    this place. Decades ago, a brilliant but deranged scientist, Dr. Alistair Voss,
    conducted horrifying experiments on the townspeople here. He vanished without
    a trace, and the manor was abandoned... or so they said.

    You know where you are now. This is the ECLIPSED MANOR.
    """

    # Display the ASCII art and intro text
    print_slow(logo)
    print_slow(intro_text)
    print(bookshelf)
    print_slow(intro_text2)


# %%
# unique interaction functions
def handle_mystery_door(item, player):
                    print_slow('You try to open the door but it seems locked. It seems like we need a three-digit code to open the door.')
                    # Expected code (from the whisper when entering the room)
                    correct_code = ["3", "7", "5"]
                    user_code = []

                    # Loop to gather the digits one by one
                    for i in range(3):
                        # Prompt for each digit
                        digit = input(f"Enter digit {i + 1} of the code: ").strip()
                        
                        # Check if the digit is correct
                        if digit == correct_code[i]:
                            print_slow(f"Digit {i + 1} is correct!")
                            user_code.append(digit)
                        else:
                            print_slow(f"Incorrect digit! The code is still locked.")
                            user_code = []  # Reset the code attempt if wrong
                            break  # Stop the loop and prompt again

                    # If all digits are correct
                    if len(user_code) == 3:
                        print_slow("You solved the puzzle! The Mystery Door unlocks.")
                        item.locked = False  # Unlock the door
                        player.move(item)  # Allow player to move through the door
                        return True
                    else:
                        print_slow("The Mystery Door remains locked.")
                        return False

# %%
# classes initialisation

class Room:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.connections = []
        self.items = []
        self.first_visit = True
    
    def describe_room(self, player):
        if self.items:
            for item in self.items:
                print_slow(f"- \033[3m{str(item)}\033[0m")
        return

    def __str__(self):
        return f"Room Object: {self.name}"
    
    def __repr__(self):
        return f"Room(name={self.name!r})"

class Item:
    def __init__(self, name, description):
        self.name = name
        self.description = description

    def inspect(self):
        # need to make unique cases for special items
        print_slow(self.description)
        return self

    def pickup(self, player):
        pickup = input(f"Do you want to pick up the {self.name}? (Y) ").upper()
        if pickup == "Y":
            if len(player.inventory) >= 2:
                print_slow("You are still very exhausted and can't carry that many things. You need to drop an item before picking up another. (1) or (2)")
                print_slow("Your current inventory:")
                for i, inv_item in enumerate(player.inventory, 1):
                    print_slow(f"{i}. {inv_item.name}")
                drop_choice = int(input("Enter the number of the item you want to drop: ")) - 1
                if 0 <= drop_choice < len(player.inventory):
                    dropped_item = player.inventory.pop(drop_choice)
                    player.current_room.items.append(dropped_item)
                    print_slow(f"You dropped {dropped_item.name} in the room.")
                else:
                    print_slow("Invalid choice. You didn't drop any item.")
            player.inventory.append(self)
            player.current_room.items.remove(self)
            print_slow(f"{self.name} added to inventory!")
        else:
            print_slow(f"{self.name} left in room")

    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return f"Item(name={self.name!r})"

class Door(Item):
    def __init__(self, name, description, room1, room2, locked, key):
        super().__init__(name, description)
        self.room1 = room1
        self.room2 = room2
        self.locked = locked
        self.key = key                          

    def __repr__(self):
        return f"Door(name={self.name!r})"
    
class Key(Item):
    def __init__(self, name, description):
        super().__init__(name, description)

class Player:
    def __init__(self):
        self.current_room = None
        self.inventory = []
        self.escaped = False
        self.name = None
        self.moves = 0

    def move(self, door):
        # check the connections of the door and adjust the location to the room wich is not the current one
        if self.current_room == door.room1:
            self.current_room = door.room2
        else:
            self.current_room = door.room1
        print_slow(f"You go through the {door.name}. {self.current_room.description} This must be the {self.current_room.name}.")

    def show_inventory(self):
        print_slow("The following items are in your inventory:")
        for item in self.inventory:
            print_slow(str(item))
class NPC:
    def __init__(self, name, description, dialogue):
        self.name = name
        self.description = description
        self.dialogue = dialogue
        
    def dialogue_tree(self, player):
        print_slow(f"{self.name} appears before you.")
        print_slow(f"{self.description}")

        for dialogue in self.dialogue:
            print_slow(f"{self.name} says: {dialogue}")

        response = input("How do you respond? (1) 'Good to see you.' (2) 'Can I help you with something?' (3) 'I don’t have time for this.': ").strip()

        if response == "1":
            print_slow(f"{self.name} nods approvingly, a faint smile forming.")
            print_slow(f"'{self.name} leans in slightly and murmurs: 'The ingredient to your escape lies within the wooden box.'")
            return True  # The player gains useful information, game continues.

        elif response == "2":
            print_slow(f"{self.name} tilts their head, studying you for a moment.")
            print_slow(f"'{self.name} remarks: 'Tread carefully. Not everything here is as it seems.'")
            return True  # No negative consequence, game continues.

        elif response == "3":
            print_slow(f"{self.name} narrows their eyes, their expression darkening.")
            print_slow(f"'{self.name} steps closer and mutters: 'Your impatience will cost you.'")
            return self.fight()  # The outcome of the fight determines True or False.

        else:
            print_slow(f"{self.name} gives you a puzzled look before fading into the shadows.")
            return True  # No major consequence, game continues.

    def fight(self):
        print_slow(f"You are now in a fight with {self.name}!")

        while True:
            action = input("Do you want to (1) Attack with your fists, (2) Kick him, or (3) Run: ").strip()
            if action == "1":
                print_slow(f"You attack {self.name} with your fists and manage to escape!")
                return True
            elif action == "2":
                print_slow(f"You kick {self.name}, but {self.name} overpowers you.")
                return False  # The player loses.
            elif action == "3":
                print_slow(f"You run away from {self.name} and hide in another room.")
                return True
            else:
                print_slow("Invalid action. Please choose (1) Attack with your fists, (2) Kick him, or (3) Run.")


    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return f"NPC(name={self.name!r})"


# %%
rooms_objects = {}
items_objects = {}

# dictionary of rooms to store Room instances of each room
for room in rooms:
    rooms_objects[room] = Room(room, rooms[room]["description"])

# dictionary of items to store Items instances of each item
for item in items:
    items_objects[item] = Item(item, items[item]["description"])

# dictionary of keys to store Key instances of each key

for key_name in keys:
    key_data = keys[key_name]
    items_objects[key_name] = Key(
        name=key_name,
        description=key_data["description"],
    )

# add items to rooms
for room in rooms:
    for item in rooms[room]["items"]:
        rooms_objects[room].items.append(items_objects[item])

# dictionary of doors to store Door instance of each door
for door_name in doors:
    door_data = doors[door_name]
    items_objects[door_name] = Door(
        name=door_name,
        description=door_data["description"],
        room1=rooms_objects[door_data["connections"][0]],
        room2=rooms_objects[door_data["connections"][1]],
        locked=door_data["locked"],
        key=door_data.get("key", None)          # ensures that if a door doesn't have a "key" property, it defaults to None
    )
    
# add room connections to rooms based on doors connections (later used to verify play move input)
for door in filter(lambda x: isinstance(items_objects[x], Door), items_objects):
    if door == "Cracked Stone Archway": 
        continue  # Skip adding secret door to rooms initially
    room1 = items_objects[door].room1
    room2 = items_objects[door].room2
    room1.connections.append(room2)
    room2.connections.append(room1)

    # add doors as items to rooms
    room1.items.append(items_objects[door])
    room2.items.append(items_objects[door])

# Define an NPC
npc = NPC(
    name="Ghostly Butler",
    description="A translucent figure in a tattered butler's uniform. His eyes are hollow, and he seems to float above the ground.",
    dialogue=[
        "Welcome to the mansion, master.",
        "Can I assist you with anything, master?",
    ]
)

rooms_objects["Gallery"].items.append(npc)
# create player and set starting room
player = Player()
player.current_room = rooms_objects["Library"]

# %%
timer_duration = 60 * 10 # 10 minutes
start_time = time.time()

# %%
# Loading the game
display_intro()
# print_slow("You wake up in a dark, cold room. You have no memory of how you got here.")
# print_slow("You notice shelves filled with old, dusty books lining the walls but don't know how you got here.")
# print_slow("The air is thick with dust, and the only light comes from a flickering bulb hanging from the ceiling.")
print_slow(f"Something seems off for sure... It is best to be out of here in {timer_duration // 60} minutes.")
print_slow("In case you are unsure what to do, type 'help'.")

# Start the game
while not player.escaped:
    # timer for the game
    if time.time() > start_time + timer_duration:
        print_slow("Time is over!")
        gameover()
        break
    player.moves += 1 # move counter
    answer = input("\n" + random.choice(input_options) + "\n").title()
    if answer == "Quit":
        break
    # Usage
    if answer == "Help":
        get_help()
    elif answer == "Scout":
            scout_time = random.randint(10, 30)
            print_slow(f"It took you {scout_time} seconds to scout what seems to be the {player.current_room.name} but you found the following item(s):")
            timer_duration -= scout_time
            player.current_room.describe_room(player)
            if player.current_room.name == "Library" and player.current_room.first_visit:
                print_slow("\nAmong the dark leather-bound volumes, you spot a shockingly colorful book:")
                print_slow("  \033[33m'Harry Potter and the Philosopher's Stone'\033[0m")
                player.current_room.first_visit = False

            elif player.current_room.name == "Hidden Lab" and player.current_room.first_visit:
                player.current_room.first_visit = False
                print_slow("A torch flickers as you enter...")
                time.sleep(1)
                print_slow("The walls are lined with jars containing unidentifiable biological specimens!")
                time.sleep(2)
                print_slow("A long surgical table dominates the room, stained with dark residues.\033[0m")
                time.sleep(1)
                print_slow("You think to yourself: best get out of here fast!")
                print_slow("You turn around and go back to the library. The Archway shuts behind you.")
                player.current_room = rooms_objects["Library"]
                player.current_room.items.remove(items_objects["Cracked Stone Archway"])

    # Item interaction
    elif answer in items_objects:
        item = items_objects[answer]

        # Check if the item is in the current room
        if item not in player.current_room.items:
            if item in player.inventory:
                print_slow(f"{item} is already in your inventory")
            else:
                print_slow(f"There is no {item.name} in this room.")
            continue            # Skip to the next iteration

        # Handle Wooden Box interaction
        if item.name == "Wooden Box":
            if any(inv_item.name == "Bloody Hammer" for inv_item in player.inventory):
                print_slow("You smash the wooden box open with the hammer!")
                print_slow("Inside, you find the Main Door Key!")

                 # Add Iron Key to the room
                iron_key = items_objects["Main Door Key"]
                player.current_room.items.append(iron_key)

                # Remove the wooden box
                player.current_room.items.remove(item)
            
                # Prompt the player to pick up the key
                iron_key.pickup(player)
            else:
                print_slow("The \033[3mwooden box\033[0m is too sturdy to open without a tool.")
            continue

        # Handle doors
        if isinstance(item, Door):
            # Handle locked doors
            if item.locked:
                if item.name == "Mystery Door":
                    solved = handle_mystery_door(item, player)
                    if solved:
                        won = npc.dialogue_tree(player)
                        if not won:
                            gameover()
                            break
                        else:
                            print_slow("Something superstitious is happening. Things become unclear, you suddenly find yourself back in the Foyer and the Mysterious Door disappears.")
                            player.current_room = rooms_objects["Foyer"]
                            player.current_room.items.remove(item)
                else:
                    # check if player has the key
                    has_key = any(isinstance(inv_item, Key) and inv_item.name == item.key for inv_item in player.inventory)
                    if has_key:
                        item.locked = False
                        print_slow(f"You unlocked the {item.name} with the {item.key}!")
                        player.move(item)
                    else:
                        print_slow(f"The {item.name} is locked! You need the {item.key}.")

            else:
                player.move(item)
                

        # Handle keys and other items
        elif isinstance(item, Key) or item.name == "Bloody Hammer" or item.name == "Flashlight" or item.name == "Harry Potter Book": #or isinstance(item, Furniture):
            # Special case for Harry Potter book
            if item.name == "Harry Potter Book" and items_objects["Cracked Stone Archway"].locked:
                print_slow("\nAs you pull the book from the shelf, you hear grinding stone...")
                time.sleep(1)
                print_slow("A section of the bookshelf swings open, revealing a hidden passage!")
                rooms_objects["Library"].items.append(items_objects["Cracked Stone Archway"])
                print_slow("A \033[1mCracked Stone Archway\033[0m has appeared in the library!")

                # Add and unlock secret door
                items_objects["Cracked Stone Archway"].locked = False
                item.description = "It seems to have lost the magic since the last touch. Seems like an ordinary book."
                print_slow("The book snaps shut and returns to the shelf.")

                # # Remove the book from the room to prevent duplication
                # if self in player.current_room.items:
                #     player.current_room.items.remove(self) 
                #     print_slow("\nAs you pull the book, you hear a grinding sound...")
                #     time.sleep(2)
                #     print_slow("A section of the bookshelf swings open, revealing a hidden passage!")
            else:
                item.inspect()
                item.pickup(player)
    
    elif answer == "Inventory":
        player.show_inventory()

    elif answer == "Time":
        minutes, seconds = timing(start_time, timer_duration)
        print_slow(f"You have {minutes} minutes and {seconds} seconds left.")

    else:
        print("Invalid command. Enter \033[3mhelp\033[0m if you are unsure about what to do.")

    if player.current_room == rooms_objects["Exit"]:
        player.escaped = True

if player.escaped:
    display_outro(player, start_time, timer_duration)
else:
    gameover()


