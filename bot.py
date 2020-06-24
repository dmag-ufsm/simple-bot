import strategies
import random
import json


# return dict with card names and ids
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


def is_playable(playable_cards, card_name):
    for current_card in playable_cards:
        if card_name == current_card:
            return True
    return False


def set_cards_weights(hand, game_state, player_state, neighbors):
    for card in hand:
        card["weight"] = strategies.card_weight_map[card["id"]](player_state, game_state, neighbors)


def choose_card_action(player_state, card_hand_data):
    if player_state["can_build_wonder"]:
        card_selected = random.choice(card_hand_data)
        return "build_wonder",  card_selected["card_name"]

    highest_weight = max_weight_value(card_hand_data)

    # if highest_weight == 0 not have playable cards
    if highest_weight == 0:
        card_selected = random.choice(card_hand_data)
        return "discard", card_selected["card_name"]

    best_cards = []

    for card in card_hand_data:
        if (card["weight"] == highest_weight) & card["playable"]:
            best_cards.append(card)

    if len(best_cards) > 1:
        card_selected = random.choice(best_cards)
        return "build_structure", card_selected["card_name"]

    return "build_structure", best_cards[0]["card_name"]


def max_weight_value(card_hand_data):
    highest = 0
    for card in card_hand_data:
        if card["playable"] & card["weight"] >= highest:
            highest = card["weight"]
    return highest


def write_json_action(action, card):
    path = "./actions/player_1.json"
    command_dict = {"command": {"subcommand": action, "argument": card}}
    print(command_dict)
    with open(path, "w") as write_file:
        json.dump(command_dict, write_file)


def play(cards, weights, game_state, players_state, player_id):
    card_hand_data = get_hand_data(cards, players_state[str(player_id)]['cards_hand'],
                                   players_state[str(player_id)]['cards_playable'])

    set_cards_weights(card_hand_data, game_state, players_state[str(player_id)], players_state)

    action, card = choose_card_action(players_state[str(player_id)], card_hand_data)

    write_json_action(action, card)
