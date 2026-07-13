import ast
import re
from pathlib import Path


SKIP_WORDS = ("tend to", "tends to", "commonly", "most often", "usually")
RARITY_WORDS = (" are rare", " is rare", " are uncommon", " is uncommon", " are common")

ALL_RACES = [
    "Anakim",
    "Human",
    "Bugbear",
    "Black Dwarf",
    "Brown Dwarf",
    "White Dwarf",
    "Dark Elf",
    "Light Elf",
    "Kobold",
    "Ogre",
    "Cliff Ogre",
    "Gruagach Ogre",
    "Kinder-fresser Ogre",
    "Borbytingarna Troll",
    "Hill Troll",
    "Subterranean Troll",
]

RACE_EXCLUSION_PHRASES = {
    "ogre": ["Ogre", "Cliff Ogre", "Gruagach Ogre", "Kinder-fresser Ogre"],
    "ogres": ["Ogre", "Cliff Ogre", "Gruagach Ogre", "Kinder-fresser Ogre"],
    "troll": ["Borbytingarna Troll", "Hill Troll", "Subterranean Troll"],
    "trolls": ["Borbytingarna Troll", "Hill Troll", "Subterranean Troll"],
    "borbytingarna": ["Borbytingarna Troll"],
    "hill troll": ["Hill Troll"],
    "hill trolls": ["Hill Troll"],
    "subterranean troll": ["Subterranean Troll"],
    "elf": ["Dark Elf", "Light Elf"],
    "elves": ["Dark Elf", "Light Elf"],
    "dark elf": ["Dark Elf"],
    "light elf": ["Light Elf"],
    "dwarf": ["Black Dwarf", "Brown Dwarf", "White Dwarf"],
    "dwarves": ["Black Dwarf", "Brown Dwarf", "White Dwarf"],
    "dwarven": ["Black Dwarf", "Brown Dwarf", "White Dwarf"],
    "bugbear": ["Bugbear"],
    "bugbears": ["Bugbear"],
    "kobold": ["Kobold"],
    "kobolds": ["Kobold"],
    "anakim": ["Anakim"],
    "human": ["Human"],
    "humans": ["Human"],
}

ABILITY_PATTERNS = [
    ("physical_fitness", r"Physical Fitness\s+(\d+)"),
    ("hand_eye_coordination", r"Hand-Eye Coordination\s+(\d+)"),
    ("analytic", r"Analytic Intelligence\s+(\d+)"),
    ("spatial", r"Spatial Intelligence\s+(\d+)"),
    ("intelligence", r"Intelligence\s*\(overall\)\s*(\d+)"),
    ("reaction_speed", r"Reaction Speed\s+(\d+)"),
    ("bodily_attractiveness", r"Bodily Attractiveness\s+(\d+)"),
    ("facial", r"Facial Charisma\s+(\d+)"),
    ("agility", r"Agility\s+(\d+)"),
    ("drive", r"Drive\s+(\d+)"),
    ("intuition", r"Intuition\s+(\d+)"),
    ("wisdom", r"Wisdom\s+(\d+)"),
    ("health", r"Health\s+(\d+)"),
    ("charisma", r"(?<!Facial )Charisma\s+(\d+)"),
    ("common_sense", r"Common Sense\s+(\d+)"),
    ("language", r"Language\s+(\d+)"),
    ("strength", r"Strength\s+(\d+)"),
    ("intelligence", r"(?<!Spatial )(?<!Analytic )Intelligence\s+(\d+)"),
]

SOCIAL_CLASS_MAP = {
    "peasant": "Peasant",
    "serf": "Serf",
    "noble": "Nobility",
    "nobility": "Nobility",
    "slave": "Slave",
    "royal": "Royalty",
    "royalty": "Royalty",
}


def should_skip(text: str) -> bool:
    if not text or not text.strip():
        return True
    lowered = text.lower().strip().rstrip(".")
    if lowered in {"any", ""}:
        return True
    if any(word in lowered for word in SKIP_WORDS):
        return True
    if any(word in lowered for word in RARITY_WORDS):
        return True
    return False


