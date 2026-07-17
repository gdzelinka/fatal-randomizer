from models.character_models import FatalModel
from race.generate_race import add_race, add_race_modifiers
from gender.generate_gender import add_gender, add_gender_modifiers
from abilities.generate_abilities import (
    calculate_main_abilities,
    calculate_sub_abilities,
    apply_subability_modifiers,
)
from disposition.generate_disposition import add_mind
from body.generate_body import add_body, generate_bpp
from society.generate_society import add_society, calculate_skills
from equipment.generate_equipment import add_equipment
from pretty_print import print_fatal_model

def generate_character():
    character = FatalModel(player_name="Abomination")

    character = calculate_sub_abilities(character)

    character = add_race(character)
    character = add_gender(character)
    character = add_race_modifiers(character)
    character = add_body(character)
    character = add_mind(character)
    character = add_gender_modifiers(character)

    character = apply_subability_modifiers(character)
    character = generate_bpp(character)

    character = calculate_main_abilities(character)
    character = add_society(character)

    # There's a chance to reroll subabilities in add_society so we do this again
    character = calculate_main_abilities(character)

    character = add_equipment(character)

    character = calculate_skills(character)

    return character


def main():
    character = generate_character()
    print_fatal_model(character)


if __name__ == "__main__":
    main()
