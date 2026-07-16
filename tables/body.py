from models.character_models import FatalModel
from tables.abilities import ability_dice
from tables.body_tables import(
    lifespan_table,
    average_height,
    average_weight,
    bmi_table,
    feature_table,
    skin_color,
    hair_color_1, hair_color_2, hair_color_3,
    hair_type,
    eye_color,
    vision_imparement,
    facial_feature_table,
    areola_diameter,
    areola_hue,
    nipple_length,
    tongue_size,
    circumference,
    cup_size,
    dick_size,
    foot_length,
    head_circumference,
    proportion_1, proportion_2, proportion_3, proportion_4
    )
from math import floor, ceil
from dice import d2, d4, d5, d6, d8, d10, d12, d20, d100, d1000, d1000000
import random


def add_body(character: FatalModel):
    character = generate_age(character)
    character = generate_height(character)
    character = generate_weight(character)
    character = generate_skin_color(character)
    character = generate_hair(character)
    character = generate_eye_color(character)
    character = generate_vision(character)
    character = generate_facial_features(character)
    character = generate_rare_features(character)

    character = apply_age_modifiers(character)
    character = apply_height_modifiers(character)
    character = apply_weight_modifiers(character)
    character = apply_bmi(character)

    character = generate_manhood(character)
    character, size_mod = generate_best_worst_features(character)
    character = generate_sexual_features(character, size_mod)

    character = freak_of_nature(character)

    return character

def get_stage(race: str, age: int) -> str:
    for label, lo, hi in lifespan_table[race]:
        if lo <= age <= hi:
            return label
    return "Venerable"

def generate_age(character: FatalModel):
    # This must be done after determining race
    age_roll = d100() + d100() + d100() + d100()
    if character.race == "Anakim":
        character.age = floor((age_roll / 2.5) - 50)
        character.stage_of_life = get_stage(character.race, character.age)
    if character.race == "Bugbear":
        character.age = floor((age_roll / 3) - 40)
        character.stage_of_life = get_stage(character.race, character.age)
    if character.race in ["Black Dwarf", "Brown Dwarf", "White Dwarf"]:
        character.age = d1000()
        character.stage_of_life = get_stage("Dwarves", character.age)
    if character.race in ["Dark Elf", "Light Elf"]:
        character.stage_of_life = "Young Adult"
        character.age = random.randint(floor(character.elf_lifespan*0.26),
                                       floor(character.elf_lifespan*.4))
    if character.race == "Human":
        character.age = floor((age_roll / 4) - 30)
        character.stage_of_life = get_stage(character.race, character.age)
    if character.race == "Kobold":
        character.age = floor((age_roll / 5) - 25)
        character.stage_of_life = get_stage(character.race, character.age)
    if character.race in ["Ogre", "Cliff Ogre", "Gruagach Ogre", "Kinder-fresser Ogre"]:
        character.age = floor((age_roll / 2) - 55)
        character.stage_of_life = get_stage("Ogres", character.age)
    if character.race in ["Borbytingarna Troll", "Hill Troll", "Subterranean Troll"]:
        character.age = floor((age_roll / 3) - 40)
        character.stage_of_life = get_stage("Trolls", character.age)
    
    return character

