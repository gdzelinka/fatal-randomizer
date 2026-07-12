from models.character_models import FatalModel
from tables.race_tables import add_race, add_race_modifiers
from tables.gender_tables import add_gender, add_gender_modifiers
from tables.abilities import calculate_main_abilities, calculate_sub_abilities, apply_subability_modifiers
from tables.disposition import add_mind
from tables.body import add_body, generate_bpp

def generate_character():
    character = FatalModel(player_name="Abomination")

    # abilities, race, gender
    character = calculate_sub_abilities(character)
    # When do people choose to reroll, let's say occupations

    character = add_race(character)
    character = add_gender(character)
    character = add_race_modifiers(character)
    character = add_body(character)
    character = add_mind(character)
    character = add_gender_modifiers(character)

    character = apply_subability_modifiers(character)
    character = generate_bpp(character)
    character = calculate_main_abilities(character)

    # society


    return character.bodily_attractiveness

def main():
    character = generate_character()

    print(character)

if __name__ == "__main__":
    main()