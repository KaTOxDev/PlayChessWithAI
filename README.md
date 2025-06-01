# ♔ Chess Master AI 🚀

<div align="center">

![Chess](https://img.shields.io/badge/Game-Chess-blue?style=for-the-badge&logo=chess.com)
![Python](https://img.shields.io/badge/Python-3.8+-green?style=for-the-badge&logo=python)
![Pygame](https://img.shields.io/badge/Pygame-2.0+-red?style=for-the-badge&logo=pygame)
![Stockfish](https://img.shields.io/badge/Engine-Stockfish-yellow?style=for-the-badge)

**A beautiful, feature-rich chess game with AI opponent powered by Stockfish**

*Train against 7 difficulty levels • Real-time move analysis • Professional move ratings*

[🚀 Quick Start](#-quick-start) • [📋 Features](#-features) • [🎮 Controls](#-controls) • [⚙️ Setup](#️-installation)

</div>

---

## 🌟 Features

### 🧠 **AI Opponent**
- **7 Difficulty Levels**: From complete beginner to grandmaster strength
- **Powered by Stockfish**: World's strongest chess engine
- **Adaptive Thinking Time**: 0.1s to 5s based on difficulty
- **Dynamic Level Switching**: Change difficulty mid-game

### 📊 **Move Analysis & Rating**
- **Real-time Evaluation**: Every move is analyzed and rated
- **Professional Ratings**:
  - ⭐⭐⭐ **Brilliant** - Outstanding moves
  - ⭐⭐ **Great** - Excellent moves
  - ⭐ **Good** - Solid moves
  - ❓❗ **Inaccuracy** - Minor mistakes
  - ❓ **Mistake** - Significant errors
  - ❓❓ **Blunder** - Major mistakes
- **Score Evaluation**: See how each move affects your position

### 🎨 **Beautiful Interface**
- **Modern Design**: Clean, professional chess board
- **Move History Panel**: Complete game notation with ratings
- **Visual Highlights**: Last move, selected piece, legal moves
- **Coordinate Labels**: File and rank indicators
- **Responsive UI**: Smooth animations and feedback

### 🎮 **Game Features**
- **Complete Chess Rules**: All standard chess rules implemented
- **Automatic Promotion**: Pawns promote to queen (customizable)
- **Check Detection**: Visual and textual check indicators
- **Game Over Detection**: Checkmate, stalemate, and draw conditions
- **Move Validation**: Only legal moves allowed

---

## 🚀 Quick Start

1. **Install Dependencies**
   ```bash
   pip install pygame python-chess
   ```

2. **Install Stockfish**
   - **Windows**: Download from [stockfishchess.org](https://stockfishchess.org/) and add to PATH
   - **Mac**: `brew install stockfish`
   - **Linux**: `sudo apt install stockfish` or `sudo pacman -S stockfish`

3. **Run the Game**
   ```bash
   python chess_game.py
   ```

4. **Choose Your Challenge**
   - Select AI difficulty level
   - Start playing as White
   - Watch your moves get rated in real-time!

---

## 🎮 Controls

| Key | Action |
|-----|--------|
| **Mouse Click** | Select piece / Make move |
| **R** | Restart game |
| **L** | Change AI difficulty level |
| **ESC** | Quit game |

### 🖱️ **Gameplay**
1. **Select a Piece**: Click on your piece (White)
2. **See Legal Moves**: Available moves highlighted in yellow
3. **Make Your Move**: Click destination square
4. **Watch AI Respond**: AI thinks and makes its move
5. **Analyze**: See move ratings and evaluations in real-time

---

## ⚙️ Installation

### 📋 **Requirements**
- Python 3.8 or higher
- Pygame 2.0+
- python-chess library
- Stockfish engine

### 🔧 **Detailed Setup**

#### **Step 1: Clone or Download**
```bash
git clone <repository-url>
cd chess-master-ai
```

#### **Step 2: Install Python Dependencies**
```bash
pip install pygame python-chess
```

#### **Step 3: Install Stockfish Engine**

**Windows:**
1. Download Stockfish from [stockfishchess.org](https://stockfishchess.org/)
2. Extract to a folder (e.g., `C:\stockfish\`)
3. Add to PATH or place executable in project folder

**macOS:**
```bash
brew install stockfish
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install stockfish
```

**Linux (Arch):**
```bash
sudo pacman -S stockfish
```

#### **Step 4: Optional - Add Piece Images**
For premium visuals, create a `chess/` folder and add PNG files:
```
chess/
├── white_pawn.png
├── white_rook.png
├── white_knight.png
├── white_bishop.png
├── white_queen.png
├── white_king.png
├── black_pawn.png
├── black_rook.png
├── black_knight.png
├── black_bishop.png
├── black_queen.png
└── black_king.png
```

*Note: Game works perfectly with built-in text pieces if images aren't provided*

---

## 🎯 AI Difficulty Levels

| Level | Name | Think Time | Depth | Strength |
|-------|------|------------|-------|----------|
| 1 | **Beginner** | 0.1s | 5 | ~800 ELO |
| 2 | **Easy** | 0.2s | 8 | ~1200 ELO |
| 3 | **Medium** | 0.5s | 10 | ~1600 ELO |
| 4 | **Hard** | 1.0s | 12 | ~2000 ELO |
| 5 | **Expert** | 2.0s | 15 | ~2400 ELO |
| 6 | **Master** | 3.0s | 18 | ~2800 ELO |
| 7 | **Grandmaster** | 5.0s | 20 | ~3200+ ELO |

---

## 🏆 Game Features in Detail

### 🎨 **Visual Elements**
- **Board Colors**: Professional tournament colors
- **Piece Highlighting**: Selected pieces shown in green
- **Legal Move Indicators**: Yellow highlights for valid moves
- **Last Move Display**: Orange highlights for previous move
- **Check Warnings**: Visual and text indicators

### 📈 **Move Analysis System**
The game uses Stockfish's evaluation to rate every move:

- **Evaluation Depth**: 12 moves ahead for accurate analysis
- **Score Tracking**: Position evaluation in centipawns
- **Rating Algorithm**: Compares move quality to best possible moves
- **Real-time Feedback**: Instant move ratings as you play

### 🎲 **Game Modes**
- **Human vs AI**: Play against Stockfish
- **Analysis Mode**: Review and learn from your games
- **Difficulty Progression**: Start easy and work your way up

---

## 🐛 Troubleshooting

### **Common Issues**

**❌ "Stockfish engine not found"**
- Ensure Stockfish is installed and in your system PATH
- Try placing stockfish executable in the same folder as the game

**❌ "No module named 'pygame'"**
```bash
pip install pygame python-chess
```

**❌ Game runs but pieces look like text**
- This is normal! Add PNG images to `chess/` folder for better graphics
- Game is fully functional with text pieces

**❌ AI takes too long to move**
- Lower the difficulty level
- Ensure you're not running other CPU-intensive programs

### **Performance Tips**
- **Slow Computer?** Use levels 1-3 for faster gameplay
- **Want Challenge?** Levels 5-7 provide tournament-strength opposition
- **Learning?** Level 3-4 is perfect for intermediate players

---

## 🎓 Learning Features

### **Improve Your Chess**
- **Move Ratings Help**: Learn what makes moves good or bad
- **Pattern Recognition**: See how the AI responds to different positions
- **Mistake Analysis**: Understand your blunders and inaccuracies
- **Progress Tracking**: Challenge higher difficulties as you improve

### **Educational Value**
- **Opening Principles**: AI demonstrates sound opening play
- **Tactical Awareness**: Spot tactical motifs through AI play
- **Endgame Technique**: Learn proper endgame technique
- **Positional Understanding**: See how small advantages accumulate

---

## 📊 Technical Specifications

- **Engine**: Stockfish 15+ compatible
- **GUI Framework**: Pygame
- **Chess Logic**: python-chess library
- **Move Generation**: Full legal move validation
- **Position Evaluation**: Stockfish UCI protocol
- **Threading**: Non-blocking AI calculations
- **Performance**: 60 FPS smooth gameplay

---

## 🎉 Future Enhancements

### **Planned Features**
- [ ] **Opening Book**: Common opening variations
- [ ] **Time Controls**: Blitz, rapid, and classical time formats
- [ ] **Game Database**: Save and replay games
- [ ] **Multiple Themes**: Different board and piece sets
- [ ] **Sound Effects**: Audio feedback for moves
- [ ] **Online Play**: Challenge friends remotely
- [ ] **Tournament Mode**: Multi-game matches
- [ ] **Puzzle Mode**: Tactical training exercises

---

## 🤝 Contributing

We welcome contributions! Whether it's:
- 🐛 Bug fixes
- ✨ New features  
- 🎨 UI improvements
- 📚 Documentation
- 🧪 Testing

Feel free to open issues and pull requests!

---

## 📜 License

This project is open source and available under the MIT License.

---

<div align="center">

**Made with ❤️ for chess enthusiasts**

*Train • Play • Improve • Master*

⭐ **Star this repo if you enjoyed playing!** ⭐

</div>
