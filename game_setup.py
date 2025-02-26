# All rooms, items and doors for game configuration


"""MB: Need to adjust layout (rooms, items and doors[keys for doors]) to drawio -> GF"""

rooms = {
    'Foyer': {
        'description': 'A dimly lit entrance hall with a grand staircase.',
        'items': ['Smelly Key']
    },
    'Library': {
        'description': 'Walls lined with ancient books. A cold draft chills you.',
        'items': ['Silver Key']
    },
    'Dining Room': {
        'description': 'An elegant dining room with an old chandelier.',
        'items': ['Bloody Hammer']
    },
    'Kitchen': {
        'description': 'A dark kitchen filled with strange smells.',
        'items': ['Wooden Box', 'Flashlight']                                     # GFM: I would delete de Flashlight or leave it as an item that doesn't do anything?
    },                              # GFM: The wooden box has to also be defined as somthing that contains the "Main Door Key"
    'Exit':{
        "description": "You made it",
        "items": []
    }
}

keys = {
    "Smelly Key": {         #GFM added keys
        "name": "Smelly Key",
        "description": "What could this key be for? The stench is almost unbearable, quite disgusting."
    },
    "Silver Key": {
        "name": "Silver Key",
        "description": "What could this key be for?"
    },
    "Bloody Hammer": {
        "name": "Bloody Hammer",
        "description": "It's a bloody hammer!"
    },
    "Wooden Box": {
        "name": "Wooden Box",
        "description": "Some sort of wooden box."
    },
    "Main Door Key": {
        "name": "Iron Key",
        "description": "It is quite big, it looks really important!"
    }
}

items = {
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
    "locked": False
    },
    "Wooden Door": {
    "name":"Wooden Door",
    "description": "A cracked wooden door. A foul, rotting stench seeps through the gaps.",
    "connections": ["Kitchen", "Dining Room"],
    "locked": False
    },
    "Bloody Door": {
    "name":"Bloody Door",
    "description": "A fancy door stained with dried blood, Pollock style!",
    "connections": ["Foyer", "Dining Room"],
    "locked": False
    },
    "Main Iron Door": {
    "name":"Main Iron Door",
    "description": "Big double iron door",
    "connections": ["Exit", "Foyer"],
    "locked": False
    },
}

