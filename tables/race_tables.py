import random
from models.character_models import FatalModel
from dice import d8, d10, d20, d100
from tables.race_traits import (
    anakim_traits,
    elf_lifespan,
    ogre_occupation,
    racial_hatred,
)

race_dict = {
    "Anakim": 1,
    "Bugbear": 15,
    "Black Dwarf": 3,
    "Brown Dwarf": 1,
    "White Dwarf": 1,
    "Dark Elf": 1,
    "Light Elf": 1,
    "Human": 30,
    "Kobold": 20,
    "Ogre": 6,
    "Cliff Ogre": 2,
    "Gruagach Ogre": 3,
    "Kinder-fresser Ogre": 1,
    "Borbytingarna Troll": 2,
    "Hill Troll": 3,
    "Subterranean Troll": 10,
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
        trait_roll = d100()
        if character.race == "Anakim":
            trait = anakim_traits[trait_roll]
        character.traits.append(trait[0])
        # Handling random modifiers
        if len(trait) > 1:
            for key, value in trait[1].items():
                if not isinstance(value, (tuple)):
                    set_nested_attr(character, key, value)
                else:
                    if isinstance(value[0], str):
                        setattr(
                            character, key, getattr(character, key).append(value[0])
                        )
                    elif isinstance(value[0], list):
                        condition_list = value[0]
                        pass_fail = False
                        and_or = condition_list[0]
                        for condition in condition_list[1:]:
                            check = condition[1]
                            if condition[0] == "bool":
                                if (
                                    and_or == "OR"
                                    and getattr(character, check) == condition[2]
                                ):
                                    pass_fail = True
                                elif (
                                    and_or == "AND"
                                    and getattr(character, check) != condition[2]
                                ):
                                    pass_fail = False
                            elif condition[0] == "less than":
                                if (
                                    and_or == "OR"
                                    and getattr(character, check) < condition[2]
                                ):
                                    pass_fail = True
                                elif (
                                    and_or == "AND"
                                    and getattr(character, check) >= condition[2]
                                ):
                                    pass_fail = False
                            elif condition[0] == "greater than":
                                if (
                                    and_or == "OR"
                                    and getattr(character, check) >= condition[2]
                                ):
                                    pass_fail = True
                                elif (
                                    and_or == "AND"
                                    and getattr(character, check) < condition[2]
                                ):
                                    pass_fail = False
                        if pass_fail:
                            set_nested_attr(character, key, value[1])
    return character


def add_race(character: FatalModel):
    # Race
    character.race = random.choices(
        population=list(race_dict.keys()), weights=list(race_dict.values()), k=1
    )[0]

    return character


def individual_racial_hatred(societal_hatred: int):
    racism_roll = d10() + d10() + d10()

    if societal_hatred == 1:
        if racism_roll < 22:
            return 1
        if racism_roll < 27:
            return 2
        if racism_roll < 29:
            return 3
        if racism_roll < 30:
            return 4
        if racism_roll < 31:
            return 5
    elif societal_hatred == 2:
        if racism_roll < 22:
            return 1
        if racism_roll < 27:
            return 2
        if racism_roll < 29:
            return 3
        if racism_roll < 30:
            return 4
        return 5
    elif societal_hatred == 3:
        if racism_roll < 5:
            return 1
        if racism_roll < 12:
            return 2
        if racism_roll < 22:
            return 3
        if racism_roll < 29:
            return 4
        return 5
    elif societal_hatred == 4:
        if racism_roll < 5:
            return 1
        if racism_roll < 8:
            return 2
        if racism_roll < 12:
            return 3
        if racism_roll < 22:
            return 4
        return 5
    elif societal_hatred == 5:
        if racism_roll < 4:
            return 1
        if racism_roll < 5:
            return 2
        if racism_roll < 7:
            return 3
        if racism_roll < 12:
            return 4
        return 5


def add_racism(character: FatalModel):
    default_racism = racial_hatred[character.race]

    character.opinion_on_anakim = individual_racial_hatred(default_racism[0])
    character.opinion_on_bugbear = individual_racial_hatred(default_racism[1])
    character.opinion_on_black_dwarf = individual_racial_hatred(default_racism[2])
    character.opinion_on_brown_dwarf = individual_racial_hatred(default_racism[3])
    character.opinion_on_white_dwarf = individual_racial_hatred(default_racism[4])
    character.opinion_on_dark_elf = individual_racial_hatred(default_racism[5])
    character.opinion_on_light_elf = individual_racial_hatred(default_racism[6])
    character.opinion_on_human = individual_racial_hatred(default_racism[7])
    character.opinion_on_kobold = individual_racial_hatred(default_racism[8])
    character.opinion_on_ogre = individual_racial_hatred(default_racism[9])
    character.opinion_on_cliff_ogre = individual_racial_hatred(default_racism[10])
    character.opinion_on_gruagach_ogre = individual_racial_hatred(default_racism[11])
    character.opinion_on_kinder_fresser_ogre = individual_racial_hatred(
        default_racism[12]
    )
    character.opinion_on_borbytingarna_troll = individual_racial_hatred(
        default_racism[13]
    )
    character.opinion_on_hill_troll = individual_racial_hatred(default_racism[14])
    character.opinion_on_subterranean_troll = individual_racial_hatred(
        default_racism[15]
    )

    return character


def add_race_modifiers(character: FatalModel):

    character = add_racism(character)

    if character.race == "Anakim":
        character.strength = character.strength + 100
        character.hand_eye_coordination = character.hand_eye_coordination - 30
        character.agility = character.agility - 25
        character.reaction_speed = character.reaction_speed - 20
        character.language = character.language + 5
        character.math = character.math + 5
        character.analytic = character.analytic + 5
        character.spatial = character.spatial + 5
        character.drive = character.drive - 5
        character.intuition = character.intuition - 10
        character.common_sense = character.common_sense - 20
        character.reflection = character.reflection - 10

        character.current_armor = 11
        character.life_points = 27

        character.ethical_points = character.ethical_points - 25
        character.moral_points = character.moral_points - 50
        character.sanguine = character.sanguine - 25
        character.melancholic = character.melancholic - 25

        if character.number_of_languages < character.max_num_of_languages:
            character.languages_spoken.append("Sapian")
            character.number_of_languages = character.number_of_languages + 1

        character.brawling_skill.points_invested = (
            character.brawling_skill.points_invested + 3
        )
        character.intimidation.points_invested = (
            character.intimidation.points_invested + 5
        )
        character.mangling.points_invested = character.mangling.points_invested + 3
        character.sexual_adeptness.points_invested = (
            character.sexual_adeptness.points_invested + 5
        )
        character.trickery.points_invested = character.trickery.points_invested + 3
        character.weapon_specific.points_invested = (
            character.weapon_specific.points_invested + 5
        )
        character.wrestling.points_invested = character.wrestling.points_invested + 5

        character = handle_anakim_traits(character)

    elif character.race == "Bugbear":
        character.strength = character.strength + 100
        character.bodily_attractiveness = character.bodily_attractiveness - 20
        character.facial = character.facial - 15
        character.rhetorical = character.rhetorical - 10
        character.hand_eye_coordination = character.hand_eye_coordination - 10
        character.agility = character.agility - 10
        character.ennunciation = character.ennunciation - 10
        character.language = character.language - 10
        character.math = character.math + 10
        character.analytic = character.analytic - 10
        character.spatial = character.spatial + 5
        character.drive = character.drive + 10

        character.current_armor = 12
        character.life_points = 25

        character.ethical_points = character.ethical_points + 25
        character.moral_points = character.moral_points - 50
        character.sanguine = character.sanguine - 25
        character.choleric = character.choleric + 25
        character.melancholic = character.melancholic + 25

        if character.number_of_languages < character.max_num_of_languages:
            character.languages_spoken.append("Kobold")
            character.number_of_languages = character.number_of_languages + 1

        character.brawling_skill.points_invested = (
            character.brawling_skill.points_invested + 3
        )
        character.delousing.points_invested = character.delousing.points_invested + 5
        character.divination_anthropomancy.points_invested = (
            character.divination_anthropomancy.points_invested + 3
        )
        character.divination_dririmancy.points_invested = (
            character.divination_dririmancy.points_invested + 3
        )
        character.law.points_invested = character.law.points_invested + 3
        character.sailing.points_invested = character.sailing.points_invested + 3
        character.search.points_invested = character.search.points_invested + 3
        character.shipwright.points_invested = character.shipwright.points_invested + 3
        character.surgery.points_invested = character.surgery.points_invested + 3
        character.tracking.points_invested = character.tracking.points_invested + 3
        character.weapon_specific.points_invested = (
            character.weapon_specific.points_invested + 5
        )
        character.wrestling.points_invested = character.wrestling.points_invested + 3

    elif character.race == "Black Dwarf":
        character.physical_fitness = character.physical_fitness - 10
        character.bodily_attractiveness = character.bodily_attractiveness - 15
        character.health = character.health + 10
        character.facial = character.facial - 15
        character.hand_eye_coordination = character.hand_eye_coordination + 50
        character.agility = character.agility - 5
        character.analytic = character.analytic + 5
        character.spatial = character.spatial + 10
        character.drive = character.drive + 10
        character.common_sense = character.common_sense + 10

        character.current_armor = 10
        character.life_points = 20

        character.moral_points = character.moral_points - 25
        character.sanguine = character.sanguine - 25
        character.choleric = character.choleric + 25

        if character.number_of_languages < character.max_num_of_languages:
            character.languages_spoken.append("Dwarven")
            character.number_of_languages = character.number_of_languages + 1

        character.appraise.points_invested = character.appraise.points_invested + 3
        character.architecture.points_invested = (
            character.architecture.points_invested + 5
        )
        character.armorsmithing.points_invested = (
            character.armorsmithing.points_invested + 3
        )
        character.blacksmithing.points_invested = (
            character.blacksmithing.points_invested + 8
        )
        character.brass_smithing.points_invested = (
            character.brass_smithing.points_invested + 3
        )
        character.climb.points_invested = character.climb.points_invested + 8
        character.coppersmithing.points_invested = (
            character.coppersmithing.points_invested + 3
        )
        character.direction_sense.points_invested = (
            character.direction_sense.points_invested + 3
        )
        character.divination_axinomancy.points_invested = (
            character.divination_axinomancy.points_invested + 3
        )
        character.divination_cleromancy.points_invested = (
            character.divination_cleromancy.points_invested + 3
        )
        character.gambling.points_invested = character.gambling.points_invested + 3
        character.gemcutting.points_invested = character.gemcutting.points_invested + 5
        character.goldsmithing.points_invested = (
            character.goldsmithing.points_invested + 3
        )
        character.mining.points_invested = character.mining.points_invested + 3
        character.mountaineering.points_invested = (
            character.mountaineering.points_invested + 3
        )
        character.pewtersmithing.points_invested = (
            character.pewtersmithing.points_invested + 3
        )
        character.silversmithing.points_invested = (
            character.silversmithing.points_invested + 3
        )
        character.stonemasonry.points_invested = (
            character.stonemasonry.points_invested + 3
        )
        character.trickery.points_invested = character.trickery.points_invested + 5
        character.weaponsmithing.points_invested = (
            character.weaponsmithing.points_invested + 3
        )

    elif character.race == "Brown Dwarf":
        character.physical_fitness = character.physical_fitness - 10
        character.bodily_attractiveness = character.bodily_attractiveness - 10
        character.health = character.health + 10
        character.facial = character.facial - 5
        character.hand_eye_coordination = character.hand_eye_coordination + 5
        character.agility = character.agility - 5
        character.analytic = character.analytic + 5
        character.spatial = character.spatial + 10
        character.drive = character.drive + 10
        character.common_sense = character.common_sense + 10

        character.current_armor = 10
        character.life_points = 20

        if character.number_of_languages < character.max_num_of_languages:
            character.languages_spoken.append("Dwarven")
            character.number_of_languages = character.number_of_languages + 1
        if character.number_of_languages < character.max_num_of_languages:
            character.languages_spoken.append("Sapian")
            character.number_of_languages = character.number_of_languages + 1

        character.appraise.points_invested = character.appraise.points_invested + 3
        character.architecture.points_invested = (
            character.architecture.points_invested + 5
        )
        character.armorsmithing.points_invested = (
            character.armorsmithing.points_invested + 3
        )
        character.blacksmithing.points_invested = (
            character.blacksmithing.points_invested + 8
        )
        character.brass_smithing.points_invested = (
            character.brass_smithing.points_invested + 3
        )
        character.cleaning.points_invested = character.cleaning.points_invested + 8
        character.climb.points_invested = character.climb.points_invested + 8
        character.coppersmithing.points_invested = (
            character.coppersmithing.points_invested + 3
        )
        character.dance.points_invested = character.dance.points_invested + 3
        character.direction_sense.points_invested = (
            character.direction_sense.points_invested + 3
        )
        character.divination_axinomancy.points_invested = (
            character.divination_axinomancy.points_invested + 3
        )
        character.gemcutting.points_invested = character.gemcutting.points_invested + 5
        character.goldsmithing.points_invested = (
            character.goldsmithing.points_invested + 3
        )
        character.mining.points_invested = character.mining.points_invested + 3
        character.mountaineering.points_invested = (
            character.mountaineering.points_invested + 3
        )
        character.pewtersmithing.points_invested = (
            character.pewtersmithing.points_invested + 3
        )
        character.silversmithing.points_invested = (
            character.silversmithing.points_invested + 3
        )
        character.stonemasonry.points_invested = (
            character.stonemasonry.points_invested + 3
        )
        character.weaponsmithing.points_invested = (
            character.weaponsmithing.points_invested + 3
        )

    elif character.race == "White Dwarf":
        character.physical_fitness = character.physical_fitness - 10
        character.bodily_attractiveness = character.bodily_attractiveness - 10
        character.health = character.health + 10
        character.facial = character.facial - 5
        character.hand_eye_coordination = character.hand_eye_coordination + 5
        character.agility = character.agility - 5
        character.analytic = character.analytic + 5
        character.spatial = character.spatial + 10
        character.drive = character.drive + 10
        character.common_sense = character.common_sense + 10

        character.current_armor = 10
        character.life_points = 20

        character.ethical_points = character.ethical_points + 25
        character.moral_points = character.moral_points + 25
        character.sanguine = character.sanguine + 25
        character.choleric = character.choleric - 25
        character.melancholic = character.melancholic - 25

        if character.number_of_languages < character.max_num_of_languages:
            character.languages_spoken.append("Dwarven")
            character.number_of_languages = character.number_of_languages + 1

        character.appraise.points_invested = character.appraise.points_invested + 3
        character.architecture.points_invested = (
            character.architecture.points_invested + 5
        )
        character.armorsmithing.points_invested = (
            character.armorsmithing.points_invested + 3
        )
        character.blacksmithing.points_invested = (
            character.blacksmithing.points_invested + 8
        )
        character.brass_smithing.points_invested = (
            character.brass_smithing.points_invested + 3
        )
        character.climb.points_invested = character.climb.points_invested + 8
        character.coppersmithing.points_invested = (
            character.coppersmithing.points_invested + 3
        )
        character.dance.points_invested = character.dance.points_invested + 3
        character.direction_sense.points_invested = (
            character.direction_sense.points_invested + 3
        )
        character.divination_axinomancy.points_invested = (
            character.divination_axinomancy.points_invested + 3
        )
        character.gemcutting.points_invested = character.gemcutting.points_invested + 5
        character.goldsmithing.points_invested = (
            character.goldsmithing.points_invested + 3
        )
        character.mining.points_invested = character.mining.points_invested + 3
        character.mountaineering.points_invested = (
            character.mountaineering.points_invested + 3
        )
        character.pewtersmithing.points_invested = (
            character.pewtersmithing.points_invested + 3
        )
        character.silversmithing.points_invested = (
            character.silversmithing.points_invested + 3
        )
        character.stonemasonry.points_invested = (
            character.stonemasonry.points_invested + 3
        )
        character.weaponsmithing.points_invested = (
            character.weaponsmithing.points_invested + 3
        )

    elif character.race == "Dark Elf":
        character.elf_lifespan = elf_lifespan[d8() + 1]

        character.physical_fitness = character.physical_fitness + 5
        character.strength = character.strength - 60
        character.bodily_attractiveness = character.bodily_attractiveness - 10
        character.health = character.health + 10
        character.facial = character.facial - 10
        character.vocal = character.vocal + 10
        character.kinetic = character.kinetic + 10
        character.hand_eye_coordination = character.hand_eye_coordination + 10
        character.agility = character.agility + 5
        character.ennunciation = character.ennunciation + 5
        character.drive = character.drive + 5
        character.intuition = character.intuition + 10
        character.common_sense = character.common_sense + 10
        character.reflection = character.reflection + 5

        character.current_armor = 10
        character.life_points = 15

        character.moral_points = character.moral_points - 25
        character.sanguine = character.sanguine - 25
        character.choleric = character.choleric + 25
        character.melancholic = character.melancholic + 25
        character.phlegmatic = character.phlegmatic - 25

        if character.number_of_languages < character.max_num_of_languages:
            character.languages_spoken.append("Elven")
            character.number_of_languages = character.number_of_languages + 1

        character.contortion.points_invested = character.contortion.points_invested + 3
        character.dance.points_invested = character.dance.points_invested + 3
        character.etiquette.points_invested = character.etiquette.points_invested + 3
        character.herbalism.points_invested = character.herbalism.points_invested + 3
        character.musical_instrument.points_invested = (
            character.musical_instrument.points_invested + 3
        )
        character.nature_plants.points_invested = (
            character.nature_plants.points_invested + 3
        )
        character.nature_trees.points_invested = (
            character.nature_trees.points_invested + 3
        )
        character.smell.points_invested = character.smell.points_invested + 3
        character.tracking.points_invested = character.tracking.points_invested + 3
        character.trickery.points_invested = character.trickery.points_invested + 3
        character.tumble.points_invested = character.tumble.points_invested + 3

    elif character.race == "Light Elf":
        character.elf_lifespan = elf_lifespan[d8() + 1]

        character.physical_fitness = character.physical_fitness + 5
        character.strength = character.strength - 60
        character.bodily_attractiveness = character.bodily_attractiveness + 10
        character.health = character.health + 10
        character.facial = character.facial + 10
        character.vocal = character.vocal + 10
        character.kinetic = character.kinetic + 10
        character.hand_eye_coordination = character.hand_eye_coordination + 10
        character.agility = character.agility + 5
        character.ennunciation = character.ennunciation + 5
        character.drive = character.drive + 5
        character.intuition = character.intuition + 10
        character.common_sense = character.common_sense + 10
        character.reflection = character.reflection + 5

        character.current_armor = 10
        character.life_points = 15

        character.moral_points = character.moral_points + 25
        character.sanguine = character.sanguine + 25
        character.melancholic = character.melancholic - 25

        if character.number_of_languages < character.max_num_of_languages:
            character.languages_spoken.append("Elven")
            character.number_of_languages = character.number_of_languages + 1

        character.climb.points_invested = character.climb.points_invested + 3
        character.contortion.points_invested = character.contortion.points_invested + 3
        character.dance.points_invested = character.dance.points_invested + 3
        character.etiquette.points_invested = character.etiquette.points_invested + 3
        character.herbalism.points_invested = character.herbalism.points_invested + 3
        character.musical_instrument.points_invested = (
            character.musical_instrument.points_invested + 3
        )
        character.nature_plants.points_invested = (
            character.nature_plants.points_invested + 3
        )
        character.nature_trees.points_invested = (
            character.nature_trees.points_invested + 3
        )
        character.smell.points_invested = character.smell.points_invested + 3
        character.tracking.points_invested = character.tracking.points_invested + 3
        character.tumble.points_invested = character.tumble.points_invested + 3

    elif character.race == "Human":
        character.current_armor = 10
        character.life_points = 20

        if character.number_of_languages < character.max_num_of_languages:
            character.languages_spoken.append("Sapian")
            character.number_of_languages = character.number_of_languages + 1

    elif character.race == "Kobold":
        character.strength = character.strength - 40
        character.bodily_attractiveness = character.bodily_attractiveness - 15
        character.facial = character.facial - 15
        character.vocal = character.vocal - 15
        character.kinetic = character.kinetic + 15
        character.hand_eye_coordination = character.hand_eye_coordination + 15
        character.agility = character.agility + 15
        character.reaction_speed = character.reaction_speed + 15
        character.ennunciation = character.ennunciation + 15
        character.language = character.language - 10
        character.analytic = character.analytic - 10
        character.spatial = character.spatial + 15
        character.drive = character.drive - 15

        character.current_armor = 10
        character.life_points = 15

        character.moral_points = character.moral_points - 50
        character.sanguine = character.sanguine - 25
        character.choleric = character.choleric + 25
        character.phlegmatic = character.phlegmatic + 25

        if character.number_of_languages < character.max_num_of_languages:
            character.languages_spoken.append("Kobold")
            character.number_of_languages = character.number_of_languages + 1

        character.direction_sense.points_invested = (
            character.direction_sense.points_invested + 3
        )
        character.mining.points_invested = character.mining.points_invested + 3
        character.trickery.points_invested = character.trickery.points_invested + 3
        character.weapon_specific.points_invested = (
            character.weapon_specific.points_invested + 5
        )

    elif character.race == "Ogre":
        character.physical_fitness = character.physical_fitness - 18
        character.strength = character.strength + 240
        character.bodily_attractiveness = character.bodily_attractiveness - 20
        character.facial = character.facial - 20
        character.kinetic = character.kinetic - 40
        character.rhetorical = character.rhetorical - 15
        character.hand_eye_coordination = character.hand_eye_coordination - 40
        character.agility = character.agility - 30
        character.reaction_speed = character.reaction_speed - 25
        character.ennunciation = character.ennunciation - 50
        character.language = character.language - 50
        character.math = character.math - 50
        character.analytic = character.analytic - 50
        character.spatial = character.spatial - 10
        character.drive = character.drive - 15
        character.intuition = character.intuition - 20
        character.common_sense = character.common_sense - 30

        character.current_armor = 13
        character.life_points = 30

        character.ethical_points = character.ethical_points - 50
        character.moral_points = character.moral_points - 50
        character.sanguine = character.sanguine - 25
        character.choleric = character.choleric + 25
        character.phlegmatic = character.phlegmatic + 25

        if (
            character.intelligence_range >= 3
            and character.number_of_languages < character.max_num_of_languages
        ):
            character.languages_spoken.append("Cigan")
            character.number_of_languages = character.number_of_languages + 1

        character.occupation = random.choices(
            population=list(ogre_occupation.keys()),
            weights=list(ogre_occupation.values()),
            k=1,
        )[0]

        character.brawling_skill.points_invested = (
            character.brawling_skill.points_invested + 5
        )
        character.mangling.points_invested = character.mangling.points_invested + 5
        character.wrestling.points_invested = character.wrestling.points_invested + 3

    elif character.race == "Cliff Ogre":
        character.strength = character.strength + 200
        character.bodily_attractiveness = character.bodily_attractiveness - 20
        character.facial = character.facial - 20
        character.kinetic = character.kinetic - 20
        character.rhetorical = character.rhetorical - 15
        character.hand_eye_coordination = character.hand_eye_coordination - 10
        character.agility = character.agility - 15
        character.reaction_speed = character.reaction_speed - 25
        character.ennunciation = character.ennunciation - 50
        character.language = character.language - 50
        character.math = character.math - 10
        character.analytic = character.analytic - 25
        character.drive = character.drive - 15
        character.intuition = character.intuition - 20
        character.common_sense = character.common_sense - 30

        character.current_armor = 13
        character.life_points = 27

        character.ethical_points = character.ethical_points - 50
        character.moral_points = character.moral_points - 50
        character.sanguine = character.sanguine - 25
        character.choleric = character.choleric + 25
        character.melancholic = character.melancholic + 25
        character.phlegmatic = character.phlegmatic - 25

        if (
            character.intelligence_range >= 3
            and character.number_of_languages < character.max_num_of_languages
        ):
            character.languages_spoken.append("Cigan")
            character.number_of_languages = character.number_of_languages + 1

        character.occupation = random.choices(
            population=list(ogre_occupation.keys()),
            weights=list(ogre_occupation.values()),
            k=1,
        )[0]

        character.brawling_skill.points_invested = (
            character.brawling_skill.points_invested + 5
        )
        character.climb.points_invested = character.climb.points_invested + 8
        character.hurl.points_invested = character.hurl.points_invested + 5
        character.mangling.points_invested = character.mangling.points_invested + 5
        character.wrestling.points_invested = character.wrestling.points_invested + 3

    elif character.race == "Gruagach Ogre":
        character.physical_fitness = character.physical_fitness - 22
        character.strength = character.strength + 275
        character.bodily_attractiveness = character.bodily_attractiveness - 30
        character.health = character.health - 5
        character.facial = character.facial - 35
        character.kinetic = character.kinetic - 75
        character.rhetorical = character.rhetorical - 30
        character.hand_eye_coordination = character.hand_eye_coordination - 40
        character.agility = character.agility - 45
        character.reaction_speed = character.reaction_speed - 35
        character.ennunciation = character.ennunciation - 50
        character.language = character.language - 60
        character.math = character.math - 60
        character.analytic = character.analytic - 60
        character.spatial = character.spatial - 15
        character.drive = character.drive - 30
        character.intuition = character.intuition - 20
        character.common_sense = character.common_sense - 60

        character.current_armor = 13
        character.life_points = 35

        character.ethical_points = character.ethical_points - 50
        character.moral_points = character.moral_points - 50
        character.melancholic = character.melancholic - 25
        character.phlegmatic = character.phlegmatic + 25

        if (
            character.intelligence_range >= 3
            and character.number_of_languages < character.max_num_of_languages
        ):
            character.languages_spoken.append("Gruagan")
            character.number_of_languages = character.number_of_languages + 1

        character.occupation = random.choices(
            population=list(ogre_occupation.keys()),
            weights=list(ogre_occupation.values()),
            k=1,
        )[0]

        character.brawling_skill.points_invested = (
            character.brawling_skill.points_invested + 5
        )
        character.mangling.points_invested = character.mangling.points_invested + 5
        character.smell.points_invested = character.smell.points_invested - 5
        character.wrestling.points_invested = character.wrestling.points_invested + 3

    elif character.race == "Kinder-fresser Ogre":
        character.strength = character.strength + 240
        character.bodily_attractiveness = character.bodily_attractiveness - 10
        character.facial = character.facial - 12
        character.kinetic = character.kinetic - 20
        character.rhetorical = character.rhetorical + 15
        character.hand_eye_coordination = character.hand_eye_coordination - 40
        character.agility = character.agility - 30
        character.reaction_speed = character.reaction_speed - 25
        character.ennunciation = character.ennunciation - 10
        character.language = character.language - 10
        character.math = character.math - 50
        character.analytic = character.analytic - 50
        character.spatial = character.spatial - 10
        character.drive = character.drive - 15
        character.common_sense = character.common_sense - 30

        character.current_armor = 13
        character.life_points = 30

        character.ethical_points = character.ethical_points - 50
        character.moral_points = character.moral_points - 50
        character.sanguine = character.sanguine - 25
        character.choleric = character.choleric + 25
        character.phlegmatic = character.phlegmatic + 25

        if character.number_of_languages < character.max_num_of_languages:
            character.languages_spoken.append("Sapian")
            character.number_of_languages = character.number_of_languages + 1

        character.occupation = random.choice(
            ["Bandit", "Berserker", "Gladiator", "Slave"]
        )

        character.hide.points_invested = character.hide.points_invested + 5
        character.mangling.points_invested = character.mangling.points_invested + 3
        character.persuasion.points_invested = character.persuasion.points_invested + 8
        character.silence.points_invested = character.silence.points_invested + 5
        character.trickery.points_invested = character.trickery.points_invested + 5

    elif character.race == "Borbytingarna Troll":
        character.physical_fitness = character.physical_fitness + 20
        character.strength = character.strength + 100
        character.bodily_attractiveness = character.bodily_attractiveness - 50
        character.facial = character.facial - 40
        character.kinetic = character.kinetic - 40
        character.hand_eye_coordination = character.hand_eye_coordination - 5
        character.agility = character.agility - 25
        character.reaction_speed = character.reaction_speed - 20
        character.language = character.language - 90
        character.math = character.math - 60
        character.analytic = character.analytic - 60
        character.spatial = character.spatial - 10

        character.current_armor = 14
        character.life_points = 27

        character.ethical_points = character.ethical_points - 50
        character.moral_points = character.moral_points - 50
        character.sanguine = character.sanguine - 25
        character.choleric = character.choleric + 25

        character.occupation = random.choice(
            ["Bandit", "Berserker", "Gladiator", "Slave"]
        )

        character.blindfighting.points_invested = (
            character.blindfighting.points_invested + 5
        )
        character.brawling_skill.points_invested = (
            character.brawling_skill.points_invested + 5
        )
        character.direction_sense.points_invested = (
            character.direction_sense.points_invested + 5
        )
        character.disarm.points_invested = character.disarm.points_invested + 3
        character.mangling.points_invested = character.mangling.points_invested + 5
        character.wrestling.points_invested = character.wrestling.points_invested + 5

    elif character.race == "Hill Troll":
        character.physical_fitness = character.physical_fitness - 25
        character.strength = character.strength + 100
        character.bodily_attractiveness = character.bodily_attractiveness - 70
        character.facial = character.facial - 40
        character.kinetic = character.kinetic - 40
        character.hand_eye_coordination = character.hand_eye_coordination - 20
        character.agility = character.agility - 25
        character.reaction_speed = character.reaction_speed - 20
        character.language = character.language - 90
        character.math = character.math - 60
        character.analytic = character.analytic - 60
        character.spatial = character.spatial - 10

        character.current_armor = 14
        character.life_points = 27

        character.ethical_points = character.ethical_points - 50
        character.moral_points = character.moral_points - 50
        character.sanguine = character.sanguine - 25
        character.choleric = character.choleric + 25

        character.occupation = random.choice(
            ["Bandit", "Berserker", "Gladiator", "Slave"]
        )

        character.blindfighting.points_invested = (
            character.blindfighting.points_invested + 5
        )
        character.brawling_skill.points_invested = (
            character.brawling_skill.points_invested + 5
        )
        character.climb.points_invested = character.climb.points_invested + 5
        character.direction_sense.points_invested = (
            character.direction_sense.points_invested + 3
        )
        character.mangling.points_invested = character.mangling.points_invested + 5
        character.taste.points_invested = character.taste.points_invested + 3
        character.weapon_specific.points_invested = (
            character.weapon_specific.points_invested + 5
        )
        character.wrestling.points_invested = character.wrestling.points_invested + 3

    elif character.race == "Subterranean Troll":
        character.physical_fitness = character.physical_fitness + 5
        character.strength = character.strength + 100
        if character.gender == "male":
            character.bodily_attractiveness = character.bodily_attractiveness - 50
            character.facial = character.facial - 40
        character.kinetic = character.kinetic - 40
        character.hand_eye_coordination = character.hand_eye_coordination - 20
        character.agility = character.agility - 25
        character.reaction_speed = character.reaction_speed - 20
        character.language = character.language + 10
        character.math = character.math + 10
        character.analytic = character.analytic + 10
        character.spatial = character.spatial + 10

        character.current_armor = 14
        character.life_points = 27

        character.ethical_points = character.ethical_points - 50
        character.moral_points = character.moral_points - 50
        character.sanguine = character.sanguine - 25
        character.choleric = character.choleric + 25

        character.blindfighting.points_invested = (
            character.blindfighting.points_invested + 5
        )
        character.brawling_skill.points_invested = (
            character.brawling_skill.points_invested + 5
        )
        character.direction_sense.points_invested = (
            character.direction_sense.points_invested + 5
        )
        character.mangling.points_invested = character.mangling.points_invested + 5
        character.sound.points_invested = character.sound.points_invested + 3
        character.trickery.points_invested = character.trickery.points_invested + 3
        character.wrestling.points_invested = character.wrestling.points_invested + 5

    return character
