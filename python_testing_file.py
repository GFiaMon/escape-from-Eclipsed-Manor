# %% [markdown]
# # Haunted Mansion Project
# 
# Welcome to the Haunted Mansion Project! This project aims to create an immersive and interactive experience that simulates a haunted mansion. The project covers the following aspects:
# 
# 1. **Storyline Development**: Crafting a compelling and spooky storyline to engage the audience.
# 2. **Character Design**: Creating detailed and eerie characters that enhance the haunted atmosphere.
# 3. **Environment Creation**: Designing a haunted mansion environment with realistic and chilling elements.
# 4. **Sound Design**: Incorporating creepy sound effects and music to heighten the suspense and fear.
# 5. **Interactive Elements**: Adding interactive features that allow users to explore and interact with the haunted mansion.
# 6. **User Experience**: Ensuring a seamless and immersive experience for the users.
# 
# By the end of this project, you will have a fully developed haunted mansion experience that can be enjoyed by users. Let's dive into the world of ghosts and ghouls!

# %%
from game_setup import rooms, items, doors # I tried to keep the file cleaner so i moved the variables to another file called "game_setup.py" and imported them

# %%
# classes initialisation

class Room:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.connections = []
        self.items = []

    def describe_room(self):
        if self.items:
            print(f"The following item(s) are in the room:")
            for item in self.items:
                print("- "+str(item))
        print("To interact with the above, type their name")
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
        print(self.description)
        return self

    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return f"Item(name={self.name!r})"

class Door(Item):
    def __init__(self, name, description, room1, room2, locked):
        super().__init__(name, description)
        self.room1 = room1
        self.room2 = room2
        self.locked = locked

    def __repr__(self):
        return f"Door(name={self.name!r})"
    
class Key(Item):
    def __init__(self, name, description):
        super().__init__(name, description)

class Furniture(Item):
    def __init__(self, name, description):
        super().__init__(name, description)
    
class Player:
    def __init__(self):
        self.current_room = None
        self.inventory = []
        self.escaped = False

    def move(self, door):
        # check the connections of the door and adjust the location to the room wich is not the current one
        if self.current_room == door.room1:
            self.current_room = door.room2
        else:
            self.current_room = door.room1
        print(f"{self.current_room.description}. This must be the {self.current_room.name}.")

    def show_inventory(self):
        print("The following items are in your inventory:")
        for item in self.inventory:
            print(str(item))


# %%
rooms

# %%
rooms_objects = {}
items_objects = {}

# dictionaroy of rooms to store Room instances of each room
for room in rooms:
    rooms_objects[room] = Room(room, rooms[room]["description"])

# dictionaroy of items to store Items instances of each item
for item in items:
    items_objects[item] = Item(item, items[item]["description"])

# add items to rooms
for room in rooms:
    for item in rooms[room]["items"]:
        rooms_objects[room].items.append(items_objects[item])

# dictionaroy of doors to store Door instance of each door
for door in doors:
    items_objects[door] = Door(door, doors[door]["description"], 
                               rooms_objects[doors[door]["connections"][0]], # get the room object of the first room that is connected with the door
                               rooms_objects[doors[door]["connections"][1]], # get the room object of the second room
                               doors[door]["locked"])
    
# add room connections to rooms based on doors connections (later used to verify play move input)
for door in filter(lambda x: isinstance(items_objects[x], Door), items_objects):
    room1 = items_objects[door].room1
    room2 = items_objects[door].room2
    room1.connections.append(room2)
    room2.connections.append(room1)

    # add doors as items to rooms
    room1.items.append(items_objects[door])
    room2.items.append(items_objects[door])

# create player and set starting room
player = Player()
player.current_room = rooms_objects["Library"]    # GFM -> change to start in Library

# %%
# start game
print("Welcome. This is what you have to do. Everything wirtte in '' can be interacted with")

# while not exited:
while not player.escaped:
    answer = input("What should i do?")
    if answer == "quit":
        break
    # look around
    elif answer == "scout":
        player.current_room.describe_room()

    # Item interaction
    elif answer in items_objects.keys():
        if type(items_objects[answer]) is Door:
            # check if it is a valid connection
            if items_objects[answer] not in player.current_room.items:
                print("Invalied Move")
            else:
                # move player to answer room
                player.move(items_objects[answer])
    
    elif answer == "inspect":
        print("What item would you like to inspect?")
        # show what can be inspected
        for item in player.current_room.items:
            print(item)
        inspect_item = input("What item would you like to inspect?")
        item = items_objects[inspect_item].inspect()

        # needs to be adjusted to append proper items and not doors
        if type(item) == Door:
            pickup = input("Do you want to pickup this item? ('Y' | 'N')")
            if pickup == 'Y':
                player.inventory.append(item)
                print("Item added to inventory")
            else:
                print("Item not picked up")
        
    elif answer in items:
        pass
    
    elif answer == "inventory":
        player.show_inventory()

    else:
        print("This command does not exist")


    """MB: General function inspect: """
    """MB: Function pickup and remove item from room"""
    """MB: Inventory function: show inventory"""
    """MB: function key dining room"""
        # if player says door
        # check if door is accessible (is it connected to the current door)
        # check if door is open
            # if player has key
                #  go through door
            # else say door is closed


    # Item interaction

# %%
player.current_room.items


