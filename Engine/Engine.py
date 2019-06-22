from Board import Board
import copy
import numpy as np
from numpy import linalg as la
from keras.models import model_from_json


class Engine:
    def __init__(self, model_path, weights_path):
        self.model_path = model_path
        # Load neural network from file. See
        # https://machinelearningmastery.com/save-load-keras-deep-learning-models/
        json_file = open(model_path, 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        self.nn_model = model_from_json(loaded_model_json)
        # load weights into new model
        self.nn_model.load_weights(weights_path)
        self.nn_model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
        print("Loaded model from disk")
        self.board = Board.Board()

    def update_opponent_move(self, algebraic_move):
        self.board.read_and_update(algebraic_move)

    def make_move(self):
        predicted_move = self.get_predicted_move()
        possible_moves = self.board.get_list_of_possible_moves_in_algebraic_form()
        move = self.get_best_move(predicted_move, possible_moves)
        self.board.read_and_update(move)
        return move

    # prediction must be a the 0, 1, 0, ... representation of a move as numpy array
    def get_best_move(self, prediction, valid_moves):
        # First look for check mates
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
            if (vectorized_valid_moves[i] == prediction).all():
                valid_prediction_ndx = i
            del board

        if valid_prediction_ndx != -1:
            return valid_moves[valid_prediction_ndx]

        max_norm = float('inf')
        optimal_prediction_ndx = None
        for i in range(0, len(vectorized_valid_moves)):
            norm = la.norm(prediction - vectorized_valid_moves[i])
            if norm <= max_norm:
                max_norm = norm
                optimal_prediction_ndx = i

        return valid_moves[optimal_prediction_ndx]

    def get_predicted_move(self):
        prediction = self.nn_model.predict(np.array([self.board.vector]))[0]
        for i in range(0, prediction.shape[0]):
            prediction[i] = round(prediction[i])
        return prediction
