# fatal-randomizer
Generate a random FATAL Character


## About the Project

Ever wanted to play FATAL? The most historically and mythically (sic.) accurate game there is! Of course you have.
But making a character is just too dang hard. 

Well that's what this project is all about. Replacing the 600+ dice rolls with one handy-dandy python script.

KamSandwich or anyone associated with the Kam Delicatessen is not allowed to use this repo until he has created his own character with pencil and die. 

### Key Features

- **Fully Implemented Racism Tables**
- **Hand Crafted Artisan Nipple Length Chart**
- **The Bowyer skill is mentioned in the occupations, but is missing from the character sheet. I can't implement it if I don't know the requirements**
- **Purchase Castle Walls 1 square foot At A Time**


### Installation

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/gdzelinka/fatal-randomizer.git](https://github.com/gdzelinka/fatal-randomizer.git)
  
3. **Install the library**
   ```bash
   cd fatal-randomizer
   pip install .
  
3. **Enjoy**
   ``` bash
   python src/character_generator.py

## Architecture & Directory Structure

```text
fatal-randomizer/
├── abilities/             # Handling the character's core 20 abilities
├── body/                  # Handling the character's various body features
├── disposition/           # Handling the character's moral disposition
├── equipment/             # Handling the character's weapons, armor, and items
├── gender/                # Handling the character's gender
├── models/                # Pydantic models defining what it is to be a Fatal Character
├── race/                  # Handling the character's race
├── society/               # Handling the character's place in society
├── character_generator.py # Script that handles everything listed above
├── dice.py                # What is a die roll
├── pretty_print.py        # Printing the chracter to the terminal in a readbale way
├── README.md              # See README
└── pyproject.toml         # Project dependencies
```
---

## Roadmap

- [ ] [Open to suggestions]

---

## Contributing

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## License

Distributed under the **MIT License**. See `LICENSE` for more information.



---

## Contact & Support

Maintainer: [ZLinked](https://github.com/gdzelinka)

Project Link: [https://github.com/gdzelinka/fatal-randomizer.git](https://github.com/gdzelinka/fatal-randomizer.git)

---

## Acknowledgments

* [Zigmenthotep](https://www.youtube.com/@zigmenthotep)
* [KamSandwich](https://www.youtube.com/@kamsandwich/)