def apply_age_modifiers(character: FatalModel):
    # This must be done after Height, Weight, Hair Color, Foot Size, and Head Circumference are generated

    hair_length_roll = d100()
    if character.age == 0:
        character.height = floor(character.height * 0.2)
        character.weight = floor(character.weight * 0.05)
        hair_length_roll = hair_length_roll - 90
        feet = character.foot_size.split(' ')[0].split('-')
        character.foot_size = f"{floor(int(feet[0])* 0.2)}-{floor(int(feet[1])*0.2)} inches"
        character.head_circumference = floor(character.head_circumference * 0.55)
        return character

    if character.stage_of_life == "Infant":
        character.height = floor(character.height * 0.4)
        character.weight = floor(character.weight * 0.4)
        hair_length_roll = hair_length_roll - 70
        feet = character.foot_size.split(' ')[0].split('-')
        character.foot_size = f"{floor(int(feet[0])* 0.4)}-{floor(int(feet[1])*0.4)} inches"
        character.head_circumference = floor(character.head_circumference * 0.7)

    elif character.stage_of_life == "Child":
        character.height = floor(character.height * 0.8)
        character.weight = floor(character.weight * 0.6)
        hair_length_roll = hair_length_roll - 50
        feet = character.foot_size.split(' ')[0].split('-')
        character.foot_size = f"{floor(int(feet[0])* 0.8)}-{floor(int(feet[1])*0.8)} inches"
        character.head_circumference = floor(character.head_circumference * 0.85)

    elif character.stage_of_life == "Puberty":
        character.height = floor(character.height * 0.9)
        character.weight = floor(character.weight * 0.8)

    elif character.stage_of_life == "Middle Age":
        character.height = floor(character.height * 0.99)
        character.weight = floor(character.weight * 1.1)
        character.hair_color = character.hair_color + "w/ some Gray"

    elif character.stage_of_life == "Old Age":
        character.height = floor(character.height * 0.98)
        character.weight = floor(character.weight * 1.1)
        character.hair_color = "Gray"

    elif character.stage_of_life == "Venerable":
        character.height = floor(character.height * 0.97)
        character.weight = floor(character.weight * 1.1)
        character.hair_color = "White"

    if character.race == "Bugbear":
        character.hair_length = f"fur {d6()}” long"
    else:
        if hair_length_roll < 11:
            character.hair_length = "4” or neck length"
        elif hair_length_roll < 30:
            character.hair_length = "4-8” or shoulder length"
        elif hair_length_roll < 51:
            character.hair_length = "9-16” or upper back"
        elif hair_length_roll < 81:
            character.hair_length = "17-22” or middle of the back"
        elif hair_length_roll < 98:
            character.hair_length = "23-30” or lower back"
        elif hair_length_roll < 100:
            character.hair_length = "31-38” or rump-length"
        elif hair_length_roll == 100:
            character.hair_length = "39-50” or thigh length"

    return character
    
def generate_height(character: FatalModel):
    if character.race == "Anakim":
        if character.gender == "male":
            character.height = d20() + d20() + 76
        elif character.gender == "female":
            character.height = d10() + d10() + d10() + d10() + 68
        character.breadth = floor(character.height / 2)
    elif character.race == "Bugbear":
        if character.gender == "male":
            character.height = d8() + d8() + d8() + d8() + d8() + d8() + 57
        elif character.gender == "female":
            character.height = d6() + d6() + d6() + d6() + d6() + d6() + d6() + d6() + 50
        character.breadth = floor(character.height / 2)
    elif character.race in ["Black Dwarf", "Brown Dwarf", "White Dwarf"]:
        if character.gender == "male":
            character.height = d6() + d6() + d6() + d6() + d6() + d6() + 27
        elif character.gender == "female":
            character.height = d4() + d4() + d4() + d4() + d4() + d4() + d4() + d4() + 27
        character.breadth = floor(character.height * 0.6)
    elif character.race in ["Dark Elf", "Light Elf"]:
        character.height = d4() + d4() + d4() + d4() + d4() + d4() + 33
        character.breadth = floor(character.height / 2)
    elif character.race == "Human":
        if character.gender == "male":
            character.height = d6() + d6() + d6() + d6() + d6() + d6() + 49
        elif character.gender == "female":
            character.height =  d4() + d4() + d4() + d4() + d4() + d4() + d4() + d4() + 44
        character.breadth = floor(character.height / 2)
    elif character.race == "Kobold":
        if character.gender == "male":
            character.height = d6() + d6() + d6() + d6() + d6() + d6() + 33
        elif character.gender == "female":
            character.height =  d4() + d4() + d4() + d4() + d4() + d4() + 36
        character.breadth = floor(character.height / 2)
    elif character.race in ["Ogre", "Cliff Ogre", "Gruagach Ogre", "Kinder-fresser Ogre"]:
        if character.gender == "male":
            character.height = d8() + d8() + d8() + d8() + d8() + d8() + 81
        elif character.gender == "female":
            character.height = d6() + d6() + d6() + d6() + d6() + d6() + d6() + d6() + 68
        character.breadth = floor(character.height * 0.45)
    elif character.race in ["Borbytingarna Troll", "Hill Troll", "Subterranean Troll"]:
        if character.gender == "male":
            character.height = d8() + d8() + d8() + d8() + d8() + d8() + 69
        elif character.gender == "female":
            character.height = d6() + d6() + d6() + d6() + d6() + d6() + d6() + d6() + 68
        character.breadth = floor(character.height * 0.6)
    return character

