from math import ceil
from models.character_models import FatalModel
from body.body_tables import lifespan_table
from abilities.ability_tables import skill_modifier
from disposition.disposition_tables import (
    ethicality_table,
    morality_table,
    male_debauchery_table,
    female_debauchery_table,
)
from dice import d2, d4, d20, d100


def add_mind(character: FatalModel):
    character = generate_piety(character)
    character = generate_disposition(character)
    character = generate_temperment(character)
    character = generate_sexuality(character)
    character = generate_debauchery(character)

    return character


def generate_sexuality(character: FatalModel):
    sexuality_roll = d100()

    if character.race == "Anakim":
        sexuality_roll = sexuality_roll + 1
    if character.race not in ["Anakim", "Dark Elf", "Light Elf", "Human"]:
        sexuality_roll = sexuality_roll + 5
    if character.race in ["Dark Elf", "Light Elf"]:
        sexuality_roll = sexuality_roll - 5

    if character.gender == "female" and character.cup_size in ["A", "AA"]:
        sexuality_roll = sexuality_roll - 4
    if character.gender == "female" and character.cup_size in ["D", ">D"]:
        sexuality_roll == 4

    if sexuality_roll < 2:
        character.sexuality = "Asexual"
    if 2 <= sexuality_roll < 4:
        character.sexuality = "Homosexual"

    if character.race == "Light Elf":
        if 4 <= sexuality_roll < 41:
            character.sexuality = "Bisexual"
        if sexuality_roll >= 41:
            character.sexuality = "Heterosexual"
    else:
        if 4 <= sexuality_roll < 6:
            character.sexuality = "Bisexual"
        if sexuality_roll >= 6:
            character.sexuality = "Heterosexual"

    return character


def generate_debauchery(character: FatalModel):
    debauchery_roll = d100() + character.debauchery_value

    if character.race == "Anakim":
        debauchery_roll = debauchery_roll + 30
    if character.race in [
        "Black Dwarf",
        "Brown Dwarf",
        "White Dwarf",
        "Dark Elf",
        "Light Elf",
        "Ogre",
        "Cliff Ogre",
        "Gruagach Ogre",
        "Kinder-fresser Ogre",
    ]:
        debauchery_roll = debauchery_roll - 10
    if character.race in [
        "Kobold",
        "Borbytingarna Troll",
        "Hill Troll",
        "Subterranean Troll",
    ]:
        debauchery_roll = debauchery_roll + 10

    if character.sexuality == "Asexual":
        debauchery_roll = debauchery_roll - 130

    if debauchery_roll < 1:
        debauchery_roll = 1
    if debauchery_roll > 100:
        debauchery_roll = 100

    if character.gender == "male":
        character.debauchery = male_debauchery_table[debauchery_roll]
    if character.gender == "female":
        character.debauchery = female_debauchery_table[debauchery_roll]

    return character


def generate_disposition(character: FatalModel):
    ethicality_roll = d100()
    ethicality_roll = ethicality_roll + character.ethical_points
    if ethicality_roll < 1:
        ethicality_roll = 1
    if ethicality_roll > 100:
        ethicality_roll = 100
    character.ethicality = ethicality_table[ceil(ethicality_roll / 5)]

    moral_roll = d100()
    moral_roll = moral_roll + character.moral_points
    if moral_roll < 1:
        moral_roll = 1
    if moral_roll > 100:
        moral_roll = 100
    character.morality = morality_table[ceil(moral_roll / 5)]

    if len(character.morality.split(" ")) == 1:
        moral_mods = [character.morality[0]]
    else:
        moral_mods = [
            character.morality.split(" ")[0][0],
            character.morality.split(" ")[-1][0],
        ]

    if len(character.ethicality.split(" ")) == 1:
        ethical_mods = [character.ethicality[0]]
    else:
        ethical_mods = [
            character.ethicality.split(" ")[0][0],
            character.ethicality.split(" ")[-1][0],
        ]

    if len(moral_mods) == 1 and len(ethical_mods) == 1:
        character.disposition = f"{ethical_mods[0]}{moral_mods[0]}"
    elif len(moral_mods) == 1:
        character.disposition = (
            f"{ethical_mods[0]}{moral_mods[0]} w/ {ethical_mods[1]}{moral_mods[0]}"
        )
    elif len(ethical_mods):
        character.disposition = (
            f"{ethical_mods[0]}{moral_mods[0]} w/ {ethical_mods[0]}{moral_mods[1]}"
        )
    else:
        character.disposition = (
            f"{ethical_mods[0]}{moral_mods[0]} w/ {ethical_mods[1]}{moral_mods[1]}"
        )

    return character


def generate_temperment(character: FatalModel):
    character.sanguine = character.sanguine + d100()
    character.choleric = character.choleric + d100()
    character.melancholic = character.melancholic + d100()
    character.phlegmatic = character.phlegmatic + d100()

    temp_dict = {
        character.sanguine: "sanguine",
        character.choleric: "choleric",
        character.melancholic: "melancholic",
        character.phlegmatic: "phlegmatic",
    }
    character.primary_temperment = temp_dict[max(temp_dict.keys())]
    temp_dict.pop(max(temp_dict.keys()))
    character.secondary_temperment = temp_dict[max(temp_dict.keys())]

    return character


def generate_piety(character: FatalModel):
    piety_points = d100()

    if character.race not in [
        "Black Dwarf",
        "Brown Dwarf",
        "White Dwarf",
        "Dark Elf",
        "Light Elf",
    ]:
        age_mod_chance = d4()
        if age_mod_chance > 1:
            race = character.race
            if character.race in [
                "Ogre",
                "Cliff Ogre",
                "Gruagach Ogre",
                "Kinder-fresser Ogre",
            ]:
                race = "Ogres"
            if character.race in [
                "Borbytingarna Troll",
                "Hill Troll",
                "Subterranean Troll",
            ]:
                race = "Trolls"
            max_age = lifespan_table[race][6][2]

            piety_points = piety_points + (character.age / max_age) * 4

    culture_mod = d2()
    if culture_mod == 1 and character.race == "Anakim":
        piety_points = piety_points + d20()

    ugly_mod = d4()
    if ugly_mod == 4:
        if character.bodily_attractiveness < 1:
            character.bodily_attractiveness = 1
        ugly_check = ceil((character.bodily_attractiveness / 6))
        piety_points = piety_points - skill_modifier[ugly_check]

    if character.race == "Bugbear":
        piety_points = piety_points + 1

    if character.race == "Kobold":
        piety_points = piety_points + 2

    if character.race in ["Ogre", "Cliff Ogre", "Gruagach Ogre", "Kinder-fresser Ogre"]:
        piety_points = piety_points - 100

    drive_mod = d4()
    if drive_mod > 1:
        drive_check = ceil((character.drive / 6))
        piety_points = piety_points + skill_modifier[drive_check]

    facial_mod = d4()
    if facial_mod == 4:
        facial_check = ceil((character.facial / 6))
        piety_points = piety_points - skill_modifier[facial_check]

    health_mod = d4()
    if health_mod > 1:
        health_check = ceil((character.health / 6))
        piety_points = piety_points - skill_modifier[health_check]

    if piety_points < 1:
        piety_points = 1
    if piety_points > 100:
        piety_points = 100

    character.piety_points = character.piety_points + piety_points
    return character
