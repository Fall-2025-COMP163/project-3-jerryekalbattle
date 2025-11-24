"""
COMP 163 - Project 3: Quest Chronicles
Character Manager Module - Starter Code

Name: Jerryeka Battle

AI Usage: [Document any AI assistance used]

This module handles character creation, loading, and saving.
"""

import os
from custom_exceptions import (
    InvalidCharacterClassError,
    CharacterNotFoundError,
    SaveFileCorruptedError,
    InvalidSaveDataError,
    CharacterDeadError
)

# ============================================================================
# CHARACTER MANAGEMENT FUNCTIONS
# ============================================================================

def create_character(name, character_class):
    """
    Create a new character with stats based on class
    
    Valid classes: Warrior, Mage, Rogue, Cleric
    
    Returns: Dictionary with character data including:
            - name, class, level, health, max_health, strength, magic
            - experience, gold, inventory, active_quests, completed_quests
    
    Raises: InvalidCharacterClassError if class is not valid
    """
    # TODO: Implement character creation
    valid_classes = {
        "Warrior": {"health": 120, "strength": 15, "magic": 5},
        "Mage": {"health": 80, "strength": 8, "magic": 20},
        "Rogue": {"health": 90, "strength": 12, "magic": 10},
        "Cleric": {"health": 100, "strength": 10, "magic": 15}
    }

    if character_class not in valid_classes:
        raise InvalidCharacterClassError(
            f"'{character_class}' is not a valid class. "
            f"Valid classes: {', '.join(valid_classes.keys())}"
        )

    stats = valid_classes[character_class]

    return {
        "name": name,
        "class": character_class,
        "level": 1,
        "health": stats["health"],
        "max_health": stats["health"],
        "strength": stats["strength"],
        "magic": stats["magic"],
        "experience": 0,
        "gold": 100,
        "inventory": [],
        "active_quests": [],
        "completed_quests": []
    }

    # Validate character_class first
    # Example base stats:
    # Warrior: health=120, strength=15, magic=5
    # Mage: health=80, strength=8, magic=20
    # Rogue: health=90, strength=12, magic=10
    # Cleric: health=100, strength=10, magic=15
    # All characters start with:
    # - level=1, experience=0, gold=100
    # - inventory=[], active_quests=[], completed_quests=[]

def save_character(character, save_directory="data/save_games"):
    """
    Save character to file
    
    Filename format: {character_name}_save.txt
    
    File format:
    NAME: character_name
    CLASS: class_name
    LEVEL: 1
    HEALTH: 120
    MAX_HEALTH: 120
    STRENGTH: 15
    MAGIC: 5
    EXPERIENCE: 0
    GOLD: 100
    INVENTORY: item1,item2,item3
    ACTIVE_QUESTS: quest1,quest2
    COMPLETED_QUESTS: quest1,quest2
    
    Returns: True if successful
    Raises: PermissionError, IOError (let them propagate or handle)
    """
    os.makedirs(save_directory, exist_ok=True)
    filename = os.path.join(save_directory, f"{character['name']}_save.txt")

    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"NAME: {character['name']}\n")
            f.write(f"CLASS: {character['class']}\n")
            f.write(f"LEVEL: {character['level']}\n")
            f.write(f"HEALTH: {character['health']}\n")
            f.write(f"MAX_HEALTH: {character['max_health']}\n")
            f.write(f"STRENGTH: {character['strength']}\n")
            f.write(f"MAGIC: {character['magic']}\n")
            f.write(f"EXPERIENCE: {character['experience']}\n")
            f.write(f"GOLD: {character['gold']}\n")
            f.write(f"INVENTORY: {','.join(character['inventory'])}\n")
            f.write(f"ACTIVE_QUESTS: {','.join(character['active_quests'])}\n")
            f.write(f"COMPLETED_QUESTS: {','.join(character['completed_quests'])}\n")

        return True
    
    except Exception as e:
        raise SaveFileCorruptedError(str(e))
    
    # TODO: Implement save functionality
    # Create save_directory if it doesn't exist
    # Handle any file I/O errors appropriately
    # Lists should be saved as comma-separated values