def apply_height_modifiers(character: FatalModel):
    height_mods = average_height[character.race][character.gender]
    average = height_mods[0]

    difference = 0
    if character.height > average:
        difference = character.height - average
    elif character.height < average:
        difference = average - character.height

    character.weight = character.weight + difference * height_mods[1][0]
    character.strength = character.strength + difference * height_mods[1][1]

    if character.gender == "male":
        character.bodily_attractiveness = character.bodily_attractiveness + difference * height_mods[1][2]
    
    return character

def generate_weight(character: FatalModel):
    if character.race == "Anakim":
        if character.gender == "male":
            character.weight = d100() + d100() + d100() + 249
        elif character.gender == "female":
            character.weight = d100() + d100() + 99
    elif character.race == "Bugbear":
        if character.gender == "male":
            character.weight = d100() + d100()+ 199
        elif character.gender == "female":
            character.weight = d100() + 200
    elif character.race in ["Black Dwarf", "Brown Dwarf", "White Dwarf"]:
        if character.gender == "male":
            character.weight = d10() + d10() + d10() + d10() + 78
        elif character.gender == "female":
            character.weight = d6() + d6() + d6() + d6() + d6() + d6() + 69
    elif character.race in ["Dark Elf", "Light Elf"]:
        if character.gender == "male":
            character.weight = d6() + d6() + 53
        elif character.gender == "female":
            character.weight = d4() + d4() + 50
    elif character.race == "Human":
        if character.gender == "male":
            character.weight = d20() + d20() + d20() + d20() + d20() + d20() + 87
        elif character.gender == "female":
            character.weight =  d12() + d12() + d12() + d12() + d12() + d12() + 76
    elif character.race == "Kobold":
        if character.gender == "male":
            character.weight = d6() + d6() + d6() + 70
        elif character.gender == "female":
            character.weight =  d6() + d6() + 63
    elif character.race in ["Ogre", "Cliff Ogre", "Gruagach Ogre", "Kinder-fresser Ogre", "Hill Troll"]:
        if character.gender == "male":
            character.weight = d100() + d100() + d100() + 499
        elif character.gender == "female":
            character.weight = d100() + d100() + 399
    elif character.race in ["Borbytingarna Troll", "Subterranean Troll"]:
        if character.gender == "male":
            character.weight = d20() + d20() + d20() + d20() + d20() + d20() + 187
        elif character.gender == "female":
            character.weight = d12() + d12() + d12() + d12() + d12() + d12() + 211

    return character

def apply_weight_modifiers(character: FatalModel):
    average = average_weight[character.race][character.gender]

    if character.weight > average:
        character.strength = character.strength + (character.weight - average)
    elif character.weight < average:
        character.strength = character.strength - (average - character.weight)
    return character

