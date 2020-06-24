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
                            "Vineyard", "Bazar",
                            "Haven", "Lighthouse", "Chamber of Commerce", "Arena"]

    count_commercial_structure = count_cards_played_matchs(player_state, commercial_structure)

    return count_commercial_structure


# rule for lumber_yard card
# return weight of card
def lumber_yard(player_state, game_state):
    amount_raw_material = player_state["resources"]["clay"] + player_state["resources"]["ore"] \
                          + player_state["resources"]["wood"] + player_state["resources"]["stone"]
    # Monopoly of wood
    if amount_raw_material < 2:
        return 4

    return 1


# rule for stone pit card
# return weight of card
def stone_pit(player_state, game_state):
    amount_raw_material = player_state["resources"]["clay"] + player_state["resources"]["ore"] \
                          + player_state["resources"]["wood"] + player_state["resources"]["stone"]

    if amount_raw_material < 2:
        return 3

    return 1


# rule for clay pool card
# return weight of card
def clay_pool(player_state, game_state):
    amount_raw_material = player_state["resources"]["clay"] + player_state["resources"]["ore"] \
                          + player_state["resources"]["wood"] + player_state["resources"]["stone"]

    if amount_raw_material < 2:
        return 3

    return 1


# rule for ore_vein card
# return weight of card
def ore_vein(player_state, game_state):
    amount_raw_material = player_state["resources"]["clay"] + player_state["resources"]["ore"] \
                          + player_state["resources"]["wood"] + player_state["resources"]["stone"]

    if amount_raw_material < 2:
        return 3

    return 1


# rule for three farm card
# return weight of card
def three_farm(player_state, game_state):
    amount_raw_material = player_state["resources"]["clay"] + player_state["resources"]["ore"] \
                          + player_state["resources"]["wood"] + player_state["resources"]["stone"]

    if amount_raw_material < 2:
        return 3

    return 1


# rule for excavation card
# return weight of card
def excavation(player_state, game_state):
    amount_raw_material = player_state["resources"]["clay"] + player_state["resources"]["ore"] \
                          + player_state["resources"]["wood"] + player_state["resources"]["stone"]

    if amount_raw_material < 2:
        return 3

    return 1


# rule for clay pit card
# return weight of card
def clay_pit(player_state, game_state):
    # starts with Rhodes or Babylon ?
    if game_state["era"] > 1 | (player_state["wonder_id"] == 3 | player_state["wonder_id"] == 10 |
                                player_state["wonder_id"] == 1 | player_state["wonder_id"] == 8):
        return 3

    return 5


def timber_yard(player_state, game_state):
    amount_raw_material = player_state["resources"]["clay"] + player_state["resources"]["ore"] \
                          + player_state["resources"]["wood"] + player_state["resources"]["stone"]

    # starts with Rhodes or Babylon ?
    if (player_state["wonder_id"] == 4 | player_state["wonder_id"] == 11 |
            player_state["wonder_id"] == 2 | player_state["wonder_id"] == 9):
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


def sawmill(player_state, game_state):
    amount_wood = player_state["resources"]["wood"]

    if amount_wood < 2:
        return 2

    return 1


def quarry(player_state, game_state):
    # Pay attention to this card so you can build Wall
    return 2


def brickyard(player_state, game_state):
    return 1


def foundry(player_state, game_state):
    return 1


def loom(player_state, game_state):
    is_in_hand = find_card(player_state, "Marketplace")
    glass = player_state["resources"]["glass"]
    loom = player_state["resources"]["loom"]

    if (not is_in_hand) & (glass < 1) & (loom < 1):
        return 4

    if not is_in_hand:
        return 2

    return 1


def glassworks(player_state, game_state):
    is_in_hand = find_card(player_state, "Marketplace")
    glass = player_state["resources"]["glass"]
    loom = player_state["resources"]["loom"]

    if (not is_in_hand) & (glass < 1) & (loom < 1):
        return 4

    if not is_in_hand:
        return 2

    return 1


def press(player_state, game_state):
    return 1


def altar(player_state, game_state):
    return 1


def theater(player_state, game_state):
    return 1


def pawnshop(player_state, game_state):
    return 2


def baths(player_state, game_state):
    return 2


def temple(player_state, game_state):
    count_civilian_structure = qt_civilian_structure(player_state)

    if count_civilian_structure < 2:
        return 3

    return 1


def courthouse(player_state, game_state):
    count_civilian_structure = qt_civilian_structure(player_state)

    if count_civilian_structure < 2:
        return 3

    return 1


def statue(player_state, game_state):
    count_civilian_structure = qt_civilian_structure(player_state)

    if count_civilian_structure < 2:
        return 3

    return 1


