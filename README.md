# 🧠 Chess AI in Python

This is a Chess AI project built in Python. The AI uses classical techniques like move generation and evaluation with NegaMax and alpha-beta pruning, and supports Standard Algebraic Notation (SAN) for move representation.

## ♟️ Features

- Play as **White** or **Black**
- Play **Human vs Human** or **Human vs AI**
- Basic AI with static evaluation
- Legal move generation
- SAN (Standard Algebraic Notation) support
- Save games in pgn formate

## 🚀 Getting Started

1. Clone this repository:
   git clone https://github.com/fenil07/chess.git

## 🕹️ Game Instructions

To play against the AI, set the following values inside the `main` function of `main.py`:

```python
playerOne = True  # True = Human plays White, False = AI plays White
playerTwo = True  # True = Human plays Black, False = AI plays Black
You can configure different match types using these flags:

Human vs Human: playerOne = True, playerTwo = True

Human vs AI (as White): playerOne = True, playerTwo = False

Human vs AI (as Black): playerOne = False, playerTwo = True

AI vs AI: playerOne = False, playerTwo = False

### 📁 Game PGN Output

After completing a game, a PGN (Portable Game Notation) file is automatically saved inside the `games/` folder.

You can use this PGN file to review or analyze your game on platforms like:

- [Lichess PGN Import](https://lichess.org/paste)
- [Chess.com Analysis Board](https://www.chess.com/analysis)

#### 📌 Example

A sample game file is included in the repository:

📄 [`games/demo_game.pgn`](games/demo_game.pgn)

You can upload this file directly to Lichess or Chess.com to see how the analysis works.

---
> If the `games/` folder doesn't exist, it will be created automatically after your first game.

[Event "Demo Game"]
[Site "Local"]
[Date "2025.04.11"]
[Round "-"]
[White "Human"]
[Black "AI"]
[Result "1-0"]

1. e4 e5 2. Nf3 Nc6 3. Bb5 a6 4. Ba4 Nf6 5. O-O Be7 6. Re1 b5 7. Bb3 d6
8. c3 O-O 9. h3 Nb8 10. d4 Nbd7 11. Nbd2 Bb7 12. Bc2 Re8 13. Nf1 Bf8
14. Ng3 g6 15. a4 c5 16. d5 c4 17. Be3 Qc7 18. Qd2 Nc5 19. Bh6 Bxh6
20. Qxh6 Kh8 21. Nf5 gxf5 22. Qxf6+ Kg8 23. Nh4 f4 24. Nf5 Ne6 25. dxe6 fxe6
26. Nh6# 1-0
