# 21EV

---

Calculate the best way to play banluck using Monte Carlo simulation with Upper Confidence Bound 1 algorithm.

## Game rules

**Initial Deal**

The banker deals 2 cards to all players face down, then deals himself 2 cards face down.

**Counting**

- 2 - 9 , face value
- 10, J, Q, K - 10
- A - 1 or 11 for a hand of 2 cards
- A - 10 or 1 for a hand of 3 to 5 cards

**Instant win**

- If any player including dealer get blackjack (an Ace and any value 10 cards) they win 2x bet
- If any player get two of the same cards (e.g. 7-7, or Q-Q) they win 2x bet, unless they get A-A, then they will win 3x bet
- If any player get value of 15 on initial draw (whether softhand A, 4 or hardhand), they can choose to fold and not participate in that round. They won't win or lose any bet. They can only fold(run away) when they have 2 cards. They are able to escape instant win and any other scenario, effectively didn't participate that round.
- If both dealer and player get same strength hand, they will draw and no one win anything. If one get A-A, and the other get blackjack or normal pair, then the one with A-A will still win 3x bet

**Payouts**

- Ngou Leng (5 cards in hand without busting) - 2X bet. This is an immediate payout event. Which means the banker pays out the moment the player Ngou Lengs.
- If you bust in your attempt to ngou(getting the 5th card), you pay the banker 2X.
- You win AS LONG AS your total point value is 21 or below. That means that you win EVEN IF your total point value is 15 or below. 2-3-3-4-2 has a point total of 14 but the banker has to pay this hand. If the player Ngou Leng and have value of 21, the player wins 3x
- Player wins 1x bet if the value of their hand is greater than dealer without busting. If player and dealer have the same value, they will draw.
- If the banker ngous in his game, all players pay 2X to the banker REGARDLESS of the player's hand (bust or no bust). If dealer bust when getting his 5th cards, he has to pay every player regardless if they bust or no bust
- If player or dealer bust, while the other didn't, they only lose 1x bet.
- A regular 21 gives 2x bet compare to normal hand when dueling

**Gameplay**

- In the Singaporean context, you cannot perform splits (split one hand into 2 if both cards drawn are of the same rank)
- Dealer cannot see players cards and player cannot see dealers cards.
- Each player draw cards until they have enough points or they busted. When a players turn ended, next player can draw cards. The dealer always go last.
- A player can hit until he has enough points. A player must have a point total of **at least 16**
- A player must show all 4 cards if he intends to ngou leng. Then he can draw the last card to gamble on it.

**Banker's Move**

- At the banker's turn, after all players have completed drawing, he can show his hand if it is 16 or above. He can then start "dueling" other players. For example, if the banker has 16, he can ask people with 3 cards to show as they could be bust. He could duel as many players before drawing his next card.

## Strategy Table

### 🎮 Player Ban-Luck Strategy Table

| Hand \ Size | 2 Cards  | 3 Cards  | 4 Cards  |
| :---------: | :------: | :------: | :------: |
|   **15**    | 🔵 STAND |    ⚪    |    ⚪    |
|   **16**    |  🔴 HIT  |  🔴 HIT  |  🔴 HIT  |
|   **17**    | 🔵 STAND | 🔵 STAND | 🔵 STAND |
|   **18**    | 🔵 STAND | 🔵 STAND | 🔵 STAND |
|   **19**    | 🔵 STAND | 🔵 STAND | 🔵 STAND |
|   **20**    | 🔵 STAND | 🔵 STAND | 🔵 STAND |
|   **S15**   |  🔴 HIT  |    ⚪    |    ⚪    |
|   **S16**   |  🔴 HIT  |  🔴 HIT  |  🔴 HIT  |
|   **S17**   |  🔴 HIT  |  🔴 HIT  |  🔴 HIT  |
|   **S18**   |  🔴 HIT  |  🔴 HIT  |  🔴 HIT  |
|   **S19**   | 🔵 STAND |  🔴 HIT  |  🔴 HIT  |
|   **S20**   | 🔵 STAND |  🔴 HIT  |  🔴 HIT  |

> **Legend:** 🔴 = Hit | 🔵 = Stand | ⚪ = Not Applicable

### 🎮 Dealer Ban-Luck Strategy Table

| Hand \ Size | 2 Cards  | 3 Cards  | 4 Cards  |
| :---------: | :------: | :------: | :------: |
|   **15**    | 🔵 STAND |    ⚪    |    ⚪    |
|   **16**    |  🔴 HIT  |  🔴 HIT  |  🔴 HIT  |
|   **17**    | 🔵 STAND | 🔵 STAND | 🔵 STAND |
|   **18**    | 🔵 STAND | 🔵 STAND | 🔵 STAND |
|   **19**    | 🔵 STAND | 🔵 STAND | 🔵 STAND |
|   **20**    | 🔵 STAND | 🔵 STAND | 🔵 STAND |
|   **S15**   |  🔴 HIT  |    ⚪    |    ⚪    |
|   **S16**   |  🔴 HIT  |  🔴 HIT  |  🔴 HIT  |
|   **S17**   |  🔴 HIT  |  🔴 HIT  |  🔴 HIT  |
|   **S18**   |  🔴 HIT  |  🔴 HIT  |  🔴 HIT  |
|   **S19**   | 🔵 STAND |  🔴 HIT  |  🔴 HIT  |
|   **S20**   | 🔵 STAND |  🔴 HIT  |  🔴 HIT  |

> **Legend:** 🔴 = Hit | 🔵 = Stand | ⚪ = Not Applicable
