import random
from math import sqrt, floor, ceil
from models.character_models import FatalModel, ItemModel, SkillModel
from dice import d3, d12, d13, d20, d96, d100, d1000
from tables.body_tables import lifespan_table
from tables.weapons import weapons_table, update_weapon
from tables.abilities import reroll_subability
from tables.ability_tables import sub_abilities
from tables.occupation_tables import lookup_occupation_requirements, age_started_working
from tables.skill_tables import skill_prerequisites_table
from tables.society_tables import(
    lookup_race_social_class,
    lookup_social_status_birthplace,
    sibling_table,
    marital_table,
    lookup_social_status_occupation,
    lookup_slave_occupation,
    skill_points_table
)
from tables.names import (
    lookup_anakim_human_male_first_name,
    lookup_anakim_human_last_name,
    anakim_human_female_first_name_table,
    lookup_kobold_male_name,
    lookup_kobold_female_name,
    lookup_elven_male_name,
    elven_female_name_table,
    lookup_subterranean_troll_male_name,
    lookup_subterranean_troll_female_name,
    dwarven_male_name_table,
    dwarven_female_name_table,
    bugbear_male_name_prefix_table,
    bugbear_male_name_suffix_table,
    bugbear_female_name_prefix_table,
    bugbear_female_name_suffix_table,
    base_ogre_male_nickname_prefix_table,
    base_ogre_male_nickname_suffix_table,
    borb_hill_troll_male_nickname_prefix_table,
    borb_hill_troll_male_nickname_suffix_table,
    cliff_ogre_male_nickname_prefix_table,
    cliff_ogre_male_nickname_suffix_table,
    gruagach_male_nickname_prefix_table,
    gruagach_male_nickname_suffix_table,
    kinder_fresser_male_nickname_prefix_table,
    kinder_fresser_male_nickname_suffix_table
)

def add_society(character: FatalModel):
    character = generate_name(character)
    character = generate_birth(character)

    if character.race not in ["Dark Elf", "Light Elf"]:
         if character.age > age_started_working[character.race]:
             character = generate_occupation(character)
    else:
        character = generate_occupation(character)

    character = generate_skills(character)

    return character

def generate_name(character: FatalModel):
    if character.race in ["Anakim", "Human"]:
        last_name = lookup_anakim_human_last_name(d1000())
        if character.gender == "male":
            first_name = lookup_anakim_human_male_first_name(d1000())
        elif character.gender == "female":
            first_name = anakim_human_female_first_name_table[d100()]
        character.character_name = f"{first_name} {last_name}"
    
    elif character.race == "Bugbear":
        if character.gender == "male":
            prefix = bugbear_male_name_prefix_table[d100()]
            suffix = bugbear_male_name_suffix_table[d100()]
        elif character.gender == "female":
            prefix = bugbear_female_name_prefix_table[d100()]
            suffix = bugbear_female_name_suffix_table[d100()]
        character.character_name = f"{prefix}-{suffix}"
    
    elif character.race in ["Black Dwarf", "Brown Dwarf", "White Dwarf"]:
        if character.gender == "male":
            character.character_name = dwarven_male_name_table[d96()]
        elif character.gender == "female":
            character.character_name = dwarven_female_name_table[d100()]
    
    elif character.race in ["Dark Elf", "Light Elf"]:
        if character.gender == "male":
            character.character_name = lookup_elven_male_name(d1000())
        elif character.gender == "female":
            character.character_name = elven_female_name_table[d100()]

    elif character.race == "Kobold":
        if character.gender == "male":
            character.character_name = lookup_kobold_male_name(d1000())
        elif character.gender =="female":
            character.character_name = lookup_kobold_female_name(d1000())
    
    elif character.race == "Ogre":
        prefix = base_ogre_male_nickname_prefix_table[d100()]
        suffix = base_ogre_male_nickname_suffix_table[d100()]
        character.character_name = prefix + suffix
    
    elif character.race == "Cliff Ogre":
        prefix = cliff_ogre_male_nickname_prefix_table[d100()]
        suffix = cliff_ogre_male_nickname_suffix_table[d100()]
        character.character_name = prefix + suffix
    
    elif character.race == "Gruagach Ogre":
        prefix = gruagach_male_nickname_prefix_table[d100()]
        suffix = gruagach_male_nickname_suffix_table[d100()]
        character.character_name = prefix + suffix
    
    elif character.race == "Kinder-Fresser Ogre":
        prefix = kinder_fresser_male_nickname_prefix_table[d100()]
        suffix = kinder_fresser_male_nickname_suffix_table[d100()]
        character.character_name = prefix + suffix
    
    elif character.race in ["Borbytingarna Troll", "Hill Troll"]:
        prefix = borb_hill_troll_male_nickname_prefix_table[d100()]
        suffix = borb_hill_troll_male_nickname_suffix_table[d100()]
        character.character_name = prefix + suffix

    elif character.race == "Subterranean Troll":
        if character.gender == "male":
            character.character_name = lookup_subterranean_troll_male_name(d1000())
        elif character.gender == "female":
            character.character_name = lookup_subterranean_troll_female_name(d1000())

    return character