def parse_ability_requirements(text: str) -> list[tuple]:
    requirements = []
    if not text or not text.strip():
        return requirements

    text = re.sub(r"-\s+", "", text)
    text = re.sub(r"\s+", " ", text).strip()

    if re.search(r"bench press", text, re.I):
        requirements.append(("bench", "weight"))

    seen: dict[str, int] = {}
    order: list[str] = []
    for attr, pattern in ABILITY_PATTERNS:
        for match in re.finditer(pattern, text, re.I):
            if attr == "strength" and re.search(r"bench press", match.group(0), re.I):
                continue
            value = int(match.group(1))
            if attr not in seen:
                order.append(attr)
                seen[attr] = value
            else:
                seen[attr] = max(seen[attr], value)

    requirements.extend((attr, seen[attr]) for attr in order)
    return requirements


def parse_gender(text: str) -> list[tuple]:
    if should_skip(text):
        return []
    lowered = text.lower()
    if "female only" in lowered:
        return [("gender", "female")]
    if re.search(r"\bmale only\b", lowered):
        return [("gender", "male")]
    return []


def parse_race_exclusions(text: str) -> list[str]:
    lowered = text.lower()
    excluded = []
    but_match = re.search(r"any but (.+?)\.", lowered)
    if not but_match:
        return excluded

    clause = but_match.group(1)
    clause = clause.replace(" and ", ", ")
    parts = [part.strip() for part in clause.split(",") if part.strip()]
    for part in parts:
        if part in RACE_EXCLUSION_PHRASES:
            excluded.extend(RACE_EXCLUSION_PHRASES[part])
            continue
        for phrase, races in RACE_EXCLUSION_PHRASES.items():
            if phrase in part:
                excluded.extend(races)
    return sorted(set(excluded), key=ALL_RACES.index)


def parse_race(text: str) -> list[tuple]:
    if should_skip(text) or len(text) > 120:
        return []
    lowered = text.lower().strip().rstrip(".")
    if lowered.startswith("any but"):
        excluded = parse_race_exclusions(text)
        if excluded:
            return [("race", "not", excluded)]
        return []
    if lowered == "human":
        return [("race", "Human")]
    return []


def parse_disposition(text: str) -> list[tuple]:
    if should_skip(text) or len(text) > 120:
        return []
    lowered = text.lower()
    requirements = []
    if "neutral regarding ethics and morality" in lowered:
        requirements.append(("ethicality", "neutral"))
        requirements.append(("morality", "neutral"))
    elif "immoral" in lowered and "ethical" not in lowered:
        requirements.append(("morality", "immoral"))
    elif "ethical" in lowered and "unethical" not in lowered:
        requirements.append(("ethicality", "ethical"))
    elif "unethical" in lowered:
        requirements.append(("ethicality", "unethical"))
    return requirements


def parse_social_class(text: str) -> list[tuple]:
    if not text or not text.strip():
        return []
    lowered = text.lower()
    if any(word in lowered for word in SKIP_WORDS + RARITY_WORDS):
        if not re.search(r"\b(peasant|serf|noble|nobility|slave|royal|royalty)\b", lowered):
            return []

    classes = []
    for key, value in SOCIAL_CLASS_MAP.items():
        if re.search(rf"\b{key}s?\b", lowered):
            if value not in classes:
                classes.append(value)

    if not classes:
        return []
    if len(classes) == 1:
        return [("social_class", classes[0])]
    return [("social_class", "in", classes)]


def parse_religion(text: str) -> list[tuple]:
    if should_skip(text) or len(text) > 80:
        return []
    lowered = text.lower()
    if "immoral" in lowered:
        return [("religion", "immoral")]
    return []


def convert_requirement_fields(fields: list) -> list[tuple]:
    if not fields:
        return []
    if fields and isinstance(fields[0], tuple):
        return list(fields)

    parsers = [
        parse_ability_requirements,
        parse_gender,
        parse_race,
        parse_disposition,
        lambda text: [],
        parse_social_class,
        parse_religion,
    ]

    converted = []
    for text, parser in zip(fields, parsers):
        converted.extend(parser(text or ""))
    return converted


def skill_name_to_attr(name: str) -> str:
    name = name.strip().lower()
    name = name.replace(" (specific)", "")
    name = name.replace("/", "_")
    name = re.sub(r"[^a-z0-9]+", "_", name)
    return name.strip("_")


