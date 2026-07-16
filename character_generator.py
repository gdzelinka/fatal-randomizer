from models.character_models import FatalModel
from tables.race_tables import add_race, add_race_modifiers
from tables.gender_tables import add_gender, add_gender_modifiers
from tables.abilities import calculate_main_abilities, calculate_sub_abilities, apply_subability_modifiers
from tables.disposition import add_mind
from tables.body import add_body, generate_bpp
from tables.society import add_society, calculate_skills
from tables.equipment import add_equipment

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

    print(character)

if __name__ == "__main__":
    main()