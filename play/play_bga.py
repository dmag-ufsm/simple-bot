# Script para jogar com o bot no BGA

from selenium import webdriver
import bs4
import json
import sys

# Cartas na ordem do BGA
CARDS = ['Stone Pit', 'Clay Pool', 'Ore Vein', 'Tree Farm', 'Excavation',
         'Clay Pit', 'Timber Yard', 'Forest Cave', 'Mine', 'Loom',
         'Glassworks', 'Press', 'Barracks', 'Stockade', 'Guard Tower',
         'Apothecary', 'Scriptorium', 'Workshop', 'East Trading Post',
         'West Trading Post', 'Marketplace', 'Tavern', 'Theater', 'Pawnshop',
         'Altar', 'Baths', 'Sawmill', 'Quarry', 'Brickyard', 'Foundry',
         'Stables', 'Walls', 'Archery Range', 'Training Ground', 'Laboratory',
         'School', 'Dispensary', 'Library', 'Vineyard', 'Bazar', 'Forum',
         'Caravansery', 'Courthouse', 'Statue', 'Temple', 'Aqueduct',
         'Circus', 'Arsenal', 'Fortifications', 'Siege Workshop', 'Observatory',
         'Academy', 'University', 'Lodge', 'Study', 'Arena',
         'Chamber of Commerce', 'Haven', 'Lighthouse', 'Palace', 'Gardens',
         'Pantheon', 'Town Hall', 'Senate', 'Workers Guild', 'Craftmens Guild',
         'Traders Guild', 'Philosophers Guild', 'Spies Guild', 'Strategists Guild', 'Shipowners Guild',
         'Scientists Guild', 'Magistrates Guild', 'Builders Guild', 'Lumber Yard']

# Maravilhas na ordem do BGA
WONDERS = ['Gizah A', 'Babylon A', 'Olympia A', 'Rhodos A', 'Ephesos A', 'Alexandria A', 'Halikarnassos A',
           'Gizah B', 'Babylon B', 'Olympia B', 'Rhodos B', 'Ephesos B', 'Alexandria B', 'Halikarnassos B']
 
# Obtem os dados de maravilha do tabuleiro recebido como parametro
def get_wonder(parsed_html):
    div_player_board_wonder = parsed_html.find('div', attrs={'class':'player_board_wonder'})

    # ID e nome do wonder do jogador
    value = float(div_player_board_wonder['style'].split(' ')[-1].split('%')[0])        
    wonder_id = round(value / 7.69231) # somar + 1 para indice comecando em 1
    wonder_name = WONDERS[wonder_id - 1]

    # Numero de estagios construidos
    div_wonder_step_built = parsed_html.find('div', attrs={'class':'wonder_step_built'})
    wonder_stage = 0
    if div_wonder_step_built != None:
        wonder_stage = len(div_wonder_step_built)

    # Se pode jogar estagio da maravilha ou nao
    for pbw in div_player_board_wonder:
        if len(pbw) <= 1:
            continue

        if ('board_wonder_step_' + str(wonder_stage + 1)) in pbw['id']:
            try:
                icon = pbw.find('div').find('div', attrs={'class':'card_status_icon'})['class'][1]
            except:
                icon = ''
            nbr = pbw.find('div').find('div', attrs={'class':'card_status_nbr'}).text

            can_build_wonder = (icon, nbr)
            break

    return {'wonder_id' : wonder_id, 'wonder_name' : wonder_name,
            'wonder_stage' : wonder_stage, 'can_build_wonder' : can_build_wonder}

# Obtem as cartas jogadas do tabuleiro recebido como parametro
def get_cards_played(parsed_html):
    cards_played = []

    div_board_item = parsed_html.find_all('div')

    for item in div_board_item:
        if 'board_item' in item['class']:
            if 'background-position' in item['style']:
                desl = item['style'].split('background-position:')[1].split(' ')
                l = int(float(desl[1].split('%')[0]) / 10)
                c = int(float(desl[2].split('%')[0]) / 12.5)
                card_name = CARDS[c * 10 + l]
            else:
                card_name = CARDS[0]
            cards_played.append(card_name)

    return cards_played

# Obtem os dados que estao "em cima" do tabuleiro
def get_boards(parsed_html):
    wonders_data = []
    cards_played = []
    coins = []
    div_boardspaces = parsed_html.body.find('div', attrs={'id':'boardspaces'})

    for boardspace in div_boardspaces:
        if isinstance(boardspace, bs4.element.Tag) and boardspace['class'][0] == 'player_board_wrap':
            wonders_data.append(get_wonder(boardspace))
            cards_played.append(get_cards_played(boardspace))
            coins.append(int(boardspace.find('div', attrs={'class':'sw_coins'}).find('span').text))

    return wonders_data, cards_played, coins

# Obtem as cartas na mao do jogador
def get_hand_cards(parsed_html):
    div_player_hand = parsed_html.body.find('div', attrs={'id':'player_hand'})

    cards_canplay = []
    cards_couldplay = []
    cards_cantplay = []

    for ph in div_player_hand:
        # Pega o nome da carta
        if 'background-position' in ph['style']:
            desl = ph['style'].split('background-position:')[1].split(' ')
            l = int(int(desl[1].split('%')[0].replace('-', '')) / 100)
            c = int(int(desl[2].split('%')[0].replace('-', '')) / 100)
            card_name = CARDS[c * 10 + l]
        else:
            card_name = CARDS[0]

        # Pega status: se eh jogavel e a quantia de moedas caso precise recursos
        id = ph['id'].split('_')[-1]
        
        icon = ph.find('div').find('div').find('div', attrs={'id':'card_status_icon_' + id})['class'][0]
        nbr = ph.find('div').find('div').find('div', attrs={'id':'card_status_nbr_' + id}).text

        if icon == 'canplay':
            cards_canplay.append(card_name)

        elif icon == 'couldplay':
            cards_couldplay.append((card_name, nbr))
        
        elif icon == 'cantplay':
            cards_cantplay.append(card_name)

    return cards_canplay, cards_couldplay, cards_cantplay

