from models.character_models import FatalModel
from dice import d8, d10, d100
from math import floor, ceil
from tables.ability_tables import (
    fitness_table,
    strength_table,
    health_table,
    facial_descriptions,
    vocal_descriptions,
    kinetic_descriptions,
    average_speech_rate,
    finger_precision,
    agility_table,
    deep_sleep_recovery,
    enunciation_table,
    language_table,
    math_descriptions, 
    unfamiliar_object_assembly,
    drive_table,
    common_sense_descriptions,
    earliest_memory_at
)
from tables.body_tables import allergies

def ability_dice():
    tendhundred = 0
    for _ in range(10):
        tendhundred += d100()
    return floor((tendhundred / 5) - 1)

def calculate_sub_abilities(character: FatalModel):
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
    if character.physique < 1:
        character.physique = 1
    character.physique_modifier = fitness_table[ceil((character.physique / 6))][0]

    character.charisma = floor((character.facial + \
                                character.vocal + \
                                character.kinetic + \
                                character.rhetorical) / 4)
    if character.charisma < 1:
        character.charisma = 1
    character.charisma_modifier = fitness_table[ceil((character.charisma / 6))][0]
    
    character.dexterity = floor((character.hand_eye_coordination + \
                                character.agility + \
                                character.reaction_speed + \
                                character.ennunciation) / 4)
    if character.dexterity < 1:
        character.dexterity = 1
    character.dexterity_modifer = fitness_table[ceil((character.dexterity / 6))][0]

    character.intelligence = floor((character.language + \
                                character.math + \
                                character.analytic + \
                                character.spatial) / 4)
    if character.intelligence < 1:
        character.intelligence = 1
    character.intelligence_modifier = fitness_table[ceil((character.intelligence / 6))][0]
    
    character.wisdom = floor((character.drive + \
                                character.intuition + \
                                character.common_sense + \
                                character.reflection) / 4)
    if character.wisdom < 1:
        character.wisdom = 1
    character.wisdom_modifier = fitness_table[ceil((character.wisdom / 6))][0]

    return character

def reroll_subability(character: FatalModel, ability_name):
    if character.num_skill_rerolls < 4:
        new_roll = sorted([d100(), d100(), d100(), d100(), d100()])
        new_ability_score = 0
        for v in new_roll[1:]:
            new_ability_score += v

        new_ability_score = (new_ability_score / 2) + 1

        setattr(character, ability_name, new_ability_score)
        character.num_skill_rerolls += 1

        mental_illness_roll = d100()

        character.mental_illnesses.append(mental_illness_table[mental_illness_roll])

