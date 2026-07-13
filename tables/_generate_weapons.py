"""Generate tables/weapons.py from weapon table data."""

from __future__ import annotations

import re
from pathlib import Path


def clean(value: str) -> str:
    value = value.strip()
    if value in {"-", "NA", "See Weapon"}:
        return "0"
    if value == "-:A":
        return "0:A"
    if value == "S:-":
        return "S:0"
    return value.replace("-/", "0/").replace("/-", "/0")


def parse_weight(value: str) -> float:
    value = clean(value)
    if value == "varies":
        return 0
    return float(value)


def parse_lmh(value: str) -> tuple[int, int, int]:
    if clean(value) == "0" and "See" in value:
        return 0, 0, 0
    parts = [part.strip() for part in value.replace(" ", "").split("/")]
    result: list[int] = []
    for part in parts:
        if part in {"", "-", "SeeWeapon"}:
            result.append(0)
        else:
            result.append(int(part))
    while len(result) < 3:
        result.append(0)
    return result[0], result[1], result[2]


def normalize_damage(value: str) -> str:
    value = clean(value)
    return re.sub(r"\s*\+\s*", "+", value)


def row(
    weapon: str,
    weapon_type: str,
    size: str,
    weight: str,
    weight_distribution: str,
    fulcrum_range: str,
    damage: str,
    penetration: str,
    weapon_range: str = "",
) -> dict:
    l, m, h = parse_lmh(penetration)
    return {
        "weapon": weapon,
        "weapon_type": clean(weapon_type),
        "size": clean(size),
        "weight": parse_weight(weight),
        "weight_distribution": clean(weight_distribution),
        "fulcrum_range": clean(fulcrum_range),
        "weapon_range": clean(weapon_range),
        "damage": normalize_damage(damage),
        "l": l,
        "m": m,
        "h": h,
    }


