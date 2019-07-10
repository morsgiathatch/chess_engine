from Board import Board
from Engine.Engine import Engine
import os
import time

if __name__ == '__main__':
    # Build blank board
    game_board = Board.Board()
    cwd = os.getcwd()
    parent = os.path.join(cwd, os.path.join(os.path.dirname(__file__)))
    player_color = input()
    # print(Board.get_board_str(game_board))
    if player_color == 'b':
        engine = Engine(model_path=parent + '/../Engine/nn_data/white/model.json',
                        weights_path=parent + '/../Engine/nn_data/white/model.h5')
        engine_move = engine.make_move()
        game_board.read_and_update(engine_move)
        # find (row, col, row, col) coordinate of piece and target and print to stdout

        # print("\nTurn %d: %s" % (game_board.turn_number, engine_move))
        # print(Board.get_board_str(game_board))
    else:
        engine = Engine(model_path=parent + '/../Engine/nn_data/black/model.json',
                        weights_path=parent + '/../Engine/nn_data/black/model.h5')
    # !! is a character meaning that a player has made a move, otherwise it is a query of possible moves for piece at
    # "row,col"
    player_move = input()
    while player_move != 'quit':
        if "!!" not in player_move:
            terms = player_move.split(',')
            row = terms[0]
            col = terms[1]
            moves = game_board.board[row][col].get_moves(game_board, ignore_check=False)
            # get moves in (row, col) form
            # print moves
            # continue

        # otherwise get move in (row, col, row, col) form where first two are piece, second two are target location

        game_board.read_and_update(player_move)
        # print("\nTurn %d: %s" % (game_board.turn_number, player_move))
        # print(Board.get_board_str(game_board))
        engine.update_opponent_move(player_move)
        engine_move = engine.make_move()
        game_board.read_and_update(engine_move)
        # print("\nTurn %d: %s" % (game_board.turn_number, engine_move))
        # print(Board.get_board_str(game_board))
        time.sleep(0.1)
        player_move = input()

else:
    exit(-1)
