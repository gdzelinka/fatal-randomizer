import random
from models.character_models import FatalModel
from dice import d8, d10, d20, d100
from tables.race_traits import anakim_traits, elf_lifespan, ogre_occupation

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


def set_nested_attr(obj, path, value):
    parts = path.split(".")
    target = obj

    # walk down to the second‑to‑last attribute
    for part in parts[:-1]:
        target = getattr(target, part)

    # set the final attribute
    value = value + getattr(target, parts[-1])
    setattr(target, parts[-1], value)

def handle_anakim_traits(character):
    number_of_traits = d10()

    for _ in range(number_of_traits):
        trait_roll = d100() + 1
        print(f"Roll: {trait_roll}")
        if character.race == "Anakim":
            trait = anakim_traits[trait_roll]
        character.traits += f" {trait[0]}, "
        # Handling random modifiers
        if len(trait) > 1:
            for key, value in trait[1].items():
                if not isinstance(value, (tuple)):
                    set_nested_attr(character, key, value)
                else:
                    if isinstance(value[0], str):
                        setattr(character, key, getattr(character, key).append(value[0]))
                    elif isinstance(value[0], list):
                        condition_list = value[0]
                        pass_fail = False
                        and_or = condition_list[0]
                        for condition in condition_list[1:]:
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
                            set_nested_attr(character, key, value[1])
    return character


def add_race(character: FatalModel):
    # Race
    character.race = random.choices(
        population=list(race_dict.keys()),
        weights=list(race_dict.values()),
        k=1
    )[0]

    return character

