import random
import os
import json
import time
import math

class Deck:
    def __init__(self):
        cards = []
        for i in range(52):
            cards.append((i%4, i%13))
        self.cards = sorted(cards)
    
    def shuffle(self):
        random.shuffle(self.cards)

    def remove_card(self, target:tuple):
        self.cards.remove(target)

    def add_card(self, target:tuple):
        self.cards.append(target)

    def rand_take_card(self):
        if not self.cards:
            return None
        index = random.randrange(len(self.cards))
        taken = self.cards[index]
        self.cards.pop(index)
        return taken

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def show_hand(p1_hand: list, p2_hand: list):
    print(f"P1 hand: {p1_hand} \nTotal P1 value: {check_value(p1_hand)}")
    print(f"P2 hand: {p2_hand} \nTotal P2 value: {check_value(p2_hand)}")

def check_value(hand: list):
    potential_values = {0}
    for card in hand:
        new_values = set()
        for v in potential_values:
            if card[1] >= 9:
                new_values.add(v + 10)
            elif card[1] == 0:
                new_values.add(v + 1)
                if len(hand) < 3:
                    new_values.add(v + 11)
                else:
                    new_values.add(v + 10)
            else:
                new_values.add(v + card[1] + 1)
        potential_values = new_values
    return sorted(list(potential_values))

# -1 means player can run, 1 or 2 means player win with that multiplier+1, 0 means player didnt win
def check_inst_win_or_run(hand: list, v: list):
    win = 0
    if len(hand) == 2:
        if 21 in v:
            win = 1
        elif hand[0][1] == hand[1][1]:
            if hand[0][1] == 0:
                win = 2
            else:
                win = 1
        elif 15 in v:
            win = -1
    return win
# return tuple (a, b), a = who wins(0, 1, 2), b = winning multiplier(0, 1, 2, 3)
def check_inst_winner(hand1: list,hand2: list, v1: list, v2: list):
    p1_win = check_inst_win_or_run(hand1, v1)
    p2_win = check_inst_win_or_run(hand2, v2)

    if p1_win <= 0 and p2_win <= 0:
        # continue fight or run away
        # Make run away possible in future
        return None
    elif (p1_win < 0 and p2_win > 0) or (p1_win > 0 and p2_win < 0):
        # one of them can run away
        return (0, 0) # Nothing happens
    else:
        if p1_win == p2_win:
            return (0, 0) #Draw no one wins
        elif p1_win > p2_win:
            return (1, p1_win+1)
        elif p1_win < p2_win:
            return (2, p2_win+1)
    


# dealer and player duel after dealer chose to stand, return tuple (a, b) where a = which player wins[0, 1, 2], and b = winning multiplier[0, 1, 2, 3]
def check_duel(hand1: list,hand2: list, v1: list, v2: list): #Assume no player reach 5 cards
    best1 = 0
    best2 = 0
    for v in v1:
        if v <= 21:
            best1 = max(best1, v)
        else:
            break
    for v in v2:
        if v <= 21:
            best2 = max(best2, v)
        else:
            break
    if best1 == best2:
        return (0, 0)
    elif best1 > best2:
        return (1, 2) if best1 == 21 else (1, 1)
    else:
        return (2, 2) if best2 == 21 else (2, 1)

# EV_table = {
#     "15": [2, 3, 4],
#     "16": [2, 3, 4],
#     "17": [2, 3, 4],
#     "18": [2, 3, 4],
#     "19": [2, 3, 4],
#     "20": [2, 3, 4],
#     "S15": [2, 3, 4],
#     "S16": [2, 3, 4],
#     "S17": [2, 3, 4],
#     "S18": [2, 3, 4],
#     "S19": [2, 3, 4],# soft 19
#     "S20": [2, 3, 4], # soft 20...
# }

# table_template = {
#     "15": [0.0, 0.0, 0.0],
#     "16": [0.0, 0.0, 0.0],
#     "17": [0.0, 0.0, 0.0],
#     "18": [0.0, 0.0, 0.0],
#     "19": [0.0, 0.0, 0.0],
#     "20": [0.0, 0.0, 0.0],
#     "S15": [0.0, 0.0, 0.0],
#     "S16": [0.0, 0.0, 0.0],
#     "S17": [0.0, 0.0, 0.0],
#     "S18": [0.0, 0.0, 0.0],
#     "S19": [0.0, 0.0, 0.0],# soft 19
#     "S20": [0.0, 0.0, 0.0],
# }
#Turn values into key for ev table for hands with enough value, if too small will have bug
def val_to_key(values: list):
    if not values:
        return None

    # Check for 21 separately
    if 21 in values:
        return None  # Or handle as special case

    # Prefer soft hand if available
    for v in reversed(values):
        if 15 <= v <= 20:
            if v > values[0]:  # Likely a soft total
                return f"S{v}"
            else:
                return str(v)

    # Fallback: use lowest valid value
    if 15 <= values[0] <= 20:
        return str(values[0])

    return None  # No valid key
