''''
    RULES FOR ALL CARDS CONSIDERING A MILITARY STRATEGY
'''


## ==========    WONDER IDS ==============================
# ( A, B) = GIZA(0, 7), BABYLON(1, 8), OLYMPIA(2, 9), RHODOS(3, 10), EPHESOS(4, 11), ALEXANDRIA(5, 12),
# HALIKARNASSOS(6, 13)
## ==================================================================

def find_card(player_state, card):
    size = len(player_state["cards_hand"])
    is_in_hand = False

    for i in range(size):
        print(player_state["cards_hand"][i])
        if player_state["cards_hand"][i] == card:
            is_in_hand = True

    return is_in_hand


def count_cards_played_matchs(player_state, type):
    size = len(player_state["cards_played"])
    count = 0

    for i in range(size):
        for j in range(len(type)):
            if player_state["cards_played"][i] == type[j]:
                count += 1

    return count


def qt_civilian_structure(player_state):
    civilian_structure = ["Altar", "Theater", "Pawnshop", "Baths", "Temple", "Courthouse", "Statue", "Aqueduct",
                          "Gardens", "Town Hall", "Senate", "Pantheon", "Palace"]

    count_civilian_structure = count_cards_played_matchs(player_state, civilian_structure)

    return count_civilian_structure


def qt_commercial_structure(player_state):
    commercial_structure = ["Tavern", "East Trading Post", "West Trading Post", "Marketplace", "Forum", "Caravansery",
                            "Vineyard", "Bazar", "Haven", "Lighthouse", "Chamber of Commerce", "Arena"]

    count_commercial_structure = count_cards_played_matchs(player_state, commercial_structure)

    return count_commercial_structure


def qt_military_structure(player_state):
    military_structure = ["Stockade", "Barracks", "Guard Tower", "Walls", "Training Ground", "Stables",
                          "Archery Range", "Fortifications", "Circus", "Arsenal", "Siege Workshop"]

    count_military_structure = count_cards_played_matchs(player_state, military_structure)

    return count_military_structure


def lumber_yard(player_state, game_state):
    amount_raw_material = player_state["resources"]["clay"] + player_state["resources"]["ore"] \
                          + player_state["resources"]["wood"] + player_state["resources"]["stone"]

    # Wonder: ALEXANDRIA B(12) Is important to play 1 Wood card and unlock the first stage
    if player_state["wonder_id"] == 12:
        return 4

    # Wonder: GIZA B(7) unlock the 1st stage
    if player_state["wonder_id"] == 7:
        return 4

    # Wonder:  OLYMPIA A(2) build your 1st stage
    if player_state["wonder_id"] == 2:
        return 5

    # Monopoly of wood
    if amount_raw_material < 2:
        return 4

    return 1


## TODO: implement rule of WONDERS [Neighboor in rhodes]
def stone_pit(player_state, game_state):
    amount_raw_material = player_state["resources"]["clay"] + player_state["resources"]["ore"] \
                          + player_state["resources"]["wood"] + player_state["resources"]["stone"]

    # Wonder: GIZA B(7) unlock the 2nd stage
    if player_state["wonder_id"] == 7:
        return 3

    # Wonder:  OLYMPIA A(2) build the 2nd stage
    if player_state["wonder_id"] == 2:
        return 4

    if amount_raw_material < 2:
        return 3

    return 1


def clay_pool(player_state, game_state):
    amount_raw_material = player_state["resources"]["clay"] + player_state["resources"]["ore"] \
                          + player_state["resources"]["wood"] + player_state["resources"]["stone"]
    clay = player_state["resources"]["clay"]

    # Wonder: ALEXANDRIA B(12) Is important to play 1 Clay card and unlock the first stage
    if player_state["wonder_id"] == 12:
        return 4

    # Wonder: BABYLON B(8)
    if player_state["wonder_id"] == 8:
        if clay < 2:
            return 3

    # Wonder: GIZA B(7) unlock the 3rd stage
    if player_state["wonder_id"] == 7:
        return 2

    # Wonder: HALIKARNASSOS B(13) unlock your 2nd stage
    if player_state["wonder_id"] == 13:
        return 4

    if amount_raw_material < 2:
        return 3

    return 1


