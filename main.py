import random
import os
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
        pass
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
    return None


# dealer and player duel after dealer chose to stand, return tuple (a, b) where a = which player wins(0, 1, 2), and b = winning multiplier(0, 1, 2, 3)
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

EV_table = {
    "15": [2, 3, 4],
    "16": [2, 3, 4],
    "17": [2, 3, 4],
    "18": [2, 3, 4],
    "19": [2, 3, 4],
    "20": [2, 3, 4],
    "S14": [2, 3, 4], # soft 14...
    "S15": [2, 3, 4],
    "S16": [2, 3, 4],
    "S17": [2, 3, 4],
    "S18": [2, 3, 4],
    "S19": [2, 3, 4],# soft 19
}
#Turn values into key for ev table for hands with enough value, if too small will have bug
def val_to_key(values: list):
    s = ""
    if len(values) < 2:
        if values[0] > 20 or values[0] < 15:
            print("ERROR: Value too big or too small")
            return None
        s = str(values[0])
    else: 
        if values[1] < 15:
            print("ERROR: softhand too small")
            return None
        if values[1] > 21: #softhand forced into hard one
            s = str(values[0])
        elif values[1] == 21:
            print("ERROR: You alr have 21")
            return None
        else: #Softhand
            s = "S" + str(values[1])
    return s
# Check if 5 cards and return result. If < 5 cards, return None
def check_five_cards(hand: list, value: list) -> str:
    if len(hand) == 5:
        if 21 in value:
            return "dragon_21"
        elif value[0] < 21:
            return "dragon"
        else:
            return "bust"
    return None

def take_until_enough(hand: list, deck:Deck) -> tuple[list, list]:
    value = check_value(hand)
    while value[-1] < 16: #Take until enough
        hand.append(deck.rand_take_card())
        value = check_value(hand)
        if len(hand) == 5: 
            break
    return hand, value

def simulate() -> None:
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
            run = random.randint(0,1)
            if run:
                player_action.append((val_to_key(player_value), run, len(player_hand)))
                # insert into EV table
                print("Player 1 ran away")
                show_hand(player_hand, dealer_hand)
                return
        if 15 in dealer_value: # Dealer run?
            run = random.randint(0,1)
            if run:
                dealer_action.append((val_to_key(dealer_value), run, len(dealer_hand)))
                # insert into EV table
                print("Dealer ran away")
                show_hand(player_hand, dealer_hand)
                return
        
        # Player forced to take cards   
        player_hand, player_value = take_until_enough(player_hand, deck)
        result = check_five_cards(player_hand, player_value)
        if result:
            match result:
                case "dragon_21":
                    print(f"Player 1 win with 3x multiplier")
                    show_hand(player_hand, dealer_hand)
                case "dragon":
                    print(f"Player 1 win with 3x multiplier")
                    show_hand(player_hand, dealer_hand)
                case "bust":
                    print(f"Player 1 lose with 2x multiplier")
                    show_hand(player_hand, dealer_hand)
                case _:
                    print("ERROR: unknown results from check_dragon")
                    show_hand(player_hand, dealer_hand)
            return #end simulation
        
        #Player's turn of taking cards actions
        while len(player_hand) < 5: 
            hit = random.randint(0,1) #randomly hit or stand until explode or stop
            if hit and player_value[0] < 21 and 21 not in player_value:
                player_action.append((val_to_key(player_value), hit, len(player_hand)))
                player_hand.append(deck.rand_take_card())
                player_value = check_value(player_hand)
            else:
                player_action.append((val_to_key(player_value), hit, len(player_hand)))
                break

        #Check if player reach 5 cards
        result = check_five_cards(player_hand, player_value)
        if result:
            match result:
                case "dragon_21":
                    print(f"Player 1 win with 3x multiplier")
                    show_hand(player_hand, dealer_hand)
                case "dragon":
                    print(f"Player 1 win with 3x multiplier")
                    show_hand(player_hand, dealer_hand)
                case "bust":
                    print(f"Player 1 lose with 2x multiplier")
                    show_hand(player_hand, dealer_hand)
                case _:
                    print("ERROR: unknown results from check_dragon")
                    show_hand(player_hand, dealer_hand)
            # Enter into EV table
            return #end simulation
            
        # dealer forced to take cards
        dealer_hand, dealer_value = take_until_enough(dealer_hand, deck)
        result = check_five_cards(dealer_hand, dealer_value)
        if result:
            match result:
                case "dragon_21":
                    print(f"Player 2 win with 3x multiplier")
                    show_hand(player_hand, dealer_hand)
                case "dragon":
                    print(f"Player 2 win with 3x multiplier")
                    show_hand(player_hand, dealer_hand)
                case "bust":
                    print(f"Player 2 lose with 2x multiplier")
                    show_hand(player_hand, dealer_hand)
                case _:
                    print("ERROR: unknown results from check_dragon")
                    show_hand(player_hand, dealer_hand)
            return #end simulation
        
        # Dealer's turn of taking card actions
        while len(dealer_hand) < 5: 
            hit = random.randint(0,1) #randomly hit or stand until explode or stop
            if hit and dealer_value[0] < 21 and 21 not in dealer_value:
                dealer_action.append((val_to_key(dealer_value), hit, len(dealer_hand)))
                dealer_hand.append(deck.rand_take_card())
                dealer_value = check_value(dealer_hand)
            else:
                dealer_action.append((val_to_key(dealer_value), hit, len(dealer_hand)))
                break
        # Check if dealer reach 5 cards
        result = check_five_cards(dealer_hand, dealer_value)
        if result:
            match result:
                case "dragon_21":
                    print(f"Player 2 win with 3x multiplier")
                    show_hand(player_hand, dealer_hand)
                case "dragon":
                    print(f"Player 2 win with 3x multiplier")
                    show_hand(player_hand, dealer_hand)
                case "bust":
                    print(f"Player 2 lose with 2x multiplier")
                    show_hand(player_hand, dealer_hand)
                case _:
                    print("ERROR: unknown results from check_dragon")
                    show_hand(player_hand, dealer_hand)
            # Enter into EV table
            return #end simulation
        
        # Make them duel then enter into EV table
        show_hand(player_hand, dealer_hand)
        print(f"Player action: {player_action}\t Dealer action: {dealer_action}") #TODO: make emptying dealer and player hand


# show_hand(hand1, hand2)
# print(check_inst_winner(hand1, hand2, v1, v2))
# print(v1)
# print(v2)
# print(check_duel(v1, v2))
# print(val_to_key(v2))
# print(EV_table[val_to_key(v2)])
# hand2 = [(3, 0), (0, 1), (1, 0)]
# v2 = check_value(hand2)


if __name__ == "__main__":
    hand1 = [(3, 9), (0, 4), (0, 4), (0, 2), (0, 1)]
    hand2 = [(0, 5), (0, 5)]
    v1 = check_value(hand1)
    v2 = check_value(hand2)
    simulate()


# while True:
#     show_hand()
#     action = input("(P1) Would you like to take a card? [Y/N]\n").upper()
#     clear()
#     if action == "Y":
#         p1_hand.append(d.rand_take_card())
#     elif action == "N":
#         break
#     else:
#         print("Invalid action, please try again.")
# while True:
#     show_hand()
#     action = input("(P2) Would you like to take a card? [Y/N]\n").upper()
#     clear()
#     if action == "Y":
#         p2_hand.append(d.rand_take_card())
#     elif action == "N":
#         break
#     else:
#         print("Invalid action, please try again.")
# show_hand()