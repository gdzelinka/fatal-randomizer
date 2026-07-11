from models.character_models import FatalModel
from body_tables import(
    lifespan_table,
    average_height,
    average_weight,
    bmi_table,
    feature_table,
    skin_color,
    hair_color_1, hair_color_2, hair_color_3,
    hair_length,
    hair_type,
    eye_color
    )
from math import floor
from dice import d4, d6, d8, d10, d12, d20, d100, d1000
import random

def get_stage(race: str, age: int) -> str:
    for label, lo, hi in lifespan_table[race]:
        if lo <= age <= hi:
            return label
    raise ValueError("Age out of range")


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
        character.stage_of_life = get_stage(character.race, character.age)
    if character.race in ["Dark Elf", "Light Elf"]:
        character.part_of_life = "Young Adulthood"
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
        character.stage_of_life = get_stage(character.race, character.age)
    if character.race in ["Borbytingarna Troll", "Hill Troll", "Subterranean Troll"]:
        character.age = floor((age_roll / 3) - 40)
        character.stage_of_life = get_stage(character.race, character.age)
    
    return character


def apply_age_modifiers(character: FatalModel):
    # This must be done after Height, Weight, Hair Color, Hair Length, Foot Size, and Head Circumference are generated
    if character.age == 0:
        character.height = floor(character.height * 0.2)
        character.weight = floor(character.weight * 0.05)
        character.hair_length = 0 if character.hair_length < 90 else character.hair_length - 90
        character.foot_size = floor(character.foot_size * 0.2)
        character.head_circumference = floor(character.head_circumference * 0.55)
        return character
    if character.stage_of_life == "Infant":
        character.height = floor(character.height * 0.4)
        character.weight = floor(character.weight * 0.4)
        character.hair_length = 0 if character.hair_length < 70 else character.hair_length - 70
        character.foot_size = floor(character.foot_size * 0.4)
        character.head_circumference = floor(character.head_circumference * 0.7)
        return character
    elif character.stage_of_life == "Child":
        character.height = floor(character.height * 0.8)
        character.weight = floor(character.weight * 0.6)
        character.hair_length = 0 if character.hair_length < 50 else character.hair_length - 50
        character.foot_size = floor(character.foot_size * 0.8)
        character.head_circumference = floor(character.head_circumference * 0.85)
        return character
    elif character.stage_of_life == "Puberty":
        character.height = floor(character.height * 0.9)
        character.weight = floor(character.weight * 0.8)
        return character
    elif character.stage_of_life == "Middle Age":
        character.height = floor(character.height * 0.99)
        character.weight = floor(character.weight * 1.1)
        character.hair_color += "w/ some Gray"
        return character
    elif character.stage_of_life == "Old Age":
        character.height = floor(character.height * 0.98)
        character.weight = floor(character.weight * 1.1)
        character.hair_color = "Gray"
        return character
    elif character.stage_of_life == "Venerable":
        character.height = floor(character.height * 0.97)
        character.weight = floor(character.weight * 1.1)
        character.hair_color = "White"
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

    if character.height > average:
        difference = character.height - average
    elif character.height < average:
        difference = average - character.height

    character.weight += difference * height_mods[1][0]
    character.strength += difference * height_mods[1][1]

    if character.gender == "male":
        character.bodily_attractiveness += difference * height_mods[1][2]
    
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
        character.strength += (character.weight - average)
    elif character.weight < average:
        character.strength -= (average - character.weight)
    return character

def apply_bmi(character: FatalModel):
    bmi = (character.weight / (character.height**2) * 705)
    bmi_bounds = bmi_table[character.race][character.gender]

    if bmi < bmi_bounds[0][0]:
        #underweight
        difference = floor((bmi_bounds[0][0] - bmi) / bmi_bounds[1][0])
        character.bodily_attractiveness += difference * bmi_bounds[1][1]
    elif bmi > bmi_bounds[0][1]:
        #overweight
        difference = floor((bmi - bmi_bounds[0][1]) / bmi_bounds[2][0])
        character.bodily_attractiveness += difference * bmi_bounds[2][1]
    
    return character

def generate_features(character: FatalModel):
    # This must be done after cupsize and manhood length
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
        character.cup_size += d10()

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
        character.cup_size -= d10()
    
    return character

def generate_skin_color(character: FatalModel):
    color_mod = skin_color[character.race]

    if isinstance(color_mod, "str"):
        character.skin_color = color_mod
    else:
        color_roll = d100()
        if isinstance(color_mod, "int"):
            color_roll += color_mod

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

    # Hair length
    if character.race == "Bugbear":
        character.hair_length = f"fur {d6()}” long"
    else:
        character.hair_length = random.choices(
            population=list(hair_length.keys()),
            weights=list(hair_length.values()),
            k=1
        )[0]
            
    # Hair type
    type_roll = d100()
    if character.gender == "female":
        type_roll += 8
    if character.race in ['Bugbear', 'Black Dwarf', 'Brown Dwarf', 'White Dwarf', 'Kobold', 'Ogre', 'Cliff Ogre', "Gruagach Ogre", "Kinder-fresser Ogre"]:
        type_roll += 10
    if character.race in ["Borbytingarna Troll", "Hill Troll", "Subterranean Troll"]:
        type_roll += 30
    if character.stage_of_life == "Infant":
        type_roll -= 74
    
    if type_roll < 1:
        type_roll = 1
    if type_roll > 100:
        type_roll = 100
    
    character.hair_type = hair_type[type_roll][0]
    character.hair_thickness = hair_type[type_roll][1]
    character.facial += hair_type[type_roll][2]

    return character

def generate_eye_color(character: FatalModel):
    character.eyes = random.choices(
            population=eye_color[character.race].keys(),
            weights=[5, 65, 10, 19, 1],
            k=1
        )[0]
    return character

def generate_vision(character: FatalModel):

