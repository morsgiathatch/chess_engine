from Board import Board
import copy
import numpy as np
from numpy import linalg as la


class Engine:
    def __init__(self, color):
        self.color = color
        # Load neural network from file. See
        # https://machinelearningmastery.com/save-load-keras-deep-learning-models/
        self.board = Board.Board(blank=True)

    def update_opponent_move(self, algebraic_move):
        self.board.read_and_update(algebraic_move)

    def make_move(self):
        predicted_move = None # Need to get prediction from neural network
        possible_moves = self.board.get_list_of_possible_moves_in_algebraic_form()
        move = self.get_best_move(predicted_move, possible_moves)
        self.board.read_and_update(move)
        return move

    # prediction must be a the 0, 1, 0, ... representation of a move as numpy array
    def get_best_move(self, prediction, valid_moves):
        # First check for check mates
        for valid_move in valid_moves:
            if '#' in valid_move:
                return valid_move

        valid_prediction_ndx = -1
        # vectorize potential moves
        vectorized_valid_moves = []
        for i, valid_move in enumerate(valid_moves):
            board = copy.deepcopy(self.board)
            board.read_and_update(valid_move)
            vectorized_valid_moves.append(np.array(board.vector))
            if vectorized_valid_moves[i] == prediction:
                valid_prediction_ndx = i

        if valid_prediction_ndx != -1:
            return valid_moves[valid_prediction_ndx]

        max_norm = float('inf')
        optimal_prediction_ndx = None
        for i in range(0, len(vectorized_valid_moves)):
            norm = la.norm(prediction, vectorized_valid_moves[i])
            if norm <= max_norm:
                max_norm = norm
                optimal_prediction_ndx = i

        return valid_moves[optimal_prediction_ndx]
