"""
COMP 163 - Project 3: Quest Chronicles
Game Data Module - Starter Code

Name: Jerryeka 
le

AI Usage: [Document any AI assistance used]

This module handles loading and validating game data from text files.
"""

import os
from custom_exceptions import (
    InvalidDataFormatError,
    MissingDataFileError,
    CorruptedDataError
)

# ============================================================================
# DATA LOADING FUNCTIONS
# ============================================================================

def load_quests(filename="data/quests.txt"):
    """
    Load quest data from file
    
    Expected format per quest (separated by blank lines):
    QUEST_ID: unique_quest_name
    TITLE: Quest Display Title
    DESCRIPTION: Quest description text
    REWARD_XP: 100
    REWARD_GOLD: 50
    REQUIRED_LEVEL: 1
    PREREQUISITE: previous_quest_id (or NONE)
    
    Returns: Dictionary of quests {quest_id: quest_data_dict}
    Raises: MissingDataFileError, InvalidDataFormatError, CorruptedDataError
    """
    if not os.path.exists(filename):
        raise MissingDataFileError(f"Missing file: {filename}")
    
    try:
        with open(filename, "r", encoding="utf-8") as f:
            content = f.read().strip()
    except Exception:
        raise CorruptedDataError("Error reading quests file")

    if not content:
        raise CorruptedDataError("Quest file is empty or corrupted")

    raw_blocks = content.split("\n\n")
    quests = {}

    for block in raw_blocks:
        lines = [line.strip() for line in block.split("\n") if line.strip()]
        quest = parse_quest_block(lines)
        validate_quest_data(quest)
        quests[quest["quest_id"]] = quest

    return quests
    # TODO: Implement this function
    # Must handle:
    # - FileNotFoundError → raise MissingDataFileError
    # - Invalid format → raise InvalidDataFormatError
    # - Corrupted/unreadable data → raise CorruptedDataError

def load_items(filename="data/items.txt"):
    """
    Load item data from file
    
    Expected format per item (separated by blank lines):
    ITEM_ID: unique_item_name
    NAME: Item Display Name
    TYPE: weapon|armor|consumable
    EFFECT: stat_name:value (e.g., strength:5 or health:20)
    COST: 100
    DESCRIPTION: Item description
    
    Returns: Dictionary of items {item_id: item_data_dict}
    Raises: MissingDataFileError, InvalidDataFormatError, CorruptedDataError
    """
    if not os.path.exists(filename):
        raise MissingDataFileError(f"Missing file: {filename}")
    
    try:
        with open(filename, "r", encoding="utf-8") as f:
            content = f.read().strip()
    except Exception:
        raise CorruptedDataError("Error reading items file")

    if not content:
        raise CorruptedDataError("Item file is empty or corrupted")

    raw_blocks = content.split("\n\n")
    items = {}

    for block in raw_blocks:
        lines = [line.strip() for line in block.split("\n") if line.strip()]
        item = parse_item_block(lines)
        validate_item_data(item)
        items[item["item_id"]] = item

    return items
    # TODO: Implement this function
    # Must handle same exceptions as load_quests

def validate_quest_data(quest_dict):
    """
    Validate that quest dictionary has all required fields
    
    Required fields: quest_id, title, description, reward_xp, 
                    reward_gold, required_level, prerequisite
    
    Returns: True if valid
    Raises: InvalidDataFormatError if missing required fields
    """
    required = [
        "quest_id", "title", "description",
        "reward_xp", "reward_gold",
        "required_level", "prerequisite"
    ]

    for key in required:
        if key not in quest_dict:
            raise InvalidDataFormatError(f"Missing quest field: {key}")

    # Numeric fields must be integers
    try:
        int(quest_dict["reward_xp"])
        int(quest_dict["reward_gold"])
        int(quest_dict["required_level"])
    except ValueError:
        raise InvalidDataFormatError("Quest numeric fields must be integers")

    return True  
    # TODO: Implement validation
    # Check that all required keys exist
    # Check that numeric values are actually numbers

def validate_item_data(item_dict):
    """
    Validate that item dictionary has all required fields
    
    Required fields: item_id, name, type, effect, cost, description
    Valid types: weapon, armor, consumable
    
    Returns: True if valid
    Raises: InvalidDataFormatError if missing required fields or invalid type
    """
    required = ["item_id", "name", "type", "effect", "cost", "description"]
    
    for key in required:
        if key not in item_dict:
            raise InvalidDataFormatError(f"Missing item field: {key}")

    if item_dict["type"] not in ["weapon", "armor", "consumable"]:
        raise InvalidDataFormatError(f"Invalid item type: {item_dict['type']}")

    try:
        int(item_dict["cost"])
    except ValueError:
        raise InvalidDataFormatError("Item cost must be an integer")

    return True
    # TODO: Implement validation