MELEE_WEAPONS = [
    row("Axe, Battle, Footman's (2H)(w/o back spike)", "H:SA", 'M 48"', "4", "0.90", "5-90", "3d10+2", "-/5/-10"),
    row("Axe, Battle, Horseman's (w/back spike)", "H(S):SA", 'S 24"', "3", "0.85", "10-90", "1d12+1", "-/5/-15"),
    row("Axe, Hand (Hatchet) (also thrown)", "H:A", 'T 15"', "2", "0.80", "10-90", "1d10", "-/-10/-20"),
    row("Club", "P:SA", 'S 24"', "2", "0.60", "10-90", "2d6", "-/-/-5"),
    row("Club, Great (2H)", "P:S", 'M 36-48"', "4", "0.60", "5-90", "3d8", "-/-/-5"),
    row("Dagger (double-edged) (also thrown)", "S:A", 'T 11-18"', "1", "-", "-", "1d10", "-/-5/-20"),
    row("Dagger, Dirk (single edge)", "S:A", 'S 17-21"', "2", "-", "-", "1d12", "-/-10/-25"),
    row("Dagger, Stiletto(triple edge)", "S:A", 'T 12"', "1", "-", "-", "1d20", "-/-/-10"),
    row(
        "Flail, Footman's, Holy Water Sprinkler (2H) [swivel end link (no chain) w/ attached 8\" spiked mace]",
        "P:SA",
        'M 36" staff +8"',
        "12",
        "0.60",
        "5-70",
        "3d10+3",
        "-/-/-5",
    ),
    row(
        "Flail, Footman's Military (2H) [swivel end link (no chain) w/ attached 15\" sectioned + spiked rod]",
        "P:SA",
        'M 36" staff +15"',
        "13",
        "0.60",
        "5-70",
        "3d12+2",
        "-/-/-5",
    ),
    row("Flail, Horseman's (w/ chain and one spiked ball)", "P:SA", 'S 24" staff +12"', "6", "0.80", "10-60", "2d10+1", "-/-5/-10"),
    row("Flail, Horseman's (w/ chains + two spiked balls)", "P:SA", 'S 24" staff +12"', "7", "0.80", "10-60", "2d10+3", "-/-5/-10"),
    row("Garrote (2H) (thin wire for choking)", "-:A", 'S 24"', "1", "-", "-", "3d8 (see description)", "-/-/-50"),
    row("Hammer, Maul (2H) (military sledge of stone)", "P:S", 'M 36"', "10", "0.90", "5-90", "4d12+4", "-/-/-5"),
    row("Hammer, War, Footman's (2H) (with back spike)", "P(S):SA", 'M 30-33"', "3", "0.70", "5-90", "3d10+2", "-/-5/-15"),
    row("Hammer, War, Horseman's (with back spike) (also thrown)", "P(S):SA", 'S 24"', "2", "0.80", "10-90", "1d20+2", "-/-5/-15"),
    row("Lance, Light (blunted end, hollow pole)", "P:SA", 'L 60"', "5", "-", "-", "1d12+2", "-/-5/-10"),
    row("Lance, Heavy (x2 charge)", "S:SA", 'L 168"', "10", "-", "-", "1d20+3", "-/-5/-10"),
    row("Lance, Jousting (x2 set charge) (blunted end)", "P:SA", 'L 168"', "6", "-", "-", "1d12+3", "-/-/-"),
    row("Mace, Footman's (2H)", "P:SA", 'M 36"', "6", "0.85", "5-90", "3d10+3", "-/-/-10"),
    row("Mace, Horseman's", "P:SA", 'S 24"', "4", "0.90", "10-90", "1d20+3", "-/-5/-15"),
    row("Mace-axe (2H)", "H/P:SA", 'M 36"', "7", "0.90", "5-90", "3d10+4", "-/-/-10"),
    row("Morgenstern (Morningstar) (2H)", "S/P:SA", 'M 48"', "8", "-/0.80", "5-90", "3d10+3", "-/-5/-10"),
    row("Pick, Military, Footman's (2H) (also called the Bisacuta, Oucin, Besague)", "H(S):SA", 'M 48"', "6", "0.85", "5-90", "3d10+3", "-/-5/-10"),
    row("Pick, Military, Horseman's", "H(S):SA", 'S 24"', "4", "0.80", "10-90", "1d20+3", "-/-5/-15"),
    row("Polearm, Awl Pike (2H) (x2 set charge)", "S:SA", 'L 216-264"', "12", "-", "-", "2d10+2", "-/-5/-15"),
    row("Polearm, Berdeesh (2H) (Bardiche or Sparth Axe)", "H:SA", 'L 60"', "7", "0.85", "5-90", "3d10+3", "-/-5/-10"),
    row("Polearm, Bec de Corbin (Raven's Beak) (2H)", "S/P:SA", 'L 72"', "6", "0.80", "0/5-90", "2d10/2d12+1", "-/-5/-10"),
    row("Polearm, Bill (2H)", "S/H:SA", 'L >95"', "10", "0.85", "0/5-90", "2d10/3d10+2", "-/-5/-15"),
    row("Polearm, Bipennis (2H) (double-bladed Poleaxe)", "H:SA", 'L 72"', "12", "0.90", "5-90", "3d12+2", "-/-/-10"),
    row("Polearm, Fauchard (2H)", "H:SA", 'L >95"', "7", "0.75", "5-90", "3d10+2", "-/-/-15"),
    row("Polearm, Glaive (2H)", "H:SA", 'L >95"', "8", "0.80", "5-90", "2d10", "-/-10/-20"),
    row("Polearm, Guisarme (2H)", "H:SA", 'L >71"', "8", "0.75", "5-90", "3d10+2", "-/-5/-10"),
    row("Polearm, Halberd (2H) (x2 set charge)", "S/H:SA", 'L 60-96"', "10", "0.85", "0/5-90", "2d10/3d12+1", "-/-5/-5"),
    row("Polearm, Military Fork (2H) (x2 set charge)", "S:SA", 'L >83"', "7", "0.80", "-", "2d12", "-/-5/-10"),
    row("Polearm, Partisan (2H) (x2 set charge)", "S:SA", 'L >83"', "8", "0.75", "-", "2d12", "-/-5/-15"),
    row("Polearm, Poleaxe (single-bladed Bipennis w/spikes on back and tip) (2H)", "S/H:SA", 'L 60-72"', "10", "0.85", "0/5-90", "2d10/3d12", "-/-/-10"),
    row("Polearm, Ranseur (2H) (x2 set charge)", "S:SA", 'L >95"', "7", "0.75", "-", "2d10+1", "-/-5/-10"),
    row("Polearm, Spetum (2H) (x2 set charge)", "S:SA", 'L >95"', "7", "0.75", "-", "2d10+1", "-/-5/-10"),
    row("Polearm, Voulge (2H) (Lochaber axe)", "H:SA", 'L >95"', "10", "0.85", "5-90", "3d10+2", "-/-5/-10"),
    row("Quarterstaff (iron end-caps)", "P:SA", 'L 60-72"', "3", "0.50", "5-90", "1d10", "-/-20/-80"),
    row("Sap", "P:SA", 'T 12"', "3", "0.90", "5-90", "1d8", "-/-5/-50"),
    row("Spear, Long (2H) (x2 set charge)", "S:SA", 'L <156"', "5", "0.90", "-", "2d10", "-/-5/-15"),
    row("Spear, Medium (also thrown)", "S:SA", 'L 48-84"', "3", "0.85", "-", "2d10", "-/-5/-15"),
    row("Spear, Short (half-spear or guard spear)", "S:SA", 'S 27"', "3", "0.80", "-", "2d10", "-/-5/-15"),
    row("Spear, Trident (2H)", "S:SA", 'M 48-96"', "6", "0.80", "-", "3d6", "-/-5/-10"),
    row("Strike, Unarmed (see Brawling skill)", "P:A", "0", "0", "-", "-", "(see Brawling skill)", "-/-50/-90"),
    row("Sword, Bastard (Hand-and-a-Half)", "H:SA", 'L 43-51"', "7", "0.25", "5-15", "3d12+1", "-/-5/-10"),
    row("Sword, Broadsword (seemingly, the average of swords)", "H:SA", 'M 34-46"', "3", "0.40", "5", "2d12", "-/-5/-15"),
    row("Sword, Cut + Thrust (thick sword of medium length)", "S/H:SA", 'M 37-40"', "4", "-/0.30", "-/10", "2d10/2d12", "-/-/-15"),
    row("Sword, Falchion (curved blade, weighted end, single edge)", "H:SA", 'S 28-30"', "4", "0.50", "10", "3d6", "-/-5/-15"),
    row("Sword, Flamberge (2H) (wavy blade)", "S:SA", 'L 48-64"', "10", "-", "-", "3d10", "-/-/-10"),
    row("Sword, Gladius", "S/H:SA", 'S 28"', "3", "-/0.20", "-/10", "2d10/4d8", "-/-5/-15"),
    row("Sword, Long (thin blade that is long for a one-handed sword)", "S:SA", 'M 34-42"', "4", "-", "-", "1d20", "-/-5/-15"),
    row("Sword, Short (sometimes called an Archer's sword)", "S:SA", 'S 22-31"', "3", "-", "-", "3d6", "-/-5/-15"),
    row("Sword, Zweihander (2H)", "S/H:S", 'L 58-75"', "15", "-/0.35", "-/5-30", "2d10/4d12", "-/-/-10"),
    row("Whip (subdual damage)", "H:A", 'M 96"', "2", "0.15", "5", "1d4", "-/-80/-95"),
    row("Whip, Bull", "H:A", 'L 168"', "3", "0.10", "5", "1d6", "-/-70/-90"),
    row("Whip, Cat-o-nine tails (subdual damage)", "H:A", 'T 18"', "1", "0.20", "5", "1", "-/-80/-95"),
    row("Whip, Scourge (a Cat-o-nine tails with barbs)", "H:A", 'T 18"', "1", "0.25", "5", "1d6", "-/-75/-90"),
]

