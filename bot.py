

# useful for neural network inputs
def card_name_to_id(cards, hand):

    for index in range(len(hand)):
        selected_card = cards.loc[cards["card_name"] == hand[index]]
        card_id = selected_card["card_id"].values[0]
        hand[index] = card_id

    return hand


def play(cards, weights, game_state, player_state):
    print('alguma coisa')
    print(player_state)
    print(game_state)