def ore_vein(player_state, game_state):
    amount_raw_material = player_state["resources"]["clay"] + player_state["resources"]["ore"] \
                          + player_state["resources"]["wood"] + player_state["resources"]["stone"]

    # Wonder: OLYMPIA A(2) build the 3rd stage
    if player_state["wonder_id"] == 2:
        return 3

    # Wonder: HALIKARNASSOS B(13) unlock your 1nd stage
    if player_state["wonder_id"] == 13:
        return 3

    if amount_raw_material < 2:
        return 3

    return 1


def three_farm(player_state, game_state):
    amount_raw_material = player_state["resources"]["clay"] + player_state["resources"]["ore"] \
                          + player_state["resources"]["wood"] + player_state["resources"]["stone"]

    # Wonder: GIZA B(7) unlock 2 stages of your wonder
    if player_state["wonder_id"] == 7:
        return 5

    if amount_raw_material < 2:
        return 3

    return 1


def excavation(player_state, game_state):
    amount_raw_material = player_state["resources"]["clay"] + player_state["resources"]["ore"] \
                          + player_state["resources"]["wood"] + player_state["resources"]["stone"]

    if amount_raw_material < 2:
        return 3

    return 1


def clay_pit(player_state, game_state):
    clay = player_state["resources"]["clay"]

    # Wonder: BABYLON B(8)
    if player_state["wonder_id"] == 8:
        if clay < 2:
            return 3

    # Wonder: HALIKARNASSOS B(13) you need both resources to build your stages
    if player_state["wonder_id"] == 13:
        return 5

    # starts with Rhodes or Babylon ?
    if game_state["era"] > 1 | (player_state["wonder_id"] == 3 | player_state["wonder_id"] == 10 |
                                player_state["wonder_id"] == 1 | player_state["wonder_id"] == 8):
        return 3

    return 5


def timber_yard(player_state, game_state):
    amount_raw_material = player_state["resources"]["clay"] + player_state["resources"]["ore"] \
                          + player_state["resources"]["wood"] + player_state["resources"]["stone"]

    # starts with Rhodes or Babylon ?
    if (player_state["wonder_id"] == 3 | player_state["wonder_id"] == 10 |
            player_state["wonder_id"] == 1 | player_state["wonder_id"] == 8):
        return 5

    if amount_raw_material < 3:
        return 3

    return 1


def forest_cave(player_state, game_state):
    amount_raw_material = player_state["resources"]["clay"] + player_state["resources"]["ore"] \
                          + player_state["resources"]["wood"] + player_state["resources"]["stone"]

    if amount_raw_material < 2:
        return 3

    return 1


def mine(player_state, game_state):
    amount_raw_material = player_state["resources"]["clay"] + player_state["resources"]["ore"] \
                          + player_state["resources"]["wood"] + player_state["resources"]["stone"]

    if amount_raw_material < 2:
        return 3

    return 1


## TODO: implement rule of WONDERS [Neighboor in olympia]
def sawmill(player_state, game_state):
    amount_wood = player_state["resources"]["wood"]

    # Wonder: EPHESOS B(11) monopoly of wood
    if player_state["wonder_id"] == 11:
        return 2

    # Wonder: ALEXANDRIA B(12) Is important to play 1 Clay card and unlock the first stage
    if player_state["wonder_id"] == 12:
        if amount_wood < 1:
            return 4
        else:
            return 2

    # Wonder: BABYLON B(8) your 2nd wonder needs and you can do the monopoly
    if player_state["wonder_id"] == 8:
        return 4

    # Wonder: GIZA B(7) unlock the 3rd stage
    if player_state["wonder_id"] == 7:
        if amount_wood < 1:
            return 5

    # Wonder:  OLYMPIA A(2)
    if player_state["wonder_id"] == 2:
        if amount_wood < 2:
            return 3

    if amount_wood < 2:
        return 2

    return 1


def quarry(player_state, game_state):
    amount_stone = player_state["resources"]["stone"]

    # Wonder: ALEXANDRIA B(12) Is important to play 1 Clay card and unlock the first stage
    if player_state["wonder_id"] == 12:
        return 4

    # Wonder: BABYLON B(8) allows to try to pick some cards like: Wall | Tablet | Compass
    if player_state["wonder_id"] == 8:
        return 3

    # Wonder: RHODOS B(10) allows to try to pick some cards like: Wall | Tablet | Compass
    if player_state["wonder_id"] == 8:
        return 5

    # Wonder: GIZA B(7) unlock the 3rd stage
    if player_state["wonder_id"] == 7:
        if amount_stone < 2:
            return 3
        elif amount_stone < 1:
            return 4

    # Wonder:  OLYMPIA A(2)
    if player_state["wonder_id"] == 2:
        if amount_stone < 2:
            return 4

    # Wonder: HALIKARNASSOS B(13) unlock your 1nd stage
    if player_state["wonder_id"] == 13:
        return 3

    # Pay attention to this card so you can build Wall
    return 2