# Check if 5 cards and return result (a, b) with who won and how much. If < 5 cards, return None
def check_five_cards(hand: list, value: list, player: int) -> tuple:
    if len(hand) == 5:
        if 21 in value:
            return (player, 3)
        elif value[0] < 21:
            return (player, 2)
        else:
            if player == 1: #opponent win by 2
                return (2, 2)
            else:
                return (1, 2)
    return None

def take_until_enough(hand: list, deck:Deck) -> tuple[list, list]:
    value = check_value(hand)
    if len(hand) < 5:
        while not any(15 < v < 22 for v in value) and value[0] < 22: #Take until enough
            hand.append(deck.rand_take_card())
            value = check_value(hand)
            if len(hand) == 5: 
                break
    return hand, value

def enter_into_table(outcome: int, actions: list, hit_table: dict, hitnum_table: dict, stand_table: dict, standnum_table: dict) -> None:
    '''
    Enter a list of actions containing tuple of ("hand", hit?, handSize/num of cards when I make the action) and the outcome, then updates the tables
    '''
    for action in actions:
        position, hit, handSize = action
        if position and handSize - 2 < 3: # Check if valid position and handSize
            if hit:
                hitnum_table[position][handSize-2] += 1
                hit_table[position][handSize-2] += outcome
            else:
                standnum_table[position][handSize-2] += 1
                stand_table[position][handSize-2] += outcome


def calc_score(hit: bool, position: str, handSize: int, earning_table: dict, hit_num_simul: dict, stand_num_simul: dict) -> float:
    '''
    Calculate score of each move whether it is hit or stand based on table
    Formula:
    score = E/N + sqrt(2 * ln(N + N')/N)
    E = total earning made from this action
    N = number of simulation for this action
    N' = number of simulation for the opposite action (if N is hit, then N' is stand and vice versa)
    '''
    try:
        E = earning_table[position][handSize-2]
        if hit: #Calculating score for player hitting?
            N = hit_num_simul[position][handSize-2]
            Np = stand_num_simul[position][handSize-2]
        else: # Calculating score for player standing
            Np = hit_num_simul[position][handSize-2]
            N = stand_num_simul[position][handSize-2]
        if N == 0: #force exploration if never explore before
            return float('inf')
        
        exploration = math.sqrt(2 * math.log(N+Np)/N)
        exploitation = E/N

        return exploitation + exploration
    except Exception as e:
        print("\n" + "="*40)
        print(f"💥 CRASH DETECTED: {type(e).__name__}: {e}")
        print("="*40)
        print("📍 Function: calc_score")
        print("📦 Variables at crash time:")
        
        # locals() returns a dictionary of all local variables
        for var_name, value in locals().items():
            # Skip hiding internal variables like 'e' or 'var_name' if you want
            print(f"   {var_name} = {value}")
            
        print("="*40 + "\n")
        
        # Re-raise the exception so the program still stops (important!)
        raise

