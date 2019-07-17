from Board import Board
from Board import ChessLogic
from Engine.Engine import Engine
import os
import sys

if __name__ == '__main__':
    # Build blank board
    game_board = Board.Board()
    cwd = os.getcwd()
    parent = os.path.join(cwd, os.path.join(os.path.dirname(__file__)))
    player_color = input()
    # print(Board.get_board_str(game_board))
    if player_color == 'b':
        opponent_color = 'w'
        engine = Engine(model_path=parent + '/../Engine/nn_data/white/model.json',
                        weights_path=parent + '/../Engine/nn_data/white/model.h5')
        engine_move = engine.make_move()
        game_board.read_and_update(engine_move)
        # find (row, col, row, col) coordinate of piece and target and print to stdout
        opponent_coord_move = ChessLogic.get_move_coordinates_from_algebraic_move(engine_move, opponent_color, game_board)
        print(opponent_coord_move)

    else:
        opponent_color = 'b'
        engine = Engine(model_path=parent + '/../Engine/nn_data/black/model.json',
                        weights_path=parent + '/../Engine/nn_data/black/model.h5')
    # !! is a character meaning that a player has made a move, otherwise it is a query of possible moves for piece at
    # "row,col"
    player_move = input()
    while player_move != 'quit':
        # This checks if the gui is merely wishing for possible moves for a given piece
        if "!!" not in player_move:
            terms = player_move.split(',')
            row = int(terms[0])
            col = int(terms[1])
            moves = game_board.board[row][col].get_moves(game_board, ignore_check=False)
            moves = ChessLogic.get_target_coordinate_from_algebraic_moves(moves, player_color)
            for move in moves:
                sys.stdout.write(move)
            sys.stdout.write('\n')
            sys.stdout.flush()
            player_move = input()
            continue

        # otherwise get move in row,col,row,col!! form where first two are piece, second two are target location
        coords = player_move.split('!!')[0]
        coords = coords.split(',')
        piece = game_board.board[coords[0]][coords[1]]
        move = piece.get_move(board=game_board, i=coords[2], j=coords[3], ignore_check=True)
        game_board.read_and_update(move)
        engine.update_opponent_move(move)

        # have engine move and convert algebraic move to coordinate to pass to gui
        engine_move = engine.make_move()
        game_board.read_and_update(engine_move)
        opponent_coord_move = ChessLogic.get_move_coordinates_from_algebraic_move(engine_move, opponent_color, game_board)
        sys.stdout.write(opponent_coord_move + '\n')
        sys.stdout.flush()
        player_move = input()

else:
    exit(-1)
