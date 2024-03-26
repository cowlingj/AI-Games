from enum import Enum
from functools import reduce
import itertools
from operator import add
import random
import time

dealer_stands = 17
starting_chips = 1000
rounds = 10
target = 21
minimum_bet = 100

values = [('A', [1, 11])] + [(str(x), [x]) for x in range(2, 11)] + [('J', [10]), ('Q', [10]), ('K', [10])]
Suit = Enum('Suit', ['CLUBS', 'DIAMONDS', 'HEARTS', 'SPADES'])
cards = [(name, suit, values) for ((name, values), suit) in itertools.product(values, Suit)]

class Deck:
    def __init__(self):
        self._deck: list[tuple[str, type[Suit], list[int]]] = []
    def draw(self) -> tuple[str, type[Suit], list[int]]:
        if len(self._deck) == 0:
            self._deck = random.sample(cards, len(cards))
        return  self._deck.pop()

def best_value(cards: list[tuple[str, type[Suit], list[int]]]) -> int:
    if len(cards) == 0:
        return 0
    possible_values = [ reduce(add, x, 0) for x in itertools.product(*[ values for (_, _, values) in cards]) ]
    not_bust = [ v for v in filter(lambda v : v <= target, possible_values) ]
    return max(not_bust) if len(not_bust) > 0 else min(filter(lambda v : v > target, possible_values))

def display_suit(suit: type[Suit]) -> str:
    return (u'\u2667', u'\u2666', u'\u2665', u'\u2664')[suit.value - 1]
def display_hand(cards: list[tuple[str, type[Suit], list[int]]]) -> str:
    return str([ f"{name}{display_suit(suit)}" for (name, suit, _) in cards ])

chips: int = starting_chips
deck = Deck()
for round in range(rounds):

    if chips <= 0:
        print("You have no more chips!")
        break

    dealers_cards = []
    players_cards = []

    print("-------------")
    print(f"round {round + 1}/{rounds}")
    print("-------------")
    
    print(f"Chips: {chips}")

    bet_str = input(f"Bet (enter a number or \"-\" for min={min(minimum_bet, chips)} bet or \"+\" for max={chips} bet) > ").strip()
    if bet_str == "+":
        bet = chips
    elif bet_str == "-":
        bet = min(minimum_bet, chips)
    else:
        bet = int(bet_str)
        if bet < minimum_bet:
            raise ValueError(f"bet \"{bet}\" is less than minimum bet of {minimum_bet}")
    
    chips -= bet  
    print(f"Chips: {chips}, Bet: {bet}")

    players_cards.append(deck.draw())
    players_cards.append(deck.draw())
    dealers_cards.append(deck.draw())

    if best_value(players_cards) == target:
        print("Blackjack! (x2 winnings)")
        chips += bet * 3
        continue
    
    while True:
        print(f"Dealer: {display_hand(dealers_cards)} = {best_value(dealers_cards)}, You: {display_hand(players_cards)} = {best_value(players_cards)}")

        if best_value(players_cards) == target:
            print(f"{target}! (1.5x winnings)")
            chips += int(bet * 2.5)
            break
        if best_value(players_cards) > target:
            print("Bust!")
            break

        if len(players_cards) == 2 and bet <= chips:
            choice = input("Hit (H), Stand (S), Double Down (D) > ").strip().upper()
        else:
            choice = input("Hit (H), Stand (S) > ").strip().upper()
        
        if choice == "D" and (len(players_cards) != 2 or bet > chips):
            raise ValueError(f"Invalid choice \"{choice}\"")

        if choice == "H":
            players_cards.append(deck.draw())
            continue

        if choice == "D":
            chips -= bet
            bet += bet
            print(f"Chips: {chips}, Bet: {bet}")
            players_cards.append(deck.draw())
            print(f"Dealer: {display_hand(dealers_cards)} = {best_value(dealers_cards)}, You: {display_hand(players_cards)} = {best_value(players_cards)}")
            if best_value(players_cards) == target:
                print(f"{target}! (1.5x winnings)")
                chips += int(bet * 2.5)
                break
            if best_value(players_cards) > target:
                print("Bust!")
                break

        if choice == "D" or choice == "S":
            while best_value(dealers_cards) <= dealer_stands:
                dealers_cards.append(deck.draw())
                print(f"Dealer: {display_hand(dealers_cards)} = {best_value(dealers_cards)}, You: {display_hand(players_cards)} = {best_value(players_cards)}")
                time.sleep(0.5)
            dealer_value = best_value(dealers_cards)
            player_value = best_value(players_cards)
            if dealer_value > target:
                print("Dealer bust!")
                chips += bet * 2
                break
            elif dealer_value > player_value:
                print("Dealer wins!")
                break
            elif dealer_value < player_value:
                print("You win!")
                chips += bet * 2
                break
            else:
                print("Tie!")
                chips += bet
                break
        else:
            raise ValueError(f"Invalid choice \"{choice}\"")

print(f"Final Score: {chips}")