def apply_subability_modifiers(character: FatalModel):
    fitness_modifier = fitness_table[ceil((character.physical_fitness /6))]
    character.physical_fitness_modifier = fitness_modifier[0]
    character.bodily_attractiveness += fitness_modifier[0]
    if character.height < 12:
        height_marker = 0
    else:
        height_marker = floor((character.height - 12) / 12)
    character.sprint = fitness_modifier[1][height_marker]

    strength_list = strength_table[ceil((character.strength /6))]
    character.strength_modifier = strength_list[0]
    # TODO Damage here?
    character.life_points += strength_list[2]
    character.cj = strength_list[3]
    character.bench = strength_list[4]
    character.dl = strength_list[5]

    character.bodily_attractiveness_modifier = fitness_table[ceil(character.bodily_attractiveness / 6)][0]

    health_mod = ceil((character.health /6))
    character.health_modifier = fitness_table[health_mod][0]
    character.int_vom = -1 * fitness_table[health_mod][0]
    character.life_points += health_table[health_mod][0]
    num_allergies = health_table[health_mod][1]
    for _ in range(num_allergies):
        allergy_roll = d8()
        new_allergy = allergies[allergy_roll]
        if new_allergy in character.allergies:
            num_allergies  = num_allergies + 1
            continue
        character.allergies.append(new_allergy)
    character.illness_immunity = health_table[health_mod][2]

    facial_mod = ceil((character.facial /6))
    character.facial_modifier = fitness_table[facial_mod][0]
    character.facial_description = facial_descriptions[facial_mod -1]

    vocal_mod = ceil((character.vocal /6))
    character.vocal_modifier = fitness_table[vocal_mod][0]
    character.vocal_description = vocal_descriptions[vocal_mod -1]

    kinetic_mod = ceil((character.kinetic /6))
    character.kinetic_modifier = fitness_table[kinetic_mod][0]
    character.kinetic_description = kinetic_descriptions[kinetic_mod -1]

    rhetorical_mod = ceil((character.rhetorical /6))
    character.rhetorical_modifier = fitness_table[rhetorical_mod][0]
    character.average_speech_rate = average_speech_rate[rhetorical_mod -1]

    hand_eye_mod = ceil((character.hand_eye_coordination /6))
    character.hand_eye_coordination_modifier = fitness_table[hand_eye_mod][0]
    character.finger_movement_precision = finger_precision[hand_eye_mod -1]

    agility_mod = ceil((character.agility /6))
    character.agility_modifier = fitness_table[agility_mod][0]
    character.current_armor += agility_table[agility_mod -1][0]
    character.brawling = agility_table[agility_mod -1][1]
    character.stand = agility_table[agility_mod -1][2]

    reaction_mod = ceil((character.reaction_speed / 6))
    character.reaction_speed_modifier = fitness_table[reaction_mod][0]
    character.deep_sleep_recovery = deep_sleep_recovery[reaction_mod -1]

    ennunciation_mod = ceil((character.ennunciation / 6))
    character.ennunciation_modifier = fitness_table[ennunciation_mod][0]
    character.maximum_speech_rate = enunciation_table[ennunciation_mod][0]
    character.casting = enunciation_table[ennunciation_mod][1]

    language_mod = ceil((character.language / 6))
    character.language_modifier = fitness_table[language_mod][0]
    character.max_num_of_languages = language_table[language_mod][0]
    character.vocabulary = language_table[language_mod][1]

    math_mod = ceil((character.math / 6))
    character.math_modifier = fitness_table[math_mod][0]
    character.highest_possible_math = math_descriptions[math_mod -1]

    character.analytic_modifier = fitness_table[ceil((character.analytic /6))][0]

    spatial_mod = ceil((character.spatial / 6))
    character.spatial_modifier = fitness_table[spatial_mod][0]
    character.unfamiliar_object_assembly = unfamiliar_object_assembly[spatial_mod -1]

    drive_mod = ceil((character.drive / 6))
    character.drive_modifier = fitness_table[drive_mod][0]
    character.life_points += drive_table[drive_mod][0]
    character.unconscioness = drive_table[drive_mod][1]
    character.hours_resting = drive_table[drive_mod][2]

    character.intuition_modifier = fitness_table[ceil((character.intuition /6))][0]

    common_sense_mod = ceil((character.common_sense / 6))
    character.common_sense_modifier = fitness_table[common_sense_mod][0]
    character.likely_to = common_sense_descriptions[common_sense_mod -1]

    reflection_mod = ceil((character.reflection / 6))
    character.reflection_modifier = fitness_table[reflection_mod][0]
    character.earliest_memory_at = earliest_memory_at[reflection_mod -1]

    return character

def determine_r_strength(character: FatalModel, intelligence: int, slow_score: int):
    r_strenth_roll = d100()
    chance = (slow_score - intelligence) * 3

    if r_strenth_roll < chance:
        increase = f"1.{(d10() + d10()):02d}"
        character.strength = floor(character.strength * float(increase))
    return character

