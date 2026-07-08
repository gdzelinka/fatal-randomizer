import random
from models.character_models import FatalModel
from dice import d10, d20, d100
from race_traits import anakim_traits

race_dict = {
    "Anakim": 1,
    "Bugbear": 15,
    "BlackDwarf": 3,
    "Brown Dwarf": 1,
    "White_Dwarf": 1,
    "Dark Elf": 1,
    "Light Elf": 1,
    "Human": 30,
    "Kobol": 20,
    "Ogre": 6,
    "Cliff Ogre": 2,
    "Gruagach Ogre": 3, 
    "Kinder-fresser Ogre": 1,
    "Borbytingarna Troll": 2,
    "Hill Troll": 3,
    "Subterranean Troll": 10
}

def add_race(character: FatalModel):
    # Race
    character.race = random.choices(
        population=race_dict.keys(),
        weights=race_dict.values(),
        k=1
    )[0]

    if character.race == "Anakim":
        character.strength_modifier += 100
        character.hand_eye_coordination_modifier -= 30
        character.agility_modifier -= 25
        character.reaction_speed_modifier -= 20
        character.language_modifier += 5
        character.math_modifier += 5
        character.analytic_modifier == 5
        character.spatial_modifier += 5
        character.drive_modifier -= 5
        character.intuition_modifier -= 10
        character.common_sense_modifier -= 20
        character.reflection_modifier -= 10

        character.current_armor = 11
        character.life_points = 27

        character.ethical_points -= 25
        character.moral_points -= 50
        character.sanguine -= 25
        character.melancholic -= 25

        character.brawling.skill_modifier += 3
        character.intimidation.skill_modifier += 5
        character.mangling.skill_modifier += 3
        character.sexual_adeptness.skill_modifier += 5
        character.trickery.skill_modifier += 3
        character.weapon_specific.skill_modifier += 5
        character.wrestling.skill_modifier += 5

        character.piety_points += d20()

        number_of_traits = d10()

        for i in range(number_of_traits):
            character.traits += f" {anakim_traits[d100()]}, "