def generate_birth(character: FatalModel):
    character.birthday = f"{d13()} / {d12() + d20() -1} / {5100 - character.age}"

    status_roll = d100()
    social_class_roll = d100()
    if status_roll < 21:
        character.birth_status = "Illigitimate (bastard)"
        social_class_roll  = social_class_roll - 2 if social_class_roll -2 >= 1 else 1
    else:
        character.birth_status = "Legitimate"

    if character.race == "Anakim":
        social_class_roll  = social_class_roll - 20 if social_class_roll -20 >= 1 else 1

    if character.race not in ["Borbytingarna Troll", "Hill Troll"]:
        social_values = lookup_race_social_class(character.race, social_class_roll)
        character.social_class = social_values[0]
        character.silver += social_values[1]
        character.literacy = social_values[2]

    if character.social_class == "Slave":
        while character.master_social_class is None:
            master_class_roll = d100()
            master_class = lookup_race_social_class(character.race, master_class_roll)[0]
            if master_class != "Slave":
                character.master_social_class = master_class
        master_occupation_roll = d1000()
        character.master_occupation = lookup_social_status_occupation(character.master_social_class, master_occupation_roll)

    birthplace_roll = d100()
        
    if character.race in ["Borbytingarna Troll", "Hill Troll"]:
        character.birthplace = "Nature"
    elif character.race in ["Ogre", "Cliff Ogre", "Gruagach Ogre", "Kinder-fresser Ogre"] and character.social_class in ["Slave", "Peasant"]:
        if birthplace_roll < 91:
            character.birthplace = 'Hamlet'
        else:
            character.birthplace = "Village"
    else:
        character.birthplace = lookup_social_status_birthplace(character.social_class, birthplace_roll)
    
    sibling_roll = d100()

    if character.race == "Anakim":
        sibling_roll = 1
    elif character.race == "Bugbear":
        sibling_roll -= 10
    elif character.race in ["Black Dwarf", "Brown Dwarf", "White Dwarf", "Dark Elf", "Light Elf"]:
        sibling_roll -= 25
    elif character.race == "Kobold":
        sibling_roll += 5
    elif character.race in ["Ogre", "Cliff Ogre", "Gruagach Ogre", "Kinder-fresser Ogre"]:
        sibling_roll -= 20
    elif character.race in ["Borbytingarna Troll", "Hill Troll", "Subterranean Troll"]:
        sibling_roll -= 15
    
    if sibling_roll < 1:
        sibling_roll = 1
    if sibling_roll > 100:
        sibling_roll = 100
    
    character.siblings = sibling_table[sibling_roll]
    total_siblings = character.siblings[0] + character.siblings[1]

    if total_siblings == 0:
        character.birth_rank = 1
    else:
        character.birth_rank = random.randint(1, total_siblings+1)

    marriage_roll = None
    while not marriage_roll:
        marriage_roll = d100()
        if character.sexuality == "Homosexual":
            if marriage_roll > 83:
                marriage_roll = None

    character.marital_status = marital_table[marriage_roll]

    return character