MISCELLANEOUS_WEAPONS = [
    row("Axe, Hand (Hatchet)", "H:A", 'T 15"', "2", "0.85", "10-90", "1d10", "-/-10/-20", "(Strength/10)'"),
    row("Bottle (if broken, treat as a knife)", "P:A", 'T 12"', "1", "0.75", "20", "1d8", "-/-5/-15", "(Strength/10)'"),
    row("Bucket", "P:SA", 'T 15"', "2", "0.75", "10", "1d4", "-/-10/-20", "-"),
    row("Chain", "P:SA", 'L 60"', "5", "0.50", "5", "1d6", "-/-10/-20", "-"),
    row("Chair (2H)", "P:SA", 'M 36"', "3", "0.75", "5-90", "1d8", "-/-10/-20", "-"),
    row("Cleaver", "H:A", 'T 12"', "2", "0.75", "10", "1d10", "-/-10/-20", "(Strength/10)'"),
    row("File, Metal", "P:A", 'T <12"', "1", "0.50", "10-90", "1d4", "-/-10/-20", "-"),
    row("Flail, Grain (wood joined by rope)", "P:SA", 'S 30"', "2", "0.30", "10-60", "1d8", "-/-10/-20", "-"),
    row("Fork, Pitch (2H)", "S:SA", 'L >83"', "6", "NA", "NA", "2d6", "-/-5/-15", "-"),
    row("Fork, Serving", "S:A", 'T 12"', "1", "NA", "NA", "1d6", "-/-5/-25", "-"),
    row("Gauntlet", "P:SA", 'T <12"', "2", "0.50", "NA", "1d4", "-/-5/-15", "-"),
    row("Hammer, Tool (w/o back spike)", "P:A", 'T 15"', "2", "0.90", "10-90", "2d10", "-/-5/-10", "(Strength/10)'"),
    row("Hammer, Sledge (2H)", "P:S", 'M 36"', "8", "0.90", "10-90", "2d20", "-/-/-5", "-"),
    row("Hoe (2H)", "H:SA", 'M 36-48"', "3", "0.75", "10-90", "1d6", "-/-10/-20", "-"),
    row("Hook, Grappling", "S/P:SA", 'T 18"', "4", "0.75", "10-70", "1d6", "-/-5/-10", "(Strength/10)'"),
    row("Knife, Hunting or Tool (single edge)", "S:A", 'T 8-13"', "1", "NA", "NA", "1d8", "-/-15/-25", "(Strength/10)'"),
    row("Mallet (all wood)", "P:A", 'T 12"', "2", "0.80", "10-75", "1d4", "-/-5/-20", "-"),
    row("Quill", "S:A", 'T 12"', "-", "NA", "NA", "1d2", "-/-30/-95", "-"),
    row("Pan, Frying (Iron)", "P:SA", 'S 18"', "4", "0.75", "10", "1d8", "-/-5/-15", "-"),
    row("Pry bar (Crowbar)", "P:SA", 'T 18"', "3", "0.50", "10-90", "1d8", "-/-5/-15", "-"),
    row("Rolling Pin", "P:SA", 'T 12"', "2", "0.60", "10", "1d4", "-/-5/-20", "-"),
    row("Scissors", "S:A", 'T <10"', "0.5", "NA", "NA", "1d6", "-/-5/-25", "-"),
    row("Scythe (2H)", "H(S):SA", 'L 60"', "5", "0.50", "10-90", "2d8", "-/-10/-20", "-"),
    row("Shield", "P:SA", "varies", "varies", "0.50", "50", "1d2", "-/-5/-10", "-"),
    row("Shoe", "P:A", 'T <12"', "0.5", "0.50", "50", "1d2", "-/-5/-25", "(Strength/10)'"),
    row("Shoe, Horse", "P:SA", 'T <8"', "2", "0.50", "50", "1d4", "-/-5/-20", "(Strength/10)'"),
    row("Shovel (2H)", "H/P:SA", 'M 36-48"', "4", "0.80", "10-90", "1d8", "-/-5/-15", "-"),
    row("Sickle", "H(S):A", 'T 18"', "2", "0.40", "10", "1d12", "-/-15/-25", "-"),
    row("Spade (2H)", "H/P:SA", 'M 36-48"', "3", "0.85", "10-90", "1d8", "-/-5/-15", "-"),
    row("Targe (Spiked Shield)", "S:SA", 'S 24"', "6", "0.50", "50", "1d8", "-/-5/-20", "-"),
    row("Torch (a burning club)", "P:SA", 'S 24"', "1", "0.55", "10-90", "2d10", "-/-5/-15", "-"),
]

