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

d = Deck()
p1_hand = []
p2_hand = []
p1_hand.append(d.rand_take_card())
p1_hand.append(d.rand_take_card())
p2_hand.append(d.rand_take_card())
p2_hand.append(d.rand_take_card())

def show_hand():
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
# return tuple (a, b), a = who wins(0, 1, 2), b = winning multiplier(0, 1, 2, 3) if any of them reach dragon or inst win else return None
def check_winner(hand1: list,hand2: list, v1: list, v2: list):
    p1_win = check_inst_win_or_run(hand1, v1)
    p2_win = check_inst_win_or_run(hand2, v2)

    if p1_win <= 0 and p2_win <= 0:
        # continue fight
        # Make run away possible in future
        pass
    elif (p1_win < 0 and p2_win > 0) or (p1_win > 0 and p2_win < 0):
        # one of them can run away
        pass
    else:
        if p1_win == p2_win:
            return (0, 0)
        elif p1_win > p2_win:
            return (1, p1_win+1)
        elif p1_win < p2_win:
            return (2, p2_win+1)
        
    #check if one of them reach 5 cards, both of them cannot reach 5 cards at the same time
    if len(hand1) == 5:
        if 21 in v1:
            return (1, 3)
        elif v1[0] < 21: 
            return (1, 2)
        else: #explode
            return (2, 2)
    if len(hand2) == 5:
        if 21 in v2:
            return (2, 3)
        elif v2[0] < 21: 
            return (2, 2)
        else: #explode
            return (1, 2)
    return None

def check_duel(v1: list, v2: list):
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

# TODO: Decide before drawing any card whether to run away
EV_table = {
    "15": [2, 3, 4],
    "16": [2, 3, 4],
    "17": [2, 3, 4],
    "18": [2, 3, 4],
    "19": [2, 3, 4],
    "20": [2, 3, 4],
    "S4": [2, 3, 4], # soft 14...
    "S5": [2, 3, 4],
    "S6": [2, 3, 4],
    "S7": [2, 3, 4],
    "S8": [2, 3, 4],
    "S9": [2, 3, 4],# soft 19
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
        else:
            s = "S" + str(values[1]-1)
    return s
    


hand1 = [(3, 3), (0, 1), (3, 1), (0, 0)]
hand2 = [(0, 6), (0, 0)]
v1 = check_value(hand1)
v2 = check_value(hand2)
# print(v1)
print(v2)
# print(check_duel(v1, v2))
print(val_to_key(v2))
# hand2 = [(3, 0), (0, 1), (1, 0)]
# v2 = check_value(hand2)
# print(v1)
# print(v2)



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