import strategies


# return dict with card names and ids
def get_hand_data(cards, hand):
    card_hand_data = []

    for index in range(len(hand)):
        selected_card = cards.loc[cards["card_name"] == hand[index]]
        card_id = selected_card["card_id"].values[0]

        card_dict = {
            "id": card_id,
            "card_name": hand[index],
            "weight": 0
        }

        card_hand_data.append(card_dict)

    return card_hand_data


def set_cards_weights(hand, game_state, player_state, neighbors):
    for card in hand:
        card["weight"] = strategies.card_weight_map[card["id"]](player_state, game_state, neighbors)
        print(card)


def play(cards, weights, game_state, players_state, player_id):
    print(players_state)
    print(game_state)

    card_hand_data = get_hand_data(cards, players_state[str(player_id)]['cards_hand'])
    set_cards_weights(card_hand_data, game_state, players_state[str(player_id)], players_state)