def get_resources(cards_played, wonder_data, coins):
    resources = {
        'clay': 0,
        'coins': coins,
        'compass': 0,
        'gear': 0,
        'glass': 0,
        'loom': 0,
        'ore': 0,
        'papyrus': 0,
        'shields': 0,
        'stone': 0,
        'tablet': 0,
        'wood': 0
    }

    wonder_name = wonder_data['wonder_name']
    wonder_stage = wonder_data['wonder_stage']

    # Recurso da maravilha
    if wonder_name[:-2] == 'Gizah':
        resources['stone'] += 1
    elif wonder_name[:-2] == 'Babylon':
        resources['clay'] += 1
    elif wonder_name[:-2] == 'Olympia':
        resources['wood'] += 1
    elif wonder_name[:-2] == 'Rhodos':
        resources['ore'] += 1
        if wonder_name[-1] == 'A': # A side
            if wonder_stage >= 2:
                resources['shields'] += 2
        else: # B side
            if wonder_stage >= 1:
                resources['shields'] += 1
            if wonder_stage >= 2:
                resources['shields'] += 1
    elif wonder_name[:-2] == 'Ephesos':
        resources['papyrus'] += 1
    elif wonder_name[:-2] == 'Alexandria':
        resources['glass'] += 1
    elif wonder_name[:-2] == 'Halikarnassos':
        resources['loom'] += 1

    # Recurso de cartas
    for card in cards_played:
        # Wood +1
        if card in ['Tree Farm', 'Timber Yard', 'Forest Cave', 'Lumber Yard']:
            resources['wood'] += 1
        # Wood +2
        elif card in ['Sawmill']:
            resources['wood'] += 2
        # Stone +1
        if card in ['Stone Pit', 'Excavation', 'Timber Yard', 'Forest Cave', 'Mine']:
            resources['stone'] += 1
        # Stone +2
        elif card in ['Quarry']:
            resources['stone'] += 2
        # Clay +1
        if card in ['Clay Pool', 'Tree Farm', 'Excavation', 'Clay Pit']:
            resources['clay'] += 1
        # Clay +2
        elif card in ['Brickyard']:
            resources['clay'] += 2
        # Ore +1
        if card in ['Ore Vein', 'Clay Pit', 'Forest Cave', 'Mine']:
            resources['ore'] += 1
        # Ore +2
        elif card in ['Foundry']:
            resources['ore'] += 2
        # Loom +1
        if card in ['Loom']:
            resources['loom'] += 1
        # Glass +1
        elif card in ['Glassworks']:
            resources['glass'] += 1
        # Papyrus +1
        elif card in ['Press']:
            resources['papyrus'] += 1
        # Compass +1
        if card in ['Apothecary', 'Dispensary', 'Academy', 'Lodge']:
            resources['compass'] += 1
        # Table +1
        elif card in ['Scriptorium', 'School', 'Library', 'University']:
            resources['tablet'] += 1
        # Gear +1
        elif card in ['Workshop', 'Laboratory', 'Observatory', 'Study']:
            resources['gear'] += 1
        # Shields +1
        if card in ['Barracks', 'Stockade', 'Guard Tower']:
            resources['shields'] += 1
        # Shields +2
        elif card in ['Stables', 'Walls', 'Archery Range', 'Training Ground']:
            resources['shields'] += 2
        # Shields +3
        elif card in ['Circus', 'Arsenal', 'Fortifications', 'Siege Workshop']:
            resources['shields'] += 3

    return resources

def Main(num_players):
    browser = webdriver.Chrome(executable_path='./chromedriver')

    try:
        browser.get('file:///home/bettker/Desktop/Bot%20BGA/htmls/A1.html')
        parsed_html = bs4.BeautifulSoup(browser.page_source)

        cards_canplay, cards_couldplay, cards_cantplay = get_hand_cards(parsed_html)
        wonders_data, cards_played, coins = get_boards(parsed_html)

        data = {}
        data['players'] = {}
        for i in range(num_players):
            data['players'][str(i)] = {}

            data['players'][str(i)]['can_build_wonder'] = wonders_data[i]['can_build_wonder'][0] != 'cantplay'
            data['players'][str(i)]['wonder_id'] = wonders_data[i]['wonder_id']
            data['players'][str(i)]['wonder_name'] = wonders_data[i]['wonder_name']
            data['players'][str(i)]['wonder_stage'] = wonders_data[i]['wonder_stage']

            # Se for o jogador, add as cartas canplay e couldplay (pega apenas nome, removendo o campo de custo)
            if i == 0:
                print(cards_canplay)
                print(cards_couldplay)
                cards_playable = cards_canplay
                for c in cards_couldplay:
                    cards_playable.append(c[0])
                data['players'][str(i)]['cards_playable'] = cards_playable
                data['players'][str(i)]['cards_hand'] = cards_playable + cards_cantplay
            else:
                data['players'][str(i)]['cards_playable'] = []
                data['players'][str(i)]['cards_hand'] = []

            data['players'][str(i)]['cards_played'] = cards_played[i]
            data['players'][str(i)]['resources'] = get_resources(cards_played[i], wonders_data[i], coins[i])

        with open('game_status.json', 'w') as outfile:
            json.dump(data, outfile)

    except:
        e = sys.exc_info()[0]
        print('Erro: ' + str(e))

    finally:
        browser.quit()

if __name__ == '__main__':
    Main(3)