def apply_bmi(character: FatalModel):
    bmi = (character.weight / (character.height**2) * 705)
    bmi_bounds = bmi_table[character.race][character.gender]

    if bmi < bmi_bounds[0][0]:
        #underweight
        difference = floor((bmi_bounds[0][0] - bmi) / bmi_bounds[1][0])
        character.bodily_attractiveness = character.bodily_attractiveness + difference * bmi_bounds[1][1]
        character.is_skinny = True
    elif bmi > bmi_bounds[0][1]:
        #overweight
        difference = floor((bmi - bmi_bounds[0][1]) / bmi_bounds[2][0])
        character.bodily_attractiveness = character.bodily_attractiveness + difference * bmi_bounds[2][1]
        character.is_fat = True
    
    return character

def generate_best_worst_features(character: FatalModel):
    # This must be done before cup_size and manhood length
    cup_size_mod = None

    most_attractive = random.choices(
        population=list(feature_table.keys()),
        weights=[15, 10, 5, 5, 15, 5, 10, 10, 10, 5, 5, 5],
        k=1
    )[0]
    character.most_attractive_feature = most_attractive
    setattr(character,
            feature_table[most_attractive],
            (getattr(character,
                     feature_table[most_attractive]) + d10()))
    if character.gender == "male" and most_attractive == "Crotch":
        character.manhood_length = floor(character.manhood_length * float(f"1.{(d10()):02d}"))
    if character.gender == "female" and most_attractive == "Chest":
        cup_size_mod = d10()

    least_attractive = None
    while not least_attractive: 
        least_attractive = random.choices(
            population=list(feature_table.keys()),
            weights=[15, 10, 5, 5, 15, 5, 10, 10, 10, 5, 5, 5],
            k=1
        )[0]
        if least_attractive == most_attractive:
            least_attractive = None
    character.most_repulsive_feature = least_attractive
    setattr(character,
            feature_table[least_attractive],
            (getattr(character,
                     feature_table[least_attractive]) - d10()))
    if character.gender == "male" and least_attractive == "Crotch":
        character.manhood_length = floor(character.manhood_length * float(f"0.{(100 - d10()):02d}"))
    if character.gender == "female" and least_attractive == "Chest":
        cup_size_mod = -1* d10()
    
    return character, cup_size_mod

def generate_skin_color(character: FatalModel):
    color_mod = skin_color[character.race]

    if isinstance(color_mod, str):
        character.skin_color = color_mod
    else:
        color_roll = d100()
        if isinstance(color_mod, int):
            color_roll = color_roll + color_mod

        if color_roll < 6:
            character.skin_color = "Deathly Pale (many think they are undead)"
        elif color_roll >= 6 and color_roll < 16:
            character.skin_color = "Pale (obviously, they rarely go outdoors)"
        elif color_roll >= 16 and color_roll < 36:
            character.skin_color = "Light or fair"
        elif color_roll >= 36 and color_roll < 61:
            character.skin_color = "Medium"
        else:
            character.skin_color = "Tan (the skin of a laborer)"
    
    return character

def generate_hair(character: FatalModel):
    # Hair color
    if character.race == "Gruagach Ogre":
        character.hair_color = "Blonde"
    elif character.race in ["Anakim", "Human", "Kobold", "Ogre", "Cliff Ogre", "Kinder-fresser Ogre"]:
        character.hair_color = random.choices(
            population=list(hair_color_1.keys()),
            weights=list(hair_color_1.values()),
            k=1
        )[0]
    elif character.race in ["Bugbear", "Black Dwarf", "Brown Dwarf", "White Dwarf", "Dark Elf", "Borbytingarna Troll", "Hill Troll", "Subterranean Troll"]:
        character.hair_color = random.choices(
            population=list(hair_color_2.keys()),
            weights=list(hair_color_2.values()),
            k=1
        )[0]
    elif character.race == "Light Elf":
        character.hair_color = random.choices(
            population=list(hair_color_3.keys()),
            weights=list(hair_color_3.values()),
            k=1
        )[0]
            
    # Hair type
    type_roll = d100()
    if character.gender == "female":
        type_roll = type_roll + 8
    if character.race in ['Bugbear', 'Black Dwarf', 'Brown Dwarf', 'White Dwarf', 'Kobold', 'Ogre', 'Cliff Ogre', "Gruagach Ogre", "Kinder-fresser Ogre"]:
        type_roll = type_roll + 10
    if character.race in ["Borbytingarna Troll", "Hill Troll", "Subterranean Troll"]:
        type_roll = type_roll + 30
    if character.stage_of_life == "Infant":
        type_roll = type_roll - 74
    
    if type_roll < 1:
        type_roll = 1
    if type_roll > 100:
        type_roll = 100
    
    character.hair_type = hair_type[type_roll][0]
    character.hair_thickness = hair_type[type_roll][1]
    character.facial = character.facial + hair_type[type_roll][2]

    return character