def load_character(character_name, save_directory="data/save_games"):
    """
    Load character from save file
    
    Args:
        character_name: Name of character to load
        save_directory: Directory containing save files
    
    Returns: Character dictionary
    Raises: 
        CharacterNotFoundError if save file doesn't exist
        SaveFileCorruptedError if file exists but can't be read
        InvalidSaveDataError if data format is wrong
    """
    # TODO: Implement load functionality
    filename = os.path.join(save_directory, f"{character_name}_save.txt")

    if not os.path.exists(filename):
        raise CharacterNotFoundError(f"No save found for {character_name}.")
    # Check if file exists → CharacterNotFoundError
    try:
        with open(filename, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except Exception as e:
        raise SaveFileCorruptedError(str(e))
    
    # Try to read file → SaveFileCorruptedError
    data = {}

    try:
        for line in lines:
            line = line.strip()
            if not line:
                continue

            # Must contain ": "
            if ":" not in line:
                raise InvalidSaveDataError("Invalid line in save file.")
    
            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip()


            required_keys = [
            "NAME", "CLASS", "LEVEL", "HEALTH", "MAX_HEALTH",
            "STRENGTH", "MAGIC", "EXPERIENCE", "GOLD",
            "INVENTORY", "ACTIVE_QUESTS", "COMPLETED_QUESTS"
        ]

        for k in required_keys:
            if k not in data:
                raise InvalidSaveDataError(f"Missing '{k}' in save file.")
        
        character = {
            "name": data["NAME"],
            "class": data["CLASS"],
            "level": int(data["LEVEL"]),
            "health": int(data["HEALTH"]),
            "max_health": int(data["MAX_HEALTH"]),
            "strength": int(data["STRENGTH"]),
            "magic": int(data["MAGIC"]),
            "experience": int(data["EXPERIENCE"]),
            "gold": int(data["GOLD"]),
            "inventory": data["INVENTORY"].split(",") if data["INVENTORY"] else [],
            "active_quests": data["ACTIVE_QUESTS"].split(",") if data["ACTIVE_QUESTS"] else [],
            "completed_quests": data["COMPLETED_QUESTS"].split(",") if data["COMPLETED_QUESTS"] else []
        }
    
        # Validate data format → InvalidSaveDataError
        validate_character_data(character)
        return character
    except ValueError:
        raise InvalidSaveDataError("Invalid number format in save file.")
    except KeyError:
        raise InvalidSaveDataError("Missing fields in save file.")

    

def list_saved_characters(save_directory="data/save_games"):
    """
    Get list of all saved character names
    
    Returns: List of character names (without _save.txt extension)
    """
    # TODO: Implement this function
    if not os.path.exists(save_directory):
        return []

    entries = []
    try:
        for fn in os.listdir(save_directory):
            if fn.endswith("_save.txt"):
                entries.append(fn[:-9])  # remove "_save.txt"
    except Exception:
        # If directory can't be read, return empty list rather than crashing
        return []

    return entries
    # Return empty list if directory doesn't exist
    # Extract character names from filenames

def delete_character(character_name, save_directory="data/save_games"):
    """
    Delete a character's save file
    
    Returns: True if deleted successfully
    Raises: CharacterNotFoundError if character doesn't exist
    """
    filename = os.path.join(save_directory, f"{character_name}_save.txt")

    if not os.path.exists(filename):
        raise CharacterNotFoundError(f"{character_name} does not exist.")

    os.remove(filename)
    return True

    # TODO: Implement character deletion
    # Verify file exists before attempting deletion

# ============================================================================
# CHARACTER OPERATIONS
# ============================================================================

def gain_experience(character, xp_amount):
    """
    Add experience to character and handle level ups
    
    Level up formula: level_up_xp = current_level * 100
    Example when leveling up:
    - Increase level by 1
    - Increase max_health by 10
    - Increase strength by 2
    - Increase magic by 2
    - Restore health to max_health
    
    Raises: CharacterDeadError if character health is 0
    """
    if character["health"] <= 0:
        raise CharacterDeadError("Cannot gain XP while dead.")

    character["experience"] += xp_amount

    leveled_up = False

    while character["experience"] >= character["level"] * 100:
        character["experience"] -= character["level"] * 100
        character["level"] += 1
        character["max_health"] += 10
        character["strength"] += 2
        character["magic"] += 2
        character["health"] = character["max_health"]
        leveled_up = True

    return leveled_up
    # TODO: Implement experience gain and leveling
    # Check if character is dead first
    # Add experience
    # Check for level up (can level up multiple times)
    # Update stats on level up

def add_gold(character, amount):
    """
    Add gold to character's inventory
    
    Args:
        character: Character dictionary
        amount: Amount of gold to add (can be negative for spending)
    
    Returns: New gold total
    Raises: ValueError if result would be negative
    """
    new_total = character["gold"] + amount

    if new_total < 0:
        raise ValueError("Gold cannot go negative.")

    character["gold"] = new_total
    return character["gold"]

    # TODO: Implement gold management
    # Check that result won't be negative
    # Update character's gold

def heal_character(character, amount):
    """
    Heal character by specified amount
    
    Health cannot exceed max_health
    
    Returns: Actual amount healed
    """
    if character["health"] <= 0:
        raise CharacterDeadError("Cannot heal a dead character.")

    original = character["health"]
    character["health"] = min(character["health"] + amount, character["max_health"])
    return character["health"] - original

    # TODO: Implement healing
    # Calculate actual healing (don't exceed max_health)
    # Update character health

def is_character_dead(character):
    """
    Check if character's health is 0 or below
    
    Returns: True if dead, False if alive
    """
    return character["health"] <= 0

    # TODO: Implement death check

def revive_character(character):
    """
    Revive a dead character with 50% health
    
    Returns: True if revived
    """
    if character["health"] > 0:
        return False
    
    character["health"] = character["max_health"] // 2

    return True
    # TODO: Implement revival
    # Restore health to half of max_health

# ============================================================================
# VALIDATION
# ============================================================================

def validate_character_data(character):
    """
    Validate that character dictionary has all required fields
    
    Required fields: name, class, level, health, max_health, 
                    strength, magic, experience, gold, inventory,
                    active_quests, completed_quests
    
    Returns: True if valid
    Raises: InvalidSaveDataError if missing fields or invalid types
    """
    required = [
        "name", "class", "level", "health", "max_health",
        "strength", "magic", "experience", "gold",
        "inventory", "active_quests", "completed_quests"
    ]

    for key in required:
        if key not in character:
            raise InvalidSaveDataError(f"Missing field: {key}")

    for field in ["level", "health", "max_health", "strength", "magic", "experience", "gold"]:
        if not isinstance(character[field], int):
            raise InvalidSaveDataError(f"Field {field} must be an integer.")

    for field in ["inventory", "active_quests", "completed_quests"]:
        if not isinstance(character[field], list):
            raise InvalidSaveDataError(f"Field {field} must be a list.")

    return True

    # TODO: Implement validation
    # Check all required keys exist
    # Check that numeric values are numbers
    # Check that lists are actually lists


# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== CHARACTER MANAGER TEST ===")
    
    # Test character creation
    try:
        char = create_character("Lily", "Healer")
        print("Created:", char)
    except Exception as e:
        print("Error:", e)
    # try:
    #     char = create_character("TestHero", "Warrior")
    #     print(f"Created: {char['name']} the {char['class']}")
    #     print(f"Stats: HP={char['health']}, STR={char['strength']}, MAG={char['magic']}")
    # except InvalidCharacterClassError as e:
    #     print(f"Invalid class: {e}")
    
    try:
        save_character(char)
        print("Character saved successfully")
    except Exception as e:
        print(f"Save error: {e}")
    
    # Test saving
    # try:
    #     save_character(char)
    #     print("Character saved successfully")
    # except Exception as e:
    #     print(f"Save error: {e}")
    
    try:
        loaded = load_character("TestHero")
        print(f"Loaded: {loaded['name']}")
    except CharacterNotFoundError:
        print("Character not found")
    except SaveFileCorruptedError:
        print("Save file corrupted")
    # Test loading
    # try:
    #     loaded = load_character("TestHero")
    #     print(f"Loaded: {loaded['name']}")
    # except CharacterNotFoundError:
    #     print("Character not found")
    # except SaveFileCorruptedError:
    #     print("Save file corrupted")