def brickyard(player_state, game_state):
    amount_clay = player_state["resources"]["clay"]

    # Wonder: EPHESOS B(11) gives you: Gear | Forum for free.
    if player_state["wonder_id"] == 11:
        return 3

    # Wonder: BABYLON B(8) allows to try to pick some cards like: Wall | Tablet | Compass
    if player_state["wonder_id"] == 8:
        if amount_clay < 2:
            return 3

    # Wonder: GIZA B(7) unlock the 3rd stage
    if player_state["wonder_id"] == 7:
        if amount_clay < 2:
            return 2
        elif amount_clay < 1:
            return 3

    # Wonder: HALIKARNASSOS B(13) unlock your 1nd stage
    if player_state["wonder_id"] == 13:
        if amount_clay < 2:
            return 4
        elif amount_clay < 1:
            return 5

    return 1


def foundry(player_state, game_state):
    amount_ore = player_state["resources"]["ore"]

    # Wonder: EPHESOS B(11) links very well with: Compass | Theater | Hero guild.
    if player_state["wonder_id"] == 11:
        return 3

    # Wonder: RHODOS B(10) you need 4x ore to build your 2nd stage
    if player_state["wonder_id"] == 8:
        return 4

    # Wonder:  OLYMPIA A(2)
    if player_state["wonder_id"] == 2:
        if amount_ore < 2:
            return 4

    # Wonder: HALIKARNASSOS B(13)
    if player_state["wonder_id"] == 13:
        if amount_ore < 2:
            return 2
        elif amount_ore < 1:
            return 5

    return 1


## TODO: implement rule of WONDERS
def loom(player_state, game_state):
    is_in_hand = find_card(player_state, "Marketplace")
    glass = player_state["resources"]["glass"]
    loom = player_state["resources"]["loom"]
    amount_ore = player_state["resources"]["ore"]

    if (not is_in_hand) & (glass < 1) & (loom < 1):
        return 4
    elif not is_in_hand:
        return 2

    return 1


## TODO: implement rule of WONDERS
def glassworks(player_state, game_state):
    is_in_hand = find_card(player_state, "Marketplace")
    glass = player_state["resources"]["glass"]
    loom = player_state["resources"]["loom"]

    if (not is_in_hand) & (glass < 1) & (loom < 1):
        return 4

    if not is_in_hand:
        return 2

    return 1


## TODO: implement rule of WONDERS
def press(player_state, game_state):
    return 1


## TODO: implement rule of WONDERS
def altar(player_state, game_state):
    return 1


## TODO: implement rule of WONDERS
def theater(player_state, game_state):
    return 1


## TODO: implement rule of WONDERS
def pawnshop(player_state, game_state):
    return 2


## TODO: implement rule of WONDERS
def baths(player_state, game_state):
    return 2


## TODO: implement rule of WONDERS
def temple(player_state, game_state):
    count_civilian_structure = qt_civilian_structure(player_state)

    if count_civilian_structure < 2:
        return 3

    return 1


## TODO: implement rule of WONDERS
def courthouse(player_state, game_state):
    count_civilian_structure = qt_civilian_structure(player_state)

    if count_civilian_structure < 2:
        return 3

    return 1


## TODO: implement rule of WONDERS
def statue(player_state, game_state):
    count_civilian_structure = qt_civilian_structure(player_state)

    if count_civilian_structure < 2:
        return 3

    return 1


## TODO: implement rule of WONDERS
def aqueduct(player_state, game_state):
    count_civilian_structure = qt_civilian_structure(player_state)

    if count_civilian_structure < 2:
        return 3

    return 1


## TODO: implement rule of WONDERS
def gardens(player_state, game_state):
    return 3


## TODO: implement rule of WONDERS
def town_hall(player_state, game_state):
    return 4


## TODO: implement rule of WONDERS
def senate(player_state, game_state):
    return 4


## TODO: implement rule of WONDERS
def pantheon(player_state, game_state):
    return 5