def generate_eye_color(character: FatalModel):
    character.eyes = random.choices(
            population=eye_color[character.race],
            weights=[5, 65, 10, 19, 1],
            k=1
        )[0]
    return character

def generate_vision(character: FatalModel):
    vision_roll = d100()
    if vision_roll <26:
        character.vision = "Near-sightedness"
    elif vision_roll >= 26 and vision_roll < 76:
        character.vision = "Perfect natural Vision"
    elif vision_roll >= 76:
        character.vision = "Far-sightedness"
    
    if character.vision == "Near-sightedness":
        character.aim.skill_modifier = character.aim.skill_modifier + vision_imparement[vision_roll]
        character.hurl.skill_modifier = character.hurl.skill_modifier + vision_imparement[vision_roll]
        character.mounted_archery.skill_modifier = character.mounted_archery.skill_modifier + vision_imparement[vision_roll]
        character.search.skill_modifier = character.search.skill_modifier + vision_imparement[vision_roll]
        character.sight.skill_modifier = character.sight.skill_modifier + vision_imparement[vision_roll]

    return character

def generate_facial_features(character: FatalModel):
    facial_roll = d100()

    character.facial_feature = facial_feature_table[facial_roll][0]
    character.appearance = facial_feature_table[facial_roll][1]

    modifier = facial_feature_table[facial_roll][2]
    if isinstance(modifier, list):
        for mod in modifier:
            if character.gender == mod[0]:
                character.facial = character.facial - mod[1]
    else:
        character.facial = character.facial + modifier
    
    return character

def freak_of_nature(character: FatalModel):
    # This must be done before applying gender modifiers
    roll = d1000000()

    if roll == 1:
        freak_roll = d5()
        if freak_roll == 1:
            character.traits.append("Funnel Chest (Pectus Excavatum)")
            character.strength = character.strength * (-1 * d10())
            character.bodily_attractiveness = character.bodily_attractiveness - d10()
        elif freak_roll == 2:
            character.traits.append("Hermaphrodite")
            character.bodily_attractiveness = character.bodily_attractiveness - d10()
        elif freak_roll == 3:
            character.traits.append("Pidgeon Chest (Pectus Carinatum)")
            character.strength = character.strength * (-1 * d10())
        elif freak_roll == 4:
            character.traits.append("Polydactyly")
            character.hand_eye_coordination = character.hand_eye_coordination + d10()
        elif freak_roll == 5:
            character.traits.append("Supermumerary Nipple")
            character.bodily_attractiveness = character.bodily_attractiveness - d10()

    return character