def simulate() -> None:
    print()
    deck = Deck()
    player_hand = []
    dealer_hand = []
    player_hand.append(deck.rand_take_card())
    player_hand.append(deck.rand_take_card())
    dealer_hand.append(deck.rand_take_card())
    dealer_hand.append(deck.rand_take_card())
    player_value = check_value(player_hand)
    dealer_value = check_value(dealer_hand)
    inst = check_inst_winner(player_hand, dealer_hand, player_value, dealer_value)
    if inst:
        print(f"player {inst[0]} inst won {inst[1]}X")
        show_hand(player_hand, dealer_hand)
    else:
        player_action = []
        dealer_action = []
        if 15 in player_value: #Player run?
            # run = random.randint(0,1)
            hit_score = calc_score(True, val_to_key(player_value), len(player_hand), player_hit_table, player_hitnum_table, player_standnum_table)
            stand_score = calc_score(False, val_to_key(player_value), len(player_hand), player_stand_table, player_hitnum_table, player_standnum_table)
            if hit_score < stand_score:
                player_action.append((val_to_key(player_value), 0, len(player_hand)))
                # insert into EV table
                player_standnum_table[val_to_key(player_value)][0] += 1 # 0 means when there is only 2 cards
                print("Player 1 ran away")
                show_hand(player_hand, dealer_hand)
                return
            else: #player hit
                player_action.append((val_to_key(player_value), 1, len(player_hand)))
                player_hand.append(deck.rand_take_card())
                player_value = check_value(player_hand)
            
        if 15 in dealer_value: # Dealer run?
            # run = random.randint(0,1)
            hit_score = calc_score(True, val_to_key(dealer_value), len(dealer_hand), dealer_hit_table, dealer_hitnum_table, dealer_standnum_table)
            stand_score = calc_score(False, val_to_key(dealer_value), len(dealer_hand), dealer_stand_table, dealer_hitnum_table, dealer_standnum_table)
            if hit_score < stand_score:
                dealer_action.append((val_to_key(dealer_value), 0, len(dealer_hand)))
                # insert into EV table
                dealer_standnum_table[val_to_key(dealer_value)][0] += 1
                print("Dealer ran away")
                show_hand(player_hand, dealer_hand)
                return
            else: 
                # dealer chose to hit
                dealer_action.append((val_to_key(dealer_value), 1, len(dealer_hand)))
                dealer_hand.append(deck.rand_take_card())
                dealer_value = check_value(dealer_hand)
        
        # Player forced to take cards   
        player_hand, player_value = take_until_enough(player_hand, deck)
        result = check_five_cards(player_hand, player_value, 1) # 1 means player 1
        if result: # forced to take cards until bust, so action is not appended
            print(f"Player {result[0]} win with {result[1]}x multiplier")
            show_hand(player_hand, dealer_hand)
            if result[0] == 1: # if player one wins
                player_reward = result[1]
            else:
                player_reward = -result[1]
            enter_into_table(player_reward, player_action, player_hit_table, player_hitnum_table, player_stand_table, player_standnum_table)
            enter_into_table(-player_reward, dealer_action, dealer_hit_table, dealer_hitnum_table, dealer_stand_table, dealer_standnum_table)
            return #end simulation


        #Player's turn of taking cards actions
        while len(player_hand) < 5:
            # Check if player are forced to take cards
            if not any(16 < v < 22 for v in player_value) and player_value[0] < 22:
                player_hand, player_value = take_until_enough(player_hand, deck)

            # Check if busted or alr 21 or reach 5 cards
            if player_value[0] >= 21 or len(player_hand) >= 5 or 21 in player_value:
                player_action.append((val_to_key(player_value), 0, len(player_hand)))
                break
            hit_score = calc_score(True, val_to_key(player_value), len(player_hand), player_hit_table, player_hitnum_table, player_standnum_table)
            stand_score = calc_score(False, val_to_key(player_value), len(player_hand), player_stand_table, player_hitnum_table, player_standnum_table)
            if (hit_score > stand_score):
                player_action.append((val_to_key(player_value), 1, len(player_hand)))
                player_hand.append(deck.rand_take_card())
                player_value = check_value(player_hand)
            else:
                player_action.append((val_to_key(player_value), 0, len(player_hand)))
                break
        
        
        #Check if player reach 5 cards
        result = check_five_cards(player_hand, player_value, 1) # 1 means player 1
        if result:
            print(f"Player {result[0]} win with {result[1]}x multiplier")
            show_hand(player_hand, dealer_hand)
            # Enter into EV table
            if result[0] == 1: # if player one wins
                player_reward = result[1]
            else:
                player_reward = -result[1]
            enter_into_table(player_reward, player_action, player_hit_table, player_hitnum_table, player_stand_table, player_standnum_table)
            enter_into_table(-player_reward, dealer_action, dealer_hit_table, dealer_hitnum_table, dealer_stand_table, dealer_standnum_table)
            return #end simulation
            
        # dealer forced to take cards
        dealer_hand, dealer_value = take_until_enough(dealer_hand, deck) 
        result = check_five_cards(dealer_hand, dealer_value, 2) # 2 means player 2
        if result:
            print(f"Player {result[0]} win with {result[1]}x multiplier")
            show_hand(player_hand, dealer_hand)
            if result[0] == 1: # if player one wins
                player_reward = result[1]
            else:
                player_reward = -result[1]
            enter_into_table(player_reward, player_action, player_hit_table, player_hitnum_table, player_stand_table, player_standnum_table)
            enter_into_table(-player_reward, dealer_action, dealer_hit_table, dealer_hitnum_table, dealer_stand_table, dealer_standnum_table)
            return #end simulation
        
        # Dealer's turn of taking card actions
        while len(dealer_hand) < 5: 
            # Check if player are forced to take cards
            if not any(16 < v < 22 for v in dealer_value) and dealer_value[0] < 22:
                dealer_hand, dealer_value = take_until_enough(dealer_hand, deck)

            # Check if busted or alr 21 or reach 5 cards
            if dealer_value[0] >= 21 or len(dealer_hand) >= 5 or 21 in dealer_value:
                dealer_action.append((val_to_key(dealer_value), 0, len(dealer_hand)))
                break
            hit_score = calc_score(True, val_to_key(dealer_value), len(dealer_hand), dealer_hit_table, dealer_hitnum_table, dealer_standnum_table)
            stand_score = calc_score(False, val_to_key(dealer_value), len(dealer_hand), dealer_stand_table, dealer_hitnum_table, dealer_standnum_table)
            if (hit_score > stand_score):
                dealer_action.append((val_to_key(dealer_value), 1, len(dealer_hand)))
                dealer_hand.append(deck.rand_take_card())
                dealer_value = check_value(dealer_hand)
            else:
                dealer_action.append((val_to_key(dealer_value), 0, len(dealer_hand)))
                break
        # Check if dealer reach 5 cards
        result = check_five_cards(dealer_hand, dealer_value, 2) # 2 means player 2
        if result:
            print(f"Player {result[0]} win with {result[1]}x multiplier")
            show_hand(player_hand, dealer_hand)
            # Enter into EV table
            if result[0] == 1: # if player one wins
                player_reward = result[1]
            else:
                player_reward = -result[1]
            enter_into_table(player_reward, player_action, player_hit_table, player_hitnum_table, player_stand_table, player_standnum_table)
            enter_into_table(-player_reward, dealer_action, dealer_hit_table, dealer_hitnum_table, dealer_stand_table, dealer_standnum_table)
            return #end simulation
        
        # Make them duel then enter into EV table
        duel_outcome = check_duel(player_hand, dealer_hand, player_value, dealer_value)
        show_hand(player_hand, dealer_hand)
        print(f"Player DUEL: player {duel_outcome[0]} wins with {duel_outcome[1]}x bet")
        print(f"Player action: {player_action}\t Dealer action: {dealer_action}")
        if duel_outcome[0] == 0:
            return # its a draw
        if duel_outcome[0] == 1: #player wins
            reward = duel_outcome[1]
        if duel_outcome[0] == 2:
            reward = -duel_outcome[1]
            
        enter_into_table(reward, player_action, player_hit_table, player_hitnum_table, player_stand_table, player_standnum_table)
        enter_into_table(-reward, dealer_action, dealer_hit_table, dealer_hitnum_table, dealer_stand_table, dealer_standnum_table)

