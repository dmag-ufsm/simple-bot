import strategies
import random
import json
import sys
import pandas as pd
from datetime import datetime


# returns structure to store player's hand information
# return type example: { id: 1, card_name: 'Loom', weight: 4, playable: True }
def get_hand_data(cards, hand, playable_cards):
    card_hand_data = []

    for index in range(len(hand)):
        selected_card = cards.loc[cards["card_name"] == hand[index]]
        card_id = selected_card["card_id"].values[0]

        is_playable(playable_cards, hand[index])

        card_dict = {
            "id": card_id,
            "card_name": hand[index],
            "weight": 0,
            "playable": is_playable(playable_cards, hand[index]),
        }

        card_hand_data.append(card_dict)

    return card_hand_data


# check if card is playable
# return type boolean
def is_playable(playable_cards, card_name):
    for current_card in playable_cards:
        if card_name == current_card:
            return True
    return False


def get_neighbors(players_state, player_id):
    neighbors = []
    id_player_left = player_id - 1
    id_player_right = player_id + 1

    if id_player_left < 0:
        id_player_left = len(players_state) - 1

    if id_player_right > (len(players_state) - 1):
        id_player_right = 0

    neighbors.append(players_state[str(id_player_left)])
    neighbors.append(players_state[str(id_player_right)])

    return neighbors


def get_player_state(players_state, player_id):
    return players_state[str(player_id)]


# returns void
def set_cards_weights(hand, game_state, players_state, player_id):

    player_state = get_player_state(players_state, player_id)
    neighbors = get_neighbors(players_state, player_id)

    for card in hand:
        card["weight"] = strategies.card_weight_map[card["id"]](player_state, game_state, neighbors)


# return chosen action and card
# return type action, card
def choose_card_action(player_state, card_hand_data):

    # check if can build wonder stage
    if player_state["can_build_wonder"]:
        card_selected = random.choice(card_hand_data)
        return "build_wonder",  card_selected["card_name"]

    # get greatest weight
    highest_weight = max_weight_value(card_hand_data)

    # if highest_weight == 0 not have playable cards
    if highest_weight == 0:
        card_selected = random.choice(card_hand_data)
        return "discard", card_selected["card_name"]

    # store cards with greatest weight
    best_cards = []

    for card in card_hand_data:
        if (card["weight"] == highest_weight) and card["playable"]:
            best_cards.append(card)

    if len(best_cards) > 1:
        card_selected = random.choice(best_cards)
        return "build_structure", card_selected["card_name"]

    return "build_structure", best_cards[0]["card_name"]


def write_log(card_hand_data, action, card, bot_id, path_bot_log):
    data = {'card_1': '', 'card_2': '', 'card_4': '', 'card_3': '', 'card_4': '', 'card_5': '', 'card_6': '', 'card_7': '', 'card_played': '', 'action': '' }

    for i in range(len(card_hand_data)):
        card_name = card_hand_data[i]["card_name"]
        data['card_{}'.format(i + 1)] = card_name

    data['card_played'] = card
    data['action'] = action

    df = pd.DataFrame([data])

    df.to_csv(path_bot_log, mode='a', header=False, index=False)


# return the greatest weight found
# return type number
def max_weight_value(card_hand_data):
    highest = 0
    for card in card_hand_data:
        if card["playable"] and card["weight"] >= highest:
            highest = card["weight"]
    return highest


# write action in json file
# return type void

def write_json_action(action, card, player_id):
    path = sys.argv[1] + "/player_" + str(player_id + 1) + ".json"
    command_dict = {"command": {"subcommand": action, "argument": card, "extra": ""}}
    print(command_dict)
    with open(path, "w") as write_file:
        json.dump(command_dict, write_file)

    file_ready = open(sys.argv[1] + "/ready.txt", "a")
    file_ready.write("ready\n")
    file_ready.close()


def play(cards, weights, game_state, players_state, player_id, path_bot_log):
    card_hand_data = get_hand_data(cards, players_state[str(player_id)]['cards_hand'],
                                   players_state[str(player_id)]['cards_playable'])

    set_cards_weights(card_hand_data, game_state, players_state, player_id)

    action, card = choose_card_action(players_state[str(player_id)], card_hand_data)

    write_json_action(action, card, player_id)
    write_log(card_hand_data, action, card, player_id, path_bot_log)