def generate_sexual_features(character: FatalModel, size_mod: int = None):
    # Must be done after bmi
    areola_diameter_roll = d100()
    if character.gender == "male":
        areola_diameter_roll = areola_diameter_roll - 15
    if character.stage_of_life in ["Infant", "Child"]:
        areola_diameter_roll = areola_diameter_roll - 30
    if areola_diameter_roll < 1:
        areola_diameter_roll = 1
    
    if areola_diameter_roll >= 86 and areola_diameter_roll < 96:
        character.bodily_attractiveness = character.bodily_attractiveness - d4()
    if areola_diameter_roll >= 96:
        character.bodily_attractiveness = character.bodily_attractiveness - d6()

    character.areola_diameter = areola_diameter[character.race][ceil(areola_diameter_roll / 5)]

    character.areola_hue = random.choices(
        population=list(areola_hue.keys()),
        weights=list(areola_hue.values()),
        k=1
    )[0]

    if character.gender == "female" and character.areola_hue == "Difficult to identify":
        character.bodily_attractiveness = character.bodily_attractiveness - d6()
    if character.gender == "female" and character.areola_hue == "Medium":
        character.bodily_attractiveness = character.bodily_attractiveness + d4()
    if character.gender == "female" and character.areola_hue == "Dark":
        character.bodily_attractiveness = character.bodily_attractiveness - d4()
    
    inverted_roll = d100()
    if inverted_roll == 1:
        double_inversion = d100()
        if double_inversion < 81:
            character.traits.append("Both nipples inverted")
        if double_inversion >= 81 and double_inversion < 91:
            character.traits.append("Left nipple inverted")
        if double_inversion >= 91:
            character.traits.append("Right nipple inverted")
    else:
        nipple_roll = d100()
        if character.gender == "male":
            nipple_roll = nipple_roll - 15
        if character.stage_of_life in ["Infant", "Child"]:
            nipple_roll = nipple_roll - 50
        
        if nipple_roll < 66:
            character.nipple_length = nipple_length[character.race][0]
            if character.gender == "female":
                character.bodily_attractiveness = character.bodily_attractiveness - d4()
        if 66 <= nipple_roll < 81:
            character.nipple_length = nipple_length[character.race][1]
        if 81 <= nipple_roll < 98:
            character.nipple_length = nipple_length[character.race][2]
            if character.gender == "female":
                character.bodily_attractiveness = character.bodily_attractiveness + d4()
        if 98 <= nipple_roll < 100:
            character.nipple_length = nipple_length[character.race][3]
            if character.gender == "female":
                character.bodily_attractiveness = character.bodily_attractiveness - d6()
        if nipple_roll == 100:
            character.nipple_length = nipple_length[character.race][4]
            if character.gender == "female":
                character.bodily_attractiveness = character.bodily_attractiveness - d6()

    tongue_roll = d100()
    if character.stage_of_life == "Infant":
        tongue_roll = tongue_roll - 80
    if character.stage_of_life == "Child":
        tongue_roll = tongue_roll - 60
    
    if tongue_roll < 1:
        tongue_roll = 1

    if tongue_roll > 98:
        character.tongue_size = tongue_size[character.race][11]
    else:
        character.tongue_size = tongue_size[character.race][ceil(tongue_roll / 10)]

    anal_circ_roll = d100()
    if character.stage_of_life == "Infant":
        anal_circ_roll = anal_circ_roll - 90
    if character.stage_of_life == "Child":
        anal_circ_roll = anal_circ_roll - 80
    if character.stage_of_life == "Puberty":
        anal_circ_roll = anal_circ_roll - 25
    if character.stage_of_life == "Middle Age":
        anal_circ_roll = anal_circ_roll + 10
    if character.stage_of_life in ["Old Age", "Venerable"]:
        anal_circ_roll = anal_circ_roll + 5
    if character.gender == "male":
        anal_circ_roll = anal_circ_roll + 5
    if "Nymphomaniac" in character.traits:
        anal_circ_roll = anal_circ_roll + (d20() + 10)
    if "Satyromaniac" in character.traits:
        anal_circ_roll = anal_circ_roll + (d20() + 10)
    
    if anal_circ_roll < 1:
        anal_circ_roll = 1
    if anal_circ_roll > 100:
        anal_circ_roll = 100

    if anal_circ_roll > 98:
        character.anal_circumference_potential = circumference[character.race][11]
    else:
        character.anal_circumference_potential = circumference[character.race][ceil(anal_circ_roll / 10)]

    depth_percent = d20() + d20() + d20()
    character.anal_depth_potential = (character.height / 12) * float(f"0.{depth_percent:02d}")

    if character.gender == "female":
        cup_size_roll = d100()
        if size_mod:
            cup_size_roll = cup_size_roll + size_mod
        if character.stage_of_life in ["Infant", "Child"]:
            cup_size_roll = cup_size_roll - 75
        if character.stage_of_life == "Puberty":
            cup_size_roll = cup_size_roll - 5
        if character.is_fat:
            cup_size_roll = cup_size_roll + 25
        if character.is_pregnant:
            cup_size_roll = cup_size_roll + 25
        if character.is_skinny:
            cup_size_roll = cup_size_roll - 25
        
        if cup_size_roll < 1:
            cup_size_roll = 1
        if cup_size_roll > 100:
            cup_size_roll = 100
        
        character.cup_size = cup_size[cup_size_roll][0]
        character.bodily_attractiveness = character.bodily_attractiveness + cup_size[cup_size_roll][1]

        vag_circ_roll = d100()
        if character.stage_of_life == "Infant":
            vag_circ_roll = vag_circ_roll - 95
        if character.stage_of_life == "Child":
            vag_circ_roll = vag_circ_roll - 85
        if character.stage_of_life == "Puberty":
            vag_circ_roll = vag_circ_roll - 25
        if character.stage_of_life == "Middle Age":
            vag_circ_roll = vag_circ_roll + 10
        if character.stage_of_life in ["Old Age", "Venerable"]:
            vag_circ_roll = vag_circ_roll + 5
        if character.is_parent:
            vag_circ_roll = vag_circ_roll + (d20() + 5)
        if "Nymphomaniac" in character.traits:
            vag_circ_roll = vag_circ_roll + (d20() + 10)
        
        if vag_circ_roll < 1:
            vag_circ_roll = 1
        if vag_circ_roll > 100:
            vag_circ_roll = 100

        if vag_circ_roll > 98:
            character.vaginal_circumference_potential = circumference[character.race][11]
        else:
            character.vaginal_circumference_potential = circumference[character.race][ceil(anal_circ_roll / 10)]

        depth_percent = d20() + d20()
        character.vaginal_depth_potential = ((character.height / 12)* float(f"0.{depth_percent:02d}"))

        character.hymen_resistance = d20() + d20() +d20() + d20() + d20()

        character.base_odds_of_orgasm = d100()

    return character

