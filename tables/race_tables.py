import random
from models.character_models import FatalModel
from dice import d10, d20, d100
from race_traits import anakim_traits

race_dict = {
    "Anakim": 1,
    "Bugbear": 15,
    "Black Dwarf": 3,
    "Brown Dwarf": 1,
    "White Dwarf": 1,
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


def handle_race_traits(character):
    number_of_traits = d10()

    for _ in range(number_of_traits):
        trait_roll = d100()
        if character.race == "Anakim":
            trait = anakim_traits[trait_roll]
        character.traits += f" {trait[0]}, "
        # Handling random modifiers
        if len(trait) > 1:
            for key, value in trait[1]:
                if not isinstance(value, (tuple)):
                    setattr(character, key, getattr(character, key) + value)
                else:
                    if isinstance(value[0], str):
                        setattr(character, key, getattr(character, key).append(value[0]))
                    elif isinstance(value[0], list):
                        pass_fail = False
                        and_or = value[0]
                        for condition in value[1:]:
                            check = condition[1]
                            if condition[0] == "bool":
                                if and_or == "OR" and getattr(character, check) == condition[2]:
                                    pass_fail = True
                                elif and_or == "AND" and getattr(character, check) != condition[2]:
                                    pass_fail = False
                            elif condition[0] == "less than":
                                if and_or == "OR" and getattr(character, check) < condition[2]:
                                    pass_fail = True
                                elif and_or == "AND" and getattr(character, check) >= condition[2]:
                                    pass_fail = False
                            elif condition[0] == "greater than":
                                if and_or == "OR" and getattr(character, check) >= condition[2]:
                                    pass_fail = True
                                elif and_or == "AND" and getattr(character, check) < condition[2]:
                                    pass_fail = False
                        if pass_fail:
                            setattr(character, key, getattr(character, key) + value[1])
    return character


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
        character.analytic_modifier += 5
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

        character.languages_spoken.append("Sapian")
        character.number_of_languages += 1

        character.brawling.skill_modifier += 3
        character.intimidation.skill_modifier += 5
        character.mangling.skill_modifier += 3
        character.sexual_adeptness.skill_modifier += 5
        character.trickery.skill_modifier += 3
        character.weapon_specific.skill_modifier += 5
        character.wrestling.skill_modifier += 5

        character.piety_points += d20()

        character = handle_race_traits(character)

    elif character.race == "Bugbear":
        character.strength_modifier += 100
        character.bodily_attractiveness_modifier -= 20
        character.facial_modifier -= 15
        character.rhetorical_modifier -= 10
        character.hand_eye_coordination_modifier -= 10
        character.agility_modifier -= 10
        character.ennunciation_modifier -= 10
        character.language_modifier -= 10
        character.math_modifier += 10
        character.analytic_modifier -= 10
        character.spatial_modifier += 5
        character.drive_modifier += 10

        character.current_armor = 12
        character.life_points = 25

        character.ethical_points += 25
        character.moral_points -= 50
        character.sanguine -= 25
        character.choleric += 25
        character.melancholic += 25

        character.languages_spoken.append("Kobold")
        character.number_of_languages += 1

        character.brawling.skill_modifier += 3
        character.delousing.skill_modifier += 5
        character.divination_anthropomancy.skill_modifier += 3
        character.divination_dririmancy.skill_modifier += 3
        character.law.skill_modifier += 3
        character.sailing.skill_modifier += 3
        character.search.skill_modifier += 3
        character.shipwright.skill_modifier += 3
        character.surgery.skill_modifier += 3
        character.tracking.skill_modifier += 3
        character.weapon_specific.skill_modifier += 5
        character.wrestling.skill_modifier += 3

    elif character.race == "Black Dwarf":

    elif character.race == "Brown Dwarf":
    elif character.race == "White Dwarf":
    elif character.race == "Dark Elf":
    elif character.race == "Light Elf":
    elif character.race == "Human":
    elif character.race == "Kobol":
    elif character.race == "Ogre":
    elif character.race == "Cliff Ogre":
    elif character.race == "Gruagach Ogre":
    elif character.race == "Kinder-fresser Ogre":
    elif character.race == "Borbytingarna Troll":
    elif character.race == "Hill Troll":
    elif character.race == "Subterranean Troll":



