# chessvis: a tool to visualize each player's control of the chessboard.

### Motivation

After watching videos from Grandmasters such as Hikaru Nakamura, Daniel Naroditsky, and Vidit Gujrathi, I noticed that the winner usually dominates the middlegame. They control almost every square on the board and prevent the other player from making any moves, leaving them free to pursue an attacking strategy. 

This led me to ask whether there was a way to visualize each player's control of the board -- that is, what squares they control and with how many pieces.

Additionally, can the winner of a chess match be predicted by the number of squares they control over the course of the middlegame?

### Requirements
numpy \n
pandas \n
seaborn \n
matplotlib \n
cv2 \n
python-chess \n

### Usage
main.py is the script that creates heatmaps to visualize control at every move of the game, concatenate those frames into a video, and produce plots of control over the course of the game.

