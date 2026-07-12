from pydantic import BaseModel
from typing import List


class SkillModel(BaseModel):
    related_abilities: List[str] = []
    total_modifier: int = 0
    skill_modifier: int = 0
    points_invested: int = 0
    learning_curve: int = 0


class BodyModel(BaseModel):
    bpp: int = 0
    cab: int = 0
    cah: int = 0
    cap: int = 0
    cas: int = 0


class ItemModel(BaseModel):
    item_name: str = ""
    location: str = ""
    weight: int = 0


class HenchModel(BaseModel):
    name: str = ""
    race: str = ""
    occupation: str = ""
    current_armor: int = 0
    attack_skill_bonus: int = 0
    number_of_attacks: int = 0
    damage: int = 0
    life_points: int = 0
    sprint: int = 0
    drive: int = 0


class WeaponModel(BaseModel):
    weapon: str = ""
    skill_modifier: int = 0
    breadth: int = 0
    weapon_type: str = ""
    size: int = 0
    weight: int = 0
    weight_distribution: int = 0
    fulcrum_range: int = 0
    delivery_penalty: int = 0
    damage: int = 0
    l: int = 0
    m: int = 0
    h: int = 0


class ArmorModel(BaseModel):
    armor: str = ""
    armor_type: str = ""
    armor_bonus: int = 0
    ip: int = 0
    agility_loss: int = 0
    weight: int = 0
    modifer_to_hide: int = 0
    modifer_to_silence: int = 0
    spell_failure: int = 0
    special_properties: str = ""
    cab_reduction: int = 0
    cah_reduction: int = 0
    cap_reduction: int = 0
    cas_reduction: int = 0


class SpellModel(BaseModel):
    spell_name: str = ""
    discipline: str = ""
    level: int = 0
    spell_range: int = 0
    duration: int = 0
    area: str = ""
    effect: str = ""
    chant: str = ""
    skill_points_invested: int = 0
    ingredients: List[str] = None
    pages_in_spellbook: int = 0
    ingredients_stored_where: str = ""