def convert_skills(skills: list) -> list[tuple]:
    if not skills:
        return []
    if skills and isinstance(skills[0], tuple):
        return list(skills)

    converted = []
    for skill in skills:
        if not skill or skill.strip().lower() in {"none.", "none"}:
            continue
        weapon_match = re.match(r"(\d+)\s+Weapon", skill, re.I)
        if weapon_match:
            converted.append(("weapon", int(weapon_match.group(1))))
            continue
        weapon_specific_match = re.match(r"Weapon\s*\(specific\)", skill, re.I)
        if weapon_specific_match:
            converted.append(("weapon", 1))
            continue
        if re.search(r"receives a\s*\+\s*\d+", skill, re.I):
            continue
        bonus_match = re.match(r"(.+?)\s*\+\s*(\d+)", skill)
        if bonus_match:
            converted.append((skill_name_to_attr(bonus_match.group(1)), int(bonus_match.group(2))))
            continue
    return converted


def py_repr_tuple_item(item) -> str:
    if isinstance(item, tuple):
        parts = ", ".join(py_repr_value(part) for part in item)
        return f"({parts})"
    return py_repr_value(item)


def py_repr_value(value) -> str:
    if isinstance(value, str):
        return repr(value)
    if isinstance(value, int):
        return str(value)
    if isinstance(value, list):
        return "[" + ", ".join(repr(item) for item in value) + "]"
    return repr(value)


def py_repr_tuple_list(items: list) -> str:
    if not items:
        return "[]"
    lines = ["["]
    for item in items:
        lines.append(f"        {py_repr_tuple_item(item)},")
    lines.append("    ]")
    return "\n".join(lines)


def py_repr_string_list(items: list) -> str:
    if not items:
        return "[]"
    lines = ["["]
    for item in items:
        lines.append(f"        {repr(item)},")
    lines.append("    ]")
    return "\n".join(lines)


def write_table(table: dict, aliases: dict, output_path: Path) -> None:
    lines = ["occupation_requirements_table = {"]
    for name in sorted(table):
        requirements, skills, equipment, magic_points = table[name]
        lines.append(f"    {repr(name)}: (")
        lines.append(f"        {py_repr_tuple_list(requirements)},")
        lines.append(f"        {py_repr_tuple_list(skills)},")
        lines.append(f"        {py_repr_string_list(equipment)},")
        lines.append(f"        {repr(magic_points)},")
        lines.append("    ),")
    lines.append("}")
    lines.append("")
    lines.append("")
    lines.append("occupation_name_aliases = {")
    for alias, canonical in sorted(aliases.items()):
        lines.append(f"    {repr(alias)}: {repr(canonical)},")
    lines.append("}")
    lines.append("")
    lines.append("")
    lines.append(
        "def lookup_occupation_requirements(occupation: str) -> tuple[list, list, list, str]:"
    )
    lines.append('    """Return requirements, skills, equipment, and magic points for an occupation."""')
    lines.append("    canonical = occupation_name_aliases.get(occupation, occupation)")
    lines.append("    try:")
    lines.append("        return occupation_requirements_table[canonical]")
    lines.append("    except KeyError as error:")
    lines.append('        raise KeyError(f"No occupation requirements for {occupation!r}") from error')
    lines.append("")
    output_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    source_path = Path("tables/occupation_tables.py")
    source = source_path.read_text(encoding="utf-8")
    table_match = re.search(
        r"occupation_requirements_table\s*=\s*(\{.*?\n\})\n\n\noccupation_name_aliases",
        source,
        re.S,
    )
    alias_match = re.search(
        r"occupation_name_aliases\s*=\s*(\{.*?\n\})\n\n\ndef lookup_occupation_requirements",
        source,
        re.S,
    )
    table = ast.literal_eval(table_match.group(1))
    aliases = ast.literal_eval(alias_match.group(1))

    converted_table = {}
    for name, entry in table.items():
        requirements, skills, equipment, magic_points = entry
        if name == "Acrobat":
            converted_table[name] = entry
            continue
        converted_table[name] = (
            convert_requirement_fields(list(requirements)),
            convert_skills(list(skills)),
            list(equipment),
            magic_points,
        )

    write_table(converted_table, aliases, source_path)
    print(f"Converted {len(converted_table)} occupations.")


if __name__ == "__main__":
    main()