## TODO: implement rule of WONDERS
def palace(player_state, game_state):
    return 5


## TODO: implement rule of WONDERS
def tavern(player_state, game_state):
    return 1


## TODO: implement rule of WONDERS
## TODO: implement rule [neighboor]
def east_trading_post(player_state, game_state):
    return 1


## TODO: implement rule of WONDERS
## TODO: implement rule [neighboor]
def west_trading_post(player_state, game_state):
    return 1


## TODO: implement rule of WONDERS
def marketplace(player_state, game_state):
    return 4


## TODO: implement rule of WONDERS
def forum(player_state, game_state):
    is_in_hand = find_card(player_state, "Marketplace")
    glass = player_state["resources"]["glass"]
    loom = player_state["resources"]["loom"]

    if (not is_in_hand) & (glass < 1) & (loom < 1):
        return 4

    if not is_in_hand:
        return 2

    return 1


## TODO: implement rule of WONDERS
def caravansery(player_state, game_state):
    return 5


## TODO: implement rule of WONDERS
## TODO: implement rule [neighboor]
def vineyard(player_state, game_state):
    return 1


## TODO: implement rule of WONDERS
## TODO: implement rule [neighboor]
def bazar(player_state, game_state):
    return 1


## TODO: implement rule of WONDERS
def haven(player_state, game_state):
    amount_raw_material = player_state["resources"]["clay"] + player_state["resources"]["ore"] \
                          + player_state["resources"]["wood"] + player_state["resources"]["stone"]

    if amount_raw_material >= 4:
        return 3

    return 1


## TODO: implement rule of WONDERS
def lighthouse(player_state, game_state):
    amound_of_commercial_structure = qt_commercial_structure(player_state)

    if amound_of_commercial_structure >= 4:
        return 3

    return 1


## TODO: implement rule of WONDERS
def chamber_of_commerce(player_state, game_state):
    amount_manufacture_good = player_state["resources"]["papyrus"] + player_state["resources"]["loom"] \
                              + player_state["resources"]["glass"]

    if amount_manufacture_good >= 2:
        return 3

    return 1


## TODO: implement rule of WONDERS
def arena(player_state, game_state):
    coins = player_state["resources"]["papyrus"]
    wonder_stage = player_state["wonder_stage"]

    if (coins < 3) & (wonder_stage >= 1):
        return 3

    return 1


## TODO: implement rule of WONDERS
def stockade(player_state, game_state):
    amound_of_military_cards = qt_military_structure(player_state)

    if amound_of_military_cards < 2:
        return 4
    if amound_of_military_cards < 1:
        return 5

    return 1


## TODO: implement rule of WONDERS
def barracks(player_state, game_state):
    amound_of_military_cards = qt_military_structure(player_state)

    if amound_of_military_cards < 2:
        return 4
    if amound_of_military_cards < 1:
        return 5

    return 1


## TODO: implement rule of WONDERS
def guard_tower(player_state, game_state):
    amound_of_military_cards = qt_military_structure(player_state)

    if amound_of_military_cards < 2:
        return 4
    if amound_of_military_cards < 1:
        return 5

    return 1


## TODO: implement rule of WONDERS
## TODO: implement rule [neighboor]
def walls(player_state, game_state):
    amound_of_military_cards = qt_military_structure(player_state)

    if amound_of_military_cards < 1:
        return 4

    return 1


## TODO: implement rule of WONDERS
## TODO: implement rule [neighboor]
def training_ground(player_state, game_state):
    amound_of_military_cards = qt_military_structure(player_state)

    if amound_of_military_cards < 1:
        return 4

    return 1


## TODO: implement rule of WONDERS
## TODO: implement rule [neighboor]
def stables(player_state, game_state):
    amound_of_military_cards = qt_military_structure(player_state)

    if amound_of_military_cards < 1:
        return 4

    return 1


## TODO: implement rule of WONDERS
## TODO: implement rule [neighboor]
def archery_range(player_state, game_state):
    amound_of_military_cards = qt_military_structure(player_state)

    if amound_of_military_cards < 1:
        return 4

    return 1


## TODO: implement rule of WONDERS
## TODO: implement rule [neighboor]
def fortifications(player_state, game_state):
    return 1


## TODO: implement rule of WONDERS
## TODO: implement rule [neighboor]
def circus(player_state, game_state):
    return 1


