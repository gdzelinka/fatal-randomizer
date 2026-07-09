from models.character_models import FatalModel
from dice import d100
from math import floor

def ability_dice():
    tendhundred = 0
    for _ in range(10):
        tendhundred += d100()
    return floor((tendhundred / 5) - 1)

def calculate_sub_abilities(character : FatalModel):
    character.physical_fitness = ability_dice()
    character.strength = ability_dice()
    character.bodily_attractiveness = ability_dice()
    character.health = ability_dice()

    character.facial = ability_dice()
    character.vocal = ability_dice()
    character.kinetic = ability_dice()
    character.rhetorical = ability_dice()

    character.hand_eye_coordination = ability_dice()
    character.agility = ability_dice()
    character.reaction_speed = ability_dice()
    character.ennunciation = ability_dice()

    character.language = ability_dice()
    character.math = ability_dice()
    character.analytic = ability_dice()
    character.spatial = ability_dice()

    character.drive = ability_dice()
    character.intuition = ability_dice()
    character.common_sense = ability_dice()
    character.reflection = ability_dice()

    return character

def calculate_main_abilities(character: FatalModel):
    character.physique = floor((character.physical_fitness + \
                                character.strength + \
                                character.bodily_attractiveness + \
                                character.health) / 4)

    character.charisma = floor((character.facial + \
                                character.vocal + \
                                character.kinetic + \
                                character.rhetorical) / 4)
    
    character.dexterity = floor((character.hand_eye_coordination + \
                                character.agility + \
                                character.reaction_speed + \
                                character.ennunciation) / 4)

    character.intelligence = floor((character.language + \
                                character.math + \
                                character.analytic + \
                                character.spatial) / 4)
    
    character.wisdom = floor((character.drive + \
                                character.intuition + \
                                character.common_sense + \
                                character.reflection) / 4)

    return character