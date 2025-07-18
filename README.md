
# 🧠 Chess AI in Python

A full-featured **Chess AI** project built with Python. This engine implements classical techniques like **move generation**, **NegaMax with Alpha-Beta pruning**, and **SAN (Standard Algebraic Notation)** for representing moves.

Designed for both educational use and casual gameplay, this project helps demonstrate algorithmic thinking, OOP, and game logic in a polished and interactive application.

---

## ♟️ Features

- ✅ **Human vs Human**, **Human vs AI**, and **AI vs AI** gameplay modes  
- ✅ Play as **White** or **Black**
- ✅ **Legal move generation** with check/checkmate detection  
- ✅ **Standard Algebraic Notation (SAN)** support  
- ✅ Automatic **PGN (Portable Game Notation)** game export  
- ✅ GUI built using **Pygame**
- ✅ Dynamic game status display (turn, check, mate, etc.)

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/fenil07/chess.git
cd chess
```

---

## 🕹️ Game Instructions

To play against the AI, set the following values inside the `main` function of `main.py`:

```python
playerOne = True  # True = Human plays White, False = AI plays White
playerTwo = True  # True = Human plays Black, False = AI plays Black
```

You can configure different match types using these flags:

- Human vs Human: `playerOne = True`, `playerTwo = True`  
- Human vs AI (as White): `playerOne = True`, `playerTwo = False`  
- Human vs AI (as Black): `playerOne = False`, `playerTwo = True`  
- AI vs AI: `playerOne = False`, `playerTwo = False`

---

### 📁 Game PGN Output

After completing a game, a PGN (Portable Game Notation) file is automatically saved inside the `games/` folder.

You can use this PGN file to review or analyze your game on platforms like:

- [Lichess PGN Import](https://lichess.org/paste)
- [Chess.com Analysis Board](https://www.chess.com/analysis)

#### 📌 Example

A sample game file is included in the repository:

📄 [`games/demo_game.pgn`](games/demo_game.pgn)

You can upload this file directly to Lichess or Chess.com to see how the analysis works.

> If the `games/` folder doesn't exist, it will be created automatically after your first game.

```pgn
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
```

---

## 🧠 AI Logic Overview

The Chess AI is built on classical techniques used in traditional chess engines:

- ♟️ **Move Generation Engine**:  
  Handles all legal moves including:
  - Checks and pins  
  - Castling (both kingside and queenside)  
  - En passant  
  - Pawn promotion

- 📈 **Evaluation Function**:  
  Uses a static evaluation based on:
  - Material balance  
  - Piece-square tables  
  - Positional considerations (e.g., central control)

- 🔍 **Search Algorithm**:  
  Implements **NegaMax** with **Alpha-Beta Pruning** to reduce the number of nodes explored and improve performance.

---

### 🧪 Extendability

This AI is simple at the time for learning purposes, but looking forward to improved by implementing:

- 📚 **Move Ordering** (e.g., killer heuristic, history heuristic)  
- 🔎 **Quiescence Search** to avoid the horizon effect  
- 🧠 **Transposition Tables** to store and reuse evaluations  
- 🤖 **Neural Network Integration** for hybrid evaluation models  
- 📘 **Opening Book** for faster and stronger early-game play  
- 🧮 **Endgame Tablebases** for perfect play in late-game scenarios  

---

## 👨‍💻 Author

**Fenil Gohil**  
📧 Email: fenilgohil124@gmail.com
🔗 LinkedIn: Fenil Gohil

---
