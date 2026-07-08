import random
from models.character_models import FatalModel
from tables.race_tables import add_race
from dice import 

def generate_character():
    character = FatalModel(player_name="Abomination")

    character = add_race(character)
    # abilities, race, gender

    # body, disposition, mind

    # society


    return character

def main():
    character = generate_character()

    print(character)

if __name__ == "__main__":
    main()