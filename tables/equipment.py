from models.character_models import FatalModel, ItemModel
from tables.weapons import weapons_table
from tables.armors import armors_table
from tables.item_tables import items_table
from tables.spells import spells_table, discipline_list, neighboring_disciplines
from dice import d3, d4, d6
import random
from math import floor


def add_equipment(character: FatalModel):
    if character.silver > 0:
        character = buy_armor(character)
        character = buy_weapons(character)
        character = buy_items(character)

    if character.magic_points > 0:
        character = get_spells(character)

    character = apply_armor(character)
    return character


def buy_armor(character: FatalModel):
    for i in range(10):
        random_armor = random.choice(list(armors_table.keys()))
        if character.silver >= armors_table[random_armor][0]:
            character.armors.append(armors_table[random_armor][1])
            character.silver = character.silver - armors_table[random_armor][0]
    return character


def apply_armor(character: FatalModel):
    if len(character.armors) > 0:
        for armor in character.armors:
            for location in armor.body_locations:
                body_part = getattr(character, location)
                body_part.cab += armor.cab_reduction
                body_part.cah += armor.cah_reduction
                body_part.cap += armor.cap_reduction
                body_part.cas += armor.cas_reduction

                setattr(character, location, body_part)
    return character


def buy_weapons(character: FatalModel):
    for i in range(10):
        random_weapon = random.choice(list(weapons_table.keys()))
        if character.silver >= weapons_table[random_weapon][0]:
            character.weapons.append(weapons_table[random_weapon][1])
            character.silver = character.silver - weapons_table[random_weapon][0]
    return character


def buy_items(character: FatalModel):
    for i in range(40):
        random_item = random.choice(list(items_table.keys()))
        if character.silver >= items_table[random_item][0]:
            character.silver = character.silver - items_table[random_item][0]
            if items_table[random_item][1] is not None:
                item_pocket = d3()
                if item_pocket == 1:
                    character.left_items.append(
                        ItemModel(
                            item_name=random_item, weight=items_table[random_item][1]
                        )
                    )
                elif item_pocket == 2:
                    character.right_items.append(
                        ItemModel(
                            item_name=random_item, weight=items_table[random_item][1]
                        )
                    )
                elif item_pocket == 3:
                    character.front_back_items.append(
                        ItemModel(
                            item_name=random_item, weight=items_table[random_item][1]
                        )
                    )
            else:
                character.misc_notes += f"has a {random_item}"
    return character


def get_spells(character: FatalModel):
    if character.occupation == "Druid" or "Hierophant":
        num_spells = 0
        disciplines = []
        disciplines.append(random.choice(discipline_list))
        disciplines.append(random.choice(neighboring_disciplines[disciplines[0]]))
        for i in range(character.occupation_level):
            num_spells += d4()

        while len(character.spells) < num_spells:
            random_spell = random.choice(spells_table)
            if (
                random_spell not in character.spells
                and random_spell.discipline in disciplines
            ):
                character.spells.append(random_spell)

    elif character.occupation == "Mage":
        num_spells = floor(character.intelligence / 10)

        while len(character.spells) < num_spells:
            random_spell = random.choice(spells_table)
            if (
                random_spell not in character.spells
                and random_spell.spell_type == "Ceremonial"
            ):
                character.spells.append(random_spell)

    elif character.occupation == "Sorcerer":
        num_disciplines = d4()
        disciplines = []
        while len(disciplines) < num_disciplines:
            random_discipline = random.choice(discipline_list)
            if random_discipline not in disciplines:
                disciplines.append(random_discipline)

        num_spells = d6() * character.occupation_level

        while len(character.spells) < num_spells:
            random_spell = random.choice(spells_table)
            if (
                random_spell not in character.spells
                and random_spell.discipline in disciplines
            ):
                character.spells.append(random_spell)
    return character