## TODO: implement rule of WONDERS
## TODO: implement rule [neighboor]
def arsenal(player_state, game_state):
    return 1


## TODO: implement rule of WONDERS
## TODO: implement rule [neighboor]
def siege_workshop(player_state, game_state):
    return 1


## TODO: implement rule of WONDERS
def apothecary(player_state, game_state):
    return 1


## TODO: implement rule of WONDERS
def workshop(player_state, game_state):
    return 1


## TODO: implement rule of WONDERS
def scriptorium(player_state, game_state):
    return 1


## TODO: implement rule of WONDERS
def dispensary(player_state, game_state):
    return 1


## TODO: implement rule of WONDERS
def laboratory(player_state, game_state):
    return 1


## TODO: implement rule of WONDERS
def library(player_state, game_state):
    return 1


## TODO: implement rule of WONDERS
def school(player_state, game_state):
    return 1


## TODO: implement rule of WONDERS
def lodge(player_state, game_state):
    return 1


## TODO: implement rule of WONDERS
def observatory(player_state, game_state):
    return 1


## TODO: implement rule of WONDERS
def university(player_state, game_state):
    return 1


## TODO: implement rule of WONDERS
def academy(player_state, game_state):
    return 1


## TODO: implement rule of WONDERS
def study(player_state, game_state):
    return 1


## TODO: implement rule of WONDERS
## TODO: implement rule
def workers_guild(player_state, game_state):
    return 1


## TODO: implement rule of WONDERS
## TODO: implement rule
def craftsmens_guild(player_state, game_state):
    return 1


## TODO: implement rule of WONDERS
## TODO: implement rule
def traders_guild(player_state, game_state):
    return 1


## TODO: implement rule of WONDERS
## TODO: implement rule
def philosophers_guild(player_state, game_state):
    return 1


## TODO: implement rule of WONDERS
## TODO: implement rule
def spies_guild(player_state, game_state):
    return 1


## TODO: implement rule of WONDERS
## TODO: implement rule
def magistrates_guild(player_state, game_state):
    return 1


## TODO: implement rule of WONDERS
## TODO: implement rule
def shipowners_guild(player_state, game_state):
    return 1


## TODO: implement rule of WONDERS
## TODO: implement rule
def strategists_guild(player_state, game_state):
    return 1


## TODO: implement rule of WONDERS
## TODO: implement rule
def scientists_guild(player_state, game_state):
    return 1


## TODO: implement rule of WONDERS
## TODO: implement rule
def builders_guild(player_state, game_state):
    return 1


# map of functions applied for a specific card
card_weight_map = {
    '1': lumber_yard,
    '2': stone_pit,
    '3': clay_pool,
    '4': ore_vein,
    '5': three_farm,
    '6': excavation,
    '7': clay_pit,
    '8': timber_yard,
    '9': forest_cave,
    '10': mine,
    '11': sawmill,
    '12': quarry,
    '13': brickyard,
    '14': foundry,
    '15': loom,
    '16': glassworks,
    '17': press,
    '18': altar,
    '19': theater,
    '20': pawnshop,
    '21': baths,
    '22': temple,
    '23': courthouse,
    '24': statue,
    '25': aqueduct,
    '26': gardens,
    '27': town_hall,
    '28': senate,
    '29': pantheon,
    '30': palace,
    '31': tavern,
    '32': east_trading_post,
    '33': west_trading_post,
    '34': marketplace,
    '35': forum,
    '36': caravansery,
    '37': vineyard,
    '38': bazar,
    '39': haven,
    '40': lighthouse,
    '41': chamber_of_commerce,
    '42': arena,
    '43': stockade,
    '44': barracks,
    '45': guard_tower,
    '46': walls,
    '47': training_ground,
    '48': stables,
    '49': archery_range,
    '50': fortifications,
    '51': circus,
    '52': arsenal,
    '53': siege_workshop,
    '54': apothecary,
    '55': workshop,
    '56': scriptorium,
    '57': dispensary,
    '58': laboratory,
    '59': library,
    '60': school,
    '61': lodge,
    '62': observatory,
    '63': university,
    '64': academy,
    '65': study,
    '66': workers_guild,
    '67': craftsmens_guild,
    '68': traders_guild,
    '69': philosophers_guild,
    '70': spies_guild,
    '71': magistrates_guild,
    '72': shipowners_guild,
    '73': strategists_guild,
    '74': scientists_guild,
    '75': builders_guild,
}