def generate_manhood(character: FatalModel):
    if character.gender == "male":
        length_roll = ability_dice()
        circ_roll = ability_dice()
        character.manhood_length = ((character.height / 12) * dick_size[length_roll])
        character.manhood_circumference = (character.manhood_length * 0.85 * dick_size[circ_roll])

    return character

def generate_rare_features(character: FatalModel):
    # This must be done after generating height

    height_mods = average_height[character.race][character.gender]
    average = height_mods[0]

    foot_roll = d100()
    if character.height > average:
        difference = character.height - average
        foot_roll = foot_roll + (difference* 10)
    elif character.height < average:
        difference = average - character.height
        foot_roll = foot_roll - (difference * 10)

    if foot_roll < 1:
        foot_roll = 1

    if foot_roll > 98:
        character.foot_size = foot_length[character.race][character.gender][11]
    else:
        character.foot_size = foot_length[character.race][character.gender][ceil(foot_roll / 10)]

    character.fist_circumference = character.foot_size

    handed_roll = d100()
    if handed_roll < 11:
        character.handedness = "Left-handed"
    else:
        character.handedness = "Right-handed"

    head_roll = d100()
    head_circ = head_circumference[character.race][head_roll]

    if character.gender == "female":
        head_circ = head_circ * 0.97
    
    head_mod = (d100() / 100)
    dirction = d2()
    if dirction == 1:
        character.head_circumference = head_circ - head_mod
    elif dirction == 2:
        character.head_circumference = head_circ + head_mod
    
    return character