def generate_occupation(character: FatalModel):
    tries = 0
    while character.occupation is None:
        if tries > 1000:
            character.occupation = "Slave"
        else:
            occupation_roll = d1000()
            if character.social_class and character.social_class != "Slave":
                occupation = lookup_social_status_occupation(character.social_class, occupation_roll)
            elif character.social_class and character.social_class == "Slave":
                slave_roll = d100()
                occupation = lookup_slave_occupation(character.gender, slave_roll)
            requirements = lookup_occupation_requirements(occupation)

            passed = True
            num_sub_abilities_failed = 0
            sub_abilities_failed = []
            for req in requirements[0]:
                if not isinstance(req[1], str):
                    if not getattr(character, req[0]) >= req[1]:
                        if req[0] in sub_abilities:
                            num_sub_abilities_failed += 1
                            sub_abilities_failed.append(req)
                        else:
                            passed = False
                else:
                    if req[1] == 'not':
                        if getattr(character, req[0]) in req[2]:
                            passed = False

                    elif req[1] == 'in':
                        if getattr(character, req[0]) not in req[2]:
                            passed = False
                    elif req[1] == 'weight':
                        if not getattr(character, req[0]) >= character.weight:
                            passed = False
                    else:
                        if getattr(character, req[0]) != req[1]:
                            passed = False
            
            if passed == True and sub_abilities_failed == 0:
                character.occupation = occupation
            elif passed == True and num_sub_abilities_failed == 1:
                character = reroll_subability(character, sub_abilities_failed[0][0])
                if getattr(character, sub_abilities_failed[0][0]) >= sub_abilities_failed[0][1]:
                    character.occupation = occupation
        tries += 1

    requirements = requirements = lookup_occupation_requirements(character.occupation)
    if character.race not in ["Dark Elf", "Light Elf"]:
        character.occupation_level = floor(sqrt(character.age - age_started_working[character.race]))
    else:
        working_age = floor(character.elf_lifespan * 0.16)
        character.occupation_level = floor(sqrt(character.age - working_age))

    for skill_bonus in requirements[1]:
        if skill_bonus[0] != "weapon":
            skill = getattr(character, skill_bonus[0])
            skill.points_invested  = skill.points_invested + skill_bonus[1]
            setattr(character, skill_bonus[0], skill)
        else:
            for i in range(skill_bonus[1]):
                _, weapon = random.choice(list(weapons_table.values()))
                weapon = update_weapon(character, weapon)
                character.weapons.append(weapon)

    for item in requirements[2]:
        item_m = ItemModel(item_name=item)
        item_location = d3()
        if item_location == 1:
            character.left_items.append(item_m)
        elif item_location == 2:
            character.right_items.append(item_m)
        elif item_location ==3:
            character.front_back_items.append(item_m)

    character.magic_points = requirements[3] * character.occupation_level

    return character

def generate_skills(character: FatalModel):
    if character.race in ['Dark Elf', 'Light Elf']:
        lifespan_list = [
        ("Infant", 0, floor(character.elf_lifespan * 0.05)),
        ("Child", floor(character.elf_lifespan * 0.05) + 1, floor(character.elf_lifespan * 0.15)),
        ("Puberty", floor(character.elf_lifespan * 0.15)+ 1, floor(character.elf_lifespan * .25)),
        ("Young Adulthood",floor(character.elf_lifespan * .25) + 1, floor(character.elf_lifespan * 0.4))]
        working_age = floor(character.elf_lifespan * 0.15)+ 1
    else:
        lifespan_list = lifespan_table[character.race]
        working_age = age_started_working[character.race]

    if character.occupation:
        occupation_skills = lookup_occupation_requirements(character.occupation)[1]
        occupation_skills_list = []
        for occ in occupation_skills:
            occupation_skills_list.append(occ[0])
    for age in range(character.age):
        for age_range in lifespan_list:
            if age_range[1] <= age <= age_range[2]:
                stage_of_life = age_range[0]
        
        sp = skill_points_table[character.race][stage_of_life]
        working_skills = 0
        if age >= working_age and len(occupation_skills_list) >= 1:
            working_skills = floor(float(f"0.{d100():02d}") * sp)
            freetime_skills = sp - working_skills
        else:
            freetime_skills = sp
        for point in range(working_skills):
            skill_to_receive_points = random.choice(occupation_skills_list)
            skill = getattr(character, skill_to_receive_points)
            skill.points_invested += 1
            setattr(character, skill_to_receive_points, skill)

        for point in range(freetime_skills):
            skill_to_receive_points = None
            while skill_to_receive_points is None:
                skill_check = random.choice(list(skill_prerequisites_table.keys()))
                prerequisites = skill_prerequisites_table[skill_check]
                if len(prerequisites) >= 1:
                    passed = True
                    for prereq in prerequisites:
                        attribute = getattr(character, prereq[0])
                        if isinstance(attribute, SkillModel):
                            if attribute.points_invested < prereq[1]:
                                passed = False
                        else:
                            if attribute < prereq[1]:
                                passed = False
                    if passed:
                        skill_to_receive_points = skill_check
            skill = getattr(character, skill_to_receive_points)
            skill.points_invested += 1
            setattr(character, skill_to_receive_points, skill)

    return character

def calculate_skills(character: FatalModel):
    for name, attribute in vars(character).items():
        if isinstance(attribute, SkillModel):
            rel_abilities = attribute.related_abilities
            skill_modifier = 0
            if len(rel_abilities) > 0:
                for ability in rel_abilities:
                    skill_modifier += getattr(character, f"{ability}_modifier")
                skill_modifier = floor(skill_modifier / len(rel_abilities))
            attribute.skill_modifier = skill_modifier
            if attribute.points_invested >= 5:
                attribute.total_modifier = attribute.skill_modifier + attribute.points_invested
            else:
                attribute.total_modifier = attribute.skill_modifier + attribute.points_invested - attribute.learning_curve
            setattr(character, name, attribute)
    return character
