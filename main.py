import chessvis
import chess.pgn
import argparse
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('pgn_path', nargs="?", default="pgn.txt",help='the path to the file with pgn information')
parser.add_argument("frame_outpath", nargs="?", default="frames/", help="the directory to save the image files")
parser.add_argument("plot_outpath", nargs="?", default="plots/", help="the directory to save the plots")
parser.add_argument("video_outpath", nargs="?", default="videos/", help="the directory to save the compiled video")
parser.add_argument("fps", nargs="?", default=15, help="the fps for the video")

args = parser.parse_args()

pgn = args.pgn_path
frame_path = args.frame_outpath
plot_outpath = args.plot_outpath
video_outpath = args.video_outpath
fps = args.fps

if not os.path.exists(frame_path):
    os.mkdir(frame_path)
if not os.path.exists(plot_outpath):
    os.mkdir(plot_outpath)
if not os.path.exists(video_outpath):
    os.mkdir(video_outpath)


### Open pgn file and create game instance
pgn_file = open(pgn)
game = chess.pgn.read_game(pgn_file)
gameboard = game.board()


### Initialize ChessVisualizer object
vis = chessvis.ChessVisualizer()


### Initialize lists of number of squares controlled by either side
controlled_white = []
controlled_black = []


### Iterate over all the moves in the game, create snapshots of heatmapped squares
move_count = 1
for move in game.mainline_moves():
    print ("Now on move..." + str(move_count))
    gameboard.push(move)

    fen_string = gameboard.fen().split(" ")[0]
    board = vis.create_board(fen_string)
    heatmap = vis.create_heatmap(board)

    numpy_version = heatmap.to_numpy().flatten()
    num_controlled_white = np.count_nonzero(numpy_version < 0)    
    num_controlled_black = np.count_nonzero(numpy_version > 0)
    
    controlled_white.append(num_controlled_white)
    controlled_black.append(num_controlled_black)

    heatmap.columns = ["a", "b", "c", "d", "e", "f", "g", "h"]
    heatmap.set_index(pd.Index(range(8,0,-1)), inplace=True)

    plt.figure(figsize=(10,10))
    sns.heatmap(heatmap, cmap="Greys", cbar=False)
    plt.savefig(frame_path + "frame" + str(move_count) + ".png")
    print ("Saved image.")
    plt.close()
    
    move_count += 1

### Create line plots of controlled squares for both sides
plt.figure(figsize=(10,8))
plt.plot(range(1,move_count), controlled_white, color="Red", label="White")
plt.plot(range(1,move_count), controlled_black, color="Black", label="Black")

plt.ylim(0, 64)
plt.xlabel("Move Count")
plt.ylabel("Squares Controlled")
plt.legend()

plt.savefig(plot_outpath + "lineplot.png", dpi=200)

### Create video from frames of control
video_obj = chessvis.VideoCreator(frame_path, video_outpath + "video.mp4", fps)
video_obj.create_video()