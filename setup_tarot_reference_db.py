#!/usr/bin/env python3
"""
Setup Tarot Reference Database - Creates a reference database of tarot card symbolism and meanings
"""

import os
import sys
import json
import argparse
import csv
from pathlib import Path

# Configuration
REFERENCE_DIR = "reference/database"
SYMBOLISM_FILE = "tarot_symbolism.json"
MEANINGS_FILE = "tarot_meanings.json"
COLORS_FILE = "tarot_colors.json"
ELEMENTS_FILE = "tarot_elements.json"

# Tarot card definitions
MAJOR_ARCANA = [
    {
        "name": "The Fool",
        "numeral": "0",
        "keywords": "beginnings, innocence, spontaneity, free spirit",
        "symbolism": [
            "cliff edge (risk, leap of faith)",
            "white rose (purity)",
            "small dog (loyalty, protection)",
            "mountains (challenges ahead)",
            "bundle (untapped potential)"
        ],
        "colors": ["yellow", "white", "blue", "green"],
        "elements": ["air"],
        "upright_meaning": "New beginnings, innocence, spontaneity, free spirit, taking a leap of faith",
        "reversed_meaning": "Recklessness, carelessness, risk-taking, naivety"
    },
    {
        "name": "The Magician",
        "numeral": "I",
        "keywords": "manifestation, resourcefulness, power, inspired action",
        "symbolism": [
            "infinity symbol (unlimited potential)",
            "ouroboros belt (continuity, renewal)",
            "red and white clothing (passion and purity)",
            "four elements on table (mastery of all elements)",
            "raised wand (channel between heaven and earth)"
        ],
        "colors": ["red", "white", "yellow"],
        "elements": ["air", "fire"],
        "upright_meaning": "Manifestation, resourcefulness, power, inspired action, skill",
        "reversed_meaning": "Manipulation, poor planning, untapped talents, deception"
    },
    {
        "name": "The High Priestess",
        "numeral": "II",
        "keywords": "intuition, sacred knowledge, divine feminine, subconscious mind",
        "symbolism": [
            "moon crescent (intuition, cycles)",
            "blue robe (wisdom, tranquility)",
            "Torah scroll (hidden knowledge)",
            "pillars B and J (duality, balance)",
            "veil (mystery, the unknown)"
        ],
        "colors": ["blue", "white", "black"],
        "elements": ["water"],
        "upright_meaning": "Intuition, sacred knowledge, divine feminine, inner voice, unconscious mind",
        "reversed_meaning": "Secrets, disconnected from intuition, withdrawal, silence"
    },
    {
        "name": "The Empress",
        "numeral": "III",
        "keywords": "femininity, beauty, nature, nurturing, abundance",
        "symbolism": [
            "pregnant woman (fertility, motherhood)",
            "venus symbol (femininity)",
            "crown of stars (divine connection)",
            "lush garden (abundance, growth)",
            "flowing water (emotions, life)"
        ],
        "colors": ["green", "red", "yellow"],
        "elements": ["earth"],
        "upright_meaning": "Femininity, beauty, nature, nurturing, abundance, fertility, creativity",
        "reversed_meaning": "Creative block, dependence, emptiness, lack of growth"
    },
    {
        "name": "The Emperor",
        "numeral": "IV",
        "keywords": "authority, structure, control, fatherhood, leadership",
        "symbolism": [
            "throne (power, authority)",
            "ram heads (determination, Aries)",
            "orb and scepter (dominion)",
            "red robe (passion, energy)",
            "mountains (stability, permanence)"
        ],
        "colors": ["red", "orange", "purple"],
        "elements": ["fire"],
        "upright_meaning": "Authority, structure, control, fatherhood, leadership, stability",
        "reversed_meaning": "Domination, excessive control, rigidity, inflexibility"
    },
    {
        "name": "The Hierophant",
        "numeral": "V",
        "keywords": "spiritual wisdom, religious beliefs, conformity, tradition",
        "symbolism": [
            "papal cross (religion, tradition)",
            "triple crown (authority)",
            "two keys (knowledge, mysteries)",
            "pillars (institution, structure)",
            "disciples (followers, conformity)"
        ],
        "colors": ["red", "white", "grey"],
        "elements": ["earth"],
        "upright_meaning": "Spiritual wisdom, religious beliefs, conformity, tradition, institutions",
        "reversed_meaning": "Personal beliefs, freedom, challenging convention, rebellion"
    },
    {
        "name": "The Lovers",
        "numeral": "VI",
        "keywords": "love, harmony, relationships, values alignment, choices",
        "symbolism": [
            "Adam and Eve (divine union, duality)",
            "angel (divine blessing)",
            "tree of knowledge (temptation)",
            "tree of life (immortality)",
            "mountain (challenges to overcome)"
        ],
        "colors": ["yellow", "orange", "red", "blue"],
        "elements": ["air"],
        "upright_meaning": "Love, harmony, relationships, values alignment, choices, union",
        "reversed_meaning": "Disharmony, imbalance, misalignment of values, discord"
    },
    {
        "name": "The Chariot",
        "numeral": "VII",
        "keywords": "control, willpower, success, action, determination",
        "symbolism": [
            "armored warrior (strength, protection)",
            "black and white sphinxes (opposing forces)",
            "chariot (vehicle of triumph)",
            "star crown (celestial guidance)",
            "walled city (civilization, achievement)"
        ],
        "colors": ["black", "white", "blue", "yellow"],
        "elements": ["water"],
        "upright_meaning": "Control, willpower, success, action, determination, overcoming obstacles",
        "reversed_meaning": "Lack of direction, lack of control, aggression, defeat"
    },
    {
        "name": "Strength",
        "numeral": "VIII",
        "keywords": "strength, courage, patience, control, compassion",
        "symbolism": [
            "woman and lion (taming wild forces)",
            "infinity symbol (unlimited potential)",
            "white dress (purity)",
            "flowers (beauty, gentleness)",
            "mountains (challenges overcome)"
        ],
        "colors": ["yellow", "white", "red"],
        "elements": ["fire"],
        "upright_meaning": "Strength, courage, patience, control, compassion, inner strength",
        "reversed_meaning": "Weakness, self-doubt, lack of self-discipline, raw emotion"
    },
    {
        "name": "The Hermit",
        "numeral": "IX",
        "keywords": "soul-searching, introspection, being alone, inner guidance",
        "symbolism": [
            "lantern (illumination, guidance)",
            "staff (support, authority)",
            "grey cloak (neutrality, wisdom)",
            "mountain peak (achievement, solitude)",
            "snow (purity, clarity)"
        ],
        "colors": ["grey", "blue", "yellow"],
        "elements": ["earth"],
        "upright_meaning": "Soul-searching, introspection, being alone, inner guidance, spiritual enlightenment",
        "reversed_meaning": "Isolation, loneliness, withdrawal, rejection, regression"
    },
    {
        "name": "Wheel of Fortune",
        "numeral": "X",
        "keywords": "good luck, karma, life cycles, destiny, turning point",
        "symbolism": [
            "wheel (cycles, change)",
            "sphinx (wisdom, riddles)",
            "four creatures (four elements, evangelists)",
            "Hebrew letters (divine name)",
            "snake (transformation)"
        ],
        "colors": ["blue", "red", "yellow", "purple"],
        "elements": ["fire", "earth"],
        "upright_meaning": "Good luck, karma, life cycles, destiny, turning point, change",
        "reversed_meaning": "Bad luck, resistance to change, breaking cycles, disruption"
    },
    {
        "name": "Justice",
        "numeral": "XI",
        "keywords": "justice, fairness, truth, cause and effect, law",
        "symbolism": [
            "scales (balance, fairness)",
            "sword (clarity, truth)",
            "crown (authority)",
            "purple cloak (dignity, power)",
            "pillars (structure, stability)"
        ],
        "colors": ["red", "yellow", "grey", "purple"],
        "elements": ["air"],
        "upright_meaning": "Justice, fairness, truth, cause and effect, law, clarity, karma",
        "reversed_meaning": "Unfairness, lack of accountability, dishonesty, injustice"
    },
    {
        "name": "The Hanged Man",
        "numeral": "XII",
        "keywords": "surrender, letting go, new perspective, sacrifice",
        "symbolism": [
            "hanging upside-down (new perspective)",
            "tree (world tree, connection)",
            "halo (enlightenment)",
            "crossed leg (integration)",
            "rope (voluntary surrender)"
        ],
        "colors": ["blue", "red", "yellow", "green"],
        "elements": ["water"],
        "upright_meaning": "Surrender, letting go, new perspective, sacrifice, suspension, waiting",
        "reversed_meaning": "Delays, resistance, stalling, indecision, stagnation"
    },
    {
        "name": "Death",
        "numeral": "XIII",
        "keywords": "endings, change, transformation, transition",
        "symbolism": [
            "skeleton (mortality, what remains)",
            "black flag (transformation)",
            "white rose (purity, new beginnings)",
            "rising sun (rebirth)",
            "boat on river (journey to afterlife)"
        ],
        "colors": ["black", "white", "blue", "grey"],
        "elements": ["water"],
        "upright_meaning": "Endings, change, transformation, transition, letting go, rebirth",
        "reversed_meaning": "Resistance to change, inability to move on, stagnation, decay"
    },
    {
        "name": "Temperance",
        "numeral": "XIV",
        "keywords": "balance, moderation, patience, purpose, meaning",
        "symbolism": [
            "angel (divine messenger)",
            "one foot on land, one in water (balance)",
            "cups (flow of emotions)",
            "path to mountain (journey to enlightenment)",
            "triangle in square (integration of spirit and matter)"
        ],
        "colors": ["blue", "yellow", "red", "white"],
        "elements": ["fire", "water"],
        "upright_meaning": "Balance, moderation, patience, purpose, meaning, harmony, synthesis",
        "reversed_meaning": "Imbalance, excess, lack of harmony, misalignment, discord"
    },
    {
        "name": "The Devil",
        "numeral": "XV",
        "keywords": "shadow self, attachment, addiction, restriction, sexuality",
        "symbolism": [
            "horned figure (primal instincts)",
            "chains (bondage, attachment)",
            "naked figures (vulnerability)",
            "pentagram (material world)",
            "torch (destructive fire)"
        ],
        "colors": ["black", "red", "brown"],
        "elements": ["earth"],
        "upright_meaning": "Shadow self, attachment, addiction, restriction, sexuality, materialism",
        "reversed_meaning": "Breaking free, release, exploring dark thoughts, detachment"
    },
    {
        "name": "The Tower",
        "numeral": "XVI",
        "keywords": "sudden change, upheaval, chaos, revelation, awakening",
        "symbolism": [
            "lightning bolt (sudden illumination)",
            "crown (false concepts)",
            "falling figures (forced removal)",
            "tower (constructed beliefs)",
            "flames (destruction, purification)"
        ],
        "colors": ["red", "orange", "black", "grey"],
        "elements": ["fire"],
        "upright_meaning": "Sudden change, upheaval, chaos, revelation, awakening, truth, liberation",
        "reversed_meaning": "Avoiding disaster, fear of change, delaying the inevitable"
    },
    {
        "name": "The Star",
        "numeral": "XVII",
        "keywords": "hope, faith, purpose, renewal, spirituality",
        "symbolism": [
            "star (divine guidance)",
            "naked woman (vulnerability, truth)",
            "water (unconscious, emotion)",
            "land (material world)",
            "birds (messengers, freedom)"
        ],
        "colors": ["blue", "yellow", "white"],
        "elements": ["air", "water"],
        "upright_meaning": "Hope, faith, purpose, renewal, spirituality, inspiration, serenity",
        "reversed_meaning": "Lack of faith, despair, discouragement, insecurity, disconnection"
    },
    {
        "name": "The Moon",
        "numeral": "XVIII",
        "keywords": "illusion, fear, anxiety, subconscious, intuition",
        "symbolism": [
            "moon (intuition, cycles)",
            "howling wolf and dog (primal instincts)",
            "crayfish (unconscious mind)",
            "path (journey through darkness)",
            "towers (gateways to unknown)"
        ],
        "colors": ["blue", "yellow", "grey", "black"],
        "elements": ["water"],
        "upright_meaning": "Illusion, fear, anxiety, subconscious, intuition, dreams, uncertainty",
        "reversed_meaning": "Release of fear, repressed emotion, inner confusion, clarity"
    },
    {
        "name": "The Sun",
        "numeral": "XIX",
        "keywords": "positivity, fun, warmth, success, vitality",
        "symbolism": [
            "sun (life force, clarity)",
            "child (innocence, joy)",
            "sunflowers (abundance, happiness)",
            "white horse (strength, purity)",
            "red banner (vitality, passion)"
        ],
        "colors": ["yellow", "orange", "white", "red"],
        "elements": ["fire"],
        "upright_meaning": "Positivity, fun, warmth, success, vitality, joy, radiance, enlightenment",
        "reversed_meaning": "Temporary depression, lack of success, sadness, blocked creativity"
    },
    {
        "name": "Judgement",
        "numeral": "XX",
        "keywords": "rebirth, inner calling, absolution, self-evaluation",
        "symbolism": [
            "angel (divine messenger)",
            "trumpet (awakening call)",
            "rising figures (resurrection)",
            "mountains (challenges overcome)",
            "flag (victory)"
        ],
        "colors": ["blue", "white", "grey", "red"],
        "elements": ["fire", "water"],
        "upright_meaning": "Rebirth, inner calling, absolution, self-evaluation, awakening, renewal",
        "reversed_meaning": "Self-doubt, refusal of self-examination, fear of change, stagnation"
    },
    {
        "name": "The World",
        "numeral": "XXI",
        "keywords": "completion, accomplishment, travel, harmony, wholeness",
        "symbolism": [
            "dancing figure (joy, freedom)",
            "wreath (completion, success)",
            "four creatures (four elements, evangelists)",
            "purple sash (spiritual achievement)",
            "wands (balance of forces)"
        ],
        "colors": ["blue", "green", "purple", "yellow"],
        "elements": ["earth"],
        "upright_meaning": "Completion, accomplishment, travel, harmony, wholeness, fulfillment",
        "reversed_meaning": "Lack of completion, lack of closure, seeking personal closure"
    }
]

