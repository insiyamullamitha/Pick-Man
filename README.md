# Pick Man 👻

Welcome to the Pick Man! This classic arcade game has been given a fresh twist with customisable themes, characters, and exciting new features. Dive into the nostalgic world of Pacman with a modern touch.

## Getting Started 🚀

1. Ensure you have latest version of Python and Pygame installed on your system
```
pip install pygame
```
2. Clone this repository:
```
git clone https://github.com/insiyamullamitha/Pick-Man.git
```
3. Navigate to the **'game.py'** file in the directory and run to start the game.
```
python3 game.py
```

## Features ✨

* **Themes:** Choose between a bright, colourful background or a dark ocean theme, the ghost images change dynamically based on your chosen theme.
* **Characters:**: Select your character wisely! Each theme comes with up to three characters.
* **Levels and Goals:** The game currently offers two exciting levels. In each level, players must complete three goals (e.g., kill a ghost) to earn stars. Collect stars to unlock and use powerups during the game.
* **Powerups**: Use your hard-earned stars to purchase powerups! Up to five powerups can be used in a single game, each with random effects, such as speeding up the player, increasing points, or allowing players to kill ghosts.
* **Ghost Algorithms:**
  1. **Random Direction Ghost:** This ghost moves in random directions, adding an unpredictable challenge.
  2. **Manhattan Distance Ghost:** This ghost uses the Manhattan distance to estimate Pacman's location, providing a rough but effective pursuit strategy.
  3. **A\* Algorithm Ghost:** Experience a more advanced ghost algorithm using the A* algorithm, making the pursuit more intelligent and challenging.
* **Help:** Click on the help button at any time for assistance. It provides guidance on game controls and objectives.
* **Pause, Quit, Replay:** Pause, quit, or replay the game whenever you want. Use the designated keys for a seamless gaming experience.
* **Leaderboard:** Compete with your friends with the leaderboard which records the performance of the top 5 players with the most points.