def determine_int_range(character: FatalModel):
    # This will need to be done before calcualting main abilities due to its ability to affect strength
    # But this must be done after assigning a race
    # This must be done before assigning race modifiers due to ogre language checking this 
    intelligence = floor((character.language + \
                            character.math + \
                                character.analytic + \
                                character.spatial) / 4)
    if character.race == "Anakim":
        if intelligence < 76:
            character.intelligence_range = 0
            character = determine_r_strength(character, intelligence, 76)
            return character
        if intelligence < 91:
            character.intelligence_range = 1
            return character
        if intelligence < 121:
            character.intelligence_range = 2
            return character
        if intelligence < 136:
            character.intelligence_range = 3
            return character
        character.intelligence_range = 4
        return character
    if character.race == "Bugbear":
        if intelligence < 69:
            character.intelligence_range = 0
            character = determine_r_strength(character, intelligence, 69)
            return character
        if intelligence < 84:
            character.intelligence_range = 1
            return character
        if intelligence < 114:
            character.intelligence_range = 2
            return character
        if intelligence < 129:
            character.intelligence_range = 3
            return character
        character.intelligence_range = 4
        return character
    if character.race in ["Black Dwarf", "Brown Dwarf", "White Dwarf"]:
        if intelligence < 74:
            character.intelligence_range = 0
            character = determine_r_strength(character, intelligence, 74)
            return character
        if intelligence < 89:
            character.intelligence_range = 1
            return character
        if intelligence < 119:
            character.intelligence_range = 2
            return character
        if intelligence < 134:
            character.intelligence_range = 3
            return character
        character.intelligence_range = 4
        return character
    if character.race in ["Dark Elf", "Light Elf", "Human"]:
        if intelligence < 71:
            character.intelligence_range = 0
            character = determine_r_strength(character, intelligence, 71)
            return character
        if intelligence < 86:
            character.intelligence_range = 1
            return character
        if intelligence < 116:
            character.intelligence_range = 2
            return character
        if intelligence < 131:
            character.intelligence_range = 3
            return character
        character.intelligence_range = 4
        return character
    if character.race == "Kobol":
        if intelligence < 69:
            character.intelligence_range = 0
            character = determine_r_strength(character, intelligence, 69)
            return character
        if intelligence < 84:
            character.intelligence_range = 1
            return character
        if intelligence < 114:
            character.intelligence_range = 2
            return character
        if intelligence < 129:
            character.intelligence_range = 3
            return character
        character.intelligence_range = 4
        return character
    if character.race == "Ogre":
        if intelligence < 31:
            character.intelligence_range = 0
            character = determine_r_strength(character, intelligence, 31)
            return character
        if intelligence < 46:
            character.intelligence_range = 1
            return character
        if intelligence < 76:
            character.intelligence_range = 2
            return character
        if intelligence < 91:
            character.intelligence_range = 3
            return character
        character.intelligence_range = 4
        return character
    if character.race == "Cliff Ogre":
        if intelligence < 49:
            character.intelligence_range = 0
            character = determine_r_strength(character, intelligence, 49)
            return character
        if intelligence < 64:
            character.intelligence_range = 1
            return character
        if intelligence < 94:
            character.intelligence_range = 2
            return character
        if intelligence < 109:
            character.intelligence_range = 3
            return character
        character.intelligence_range = 4
        return character
    if character.race == "Gruagach Ogre":
        if intelligence < 22:
            character.intelligence_range = 0
            character = determine_r_strength(character, intelligence, 22)
            return character
        if intelligence < 37:
            character.intelligence_range = 1
            return character
        if intelligence < 67:
            character.intelligence_range = 2
            return character
        if intelligence < 82:
            character.intelligence_range = 3
            return character
        character.intelligence_range = 4
        return character
    if character.race == "Kinder-fresser Ogre":
        if intelligence < 41:
            character.intelligence_range = 0
            character = determine_r_strength(character, intelligence, 41)
            return character
        if intelligence < 56:
            character.intelligence_range = 1
            return character
        if intelligence < 86:
            character.intelligence_range = 2
            return character
        if intelligence < 101:
            character.intelligence_range = 3
            return character
        character.intelligence_range = 4
        return character
    if character.race in ["Borbytingarna Troll", "Hill Troll"]:
        if intelligence < 16:
            character.intelligence_range = 0
            character = determine_r_strength(character, intelligence, 16)
            return character
        if intelligence < 31:
            character.intelligence_range = 1
            return character
        if intelligence < 61:
            character.intelligence_range = 2
            return character
        if intelligence < 76:
            character.intelligence_range = 3
            return character
        character.intelligence_range = 4
        return character
    if character.race == "Subterranean Troll":
        if intelligence < 81:
            character.intelligence_range = 0
            character = determine_r_strength(character, intelligence, 81)
            return character
        if intelligence < 96:
            character.intelligence_range = 1
            return character
        if intelligence < 126:
            character.intelligence_range = 2
            return character
        if intelligence < 141:
            character.intelligence_range = 3
            return character
        character.intelligence_range = 4
        return character
