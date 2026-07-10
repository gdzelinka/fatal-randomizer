from models.character_models import FatalModel
from tables.race_tables import add_race, add_race_modifiers
from tables.gender_tables import add_gender, add_gender_modifiers
from tables.abilities import calculate_main_abilities, calculate_sub_abilities

def generate_character():
    character = FatalModel(player_name="Abomination")

    # abilities, race, gender
    character = calculate_sub_abilities(character)
    # When do people choose to reroll, let's say occupations

    character = add_race(character)
    character = add_gender(character)
    character = add_race_modifiers(character)
    character = add_gender_modifiers(character)
    character = calculate_main_abilities(character)

    # body, disposition, mind

    # society


    return character

def main():
    character = generate_character()

    print(character)

if __name__ == "__main__":
    main()