

# useful for neural network inputs
def card_name_to_id(cards, hand):

    for index in range(len(hand)):
        selected_card = cards.loc[cards["card_name"] == hand[index]]
        card_id = selected_card["card_id"].values[0]
        hand[index] = card_id

    return hand


# return a card and the action taken
def make_decision(weights, game_state, player_state):
    # weights_age = weights.loc[weights["age"] == game_state["era"]]
    print(weights)


def play(cards, weights, game_state, player_state):
    # player_hand = player_state["cards_hand"]
    # player_hand_playable = player_state["cards_playable"]

    make_decision(weights, game_state, player_state)