MISSILE_WEAPONS = [
    row("Arrows (12 w/quiver)", "S:-", 'S 30"', "2", "See Weapon", "See Weapon", "See Weapon", "See Weapon", "See Weapon"),
    row("Axe, Hand (Hatchet)", "H:SA", 'T 15"', "2", "(Strength/10)'", "20", "1d10", "-/-10/-20", "(Strength/10)'"),
    row("Bolas", "P:SA", 'S 24"', "2", "(Strength/5)'", "20", "3d4", "-/-20/-90", "(Strength/5)'"),
    row("Bolts (20 w/ quiver)", "S:-", 'T 18"', "3", "See Weapon", "See Weapon", "See Weapon", "See Weapon", "See Weapon"),
    row("Boomerang (does not return to thrower)", "P:A", 'T 18"', "1", "(Strength/5)'", "10", "1d6", "-/-10/-20", "(Strength/5)'"),
    row("Bottle (if broken, treat as a knife)", "P:SA", 'T 12"', "1", "(Strength/10)'", "10", "1d8", "-/-5/-15", "(Strength/10)'"),
    row("Bottle, Oil (with ignited wick) (Molotov cocktail)", "P:SA", 'T 12"', "2", "(Strength/10)'", "20", "1d20/then1d10", "-/-5/-10", "(Strength/10)'"),
    row("Bow, Short (2H) (can use mounted)", "S:A", 'M 48"', "2", "60'", "20", "1d12", "-/-20/-50", "60'"),
    row("Bow, Long (2H) (too big to use mounted)", "S:A", 'L 66-79"', "3", "100'", "30", "1d20", "-/-5/-10", "100'"),
    row("Cleaver", "H:SA", 'T 12"', "2", "(Strength/10)'", "10", "1d10", "-/-10/-20", "(Strength/10)'"),
    row(
        "Crossbow, Hand (2H) (drawn by the hand) [Note: Crossbows and crossbowmen are also called arbalests + arbalestiers.]",
        "S:A",
        'M 36"',
        "7",
        "80'",
        "70",
        "2d10+1",
        "-/-/-5",
        "80'",
    ),
    row(
        "Crossbow, Wheel + Ratchet (2H) (must be cranked) [Note: Crossbows and crossbowmen are also called arbalests + arbalestiers. 400 draw lbs. required.]",
        "S:A",
        'M 36"',
        "14",
        "120'",
        "100",
        "3d10+2",
        "-/-/-",
        "120'",
    ),
    row("Dagger (double-edged)", "S:A", 'T 11-18"', "1", "(Strength/10)'", "10", "1d10", "-/-5/-20", "(Strength/10)'"),
    row("Dart", "S:A", 'T 18"', "0.5", "(Strength/5)'", "5", "1d8", "-/-25/-75", "(Strength/5)'"),
    row("Flask", "P:SA", 'T 72"', "1", "(Strength/10)'", "10", "1d4", "-/-10/-25", "(Strength/10)'"),
    row("Flask, Oil (with ignited wick)", "P:SA", 'T 72"', "1", "(Strength/10)'", "10", "1d8/then1d4", "-/-10/-20", "(Strength/10)'"),
    row("Hammer, Tool (w/o back spike)", "P:SA", 'T 15"', "2", "(Strength/10)'", "20", "1d12", "-/-5/-10", "(Strength/10)'"),
    row("Hammer, War, Horseman's (with back spike)", "P(S):SA", 'S 24"', "2", "(Strength/10)'", "20", "1d20+2", "-/-5/-15", "(Strength/10)'"),
    row("Hook, Grappling", "S/P:SA", 'T 18"', "4", "(Strength/10)'", "40", "1d6", "-/-5/-10", "(Strength/10)'"),
    row("Hudbat (all metal hand ax)", "H(S):SA", 'S 22"', "4", "(Strength/10)'", "40", "1d20", "-/-5/-15", "(Strength/10)'"),
    row("Javelin", "S:SA", 'M 60"', "2", "(Strength/4)'", "20", "1d12", "-/-10/-25", "(Strength/4)'"),
    row("Knife, Hunting or Tool (single edge)", "S:A", 'T 8-12"', "1", "(Strength/10)'", "10", "1d8", "-/-15/-25", "(Strength/10)'"),
    row("Knife, Throwing (double-edged)", "S:A", 'T <8"', "0.5", "(Strength/5)'", "5", "1d6", "-/-10/-20", "(Strength/5)'"),
    row("Net, Weighted", "P:SA", 'L 120"', "10", "(Strength/10)'", "100", "-", "-/-/-", "(Strength/10)'"),
    row("Pilum", "S:SA", 'L 72-84"', "1", "(Strength/4)'", "10", "1d12", "-/-5/-10", "(Strength/4)'"),
    row("Rock", "P:A", 'T 3"', "1", "(Strength/4)'", "10", "1d8", "-/-5/-25", "(Strength/4)'"),
    row("Sling (2H)", "P:SA", 'S 24-36"', "1", "(Strength/2)'", "5", "1d8+1", "-/-5/-25", "(Strength/2)'"),
    row("Spear, Medium", "S:SA", 'L 60-84"', "3", "(Strength/5)'", "30", "2d10", "-/-5/-15", "(Strength/5)'"),
    row("Vial", "P:SA", 'T 4"', "0.5", "(Strength/5)'", "5", "1d4", "-/-10/-50", "(Strength/5)'"),
]


def render_weapon(weapon: dict) -> str:
    lines = ["    WeaponModel("]
    for key in (
        "weapon",
        "weapon_type",
        "size",
        "weight",
        "weight_distribution",
        "fulcrum_range",
        "weapon_range",
        "damage",
        "l",
        "m",
        "h",
    ):
        value = weapon[key]
        if isinstance(value, str):
            lines.append(f"        {key}={value!r},")
        elif isinstance(value, float) and value.is_integer():
            lines.append(f"        {key}={int(value)},")
        else:
            lines.append(f"        {key}={value!r},")
    lines.append("    ),")
    return "\n".join(lines)


def main() -> None:
    all_weapons = MELEE_WEAPONS + MISCELLANEOUS_WEAPONS + MISSILE_WEAPONS
    lines = [
        "from models.character_models import WeaponModel",
        "",
        "",
        "weapons_table = [",
    ]
    for weapon in all_weapons:
        lines.append(render_weapon(weapon))
    lines.append("]")
    lines.append("")
    Path("tables/weapons.py").write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {len(all_weapons)} weapons to tables/weapons.py")


if __name__ == "__main__":
    main()
