# Duo-Othello-AI-Agent

This repository contains an implementation of an AI agent for the Duo-Othello game, a variant of the classic Reversi/Othello game. The agent reads the current game state from an input file, determines the best move using the Minimax algorithm with Alpha-Beta pruning, and writes the chosen move to an output file.

## Project Description

Duo-Othello is played on a 12x12 board with an initial configuration of 8 pieces. The game rules follow standard Reversi/Othello rules, with additional constraints and scoring rules:

1. The game starts with 8 pieces on the board.
2. Players alternate turns, with the second player receiving a +1 bonus at the end of the game.
3. The game ends when neither player can make a move, and the player with the most pieces, considering the bonus, wins.

## File Formats

- **Input File (`input.txt`)**: Contains the current game state, the player to move, remaining times, and the board configuration.
- **Output File (`output.txt`)**: Contains the chosen move in the format `<column><row>`, e.g., `c2`.

## Methodology

The agent uses the following components to determine the best move:

1. **Minimax Algorithm with Alpha-Beta Pruning**: This algorithm evaluates possible moves up to a certain depth to maximize the score for the player and minimize the score for the opponent.
2. **Board Evaluation Function**: This function evaluates the board state based on various factors such as board control, corner control, edge control, mobility, and potential mobility.
3. **Dynamic Depth Adjustment**: The search depth is dynamically adjusted based on the remaining time to balance between move quality and computation time.
4. **Move Generation and Application**: Legal moves are generated based on the current board state, and the resulting board state is updated after applying a move.