def create_default_data_files():
    """
    Create default data files if they don't exist
    This helps with initial setup and testing
    """
    os.makedirs("data", exist_ok=True)

    if not os.path.exists("data/quests.txt"):
        with open("data/quests.txt", "w", encoding="utf-8") as f:
            f.write(
                "QUEST_ID: first_steps\n"
                "TITLE: First Steps\n"
                "DESCRIPTION: Begin your journey.\n"
                "REWARD_XP: 25\n"
                "REWARD_GOLD: 10\n"
                "REQUIRED_LEVEL: 1\n"
                "PREREQUISITE: NONE\n\n"

                "QUEST_ID: goblin_hunter\n"
                "TITLE: Goblin Hunter\n"
                "DESCRIPTION: Clear out the goblins threatening the village.\n"
                "REWARD_XP: 150\n"
                "REWARD_GOLD: 50\n"
                "REQUIRED_LEVEL: 2\n"
                "PREREQUISITE: first_steps\n\n"

                "QUEST_ID: dragon_slayer\n"
                "TITLE: Dragon Slayer\n"
                "DESCRIPTION: Defeat the mighty dragon and save the kingdom.\n"
                "REWARD_XP: 500\n"
                "REWARD_GOLD: 300\n"
                "REQUIRED_LEVEL: 3\n"
                "PREREQUISITE: goblin_hunter\n"
            )

    # TODO: Implement this function
    # Create data/ directory if it doesn't exist
    # Create default quests.txt and items.txt files
    # Handle any file permission errors appropriately

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def parse_quest_block(lines):
    """
    Parse a block of lines into a quest dictionary
    
    Args:
        lines: List of strings representing one quest
    
    Returns: Dictionary with quest data
    Raises: InvalidDataFormatError if parsing fails
    """
    quest = {}
    for line in lines:
        if ": " not in line:
            raise InvalidDataFormatError(f"Invalid line in quest block: {line}")

        key, value = line.split(": ", 1)
        key = key.strip().lower()
        value = value.strip()

        # Convert numeric fields
        if key in ["reward_xp", "reward_gold", "required_level"]:
            try:
                quest[key] = int(value)
            except ValueError:
                raise InvalidDataFormatError(f"Invalid number for {key}")

        # Handle optional prerequisite
        elif key == "prerequisite":
            quest[key] = None if value.upper() == "NONE" else value

        else:
            quest[key] = value

    return quest
    # TODO: Implement parsing logic
    # Split each line on ": " to get key-value pairs
    # Convert numeric strings to integers
    # Handle parsing errors gracefully

def parse_item_block(lines):
    """
    Parse a block of lines into an item dictionary
    
    Args:
        lines: List of strings representing one item
    
    Returns: Dictionary with item data
    Raises: InvalidDataFormatError if parsing fails
    """
    item = {}

    for raw in lines:
        line = raw.strip()
        if not line or ":" not in line:
            continue

        key, value = line.split(":", 1)
        key = key.strip().upper()
        value = value.strip()

        if key == "ITEM_ID":
            key = "id"
        else:
            key = key.lower()

        if key == "cost":
            try:
                value = int(value)
            except ValueError:
                raise InvalidDataFormatError(f"Invalid COST value: {value}")

        item[key] = value

    required = ["id", "name", "type", "effect", "cost"]
    for r in required:
        if r not in item:
            raise InvalidDataFormatError(f"Missing required field: {r.upper()}")

    return item

        

    # TODO: Implement parsing logic

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== GAME DATA MODULE TEST ===")
    
    create_default_data_files()
    # Test creating default files
    # create_default_data_files()
    
    try:
        quests = load_quests()
        print(f"Loaded {len(quests)} quests")
    except MissingDataFileError:
        print("Quest file not found")
    except InvalidDataFormatError as e:
        print(f"Invalid quest format: {e}")
    # Test loading quests
    # try:
    #     quests = load_quests()
    #     print(f"Loaded {len(quests)} quests")
    # except MissingDataFileError:
    #     print("Quest file not found")
    # except InvalidDataFormatError as e:
    #     print(f"Invalid quest format: {e}")
    
    try:
        items = load_items()
        print(f"Loaded {len(items)} items")
    except MissingDataFileError:
        print("Item file not found")
    except InvalidDataFormatError as e:
        print(f"Invalid item format: {e}")
    # Test loading items
    # try:
    #     items = load_items()
    #     print(f"Loaded {len(items)} items")
    # except MissingDataFileError:
    #     print("Item file not found")
    # except InvalidDataFormatError as e:
    #     print(f"Invalid item format: {e}")