def add_race_modifiers(character: FatalModel):

    if character.race == "Anakim":
        character.strength += 100
        character.hand_eye_coordination -= 30
        character.agility -= 25
        character.reaction_speed -= 20
        character.language += 5
        character.math += 5
        character.analytic += 5
        character.spatial += 5
        character.drive -= 5
        character.intuition -= 10
        character.common_sense -= 20
        character.reflection -= 10

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

        character = handle_anakim_traits(character)

    elif character.race == "Bugbear":
        character.strength += 100
        character.bodily_attractiveness -= 20
        character.facial -= 15
        character.rhetorical -= 10
        character.hand_eye_coordination -= 10
        character.agility -= 10
        character.ennunciation -= 10
        character.language -= 10
        character.math += 10
        character.analytic -= 10
        character.spatial += 5
        character.drive += 10

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
        character.physical_fitness -= 10
        character.bodily_attractiveness -= 15
        character.health += 10
        character.facial -= 15
        character.hand_eye_coordination += 50
        character.agility -= 5
        character.analytic += 5
        character.spatial += 10
        character.drive += 10
        character.common_sense += 10

        character.current_armor = 10
        character.life_points = 20

        character.moral_points -= 25
        character.sanguine -= 25
        character.choleric += 25

        character.languages_spoken.append("Dwarven")
        character.number_of_languages += 1

        character.appraise.skill_modifier += 3
        character.architecture.skill_modifier += 5
        character.armorsmithing.skill_modifier += 3
        character.blacksmithing.skill_modifier += 8
        character.brass_smithing.skill_modifier += 3
        character.climb.skill_modifier += 8
        character.coppersmithing.skill_modifier += 3
        character.direction_sense.skill_modifier += 3
        character.divination_axinomancy.skill_modifier += 3
        character.divination_cleromancy.skill_modifier += 3
        character.gambling.skill_modifier += 3
        character.gemcutting.skill_modifier += 5
        character.goldsmithing.skill_modifier += 3
        character.mining.skill_modifier += 3
        character.mountaineering.skill_modifier += 3
        character.pewtersmithing.skill_modifier += 3
        character.silversmithing.skill_modifier += 3
        character.stonemasonry.skill_modifier += 3
        character.trickery.skill_modifier += 5
        character.weaponsmithing.skill_modifier += 3

    elif character.race == "Brown Dwarf":
        character.physical_fitness -= 10
        character.bodily_attractiveness -= 10
        character.health += 10
        character.facial -= 5
        character.hand_eye_coordination += 5
        character.agility -= 5
        character.analytic += 5
        character.spatial += 10
        character.drive += 10
        character.common_sense += 10

        character.current_armor = 10
        character.life_points = 20

        character.languages_spoken.append("Dwarven")
        character.languages_spoken.append("Sapian")
        character.number_of_languages += 2

        character.appraise.skill_modifier += 3
        character.architecture.skill_modifier += 5
        character.armorsmithing.skill_modifier += 3
        character.blacksmithing.skill_modifier += 8
        character.brass_smithing.skill_modifier += 3
        character.cleaning.skill_modifier += 8
        character.climb.skill_modifier += 8
        character.coppersmithing.skill_modifier += 3
        character.dance.skill_modifier += 3
        character.direction_sense.skill_modifier += 3
        character.divination_axinomancy.skill_modifier += 3
        character.gemcutting.skill_modifier += 5
        character.goldsmithing.skill_modifier += 3
        character.mining.skill_modifier += 3
        character.mountaineering.skill_modifier += 3
        character.pewtersmithing.skill_modifier += 3
        character.silversmithing.skill_modifier += 3
        character.stonemasonry.skill_modifier += 3
        character.weaponsmithing.skill_modifier += 3

    elif character.race == "White Dwarf":
        character.physical_fitness -= 10
        character.bodily_attractiveness -= 10
        character.health += 10
        character.facial -= 5
        character.hand_eye_coordination += 5
        character.agility -= 5
        character.analytic += 5
        character.spatial += 10
        character.drive += 10
        character.common_sense += 10

        character.current_armor = 10
        character.life_points = 20

        character.ethical_points += 25
        character.moral_points += 25
        character.sanguine += 25
        character.choleric -= 25
        character.melancholic -= 25

        character.languages_spoken.append("Dwarven")
        character.number_of_languages += 1

        character.appraise.skill_modifier += 3
        character.architecture.skill_modifier += 5
        character.armorsmithing.skill_modifier += 3
        character.blacksmithing.skill_modifier += 8
        character.brass_smithing.skill_modifier += 3
        character.climb.skill_modifier += 8
        character.coppersmithing.skill_modifier += 3
        character.dance.skill_modifier += 3
        character.direction_sense.skill_modifier += 3
        character.divination_axinomancy.skill_modifier += 3
        character.gemcutting.skill_modifier += 5
        character.goldsmithing.skill_modifier += 3
        character.mining.skill_modifier += 3
        character.mountaineering.skill_modifier += 3
        character.pewtersmithing.skill_modifier += 3
        character.silversmithing.skill_modifier += 3
        character.stonemasonry.skill_modifier += 3
        character.weaponsmithing.skill_modifier += 3

    elif character.race == "Dark Elf":
        character.elf_lifespan = elf_lifespan[d8()+1]

        character.physical_fitness += 5
        character.strength -= 60
        character.bodily_attractiveness -= 10
        character.health += 10
        character.facial -= 10
        character.vocal += 10
        character.kinetic += 10
        character.hand_eye_coordination += 10
        character.agility += 5
        character.ennunciation += 5
        character.drive += 5
        character.intuition += 10
        character.common_sense += 10
        character.reflection += 5

        character.current_armor = 10
        character.life_points = 15

        character.moral_points -= 25
        character.sanguine -= 25
        character.choleric += 25
        character.melancholic += 25
        character.phlegmatic -= 25

        character.languages_spoken.append("Elven")
        character.number_of_languages += 1

        character.contortion.skill_modifier += 3
        character.dance.skill_modifier += 3
        character.etiquette.skill_modifier += 3
        character.herbalism.skill_modifier += 3
        character.musical_instrument.skill_modifier += 3
        character.nature_plants.skill_modifier += 3
        character.nature_trees.skill_modifier += 3
        character.smell.skill_modifier += 3
        character.tracking.skill_modifier += 3
        character.trickery.skill_modifier += 3
        character.tumble.skill_modifier += 3

    elif character.race == "Light Elf":
        character.elf_lifespan = elf_lifespan[d8()+1]

        character.physical_fitness += 5
        character.strength -= 60
        character.bodily_attractiveness += 10
        character.health += 10
        character.facial += 10
        character.vocal += 10
        character.kinetic += 10
        character.hand_eye_coordination += 10
        character.agility += 5
        character.ennunciation += 5
        character.drive += 5
        character.intuition += 10
        character.common_sense += 10
        character.reflection += 5

        character.current_armor = 10
        character.life_points = 15

        character.moral_points += 25
        character.sanguine += 25
        character.melancholic -= 25

        character.languages_spoken.append("Elven")
        character.number_of_languages += 1

        character.climb.skill_modifier += 3
        character.contortion.skill_modifier += 3
        character.dance.skill_modifier += 3
        character.etiquette.skill_modifier += 3
        character.herbalism.skill_modifier += 3
        character.musical_instrument.skill_modifier += 3
        character.nature_plants.skill_modifier += 3
        character.nature_trees.skill_modifier += 3
        character.smell.skill_modifier += 3
        character.tracking.skill_modifier += 3
        character.tumble.skill_modifier += 3

    elif character.race == "Human":
        character.current_armor = 10
        character.life_points = 20

        character.languages_spoken.append("Sapian")
        character.number_of_languages += 1

    elif character.race == "Kobol":
        character.strength -= 40
        character.bodily_attractiveness -= 15
        character.facial -= 15
        character.vocal -= 15
        character.kinetic += 15
        character.hand_eye_coordination += 15
        character.agility += 15
        character.reaction_speed += 15
        character.ennunciation += 15
        character.language -= 10
        character.analytic -= 10
        character.spatial += 15
        character.drive -= 15

        character.current_armor = 10
        character.life_points = 15

        character.moral_points -= 50
        character.sanguine -= 25
        character.choleric += 25
        character.phlegmatic += 25

        character.languages_spoken.append("Kobold")
        character.number_of_languages += 1

        character.direction_sense.skill_modifier += 3
        character.mining.skill_modifier += 3
        character.trickery.skill_modifier += 3
        character.weapon_specific.skill_modifier += 5

    elif character.race == "Ogre":
        character.physical_fitness -= 18
        character.strength += 240
        character.bodily_attractiveness -= 20
        character.facial -= 20
        character.kinetic -= 40
        character.rhetorical -= 15
        character.hand_eye_coordination -= 40
        character.agility -= 30
        character.reaction_speed -= 25
        character.ennunciation -= 50
        character.language -= 50
        character.math -= 50
        character.analytic -= 50
        character.spatial -= 10
        character.drive -= 15
        character.intuition -= 20
        character.common_sense -= 30

        character.current_armor = 13
        character.life_points = 30

        character.ethical_points -= 50
        character.moral_points -= 50
        character.sanguine -= 25
        character.choleric += 25
        character.phlegmatic += 25

        # TODO check gifted here
        # character.languages_spoken.append("Cigan")
        # character.number_of_languages += 1

        character.occupation = random.choices(
            population=list(ogre_occupation.keys()),
            weights=list(ogre_occupation.values()),
            k=1
        )[0]

        character.brawling.skill_modifier += 5
        character.mangling.skill_modifier += 5
        character.wrestling.skill_modifier += 3

    elif character.race == "Cliff Ogre":
        character.strength += 200
        character.bodily_attractiveness -= 20
        character.facial -= 20
        character.kinetic -= 20
        character.rhetorical -= 15
        character.hand_eye_coordination -= 10
        character.agility -= 15
        character.reaction_speed -= 25
        character.ennunciation -= 50
        character.language -= 50
        character.math -= 10
        character.analytic -= 25
        character.drive -= 15
        character.intuition -= 20
        character.common_sense -= 30

        character.current_armor = 13
        character.life_points = 27

        character.ethical_points -= 50
        character.moral_points -= 50
        character.sanguine -= 25
        character.choleric += 25
        character.melancholic += 25
        character.phlegmatic -= 25

        # TODO check gifted here
        # character.languages_spoken.append("Cigan")
        # character.number_of_languages += 1

        character.occupation = random.choices(
            population=list(ogre_occupation.keys()),
            weights=list(ogre_occupation.values()),
            k=1
        )[0]

        character.brawling.skill_modifier += 5
        character.climb.skill_modifier += 8
        character.hurl.skill_modifier += 5
        character.mangling.skill_modifier += 5
        character.wrestling.skill_modifier += 3

    elif character.race == "Gruagach Ogre":
        character.physical_fitness -= 22
        character.strength += 275
        character.bodily_attractiveness -= 30
        character.health -= 5
        character.facial -= 35
        character.kinetic -= 75
        character.rhetorical -= 30
        character.hand_eye_coordination -= 40
        character.agility -= 45
        character.reaction_speed -= 35
        character.ennunciation -= 50
        character.language -= 60
        character.math -= 60
        character.analytic -= 60
        character.spatial -= 15
        character.drive -= 30
        character.intuition -= 20
        character.common_sense -= 60

        character.current_armor = 13
        character.life_points = 35

        character.ethical_points -= 50
        character.moral_points -= 50
        character.melancholic -= 25
        character.phlegmatic += 25

        # TODO check gifted here
        # character.languages_spoken.append("Gruagan")
        # character.number_of_languages += 1

        character.occupation = random.choices(
            population=list(ogre_occupation.keys()),
            weights=list(ogre_occupation.values()),
            k=1
        )[0]

        character.brawling.skill_modifier += 5
        character.mangling.skill_modifier += 5
        character.smell.skill_modifier -= 5
        character.wrestling.skill_modifier += 3

    elif character.race == "Kinder-fresser Ogre":
        character.strength += 240
        character.bodily_attractiveness -= 10
        character.facial -= 12
        character.kinetic -= 20
        character.rhetorical += 15
        character.hand_eye_coordination -= 40
        character.agility -= 30
        character.reaction_speed -= 25
        character.ennunciation -= 10
        character.language -= 10
        character.math -= 50
        character.analytic -= 50
        character.spatial -= 10
        character.drive -= 15
        character.common_sense -= 30

        character.current_armor = 13
        character.life_points = 30

        character.ethical_points -= 50
        character.moral_points -= 50
        character.sanguine -= 25
        character.choleric += 25
        character.phlegmatic += 25

        character.languages_spoken.append("Sapian")
        character.number_of_languages += 1

        character.occupation = random.choice(
            ["Bandit", "Berserker", "Gladiator", "Slave"]
        )

        character.hide.skill_modifier += 5
        character.mangling.skill_modifier += 3
        character.persuasion.skill_modifier += 8
        character.silence.skill_modifier += 5
        character.trickery.skill_modifier += 5

    elif character.race == "Borbytingarna Troll":
        character.physical_fitness += 20
        character.strength += 100
        character.bodily_attractiveness -= 50
        character.facial -= 40
        character.kinetic -= 40
        character.hand_eye_coordination -= 5
        character.agility -= 25
        character.reaction_speed -= 20
        character.language -= 90
        character.math -= 60
        character.analytic -= 60
        character.spatial -= 10

        character.current_armor = 14
        character.life_points = 27

        character.ethical_points -= 50
        character.moral_points -= 50
        character.sanguine -= 25
        character.choleric += 25

        character.occupation = random.choice(
            ["Bandit", "Berserker", "Gladiator", "Slave"]
        )

        character.blindfighting.skill_modifier += 5
        character.brawling.skill_modifier += 5
        character.direction_sense.skill_modifier += 5
        character.disarm.skill_modifier += 3
        character.mangling.skill_modifier += 5
        character.wrestling.skill_modifier += 5

    elif character.race == "Hill Troll":
        character.physical_fitness -= 25
        character.strength += 100
        character.bodily_attractiveness -= 70
        character.facial -= 40
        character.kinetic -= 40
        character.hand_eye_coordination -= 20
        character.agility -= 25
        character.reaction_speed -= 20
        character.language -= 90
        character.math -= 60
        character.analytic -= 60
        character.spatial -= 10

        character.current_armor = 14
        character.life_points = 27

        character.ethical_points -= 50
        character.moral_points -= 50
        character.sanguine -= 25
        character.choleric += 25

        character.occupation = random.choice(
            ["Bandit", "Berserker", "Gladiator", "Slave"]
        )

        character.blindfighting.skill_modifier += 5
        character.brawling.skill_modifier += 5
        character.climb.skill_modifier += 5
        character.direction_sense.skill_modifier += 3
        character.mangling.skill_modifier += 5
        character.taste.skill_modifier += 3
        character.weapon_specific.skill_modifier += 5
        character.wrestling.skill_modifier += 3

    elif character.race == "Subterranean Troll":
        character.physical_fitness += 5
        character.strength += 100
        if character.gender == 'male':
            character.bodily_attractiveness -= 50
            character.facial -= 40
        character.kinetic -= 40
        character.hand_eye_coordination -= 20
        character.agility -= 25
        character.reaction_speed -= 20
        character.language += 10
        character.math += 10
        character.analytic += 10
        character.spatial += 10

        character.current_armor = 14
        character.life_points = 27

        character.ethical_points -= 50
        character.moral_points -= 50
        character.sanguine -= 25
        character.choleric += 25

        character.blindfighting.skill_modifier += 5
        character.brawling.skill_modifier += 5
        character.direction_sense.skill_modifier += 5
        character.mangling.skill_modifier += 5
        character.sound.skill_modifier += 3
        character.trickery.skill_modifier += 3
        character.wrestling.skill_modifier += 5

    return character