def create_symbolism_database():
    """Create a database of tarot card symbolism"""
    symbolism_data = {}
    
    for card in MAJOR_ARCANA:
        symbolism_data[card["name"]] = {
            "numeral": card["numeral"],
            "keywords": card["keywords"],
            "symbolism": card["symbolism"]
        }
    
    return symbolism_data

def create_meanings_database():
    """Create a database of tarot card meanings"""
    meanings_data = {}
    
    for card in MAJOR_ARCANA:
        meanings_data[card["name"]] = {
            "numeral": card["numeral"],
            "upright_meaning": card["upright_meaning"],
            "reversed_meaning": card["reversed_meaning"]
        }
    
    return meanings_data

def create_colors_database():
    """Create a database of tarot card colors"""
    colors_data = {}
    
    for card in MAJOR_ARCANA:
        colors_data[card["name"]] = {
            "numeral": card["numeral"],
            "colors": card["colors"]
        }
    
    return colors_data

def create_elements_database():
    """Create a database of tarot card elements"""
    elements_data = {}
    
    for card in MAJOR_ARCANA:
        elements_data[card["name"]] = {
            "numeral": card["numeral"],
            "elements": card["elements"]
        }
    
    return elements_data

def save_json_file(data, filename):
    """Save data to a JSON file"""
    try:
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"Saved {filename}")
        return True
    except Exception as e:
        print(f"Error saving {filename}: {e}")
        return False

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Setup tarot reference database")
    
    args = parser.parse_args()
    
    print("Tarot Reference Database Setup")
    print("=============================")
    print()
    
    # Create reference directory
    os.makedirs(REFERENCE_DIR, exist_ok=True)
    
    # Create symbolism database
    symbolism_data = create_symbolism_database()
    symbolism_file = os.path.join(REFERENCE_DIR, SYMBOLISM_FILE)
    save_json_file(symbolism_data, symbolism_file)
    
    # Create meanings database
    meanings_data = create_meanings_database()
    meanings_file = os.path.join(REFERENCE_DIR, MEANINGS_FILE)
    save_json_file(meanings_data, meanings_file)
    
    # Create colors database
    colors_data = create_colors_database()
    colors_file = os.path.join(REFERENCE_DIR, COLORS_FILE)
    save_json_file(colors_data, colors_file)
    
    # Create elements database
    elements_data = create_elements_database()
    elements_file = os.path.join(REFERENCE_DIR, ELEMENTS_FILE)
    save_json_file(elements_data, elements_file)
    
    print("\nTarot reference database setup complete!")
    print(f"Reference files saved to {REFERENCE_DIR}")
    
    return 0

if __name__ == "__main__":
    try:
        exit_code = main()
        exit(exit_code)
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        exit(1)
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
        exit(1)
