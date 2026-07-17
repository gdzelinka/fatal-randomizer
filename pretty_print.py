"""Terminal pretty-printer for FatalModel character sheets."""

from __future__ import annotations

from typing import Any

from rich import box
from rich.console import Console, Group
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from models.character_models import ArmorModel, FatalModel, ItemModel, SkillModel, SpellModel, WeaponModel

console = Console()


def _val(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "Yes" if value else "No"
    if isinstance(value, float) and value == int(value):
        return str(int(value))
    return str(value)


def _height(inches: int) -> str:
    if not inches:
        return ""
    return f"{inches // 12}'{inches % 12}\""


def _siblings(siblings: tuple[int, int]) -> str:
    if not siblings or siblings == (0, 0):
        return ""
    return f"{siblings[0]}/{siblings[1]}"


def _skill_name(field: str) -> str:
    special = {
        "acting_drama": "Acting, Drama",
        "comedy_buffoonery": "Comedy, Buffoonery",
        "comedy_physical": "Comedy, Physical",
        "comedy_pun": "Comedy, Pun",
        "brawling_skill": "Brawling",
        "sprint_skill": "Sprint",
        "language_read_write": "Language, Read/Write",
        "language_speak": "Language, Speak",
        "math_algebra": "Math, Algebra",
        "math_fundamental": "Math, Fundamental",
        "math_geometry": "Math, Geometry",
        "math_trigonometry": "Math, Trigonometry",
        "history_cultural": "History, Cultural",
        "history_legendary": "History, Legendary",
        "history_local": "History, Local",
        "history_military": "History, Military",
        "nature_animals": "Nature, Animals",
        "nature_beasts": "Nature, Beasts",
        "nature_birds": "Nature, Birds",
        "nature_fish": "Nature, Fish",
        "nature_geography": "Nature, Geography",
        "nature_humanoids": "Nature, Humanoids",
        "nature_minerals": "Nature, Minerals",
        "nature_mycology": "Nature, Mycology",
        "nature_plants": "Nature, Plants",
        "nature_trees": "Nature, Trees",
        "religion_cultural": "Religion, Cultural",
        "religion_specific": "Religion, Specific",
        "cosmos_general_planes": "Cosmos, General Planes",
        "cosmos_specific_plane": "Cosmos, Specific Plane",
        "music_counterpoint": "Music, Counterpoint",
        "music_theory": "Music, Theory",
        "musical_instrument": "Musical Instrument",
        "spellcasting_combat": "Spellcasting, Combat",
        "spellcasting_familiarity": "Spellcasting, Familiarity",
        "spellcasting_specific": "Spellcasting, Specific",
        "weapon_general": "Weapon, General",
        "weapon_specific": "Weapon, Specific",
        "weapon_mastery": "Weapon Mastery",
        "weapon_trick": "Weapon Trick",
    }
    if field in special:
        return special[field]
    if field.startswith("divination_"):
        return "Divination, " + field.removeprefix("divination_").replace("_", " ").title()
    return field.replace("_", " ").title()


def _related_abilities(skill: SkillModel) -> str:
    return ", ".join(a.replace("_", " ").title() for a in skill.related_abilities)


def _general_info(character: FatalModel) -> Table:
    rows = [
        [("Character Name", character.character_name), ("Gender", character.gender), ("Race", character.race)],
        [("Player Name", character.player_name), ("Occupation", character.occupation or ""), ("", "")],
        [("Homeland", character.homeland), ("Level", character.level), ("Religion", character.religion)],
        [
            ("Height", _height(character.height)),
            ("Weight", character.weight),
            ("Siblings", _siblings(character.siblings)),
        ],
        [
            ("Age", character.age),
            ("Eyes", character.eyes),
            ("Skin Color", character.skin_color),
        ],
        [
            ("Birth Rank", character.birth_rank),
            ("Sexuality", character.sexuality),
            ("Debauchery", character.debauchery or character.debauchery_value),
        ],
        [
            ("Marital Status", character.marital_status),
            ("Birth Status", character.birth_status),
            ("Literacy", character.literacy),
        ],
        [
            ("Hair Color", character.hair_color),
            ("Hair Thickness", character.hair_thickness),
            ("Facial Feature", character.facial_feature),
        ],
        [
            ("Birthplace", character.birthplace),
            ("Hair Length", character.hair_length),
            ("Hair Type", character.hair_type),
        ],
        [
            ("Birthday", character.birthday),
            ("Vision", character.vision),
            ("Stage of Life", character.stage_of_life),
        ],
        [
            ("Most Attractive Feature", character.most_attractive_feature),
            ("Breadth", character.breadth),
            ("BMI", character.bmi),
        ],
        [
            ("Most Repulsive Feature", character.most_repulsive_feature),
            ("Appearance", character.appearance),
            ("Social Class", character.social_class or ""),
        ],
        [
            (
                "Notes",
                ", ".join(character.traits) if character.traits else character.misc_notes,
            ),
            ("", ""),
            ("", ""),
        ],
    ]
    table = Table(box=box.SQUARE, expand=True, show_header=False, padding=(0, 1))
    for _ in range(3):
        table.add_column(ratio=1)
    table.add_row(
        Text("GENERAL INFORMATION", style="bold white on grey50", justify="center"),
        "",
        "",
        end_section=True,
    )
    for row in rows:
        table.add_row(
            *[f"{label}: {_val(value)}" if label else "" for label, value in row]
        )
    return table


def _abilities_table(character: FatalModel) -> Table:
    table = Table(
        box=box.SQUARE,
        expand=True,
        show_header=True,
        header_style="bold white on grey50",
        padding=(0, 1),
    )
    table.add_column("(Sub)Ability", ratio=2)
    table.add_column("Score", justify="right", width=6)
    table.add_column("Skill Mod.", justify="right", width=8)
    table.add_column("Derived / Description", ratio=3)

    def ability_row(label: str, score: int, modifier: int, derived: str = "", style: str = "") -> None:
        table.add_row(
            Text(label, style=style),
            _val(score),
            _val(modifier),
            derived,
        )

    def section(title: str) -> None:
        table.add_row(Text(title, style="bold white on grey37"), "", "", "", end_section=True)

    section("PHYSIQUE")
    ability_row("Physical Fitness", character.physical_fitness, character.physical_fitness_modifier, f"Sprint: {character.sprint}")
    ability_row("Strength", character.strength, character.strength_modifier, f"Dmg: {character.dmg}  C&J: {character.cj}  Bench: {character.bench}  DL: {character.dl}")
    ability_row("Bodily Attractiveness", character.bodily_attractiveness, character.bodily_attractiveness_modifier)
    ability_row("Health", character.health, character.health_modifier, f"Int/Vom: {character.int_vom}  All: {character.health_all}  Ill. Im.: {character.im}")

    section("CHARISMA")
    ability_row("Facial", character.facial, character.facial_modifier, character.facial_description)
    ability_row("Vocal", character.vocal, character.vocal_modifier, character.vocal_description)
    ability_row("Kinetic", character.kinetic, character.kinetic_modifier, character.kinetic_description)
    ability_row("Rhetorical", character.rhetorical, character.rhetorical_modifier, f"Avg Speech Rate: {character.average_speech_rate}")

    section("DEXTERITY")
    ability_row("Hand-Eye Coordination", character.hand_eye_coordination, character.hand_eye_coordination_modifier, f"Finger Movement Precision: {character.finger_movement_precision}")
    ability_row("Agility", character.agility, character.agility_modifier, f"CA Bonus: {character.ca_bonus}  Brawling: {character.brawling}  Stand: {character.stand}")
    ability_row("Reaction Speed", character.reaction_speed, character.reaction_speed_modifier, f"Deep Sleep Recovery: {character.deep_sleep_recovery}")
    ability_row("Enunciation", character.ennunciation, character.ennunciation_modifier, f"Max Speech Rate: {character.maximum_speech_rate}  Casting: {character.casting}")

    section("INTELLIGENCE")
    ability_row("Language", character.language, character.language_modifier, f"#: {character.number_of_languages}/{character.max_num_of_languages}  Vocabulary: {character.vocabulary}")
    ability_row("Math", character.math, character.math_modifier, f"Highest Possible Math: {character.highest_possible_math}")
    ability_row("Analytic", character.analytic, character.analytic_modifier)
    ability_row("Spatial", character.spatial, character.spatial_modifier, f"Unfamiliar Object Assembly: {character.unfamiliar_object_assembly} pieces")

    section("WISDOM")
    ability_row("Drive", character.drive, character.drive_modifier, f"Unconsciousness: {character.unconscioness}  Hours Resting: {character.hours_resting}")
    ability_row("Intuition", character.intuition, character.intuition_modifier)
    ability_row("Common Sense", character.common_sense, character.common_sense_modifier, f"Likely to: {character.likely_to}")
    ability_row("Reflection", character.reflection, character.reflection_modifier, f"Earliest Memory at: {character.earliest_memory_at}")

    return table


def _point_totals(character: FatalModel) -> Table:
    table = Table(box=box.SQUARE, expand=False, show_header=False, padding=(0, 2))
    table.add_column(width=18)
    table.add_column(width=18)
    table.add_row("Life Points", _val(character.life_points))
    table.add_row("Magic Points", _val(character.magic_points))
    table.add_row("Unconscious (20% L.P.)", _val(character.unconscious))
    table.add_row("Piety Points", _val(character.piety_points))
    return Panel(table, title="Point Totals", box=box.SQUARE)


def _disposition(character: FatalModel) -> Table:
    table = Table(box=box.SQUARE, expand=True, show_header=True, header_style="bold white on grey50")
    table.add_column("DISPOSITION", ratio=1)
    table.add_column("TEMPERAMENT", ratio=1)
    disp = [
        f"Ethical Points: {character.ethical_points}",
        f"Moral Points: {character.moral_points}",
        f"Ethicality: {character.ethicality}",
        f"Morality: {character.morality}",
        f"Disposition: {character.disposition}",
    ]
    temp = [
        f"Sanguine: {character.sanguine}",
        f"Choleric: {character.choleric}",
        f"Melancholic: {character.melancholic}",
        f"Phlegmatic: {character.phlegmatic}",
        f"Primary: {character.primary_temperment}",
        f"Secondary: {character.secondary_temperment}",
    ]
    for i in range(max(len(disp), len(temp))):
        table.add_row(disp[i] if i < len(disp) else "", temp[i] if i < len(temp) else "")
    return table


def _initiative(character: FatalModel) -> Panel:
    lines = []
    if character.weapons:
        for weapon in character.weapons:
            reach = int(weapon.weapon_range) if isinstance(weapon.weapon_range, (int, float)) else 0
            total = character.reaction_speed_modifier + weapon.breadth + reach - weapon.delivery_penalty
            lines.append(
                f"{weapon.weapon}: {total} = Reaction {character.reaction_speed_modifier} + "
                f"Breadth {weapon.breadth} + Reach {reach} - Delivery {weapon.delivery_penalty}"
            )
    else:
        lines.append(
            f"Modifier Total: {character.reaction_speed_modifier} = Reaction Speed Mod. (no weapon equipped)"
        )
    return Panel("\n".join(lines), title="INITIATIVE", box=box.SQUARE)


def _weapons_table(weapons: list[WeaponModel]) -> Table:
    table = Table(box=box.SQUARE, expand=True, show_header=True, header_style="bold white on grey50")
    headers = ["Weapon", "Skill Mod.", "Breadth", "Type", "Size", "Weight", "Wt Dist.", "Fulc/Range", "Del. Pen.", "Damage", "L", "M", "H"]
    for header in headers:
        table.add_column(header, no_wrap=False)
    rows = weapons or [None]
    for weapon in rows:
        if weapon is None:
            table.add_row(*([""] * len(headers)))
            continue
        table.add_row(
            weapon.weapon,
            _val(weapon.skill_modifier),
            _val(weapon.breadth),
            weapon.weapon_type,
            weapon.size,
            _val(weapon.weight),
            _val(weapon.weight_distribution),
            f"{weapon.fulcrum_range}/{weapon.weapon_range}",
            _val(weapon.delivery_penalty),
            _val(weapon.damage),
            _val(weapon.l),
            _val(weapon.m),
            _val(weapon.h),
        )
    return Panel(table, title="WEAPONS", box=box.SQUARE)


def _armors_table(armors: list[ArmorModel]) -> Table:
    table = Table(box=box.SQUARE, expand=True, show_header=True, header_style="bold white on grey50")
    headers = [
        "Armor/Shield/Protective Item",
        "Type",
        "Armor Bonus",
        "IP",
        "Agility Loss",
        "Weight",
        "Mod. Hide",
        "Mod. Silence",
        "Spell Failure",
        "Special Properties",
    ]
    for header in headers:
        table.add_column(header)
    rows = armors or [None]
    for armor in rows:
        if armor is None:
            table.add_row(*([""] * len(headers)))
            continue
        name = armor.armor or armor.armor_type
        table.add_row(
            name,
            armor.armor_type,
            _val(armor.armor_bonus),
            _val(armor.ip),
            _val(armor.agility_loss),
            _val(armor.weight),
            _val(armor.modifer_to_hide),
            _val(armor.modifer_to_silence),
            _val(armor.spell_failure),
            armor.special_properties,
        )
    return Panel(table, title="ARMOR", box=box.SQUARE)


def _sexual_and_rare(character: FatalModel) -> Table:
    col1 = [
        ("Manhood Length", character.manhood_length),
        ("Manhood Circumference", character.manhood_circumference),
        ("Anal Circumference Potential", character.anal_circumference_potential),
        ("Vaginal Circumference Potential", character.vaginal_circumference_potential),
        ("Vaginal Depth Potential", character.vaginal_depth_potential),
    ]
    col2 = [
        ("Areola Diameter", character.areola_diameter),
        ("Nipple Length", character.nipple_length),
        ("Cup Size", character.cup_size),
        ("Tongue Size", character.tongue_size),
        ("Hymen Resistance", character.hymen_resistance),
    ]
    col3 = [
        ("Areola Hue", character.areola_hue),
        ("Foot Size", character.foot_size),
        ("Fist Circumference", character.fist_circumference),
        ("Head Circumference", character.head_circumference),
        ("Handedness", character.handedness),
    ]
    table = Table(box=box.SQUARE, expand=True, show_header=False, padding=(0, 1))
    table.add_column(ratio=1)
    table.add_column(ratio=1)
    table.add_column(ratio=1)
    table.add_row(
        Text("SEXUAL AND RARE FEATURES", style="bold white on grey50", justify="center"),
        "",
        "",
        end_section=True,
    )
    for i in range(max(len(col1), len(col2), len(col3))):
        c1 = f"{col1[i][0]}: {_val(col1[i][1])}" if i < len(col1) else ""
        c2 = f"{col2[i][0]}: {_val(col2[i][1])}" if i < len(col2) else ""
        c3 = f"{col3[i][0]}: {_val(col3[i][1])}" if i < len(col3) else ""
        table.add_row(c1, c2, c3)
    return table


def _languages(character: FatalModel) -> Table:
    table = Table(box=box.SQUARE, expand=True, show_header=True, header_style="bold white on grey50")
    table.add_column("LANGUAGES SPOKEN", ratio=1)
    table.add_column("LANGUAGES READ AND WRITTEN", ratio=1)
    spoken = character.languages_spoken or []
    written = character.languages_read_and_written or []
    for i in range(max(len(spoken), len(written), 5)):
        table.add_row(
            spoken[i] if i < len(spoken) else "",
            written[i] if i < len(written) else "",
        )
    return table


def _special_abilities(abilities: list[str] | None) -> Table:
    table = Table(box=box.SQUARE, expand=True, show_header=True, header_style="bold white on grey50")
    table.add_column("SPECIAL ABILITIES", ratio=1)
    table.add_column("", ratio=1)
    items = abilities or []
    for i in range(0, max(len(items), 10), 2):
        table.add_row(
            items[i] if i < len(items) else "",
            items[i + 1] if i + 1 < len(items) else "",
        )
    return table


def _equipment(character: FatalModel) -> Table:
    table = Table(box=box.SQUARE, expand=True, show_header=True, header_style="bold white on grey50")
    for title in ("Left Side", "Front/Back", "Right Side"):
        table.add_column(f"{title}\nItem", ratio=2)
        table.add_column("Location", ratio=1)
        table.add_column("Weight", ratio=1)

    def rows(items: list[ItemModel]) -> list[tuple[str, str, str]]:
        data = [(i.item_name, i.location, _val(i.weight)) for i in items]
        while len(data) < 18:
            data.append(("", "", ""))
        return data[:18]

    left = rows(character.left_items or [])
    front = rows(character.front_back_items or [])
    right = rows(character.right_items or [])
    table.add_row(
        Text("EQUIPMENT", style="bold white on grey50", justify="center"),
        *([""] * 8),
        end_section=True,
    )
    for i in range(18):
        l = left[i]
        f = front[i]
        r = right[i]
        table.add_row(l[0], l[1], l[2], f[0], f[1], f[2], r[0], r[1], r[2])
    return table


def _wealth_and_advancement(character: FatalModel) -> Table:
    table = Table(box=box.SQUARE, expand=True, show_header=False, padding=(0, 1))
    table.add_column(ratio=1)
    table.add_column(ratio=1)
    table.add_row(
        Text("ADVANCEMENT POINTS", style="bold white on grey50", justify="center"),
        Text("WEALTH", style="bold white on grey50", justify="center"),
        end_section=True,
    )
    table.add_row(str(character.advancement_points), f"Bronze: {character.bronze}")
    table.add_row("", f"Copper: {character.copper}")
    table.add_row("", f"Silver: {character.silver}")
    table.add_row("", f"Electrum: {character.electrum}")
    table.add_row("", f"Gold: {character.gold}")
    table.add_row("", f"Gems: {character.gems}")
    table.add_row("", f"Jewelry: {character.jewelry}")
    table.add_row("", f"Plunder: {character.plunder}")
    table.add_row(
        f"Needed for Next Level: {character.ap_needed_for_next_level}",
        "",
    )
    return table


def _encumbrance(character: FatalModel) -> Table:
    table = Table(box=box.SQUARE, expand=True, show_header=True, header_style="bold white on grey50")
    headers = [
        "Unencumbered\n(100% Sprint / 100% Agility)",
        "Light Load\n(75% / 95%)",
        "Medium Load\n(50% / 85%)",
        "Heavy Load\n(25% / 75%)",
        "Pull/Push",
    ]
    for header in headers:
        table.add_column(header, justify="center")
    table.add_row(
        _val(character.unencumbered),
        _val(character.light_load),
        _val(character.medium_load),
        _val(character.heavy_load),
        _val(character.pull_push),
    )
    return Panel(table, title="ENCUMBRANCE", box=box.SQUARE)


def _henchmen(henchmen: list | None) -> Table:
    table = Table(box=box.SQUARE, expand=True, show_header=True, header_style="bold white on grey50")
    headers = ["Name", "Race/Occupation", "Current Armor", "Attack Skill Bonus", "# Attacks", "Damage", "Life Points", "Sprint", "Drive"]
    for header in headers:
        table.add_column(header)
    rows = henchmen or []
    for i in range(max(len(rows), 10)):
        if i < len(rows):
            h = rows[i]
            table.add_row(
                h.name,
                f"{h.race}/{h.occupation}".strip("/"),
                _val(h.current_armor),
                _val(h.attack_skill_bonus),
                _val(h.number_of_attacks),
                _val(h.damage),
                _val(h.life_points),
                _val(h.sprint),
                _val(h.drive),
            )
        else:
            table.add_row("", "", "", "", "", "", "", "", "")
    return Panel(table, title="HENCHMEN / FAMILIARS / SLAVES", box=box.SQUARE)


def _notes(character: FatalModel) -> Panel:
    allergies = ", ".join(character.allergies) if character.allergies else ""
    illnesses = ", ".join(character.mental_illnesses) if character.mental_illnesses else ""
    text = (
        f"Allergies:\n{allergies or '—'}\n\n"
        f"Mental Illnesses:\n{illnesses or '—'}\n\n"
        f"Miscellaneous Notes:\n{character.misc_notes or '—'}"
    )
    return Panel(text, title="Notes", box=box.SQUARE)


def _skills_table(character: FatalModel) -> Table:
    table = Table(box=box.SQUARE, expand=True, show_header=True, header_style="bold white on grey50")
    table.add_column("Skill", ratio=2)
    table.add_column("Related Ability", ratio=2)
    table.add_column("Total Mod.", justify="right", width=8)
    table.add_column("Skill Mod.", justify="right", width=8)
    table.add_column("Points Invested", justify="right", width=10)
    table.add_column("Learning Curve", justify="right", width=10)
    skills = []
    for name, value in character:
        if isinstance(value, SkillModel):
            skills.append((name, value))
    for name, skill in sorted(skills, key=lambda item: _skill_name(item[0])):
        table.add_row(
            _skill_name(name),
            _related_abilities(skill),
            _val(skill.total_modifier),
            _val(skill.skill_modifier),
            _val(skill.points_invested),
            _val(skill.learning_curve),
        )
    return Panel(table, title="SKILLS", box=box.SQUARE)


def _body_part_row(label: str, part) -> list[str]:
    return [label, _val(part.bpp), _val(part.cab), _val(part.cah), _val(part.cap), _val(part.cas)]


def _body_parts(character: FatalModel) -> Group:
    parts_table = Table(box=box.SQUARE, expand=True, show_header=True, header_style="bold white on grey50")
    parts_table.add_column("Body Part", ratio=1)
    parts_table.add_column("BPP", justify="right", width=5)
    parts_table.add_column("CAB", justify="right", width=5)
    parts_table.add_column("CAH", justify="right", width=5)
    parts_table.add_column("CAP", justify="right", width=5)
    parts_table.add_column("CAS", justify="right", width=5)

    body_parts = [
        ("Head", character.head),
        ("Face", character.face),
        ("Torso, U.", character.upper_torso),
        ("Torso, L.", character.lower_torso),
        ("Groin", character.groin),
        ("Arm, Upper, R.", character.upper_right_arm),
        ("Arm, Upper, L.", character.upper_left_arm),
        ("Arm, Lower, R.", character.lower_right_arm),
        ("Arm, Lower, L.", character.lower_left_arm),
        ("Hand, Right", character.right_hand),
        ("Hand, Left", character.left_hand),
        ("Leg, Upper, R.", character.upper_right_leg),
        ("Leg, Upper, L.", character.upper_left_leg),
        ("Leg, Lower, R.", character.lower_right_leg),
        ("Leg, Lower, L.", character.lower_left_leg),
        ("Foot, Right", character.right_foot),
        ("Foot, Left", character.left_foot),
    ]
    if character.tail.bpp or character.tail.cab:
        body_parts.append(("Tail", character.tail))
    if character.wings.bpp or character.wings.cab:
        body_parts.append(("Wings", character.wings))

    for label, part in body_parts:
        parts_table.add_row(*_body_part_row(label, part))

    armor_table = Table(box=box.SQUARE, expand=True, show_header=True, header_style="bold white on grey50")
    armor_table.add_column("Armor Description", ratio=2)
    armor_table.add_column("Locations", ratio=2)
    armor_table.add_column("CAB", justify="right", width=5)
    armor_table.add_column("CAH", justify="right", width=5)
    armor_table.add_column("CAP", justify="right", width=5)
    armor_table.add_column("CAS", justify="right", width=5)
    for armor in character.armors or [None]:
        if armor is None:
            armor_table.add_row("", "", "", "", "", "")
            continue
        armor_table.add_row(
            armor.armor or armor.armor_type,
            ", ".join(armor.body_locations),
            _val(armor.cab_reduction),
            _val(armor.cah_reduction),
            _val(armor.cap_reduction),
            _val(armor.cas_reduction),
        )

    modifiers = Table(box=box.SQUARE, expand=True, show_header=True, header_style="bold white on grey50")
    for header in [
        "Base Current Armor",
        "Agility Modifier",
        "Armor (General) Mod.",
        "Armor (Specific) Mod.",
        "Magical Modifiers",
        "Miscellaneous Modifiers",
    ]:
        modifiers.add_column(header, justify="center")
    general = getattr(character.armor_general_type, "total_modifier", "")
    specific = getattr(character.armor_specific, "total_modifier", "")
    modifiers.add_row(
        _val(character.current_armor),
        _val(character.agility_modifier),
        _val(general),
        _val(specific),
        "",
        "",
    )

    return Group(
        Panel(parts_table, title="FATAL Character Body Parts", box=box.SQUARE),
        Panel(armor_table, title="Armor by Location", box=box.SQUARE),
        Panel(modifiers, title="Current Armor Modifiers", box=box.SQUARE),
    )


def _spells_known(character: FatalModel) -> Table:
    counts = {level: 0 for level in range(1, 11)}
    for spell in character.spells or []:
        if 1 <= spell.level <= 10:
            counts[spell.level] += 1
    table = Table(box=box.SQUARE, expand=True, show_header=True, header_style="bold white on grey50")
    table.add_column("Spell Level", justify="center")
    for level in range(1, 11):
        table.add_column(f"{level}{'st' if level == 1 else 'nd' if level == 2 else 'rd' if level == 3 else 'th'}", justify="center")
    table.add_row("Spells Known", *[str(counts[level]) for level in range(1, 11)])
    return table


def _spell_block(spell: SpellModel | None) -> Panel:
    if spell is None:
        spell = SpellModel()
    ingredients = ", ".join(spell.ingredients) if spell.ingredients else ""
    text = (
        f"Spell: {spell.spell_name:<28} Discipline: {spell.discipline}\n"
        f"Level: {spell.level:<10} Range: {spell.spell_range}\n"
        f"Duration: {spell.duration:<8} Area: {spell.area}\n"
        f"Effect:\n{spell.effect or '—'}\n"
        f"{'─' * 72}\n"
        f"Chant: {spell.chant:<24} Skill Points Invested: {spell.skill_points_invested}\n"
        f"Ingredients: {ingredients}\n"
        f"Pages in Spellbook: {spell.pages_in_spellbook:<6} Ingredients stored where: {spell.ingredients_stored_where}\n"
        f"Type: {spell.spell_type}   Ritual: {spell.ritual or '—'}"
    )
    return Panel(text, box=box.SQUARE)


def _spells(character: FatalModel) -> Group:
    known = _spells_known(character)
    description = Panel(
        character.spellbook_description or "—",
        title="Describe Spellbook",
        box=box.SQUARE,
    )
    spells = character.spells or []
    blocks = [_spell_block(spell) for spell in spells]
    while len(blocks) < 4:
        blocks.append(_spell_block(None))
    return Group(
        known,
        description,
        *blocks[:4],
        *([_spell_block(spell) for spell in spells[4:]] if len(spells) > 4 else []),
    )


def print_fatal_model(character: FatalModel, *, file: Any | None = None) -> None:
    """Print a FatalModel to the terminal in character-sheet layout."""
    out = Console(file=file) if file is not None else console
    out.print()
    out.print(Panel(Text("FATAL CHARACTER SHEET", style="bold white on grey23", justify="center"), box=box.DOUBLE))
    out.print(_general_info(character))
    out.print(_abilities_table(character))
    out.print(_point_totals(character))
    out.print()
    out.print(_disposition(character))
    out.print(_initiative(character))
    out.print(_weapons_table(character.weapons))
    out.print(_armors_table(character.armors))
    out.print(_sexual_and_rare(character))
    out.print()
    out.print(_languages(character))
    out.print(_special_abilities(character.special_abilities))
    out.print(_equipment(character))
    out.print(_wealth_and_advancement(character))
    out.print()
    out.print(_encumbrance(character))
    out.print(_henchmen(character.henchmen))
    out.print(_notes(character))
    out.print()
    out.print(_skills_table(character))
    out.print()
    out.print(_body_parts(character))
    out.print()
    out.print(Panel(_spells(character), title="SPELLS", box=box.SQUARE))
    out.print()