class FatalModel(BaseModel):
    """Major Laterals"""
    character_name: str = ""
    gender: str = ""
    race: str = ""
    player_name: str = "John Doe"
    occupation: str = ""
    homeland: str = ""
    level: int = 0
    religion: str = ""
    height: int = 0 # in inches
    weight: int = 0 # in pounds
    siblings: int = 0
    social_class: str = ""
    age: int = 0
    stage_of_life: str = ''
    eyes: str = ""
    skin_color: str = ""
    birth_rank: str = ""
    sexuality: str = ""
    debauchery_value: int = 0
    debauchery: str = ''
    marital_status: str = ""
    birth_status: str = ""
    hair_color: str = ""
    hair_thickness: str = ""
    facial_feature: str = ""
    birthplace: str = ""
    hair_length: str = ''
    hair_type: str = ""
    birthday: str = ""
    vision: str = ''
    most_attractive_feature: str = ""
    most_repulsive_feature: str = ""
    breadth: int = 0
    bmi: str = ""
    appearance: str = ""
    traits: list[str] = []

    """Abilities"""
    physique: int = 0
    physique_modifier: int = 0
    physical_fitness: int = 0
    physical_fitness_modifier: int = 0
    sprint: int = 0
    strength: int = 0
    strength_modifier: int = 0
    dmg: int = 0
    cj: int = 0
    bench: int = 0
    dl: int = 0
    bodily_attractiveness: int = 0
    bodily_attractiveness_modifier: int = 0
    health: int = 0
    health_modifier: int = 0
    int_vom: int = 0
    health_all: int = 0
    im: int = 0
    current_armor: int = 0

    charisma: int = 0
    charisma_modifier: int = 0
    facial: int = 0
    facial_modifier: int = 0
    facial_description: str = ""
    vocal: int = 0
    vocal_modifier: int = 0
    vocal_description: str = ""
    kinetic: int = 0
    kinetic_modifier: int = 0
    kinetic_description: str = ""
    rhetorical: int = 0
    rhetorical_modifier: int = 0
    rhetorical_description: int = 0
    average_speech_rate: int = 0

    dexterity: int = 0
    dexterity_modifer: int = 0
    hand_eye_coordination: int = 0
    hand_eye_coordination_modifier: int = 0
    finger_movement_precision: int = 0
    agility: int = 0
    agility_modifier: int = 0
    ca_bonus: int = 0
    brawling: int = 0
    stand: int = 0
    reaction_speed: int = 0
    reaction_speed_modifier: int = 0
    deep_sleep_recovery: int = 0
    ennunciation: int = 0
    ennunciation_modifier: int = 0
    maximum_speech_rate: int = 0
    casting: str = ""

    intelligence: int = 0
    intelligence_modifier: int = 0
    intelligence_range: int = 0
    language: int = 0
    language_modifier: int = 0
    max_num_of_languages: int = 0
    number_of_languages: int = 0
    vocabulary: str = ""
    math: int = 0
    math_modifier: int = 0
    highest_possible_math: str = ""
    analytic: int = 0
    analytic_modifier: int = 0
    spatial: int = 0
    spatial_modifier: int = 0
    unfamiliar_object_assembly: int = 0 # number of pieces

    wisdom: int = 0
    wisdom_modifier: int = 0
    drive: int = 0
    drive_modifier: int = 0
    unconscioness: str = ''
    hours_resting: int = 0
    intuition: int = 0
    intuition_modifier: int = 0
    common_sense: int = 0
    common_sense_modifier: int = 0
    likely_to: str = ""
    reflection: int = 0
    reflection_modifier: int = 0
    earliest_memory_at: int = 0

    life_points: int = 0
    magic_points: int = 0
    unconscious: int = 0
    piety_points: int = 0

    """Disposition and Temperment"""

    ethical_points: int = 0
    moral_points: int = 0
    ethicality: str = ''
    morality: str = ''
    disposition: str = ""

    sanguine: int = 0
    choleric: int = 0
    melancholic: int = 0
    phlegmatic: int = 0
    primary_temperment: str = ""
    secondary_temperment: str = ""

    """Equipment"""
    weapons: List[WeaponModel] = None
    armors: List[ArmorModel] = None

    left_items: List[ItemModel] = None
    right_items: List[ItemModel] = None
    front_back_items: List[ItemModel] = None

    """Sexual and Rare"""
    horn_length: int = 0
    manhood_length: int = 0
    manhood_circumference: int = 0
    anal_circumference_potential: str = ''
    anal_depth_potential: float = ''
    vaginal_circumference_potential: int = 0
    vaginal_depth_potential: int = 0
    areola_diameter: float = 0
    areola_hue: str = ''
    nipple_length: float = 0
    cup_size: str = ''
    tongue_size: float = 0
    hymen_resistance: int = 0
    areola_hue: str = ""
    foot_size: str = ''
    fist_circumference: str = ''
    head_circumference: float = 0
    handedness: str = ""
    is_pregnant: bool = False
    is_fat: bool = False
    is_skinny: bool = False
    is_parent: bool = False

    languages_spoken: List[str] = []
    languages_read_and_written: List[str] = []

    special_abilities: List[str] = None

    """Wealth"""
    bronze: int = 0
    copper: int = 0
    silver: int = 0
    electrum: int = 0
    gold: int = 0
    gems: int = 0
    jewelry: int = 0
    plunder: int = 0

    advancement_points: int = 0
    ap_needed_for_next_level: int = 0

    henchmen: List[HenchModel] = None

    """Encumberance"""
    unencumbered: int = 0
    light_load: int = 0
    medium_load: int = 0
    heavy_load: int = 0
    pull_push: int = 0

    """Racism"""
    opinion_on_anakim: int = 0
    opinion_on_bugbear: int = 0
    opinion_on_black_dwarf: int = 0
    opinion_on_brown_dwarf: int = 0
    opinion_on_white_dwarf: int = 0
    opinion_on_dark_elf: int = 0
    opinion_on_light_elf: int = 0
    opinion_on_human: int = 0
    opinion_on_kobold: int = 0
    opinion_on_ogre: int = 0
    opinion_on_cliff_ogre: int = 0
    opinion_on_gruagach_ogre: int = 0
    opinion_on_kinder_fresser_ogre: int = 0
    opinion_on_borbytingarna_troll: int = 0
    opinion_on_hill_troll: int = 0
    opinion_on_subterranean_troll: int = 0

    """Misc"""
    allergies: List[str] = []
    illness_immunity: int = None
    mental_illnesses: List[str] = []
    misc_notes: str = ""
    num_skill_rerolls: int = 0

    """Skills"""
    acting_drama: SkillModel = SkillModel(related_abilities = ['charisma', 'intelligence'])
    agriculture: SkillModel = SkillModel(related_abilities = ['common_sense'])
    aim: SkillModel = SkillModel(related_abilities = ['hand_eye_coordination', 'vision'])
    ambidexterity: SkillModel = SkillModel(related_abilities = ['hand_eye_coordination'])
    anatomy: SkillModel = SkillModel(related_abilities = ['intelligence'])
    animal_conditioning: SkillModel = SkillModel(related_abilities = ['drive', 'inutition'])
    animal_handling: SkillModel = SkillModel(related_abilities = ['intuition'])
    appraise: SkillModel = SkillModel(related_abilities = ['analytic'])
    architecture: SkillModel = SkillModel(related_abilities = ['math', 'spatial'])
    armor_general_type: SkillModel = SkillModel(related_abilities = ['agility'])
    armor_specific: SkillModel = SkillModel(related_abilities = ['agility'])
    armorsmithing: SkillModel = SkillModel(related_abilities = ['spatial'])
    balance: SkillModel = SkillModel(related_abilities = ['agility'])
    basketweaving: SkillModel = SkillModel(related_abilities = ['hand_eye_coordination', 'common_sense'])
    blacksmithing: SkillModel = SkillModel(related_abilities = ['strength', 'spatial'])
    blindfighting: SkillModel = SkillModel(related_abilities = ['hand_eye_coordination', 'reaction_speed', 'intuition'])
    bookbinding: SkillModel = SkillModel(related_abilities = ['common_sense'])
    brass_smithing: SkillModel = SkillModel(related_abilities = ['strength', 'spatial'])
    brawling: SkillModel = SkillModel(related_abilities = ['agility'])
    brewing: SkillModel = SkillModel(related_abilities = ['common_sense'])
    brickmaking: SkillModel = SkillModel(related_abilities = ['common_sense'])
    candlemaking: SkillModel = SkillModel(related_abilities = ['common_sense'])
    carpentry: SkillModel = SkillModel(related_abilities = ['spatial'])
    cartography: SkillModel = SkillModel(related_abilities = ['spatial'])
    catching: SkillModel = SkillModel(related_abilities = ['hand_eye_coordination'])
    charioteering: SkillModel = SkillModel(related_abilities = ['dexterity'])
    chemistry: SkillModel = SkillModel(related_abilities = ['math', 'analytic' 'intuition'])
    cleaning: SkillModel = SkillModel(related_abilities = ['common_sense'])
    climb: SkillModel = SkillModel(related_abilities = ['physical_fitness', 'agility'])
    clockmaking: SkillModel = SkillModel(related_abilities = ['spatial'])
    cobbling: SkillModel = SkillModel(related_abilities = ['common_sense'])
    comedy_buffoonery: SkillModel = SkillModel(related_abilities = ['charisma'])
    comedy_physical: SkillModel = SkillModel(related_abilities = ['charisma', 'agility'])
    comedy_pun: SkillModel = SkillModel(related_abilities = ['charisma'])
    constellations: SkillModel = SkillModel(related_abilities = ['reflection', 'spatical', 'vision'])
    contortion: SkillModel = SkillModel(related_abilities = ['physical_fitness', 'agility'])
    cooking: SkillModel = SkillModel(related_abilities = ['common_sense'])
    coppersmithing: SkillModel = SkillModel(related_abilities = ['spatial', 'strength'])
    cosmetics: SkillModel = SkillModel(related_abilities = ['spatial_intelligence', 'intuition'])
    cosmos_general_planes: SkillModel = SkillModel(related_abilities = ['intelligence'])
    cosmos_specific_plane: SkillModel = SkillModel(related_abilities = ['intelligence'])
    dance: SkillModel = SkillModel(related_abilities = ['kinetic_charisma', 'agility'])
    delousing: SkillModel = SkillModel(related_abilities = ['hand_eye_coordination'])
    diagnosing: SkillModel = SkillModel(related_abilities = ['intelligence', 'wisdom'])
    direction_sense: SkillModel = SkillModel(related_abilities = ['intuition'])
    disarm: SkillModel = SkillModel(related_abilities = ['hand_eye_coordination', 'agility'])
    disguise: SkillModel = SkillModel(related_abilities = ['charisma', 'common_sense'])
    dismemberment: SkillModel = SkillModel(related_abilities = [])
    divination_alectromancy: SkillModel = SkillModel(related_abilities = ['intuition'])
    divination_anthropomancy: SkillModel = SkillModel(related_abilities = ['intuition'])
    divination_aspidomancy: SkillModel = SkillModel(related_abilities = ['intuition'])
    divination_astrology: SkillModel = SkillModel(related_abilities = ['intuition'])
    divination_austromancy: SkillModel = SkillModel(related_abilities = ['intuition'])
    divination_axinomancy: SkillModel = SkillModel(related_abilities = ['intuition'])
    divination_belomancy: SkillModel = SkillModel(related_abilities = ['intuition'])
    divination_ceraunoscopy: SkillModel = SkillModel(related_abilities = ['intuition'])
    divination_chiromancy: SkillModel = SkillModel(related_abilities = ['intuition'])
    divination_cleromancy: SkillModel = SkillModel(related_abilities = ['intuition'])
    divination_crystalomancy: SkillModel = SkillModel(related_abilities = ['intuition'])
    divination_dririmancy: SkillModel = SkillModel(related_abilities = ['intuition'])
    divination_gastromancy: SkillModel = SkillModel(related_abilities = ['intuition'])
    divination_gyromancy: SkillModel = SkillModel(related_abilities = ['intuition'])
    divination_hydromancy: SkillModel = SkillModel(related_abilities = ['intuition'])
    divination_libanomancy: SkillModel = SkillModel(related_abilities = ['intuition'])
    divination_lithomancy: SkillModel = SkillModel(related_abilities = ['intuition'])
    divination_lunomancy: SkillModel = SkillModel(related_abilities = ['intuition'])
    divination_necromancy: SkillModel = SkillModel(related_abilities = ['intuition'])
    divination_numerology: SkillModel = SkillModel(related_abilities = ['intuition'])
    divination_omphalomancy: SkillModel = SkillModel(related_abilities = ['intuition'])
    divination_oneiromancy: SkillModel = SkillModel(related_abilities = ['intuition'])
    divination_onomancy: SkillModel = SkillModel(related_abilities = ['intuition'])
    divination_oomancy: SkillModel = SkillModel(related_abilities = ['intuition'])
    divination_ornithomancy: SkillModel = SkillModel(related_abilities = ['intuition'])
    divination_pyromancy: SkillModel = SkillModel(related_abilities = ['intuition'])
    divination_scatomancy: SkillModel = SkillModel(related_abilities = ['intuition'])
    divination_sortilege: SkillModel = SkillModel(related_abilities = ['intuition'])
    divination_stichomancy: SkillModel = SkillModel(related_abilities = ['intuition'])
    divination_urimancy: SkillModel = SkillModel(related_abilities = ['intuition'])
    divination_xenomancy: SkillModel = SkillModel(related_abilities = ['intuition'])
    dying: SkillModel = SkillModel(related_abilities = ['hand_eye_coordination'])
    enameling: SkillModel = SkillModel(related_abilities = ['hand_eye_coordination'])
    engraving: SkillModel = SkillModel(related_abilities = ['hand_eye_coordination'])
    etiquette: SkillModel = SkillModel(related_abilities = ['common_sense', 'intuition', 'reflection'])
    fishing: SkillModel = SkillModel(related_abilities = ['common_sense'])
    fletching: SkillModel = SkillModel(related_abilities = ['spatial'])
    foresting: SkillModel = SkillModel(related_abilities = ['common_sense'])
    forgery: SkillModel = SkillModel(related_abilities = ['hand_eye_coordination'])
    gambling: SkillModel = SkillModel(related_abilities = ['common_sense', 'math'])
    gemcutting: SkillModel = SkillModel(related_abilities = ['spatial'])
    genealogy: SkillModel = SkillModel(related_abilities = ['common_sense'])
    girdlemaking: SkillModel = SkillModel(related_abilities = ['common_sense'])
    glassblowing: SkillModel = SkillModel(related_abilities = ['spatial'])
    glovemaking: SkillModel = SkillModel(related_abilities = ['spatial'])
    goldsmithing: SkillModel = SkillModel(related_abilities = ['spatial'])
    grooming: SkillModel = SkillModel(related_abilities = ['common_sense'])
    haggling: SkillModel = SkillModel(related_abilities = ['rhetorical_charisma', 'ituition'])
    hairstyling: SkillModel = SkillModel(related_abilities = ['hand_eye_coordination', 'spatial'])
    hatmaking: SkillModel = SkillModel(related_abilities = ['common_sense'])
    heraldry: SkillModel = SkillModel(related_abilities = ['common_sense'])
    herbalism: SkillModel = SkillModel(related_abilities = ['intelligence'])
    hewing: SkillModel = SkillModel(related_abilities = ['strength'])
    hide: SkillModel = SkillModel(related_abilities = ['agility', 'common_sense'])
    history_cultural: SkillModel = SkillModel(related_abilities = ['intelligence'])
    history_legendary: SkillModel = SkillModel(related_abilities = ['intelligence'])
    history_local: SkillModel = SkillModel(related_abilities = ['intelligence'])
    history_military: SkillModel = SkillModel(related_abilities = ['intelligence'])
    hunting: SkillModel = SkillModel(related_abilities = ['hand_eye_coordination', 'vision'])
    hurl: SkillModel = SkillModel(related_abilities = ['hand_eye_coordination', 'vision'])
    impaling: SkillModel = SkillModel(related_abilities = [])
    inkmaking: SkillModel = SkillModel(related_abilities = ['common_sense'])
    intimidation: SkillModel = SkillModel(related_abilities = ['physique', 'charisma'])
    juggling: SkillModel = SkillModel(related_abilities = ['hand_eye_coordination', 'agility'])
    jump: SkillModel = SkillModel(related_abilities = ['physical_fitness'])
    language_read_write: SkillModel = SkillModel(related_abilities = ['language'])
    language_speak: SkillModel = SkillModel(related_abilities = ['language'])
    law: SkillModel = SkillModel(related_abilities = ['intelligence'])
    locksmithing: SkillModel = SkillModel(related_abilities = ['spatial'])
    lock_picking: SkillModel = SkillModel(related_abilities = ['hand_eye_coordination'])
    logic: SkillModel = SkillModel(related_abilities = ['analytic'])
    mangling: SkillModel = SkillModel(related_abilities = [])
    massage: SkillModel = SkillModel(related_abilities = ['hand_eye_coordination', 'kinetic_charisma'])
    math_algebra : SkillModel = SkillModel(related_abilities = ['math'])
    math_fundamental : SkillModel = SkillModel(related_abilities = ['math'])
    math_geometry : SkillModel = SkillModel(related_abilities = ['math'])
    math_trigonometry : SkillModel = SkillModel(related_abilities = ['math'])
    milking: SkillModel = SkillModel(related_abilities = ['hand_eye_coordination', 'common_sense'])
    milling: SkillModel = SkillModel(related_abilities = ['common_sense'])
    mining: SkillModel = SkillModel(related_abilities = ['common_sense'])
    minting: SkillModel = SkillModel(related_abilities = ['common_sense'])
    mountaineering: SkillModel = SkillModel(related_abilities = ['physical_fitness', 'strength', 'agility'])
    mounted_archery: SkillModel = SkillModel(related_abilities = ['hand_eye_coordination', 'agility', 'vision'])
    music_counterpoint: SkillModel = SkillModel(related_abilities = ['analytic', 'math'])
    music_theory: SkillModel = SkillModel(related_abilities = ['math'])
    musical_instrument: SkillModel = SkillModel(related_abilities = ['hand_eye_coordination', 'spatial'])
    nature_animals: SkillModel = SkillModel(related_abilities = ['intelligence'])
    nature_beasts: SkillModel = SkillModel(related_abilities = ['intelligence'])
    nature_birds: SkillModel = SkillModel(related_abilities = ['intelligence'])
    nature_fish: SkillModel = SkillModel(related_abilities = ['intelligence'])
    nature_geography: SkillModel = SkillModel(related_abilities = ['intelligence'])
    nature_humanoids: SkillModel = SkillModel(related_abilities = ['intelligence'])
    nature_minerals: SkillModel = SkillModel(related_abilities = ['intelligence'])
    nature_mycology: SkillModel = SkillModel(related_abilities = ['intelligence'])
    nature_plants: SkillModel = SkillModel(related_abilities = ['intelligence'])
    nature_trees: SkillModel = SkillModel(related_abilities = ['intelligence'])
    painting: SkillModel = SkillModel(related_abilities = ['hand_eye_coordination', 'spatial'])
    papermaking: SkillModel = SkillModel(related_abilities = ['spatial'])
    parry: SkillModel = SkillModel(related_abilities = ['hand_eye_coordination', 'agility'])
    perfumemaking: SkillModel = SkillModel(related_abilities = ['common_sense'])
    persuasion: SkillModel = SkillModel(related_abilities = ['charisma'])
    pewtersmithing: SkillModel = SkillModel(related_abilities = ['common_sense'])
    philosophy: SkillModel = SkillModel(related_abilities = ['intelligence'])
    pick_pocket: SkillModel = SkillModel(related_abilities = ['hand_eye_coordination'])
    pottery: SkillModel = SkillModel(related_abilities = ['common_sense'])
    pursemaking: SkillModel = SkillModel(related_abilities = ['common_sense'])
    read_lips: SkillModel = SkillModel(related_abilities = ['intuition'])
    religion_cultural: SkillModel = SkillModel(related_abilities = ['intelligence'])
    religion_specific: SkillModel = SkillModel(related_abilities = ['intelligence'])
    remember_detail: SkillModel = SkillModel(related_abilities = ['reflection'])
    research_library: SkillModel = SkillModel(related_abilities = ['intelligence'])
    riding: SkillModel = SkillModel(related_abilities = ['agility'])
    ritual_complex: SkillModel = SkillModel(related_abilities = ['hand_eye_coordination', 'intelligence'])
    ropemaking: SkillModel = SkillModel(related_abilities = ['common_sense'])
    rope_use: SkillModel = SkillModel(related_abilities = ['hand_eye_coordination'])
    saddlemaking: SkillModel = SkillModel(related_abilities = ['common_sense'])
    sailing: SkillModel = SkillModel(related_abilities = ['intelligence', 'vision'])
    sailmaking: SkillModel = SkillModel(related_abilities = ['spatial'])
    sculpture: SkillModel = SkillModel(related_abilities = ['hand_eye_coordination', 'intuition'])
    search: SkillModel = SkillModel(related_abilities = ['intuition', 'common_sense'])
    seduction: SkillModel = SkillModel(related_abilities = ['bodily_attractiveness', 'charisma'])
    sexual_adeptness: SkillModel = SkillModel(related_abilities = ['bodily_attractiveness', 'facial', 'kinetic'])
    sheathmaking: SkillModel = SkillModel(related_abilities = ['common_sense'])
    shipwright: SkillModel = SkillModel(related_abilities = ['spatial'])
    sight: SkillModel = SkillModel(related_abilities = ['vision'])
    silence: SkillModel = SkillModel(related_abilities = ['agility', 'common_sense'])
    silversmithing: SkillModel = SkillModel(related_abilities = ['strength', 'spatial'])
    skinning: SkillModel = SkillModel(related_abilities = ['common_sense'])
    smell: SkillModel = SkillModel(related_abilities = [])
    soapmaking: SkillModel = SkillModel(related_abilities = ['common_sense'])
    sound: SkillModel = SkillModel(related_abilities = [])
    spellcasting_combat: SkillModel = SkillModel(related_abilities = ['drive'])
    spellcasting_famiarity: SkillModel = SkillModel(related_abilities = ['intelligence'])
    spellcasting_specific: SkillModel = SkillModel(related_abilities = [])
    spitting: SkillModel = SkillModel(related_abilities = ['ennunciation'])
    sprint: SkillModel = SkillModel(related_abilities = ['physical_fitness'])
    stonemasonry: SkillModel = SkillModel(related_abilities = ['strength', 'spatial'])
    storytelling: SkillModel = SkillModel(related_abilities = ['charisma'])
    surgery: SkillModel = SkillModel(related_abilities = ['hand_eye_coordination', 'intelligence'])
    swim: SkillModel = SkillModel(related_abilities = ['physical_fitness', 'strength'])
    symbology: SkillModel = SkillModel(related_abilities = ['intelligence'])
    tailoring: SkillModel = SkillModel(related_abilities = ['hand_eye_coordination', 'spatial'])
    tanning: SkillModel = SkillModel(related_abilities = ['common_sense'])
    taste: SkillModel = SkillModel(related_abilities = [])
    teaching: SkillModel = SkillModel(related_abilities = ['intelligence', 'intuition', 'common_sense'])
    thatching: SkillModel = SkillModel(related_abilities = ['common_sense'])
    tilemaking: SkillModel = SkillModel(related_abilities = ['common_sense'])
    tinkering: SkillModel = SkillModel(related_abilities = ['common_sense'])
    touch: SkillModel = SkillModel(related_abilities = [])
    toxicology: SkillModel = SkillModel(related_abilities = ['intelligence'])
    tracking: SkillModel = SkillModel(related_abilities = ['intelligence'])
    transcribing: SkillModel = SkillModel(related_abilities = ['language'])
    trapping: SkillModel = SkillModel(related_abilities = ['common_sense'])
    trickery: SkillModel = SkillModel(related_abilities = ['charisma'])
    tumble: SkillModel = SkillModel(related_abilities = ['agility'])
    urinating: SkillModel = SkillModel(related_abilities = ['health', 'hand_eye_coordination'])
    ventriloquism: SkillModel = SkillModel(related_abilities = ['intelligence', 'ennunciation'])
    wainwrighting: SkillModel = SkillModel(related_abilities = ['common_sense'])
    weapon_general: SkillModel = SkillModel(related_abilities = [])
    weapon_specific: SkillModel = SkillModel(related_abilities = [])
    weapon_mastery: SkillModel = SkillModel(related_abilities = [])
    weapon_trick: SkillModel = SkillModel(related_abilities = ['hand_eye_coordination'])
    weaponsmithing: SkillModel = SkillModel(related_abilities = ['spatial'])
    weather_prediction: SkillModel = SkillModel(related_abilities = ['common_sense', 'reflection'])
    weaving: SkillModel = SkillModel(related_abilities = ['common_sense'])
    wheelwrighting: SkillModel = SkillModel(related_abilities = ['spatial'])
    wildernes_lore: SkillModel = SkillModel(related_abilities = ['intelligence'])
    wrestling: SkillModel = SkillModel(related_abilities = ['strength', 'agility'])

    """Body Parts"""
    head: BodyModel = BodyModel()
    face: BodyModel = BodyModel()
    upper_torso: BodyModel = BodyModel()
    lower_torso: BodyModel = BodyModel()
    groin: BodyModel = BodyModel()
    upper_right_arm: BodyModel = BodyModel()
    lower_right_arm: BodyModel = BodyModel()
    right_hand: BodyModel = BodyModel()
    upper_left_arm: BodyModel = BodyModel()
    lower_left_arm: BodyModel = BodyModel()
    left_hand: BodyModel = BodyModel()
    upper_right_leg: BodyModel = BodyModel()
    lower_right_leg: BodyModel = BodyModel()
    right_foot: BodyModel = BodyModel()
    upper_left_leg: BodyModel = BodyModel()
    lower_left_leg: BodyModel = BodyModel()
    left_foot: BodyModel = BodyModel()

    tail: BodyModel = BodyModel()
    wings: BodyModel = BodyModel()

    elf_lifespan: int = None

    """Spells"""
    spells_known: List[int] = None

    spellbook_description: str = ""

    spells: List[SpellModel] = None
