from models.character_models import FatalModel
from dice import d100
from math import floor

def add_gender(character: FatalModel):
    gender_roll = d100()

    if character.race in ["Anakim", "Ogre", "Troll"]:
        gender_roll += 10
    
    if gender_roll < 53:
        character.gender = "female"
    else:
        character.gender = "male"
    
    return character

def add_gender_modifiers(character: FatalModel):
    if "Hermaphrodite" in character.traits:
        return character

    if character.gender == "male":
        character.physical_fitness = floor(character.physical_fitness * 1.05)
        character.strength = floor(character.strength * 1.3)
        character.bodily_attractiveness = floor(character.bodily_attractiveness * 0.97)
        character.facial = floor(character.facial * 0.97)
        character.language = floor(character.language * 0.98)
        character.math = floor(character.math * 1.03)
        character.spatial = floor(character.spatial * 1.03)
        character.drive = floor(character.drive * 1.02)
        character.intuition = floor(character.intuition * 0.95)
        character.reflection = floor(character.reflection * 0.96)

        character.sanguine -= 2
        character.choleric += 2

    elif character.gender == "female":
        character.physical_fitness = floor(character.physical_fitness * 0.95)
        character.strength = floor(character.strength * 0.7)
        character.bodily_attractiveness = floor(character.bodily_attractiveness * 1.03)
        character.facial = floor(character.facial * 1.03)
        character.language = floor(character.language * 1.02)
        character.math = floor(character.math * 0.97)
        character.spatial = floor(character.spatial * 0.97)
        character.drive = floor(character.drive * 0.98)
        character.intuition = floor(character.intuition * 1.05)
        character.reflection = floor(character.reflection * 1.04)

        character.sanguine += 2
        character.choleric -= 2
    
    return character