def generate_bpp(character: FatalModel):
    if character.race in ["Anakim", "Bugbear", "Dark Elf", "Light Elf", "Human", "Kobold"]:
        proportion_table = proportion_1
    if character.race in ["Black Dwarf", "Brown Dwarf", "White Dwarf", "Ogre", "Cliff Ogre", "Gruagach Ogre", "Kinder-fresser Ogre"]:
        proportion_table = proportion_2
    if character.race in ["Borbytingarna Troll", "Subterranean Troll"]:
        proportion_table = proportion_3
    if character.race == "Hill Troll":
        proportion_table = proportion_4
    
    character.head.bpp = floor(character.life_points * proportion_table["Head"]) if floor(character.life_points * proportion_table["Head"]) >= 1 else 1
    character.face.bpp = floor(character.life_points * proportion_table["Face"]) if floor(character.life_points * proportion_table["Face"]) >= 1 else 1
    character.upper_torso.bpp = floor(character.life_points * proportion_table["Upper Torso"]) if floor(character.life_points * proportion_table["Upper Torso"]) >= 1 else 1
    character.lower_torso.bpp = floor(character.life_points * proportion_table["Lower Torso"]) if floor(character.life_points * proportion_table["Lower Torso"]) >= 1 else 1
    character.groin.bpp = floor(character.life_points * proportion_table["Groin"]) if floor(character.life_points * proportion_table["Groin"]) >= 1 else 1
    character.upper_right_arm.bpp = floor(character.life_points * proportion_table["Upper Right Arm"]) if floor(character.life_points * proportion_table["Upper Right Arm"]) >= 1 else 1
    character.lower_right_arm.bpp = floor(character.life_points * proportion_table["Lower Right Arm"]) if floor(character.life_points * proportion_table["Lower Right Arm"]) >= 1 else 1
    character.right_hand.bpp = floor(character.life_points * proportion_table["Right Hand"]) if floor(character.life_points * proportion_table["Right Hand"]) >= 1 else 1
    character.upper_left_arm.bpp = floor(character.life_points * proportion_table["Upper Left Arm"]) if floor(character.life_points * proportion_table["Upper Left Arm"]) >= 1 else 1
    character.lower_left_arm.bpp = floor(character.life_points * proportion_table["Lower Left Arm"]) if floor(character.life_points * proportion_table["Lower Left Arm"]) >= 1 else 1
    character.left_hand.bpp = floor(character.life_points * proportion_table["Left Hand"]) if floor(character.life_points * proportion_table["Left Hand"]) >= 1 else 1
    character.upper_right_leg.bpp = floor(character.life_points * proportion_table["Upper Right Leg"]) if floor(character.life_points * proportion_table["Upper Right Leg"]) >= 1 else 1
    character.lower_right_leg.bpp = floor(character.life_points * proportion_table["Lower Right Leg"]) if floor(character.life_points * proportion_table["Lower Right Leg"]) >= 1 else 1
    character.right_foot.bpp = floor(character.life_points * proportion_table["Right Foot"]) if floor(character.life_points * proportion_table["Right Foot"]) >= 1 else 1
    character.upper_left_leg.bpp = floor(character.life_points * proportion_table["Upper Left Leg"]) if floor(character.life_points * proportion_table["Upper Left Leg"]) >= 1 else 1
    character.lower_left_leg.bpp = floor(character.life_points * proportion_table["Lower Left Leg"]) if floor(character.life_points * proportion_table["Lower Left Leg"]) >= 1 else 1
    character.left_foot.bpp = floor(character.life_points * proportion_table["Left Foot"]) if floor(character.life_points * proportion_table["Left Foot"]) >= 1 else 1

    return character