def open_or_create_file(filepath: str) -> dict:
    table_template = {
        "15": [0, 0, 0],
        "16": [0, 0, 0],
        "17": [0, 0, 0],
        "18": [0, 0, 0],
        "19": [0, 0, 0],
        "20": [0, 0, 0],
        "S15": [0, 0, 0],
        "S16": [0, 0, 0],
        "S17": [0, 0, 0],
        "S18": [0, 0, 0],
        "S19": [0, 0, 0],# soft 19
        "S20": [0, 0, 0],
    }
    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            resultDict = json.load(f)
    else:
        with open(filepath, "w") as f:
            json.dump(table_template, f, indent=4)
            resultDict = table_template
    return resultDict

if __name__ == "__main__":
    start_time = time.perf_counter()
    hand1 = [(3, 10), (0, 7), (0, 2)]
    hand2 = [(0, 0), (0, 3), (0, 0)]
    v1 = check_value(hand1)
    v2 = check_value(hand2)
    # Load from file, create if file doesn't exist
    player_hit_table = open_or_create_file("player_hit_table.json")
    player_stand_table = open_or_create_file("player_stand_table.json")
    player_hitnum_table = open_or_create_file("player_hitnum_table.json")
    player_standnum_table = open_or_create_file("player_standnum_table.json")
    dealer_hit_table = open_or_create_file("dealer_hit_table.json")
    dealer_stand_table = open_or_create_file("dealer_stand_table.json")
    dealer_hitnum_table = open_or_create_file("dealer_hitnum_table.json")
    dealer_standnum_table = open_or_create_file("dealer_standnum_table.json")

    # Runs simulate for n amount of times
    for i in range(1000):
        simulate()

    # Write everythings into the files
    with open("player_hit_table.json", "w") as f:
        json.dump(player_hit_table, f, indent=4)
    with open("player_stand_table.json", "w") as f:
        json.dump(player_stand_table, f, indent=4)
    with open("player_hitnum_table.json", "w") as f:
        json.dump(player_hitnum_table, f, indent=4)
    with open("player_standnum_table.json", "w") as f:
        json.dump(player_standnum_table, f, indent=4)

    with open("dealer_hit_table.json", "w") as f:
        json.dump(dealer_hit_table, f, indent=4)
    with open("dealer_stand_table.json", "w") as f:
        json.dump(dealer_stand_table, f, indent=4)
    with open("dealer_hitnum_table.json", "w") as f:
        json.dump(dealer_hitnum_table, f, indent=4)
    with open("dealer_standnum_table.json", "w") as f:
        json.dump(dealer_standnum_table, f, indent=4)
    end_time = time.perf_counter()
    elapsed_time = end_time - start_time
    print(f"Code executed in {elapsed_time:.4f} seconds")
