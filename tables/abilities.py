from models.character_models import FatalModel
from dice import d8, d10, d100, d1000
from math import floor, ceil
from tables.ability_tables import (
    skill_modifier,
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
from tables.disposition_tables import lookup_mental_illness

def ability_dice():
    tendhundred = 0
    for _ in range(10):
        tendhundred = tendhundred + d100()
    return floor((tendhundred / 5) - 1)

def calculate_sub_abilities(character: FatalModel):
    character.physical_fitness = character.original_physical_fitness = ability_dice()
    character.strength = character.original_strength = ability_dice()
    character.bodily_attractiveness = character.original_bodily_attractiveness = ability_dice()
    character.health = character.original_health = ability_dice()

    character.facial = character.original_facial = ability_dice()
    character.vocal = character.original_vocal = ability_dice()
    character.kinetic = character.original_kinetic = ability_dice()
    character.rhetorical = character.original_rhetorical = ability_dice()

    character.hand_eye_coordination = character.original_hand_eye_coordination = ability_dice()
    character.agility = character.original_agility = ability_dice()
    character.reaction_speed = character.original_reaction_speed = ability_dice()
    character.ennunciation = character.original_ennunciation = ability_dice()

    character.language = character.original_language = ability_dice()
    character.math = character.original_math = ability_dice()
    character.analytic = character.original_analytic = ability_dice()
    character.spatial = character.original_spatial = ability_dice()

    character.drive = character.original_drive = ability_dice()
    character.intuition = character.original_intuition = ability_dice()
    character.common_sense = character.original_common_sense = ability_dice()
    character.reflection = character.original_reflection = ability_dice()

    return character

def calculate_main_abilities(character: FatalModel):
    character.physique = floor((character.physical_fitness + \
                                character.strength + \
                                character.bodily_attractiveness + \
                                character.health) / 4)
    if character.physique < 1:
        character.physique = 1
    character.physique_modifier = skill_modifier[ceil((character.physique / 6))]

    character.charisma = floor((character.facial + \
                                character.vocal + \
                                character.kinetic + \
                                character.rhetorical) / 4)
    if character.charisma < 1:
        character.charisma = 1
    character.charisma_modifier = skill_modifier[ceil((character.charisma / 6))]
    
    character.dexterity = floor((character.hand_eye_coordination + \
                                character.agility + \
                                character.reaction_speed + \
                                character.ennunciation) / 4)
    if character.dexterity < 1:
        character.dexterity = 1
    character.dexterity_modifer = skill_modifier[ceil((character.dexterity / 6))]

    character.intelligence = floor((character.language + \
                                character.math + \
                                character.analytic + \
                                character.spatial) / 4)
    if character.intelligence < 1:
        character.intelligence = 1
    character.intelligence_modifier = skill_modifier[ceil((character.intelligence / 6))]
    
    character.wisdom = floor((character.drive + \
                                character.intuition + \
                                character.common_sense + \
                                character.reflection) / 4)
    if character.wisdom < 1:
        character.wisdom = 1
    character.wisdom_modifier = skill_modifier[ceil((character.wisdom / 6))]

    return character

def reroll_subability(character: FatalModel, ability_name):
    if character.num_skill_rerolls < 4:
        new_roll = sorted([d100(), d100(), d100(), d100(), d100()])
        new_ability_score = 0
        for v in new_roll[1:]:
            new_ability_score = new_ability_score + v

        new_ability_score = (new_ability_score / 2) + 1

        modifiers = getattr(character, ability_name) + getattr(character, f"original_{ability_name}")
        setattr(character, ability_name, new_ability_score + modifiers)
        character.num_skill_rerolls = character.num_skill_rerolls + 1

        mental_illness_roll = None
        while mental_illness_roll is None:
            mental_illness_roll = d1000()
            if mental_illness_roll == 999:
                mental_illness_roll = None
            if mental_illness_roll == 1000:
                bonus_roll = d1000()
                illness = lookup_mental_illness(bonus_roll)
                if illness[1] and character.gender == illness[1]:
                    character.mental_illnesses.append(illness[0])
                    for mod in illness[2]:
                        setattr(character, mod[0], getattr(character, mod[0] + mod[1]))
                    for mod in illness[3]:
                        setattr(character, mod[0], getattr(character, mod[0]) * mod[1])
        illness = lookup_mental_illness(mental_illness_roll)
        if illness[1] and character.gender == illness[1]:
            character.mental_illnesses.append(illness[0])
            for mod in illness[2]:
                setattr(character, mod[0], getattr(character, mod[0]) + mod[1])
            for mod in illness[3]:
                setattr(character, mod[0], getattr(character, mod[0]) * mod[1])
    
    return character

def apply_subability_modifiers(character: FatalModel):
    if character.physical_fitness < 1:
        character.physical_fitness = 1
    fitness_modifier = skill_modifier[ceil((character.physical_fitness /6))]
    character.physical_fitness_modifier = fitness_modifier
    character.bodily_attractiveness = character.bodily_attractiveness + fitness_modifier
    if character.height < 12:
        height_marker = 0
    else:
        height_marker = floor((character.height - 12) / 12)
    character.sprint = fitness_table[ceil((character.physical_fitness /6))][height_marker]

    if character.strength < 1:
        character.strength = 1
    strength_check = ceil((character.strength /6))
    if strength_check > 200:
        strength_check = 200
    strength_list = strength_table[strength_check]
    character.strength_modifier = strength_list[0]
    # TODO Damage here?
    character.life_points = character.life_points + strength_list[2]
    character.cj = strength_list[3]
    character.bench = strength_list[4]
    character.dl = strength_list[5]

    if character.bodily_attractiveness < 1:
        character.bodily_attractiveness = 1
    character.bodily_attractiveness_modifier = skill_modifier[ceil(character.bodily_attractiveness / 6)]

    if character.health < 1:
        character.health = 1
    health_mod = ceil((character.health /6))
    character.health_modifier = skill_modifier[health_mod]
    character.int_vom = -1 * skill_modifier[health_mod]
    character.life_points = character.life_points + health_table[health_mod][0]
    num_allergies = health_table[health_mod][1]
    for _ in range(num_allergies):
        allergy_roll = d8()
        new_allergy = allergies[allergy_roll]
        if new_allergy in character.allergies:
            num_allergies  = num_allergies + 1
            continue
        character.allergies.append(new_allergy)
    character.illness_immunity = health_table[health_mod][2]

    if character.facial < 1:
        character.facial = 1
    facial_mod = ceil((character.facial /6))
    character.facial_modifier = skill_modifier[facial_mod]
    character.facial_description = facial_descriptions[facial_mod -1]

    if character.vocal < 1:
        character.vocal = 1
    vocal_mod = ceil((character.vocal /6))
    character.vocal_modifier = skill_modifier[vocal_mod]
    character.vocal_description = vocal_descriptions[vocal_mod -1]

    if character.kinetic < 1:
        character.kinetic = 1
    kinetic_mod = ceil((character.kinetic /6))
    character.kinetic_modifier = skill_modifier[kinetic_mod]
    character.kinetic_description = kinetic_descriptions[kinetic_mod -1]

    if character.rhetorical < 1:
        character.rhetorical = 1
    rhetorical_mod = ceil((character.rhetorical /6))
    character.rhetorical_modifier = skill_modifier[rhetorical_mod]
    character.average_speech_rate = average_speech_rate[rhetorical_mod -1]

    if character.hand_eye_coordination < 1:
        character.hand_eye_coordination = 1
    hand_eye_mod = ceil((character.hand_eye_coordination /6))
    character.hand_eye_coordination_modifier = skill_modifier[hand_eye_mod]
    character.finger_movement_precision = finger_precision[hand_eye_mod -1]

    if character.agility < 1:
        character.agility = 1
    agility_mod = ceil((character.agility /6))
    character.agility_modifier = skill_modifier[agility_mod]
    character.current_armor = character.current_armor + agility_table[agility_mod -1][0]
    character.brawling = agility_table[agility_mod -1][1]
    character.stand = agility_table[agility_mod -1][2]

    if character.reaction_speed < 1:
        character.reaction_speed = 1
    reaction_mod = ceil((character.reaction_speed / 6))
    character.reaction_speed_modifier = skill_modifier[reaction_mod]
    character.deep_sleep_recovery = deep_sleep_recovery[reaction_mod -1]

    if character.ennunciation < 1:
        character.ennunciation = 1
    ennunciation_mod = ceil((character.ennunciation / 6))
    character.ennunciation_modifier = skill_modifier[ennunciation_mod]
    character.maximum_speech_rate = enunciation_table[ennunciation_mod][0]
    character.casting = enunciation_table[ennunciation_mod][1]

    if character.language < 1:
        character.language = 1
    language_mod = ceil((character.language / 6))
    character.language_modifier = skill_modifier[language_mod]
    character.max_num_of_languages = language_table[language_mod][0]
    character.vocabulary = language_table[language_mod][1]

    if character.math < 1:
        character.math = 1
    math_mod = ceil((character.math / 6))
    character.math_modifier = skill_modifier[math_mod]
    character.highest_possible_math = math_descriptions[math_mod -1]

    if character.analytic < 1:
        character.analytic = 1
    character.analytic_modifier = skill_modifier[ceil((character.analytic /6))]

    if character.spatial < 1:
        character.spatial = 1
    spatial_mod = ceil((character.spatial / 6))
    character.spatial_modifier = skill_modifier[spatial_mod]
    character.unfamiliar_object_assembly = unfamiliar_object_assembly[spatial_mod -1]

    if character.drive < 1:
        character.drive = 1
    drive_mod = ceil((character.drive / 6))
    character.drive_modifier = skill_modifier[drive_mod]
    character.life_points = character.life_points + drive_table[drive_mod][0]
    character.unconscioness = drive_table[drive_mod][1]
    character.hours_resting = drive_table[drive_mod][2]

    if character.intuition < 1:
        character.intuition = 1
    character.intuition_modifier = skill_modifier[ceil((character.intuition /6))]

    if character.common_sense < 1:
        character.common_sense = 1
    common_sense_mod = ceil((character.common_sense / 6))
    character.common_sense_modifier = skill_modifier[common_sense_mod]
    character.likely_to = common_sense_descriptions[common_sense_mod -1]

    if character.reflection < 1:
        character.reflection = 1
    reflection_mod = ceil((character.reflection / 6))
    character.reflection_modifier = skill_modifier[reflection_mod]
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
    if character.race == "Kobold":
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