def aqueduct(player_state, game_state):
    count_civilian_structure = qt_civilian_structure(player_state)

    if count_civilian_structure < 2:
        return 3

    return 1


def gardens(player_state, game_state):
    return 3


def town_hall(player_state, game_state):
    return 4


def senate(player_state, game_state):
    return 4


def pantheon(player_state, game_state):
    return 5


def palace(player_state, game_state):
    return 5


def tavern(player_state, game_state):
    return 1


## TODO: implement rule [neighboor]
def east_trading_post(player_state, game_state):
    return 1


## TODO: implement rule [neighboor]
def west_trading_post(player_state, game_state):
    return 1


def marketplace(player_state, game_state):
    return 4


def forum(player_state, game_state):
    is_in_hand = find_card(player_state, "Marketplace")
    glass = player_state["resources"]["glass"]
    loom = player_state["resources"]["loom"]

    if (not is_in_hand) & (glass < 1) & (loom < 1):
        return 4

    if not is_in_hand:
        return 2

    return 1


def caravansery(player_state, game_state):
    return 5


## TODO: implement rule [neighboor]
def vineyard(player_state, game_state):
    return 1


## TODO: implement rule [neighboor]
def bazar(player_state, game_state):
    return 1


def haven(player_state, game_state):
    amount_raw_material = player_state["resources"]["clay"] + player_state["resources"]["ore"] \
                          + player_state["resources"]["wood"] + player_state["resources"]["stone"]

    if amount_raw_material >= 4:
        return 3

    return 1


def lighthouse(player_state, game_state):
    amound_of_commercial_structure = qt_commercial_structure(player_state)

    if amound_of_commercial_structure >= 4:
        return 3

    return 1


def chamber_of_commerce(player_state, game_state):
    amount_manufacture_good = player_state["resources"]["papyrus"] + player_state["resources"]["loom"] \
                          + player_state["resources"]["glass"]

    if amount_manufacture_good >= 2:
        return 3

    return 1


def arena(player_state, game_state):
    coins = player_state["resources"]["papyrus"]
    wonder_stage = player_state["wonder_stage"]

    if (coins < 3) & (wonder_stage >= 1):
        return 3

    return 1


## TODO: implement rule
def stockade(player_state, game_state):
    return 1


## TODO: implement rule
def barracks(player_state, game_state):
    return 1


## TODO: implement rule
def guard_tower(player_state, game_state):
    return 1


## TODO: implement rule
def walls(player_state, game_state):
    return 1


## TODO: implement rule
def training_ground(player_state, game_state):
    return 1


## TODO: implement rule
def stables(player_state, game_state):
    return 1


## TODO: implement rule
def archery_range(player_state, game_state):
    return 1


## TODO: implement rule
def fortifications(player_state, game_state):
    return 1


## TODO: implement rule
def circus(player_state, game_state):
    return 1


## TODO: implement rule
def arsenal(player_state, game_state):
    return 1


## TODO: implement rule
def siege_workshop(player_state, game_state):
    return 1


## TODO: implement rule
def apothecary(player_state, game_state):
    return 1


## TODO: implement rule
def workshop(player_state, game_state):
    return 1


## TODO: implement rule
def scriptorium(player_state, game_state):
    return 1


## TODO: implement rule
def dispensary(player_state, game_state):
    return 1


## TODO: implement rule
def laboratory(player_state, game_state):
    return 1


## TODO: implement rule
def library(player_state, game_state):
    return 1


## TODO: implement rule
def school(player_state, game_state):
    return 1


## TODO: implement rule
def lodge(player_state, game_state):
    return 1


## TODO: implement rule
def observatory(player_state, game_state):
    return 1


## TODO: implement rule
def university(player_state, game_state):
    return 1


## TODO: implement rule
def academy(player_state, game_state):
    return 1


## TODO: implement rule
def study(player_state, game_state):
    return 1


## TODO: implement rule
def workers_guild(player_state, game_state):
    return 1


## TODO: implement rule
def craftsmens_guild(player_state, game_state):
    return 1


## TODO: implement rule
def traders_guild(player_state, game_state):
    return 1


## TODO: implement rule
def philosophers_guild(player_state, game_state):
    return 1


## TODO: implement rule
def spies_guild(player_state, game_state):
    return 1


## TODO: implement rule
def magistrates_guild(player_state, game_state):
    return 1


## TODO: implement rule
def shipowners_guild(player_state, game_state):
    return 1


## TODO: implement rule
def strategists_guild(player_state, game_state):
    return 1


## TODO: implement rule
def scientists_guild(player_state, game_state):
    return 1


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
