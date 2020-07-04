# chessvis: a tool to visualize each player's control of the chessboard.

### Motivation

After watching videos from Grandmasters such as Hikaru Nakamura, Daniel Naroditsky, and Vidit Gujrathi, I noticed that the winner usually dominates the middlegame. They control almost every square on the board and prevent the other player from making any moves, leaving them free to pursue an attacking strategy. 

This led me to ask whether there was a way to visualize each player's control of the board -- that is, what squares they control and with how many pieces.

Additionally, can the winner of a chess match be predicted by the number of squares they control over the course of the middlegame?

### Requirements
numpy  
pandas  
seaborn  
matplotlib  
cv2  
python-chess  

### Usage
main.py is the script that creates heatmaps to visualize control at every move of the game, concatenate those frames into a video, and produce plots of control over the course of the game.

```unix
$ python3 main.py pgnfile frame_outpath plot_outpath video_outpath desired_fps
```
pgnfile: default is pgn.txt
frame_outpath: default is frames/
plot_outpath: default is plots/
video_outpath: default is videos/
desired_fps: default is 15


