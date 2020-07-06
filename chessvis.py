"""
Chessvis Engine

Aalok Patwa
github.com/aalokpatwa
"""

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import cv2
import os
from os.path import isfile, join

class ChessVisualizer:
    def get_position(self, fen_string):
        return fen_string.split(" ")[0]

    def split_ranks(self, position_string):
        return position_string.split("/")

    def reverse_ranks(self, ranks_split):
        return ranks_split[::-1]
    def create_board(self, fen_string):
        position_string = self.get_position(fen_string)
        split = self.split_ranks(position_string)
        num_ranks = 8
        num_files = 8
        
        board = pd.DataFrame(data=np.zeros((8,8), dtype="object"))
        
        for rank in range(0,num_ranks):
            file = 0
            this_rank = split[rank]
            for character in this_rank:
                if file > 8:
                    break
                try:
                    character = int(character)
                    board.loc[rank, file:file+character] = "."
                    file = file+character
                except ValueError:
                    board.loc[rank, file] = character
                    file += 1
        return board
    def square_exists(self, rank, file):
        if rank < 0 or rank > 7 or file < 0 or file > 7:
            return False
        else:
            return True
    def square_is_taken(self, board, rank, file):
        if board.at[rank, file] == 0:
            return False
        else:
            return True
        
    def check_white_pawn(self, board, rank, file):
        possible_squares = [(rank-1, file+1), (rank-1, file-1)]
        controlled_squares = []
        for square in possible_squares:
            if self.square_exists(square[0], square[1]):
                controlled_squares.append(square)
            else:
                continue
        return controlled_squares

    def check_black_pawn(self, board, rank, file):
        possible_squares = [(rank+1, file+1), (rank+1, file-1)]
        controlled_squares = []
        for square in possible_squares:
            if self.square_exists(square[0], square[1]):
                controlled_squares.append(square)
            else:
                continue
        return controlled_squares

    def check_knight(self, board, rank, file):
        possible_squares = [(rank+1, file+2), (rank+1, file-2), (rank-1, file+2), (rank-1, file-2),
                            (rank+2, file+1), (rank+2, file-1), (rank-2, file+1), (rank-2, file-1)]
        controlled_squares = []
        for square in possible_squares:
            if self.square_exists(square[0], square[1]):
                controlled_squares.append(square)
            else:
                continue
        return controlled_squares

    def check_bishop(self, board, rank, file):
        possible_left = file
        possible_right = 7-file
        possible_down = rank
        possible_up = 7-rank
        
        controlled_squares = []
        
        diag_squares_ur = min(possible_up, possible_right)
        diag_squares_ul = min(possible_up, possible_left)
        diag_squares_dr = min(possible_down, possible_right)
        diag_squares_dl = min(possible_down, possible_left)
        
        #Upper right diagonal line
        for ur_square in range(1, diag_squares_ur+1):
            test_square = (rank+ur_square, file+ur_square)
            if self.square_is_taken(board, test_square[0], test_square[1]):
                controlled_squares.append((test_square[0], test_square[1]))
                break
            else:
                controlled_squares.append((test_square[0], test_square[1]))
                
        #Upper left diagonal line
        for ul_square in range(1, diag_squares_ul+1):
            test_square = (rank+ul_square, file-ul_square)
            if self.square_is_taken(board, test_square[0], test_square[1]):
                controlled_squares.append((test_square[0], test_square[1]))
                break
            else:
                controlled_squares.append((test_square[0], test_square[1]))
                
        #Down right diagonal line
        for dr_square in range(1, diag_squares_dr+1):
            test_square = (rank-dr_square, file+dr_square)
            if self.square_is_taken(board, test_square[0], test_square[1]):
                controlled_squares.append((test_square[0], test_square[1]))
                break
            else:
                controlled_squares.append((test_square[0], test_square[1]))
                
        #Down left diagonal line
        for dl_square in range(1, diag_squares_dl+1):
            test_square = (rank-dl_square, file-dl_square)
            if self.square_is_taken(board, test_square[0], test_square[1]):
                controlled_squares.append((test_square[0], test_square[1]))
                break
            else:
                controlled_squares.append((test_square[0], test_square[1]))
                
                

        
        return controlled_squares
        
    def check_rook(self, board, rank, file):
        controlled_squares = []
        
        #Up line
        for up_square in range (1, 8+1):
            test_square = (rank+up_square, file)
            if not self.square_exists(test_square[0], test_square[1]):
                break
            if self.square_is_taken(board, test_square[0], test_square[1]):
                controlled_squares.append((test_square[0], test_square[1]))
                break
            else:
                controlled_squares.append((test_square[0], test_square[1]))
        
        #Right line
        for right_square in range (1, 8+1):
            test_square = (rank, file+right_square)
            if not self.square_exists(test_square[0], test_square[1]):
                break
            if self.square_is_taken(board, test_square[0], test_square[1]):
                controlled_squares.append((test_square[0], test_square[1]))
                break
            else:
                controlled_squares.append((test_square[0], test_square[1]))
        
        # Down line
        for down_square in range (1, 8+1):
            test_square = (rank-down_square, file)
            if not self.square_exists(test_square[0], test_square[1]):
                break
            if self.square_is_taken(board, test_square[0], test_square[1]):
                controlled_squares.append((test_square[0], test_square[1]))
                break
            else:
                controlled_squares.append((test_square[0], test_square[1]))
        
        # Left line
        for left_square in range (1, 8+1):
            test_square = (rank, file-left_square)
            if not self.square_exists(test_square[0], test_square[1]):
                break
            if self.square_is_taken(board, test_square[0], test_square[1]):
                controlled_squares.append((test_square[0], test_square[1]))
                break
            else:
                controlled_squares.append((test_square[0], test_square[1]))
        return controlled_squares

    def check_queen(self, board, rank, file):
        diagonal_controlled = self.check_bishop(board, rank, file)
        horizontal_controlled = self.check_rook(board, rank, file)
        controlled_squares = diagonal_controlled + horizontal_controlled
        return controlled_squares

    def check_king(self, board, rank, file):
        possible_squares = [(rank+1, file),(rank-1, file),(rank+1, file+1),(rank+1, file-1),
                            (rank-1, file+1),(rank-1, file-1),(rank, file+1),(rank, file-1)]
        controlled_squares = []
        for square in possible_squares:
            if self.square_exists(square[0], square[1]):
                controlled_squares.append(square)
            else:
                continue
        return controlled_squares

    def update_heatmap_white(self, controlled_list, board_heatmap):
        for square in controlled_list:
            board_heatmap.at[square[0], square[1]] -= 1
            
    def update_heatmap_black(self, controlled_list, board_heatmap):
        for square in controlled_list:
            board_heatmap.at[square[0], square[1]] += 1
    def create_heatmap(self, board):
        board_heatmap = pd.DataFrame(data=np.zeros((8,8), dtype="int"))
        for rank in range(8):
            for file in range(8):
                piece = board.at[rank, file]
                if piece == "P":
                    controlled = self.check_white_pawn(board, rank, file)
                    self.update_heatmap_white(controlled, board_heatmap)
                if piece == "p":
                    controlled = self.check_black_pawn(board, rank, file)
                    self.update_heatmap_black(controlled, board_heatmap)
                if piece == "N":
                    controlled = self.check_knight(board, rank, file)
                    self.update_heatmap_white(controlled, board_heatmap)
                if piece == "n":
                    controlled = self.check_knight(board, rank, file)
                    self.update_heatmap_black(controlled, board_heatmap)
                if piece == "B":
                    controlled = self.check_bishop(board, rank, file)
                    self.update_heatmap_white(controlled, board_heatmap)
                if piece == "b":
                    controlled = self.check_bishop(board, rank, file)
                    self.update_heatmap_black(controlled, board_heatmap)
                if piece == "R":
                    controlled = self.check_rook(board, rank, file)
                    self.update_heatmap_white(controlled, board_heatmap)
                if piece == "r":
                    controlled = self.check_rook(board, rank, file)
                    self.update_heatmap_black(controlled, board_heatmap)
                if piece == "Q":
                    controlled = self.check_queen(board, rank, file)
                    self.update_heatmap_white(controlled, board_heatmap)
                if piece == "q":
                    controlled = self.check_queen(board, rank, file)
                    self.update_heatmap_black(controlled, board_heatmap)
                if piece == "K":
                    controlled = self.check_king(board, rank, file)
                    self.update_heatmap_white(controlled, board_heatmap)
                if piece == "k":
                    controlled = self.check_king(board, rank, file)
                    self.update_heatmap_black(controlled, board_heatmap)
        

        return board_heatmap


class VideoCreator():
    def __init__(self, pathIn, pathOut, fps):
        self.pathIn = pathIn
        self.pathOut = pathOut
        self.fps = fps
    def set_fps(self, new_fps):
        self.fps = new_fps
    def create_video(self):
        frame_array = []
        files = [f for f in os.listdir(self.pathIn) if isfile(join(self.pathIn, f))]
        #for sorting the file names properly
        files = sorted(files,key=lambda x: int(os.path.splitext(x)[0][5:]))
        for i in range(len(files)):
            filename=self.pathIn + files[i]
            #reading each files
            img = cv2.imread(filename)
            height, width, layers = img.shape
            size = (width,height)

            #inserting the frames into an image array
            frame_array.append(img)
        out = cv2.VideoWriter(self.pathOut,cv2.VideoWriter_fourcc(*'DIVX'), self.fps, size)
        for i in range(len(frame_array)):
            # writing to a image array
            out.write(frame_array[i])
        out.release()
