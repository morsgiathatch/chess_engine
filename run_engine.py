from Board import Board
from Board import ChessLogic
from Engine.Engine import Engine
import time
import os
import sys

if __name__ == '__main__':
    # Build blank board
    time.sleep(5)
    game_board = Board.Board()
    cwd = os.getcwd()
    parent = os.path.join(cwd, os.path.join(os.path.dirname(__file__)))
    player_color = sys.stdin.readline()
    # while player_color != 'w\n' or player_color != 'b\n':
    #     player_color = sys.stdin.readline()
    sys.stderr.write(player_color)
    sys.stderr.flush()
    # print(Board.get_board_str(game_board))
    if 'b' in player_color:
        opponent_color = 'w'
        engine = Engine(model_path=parent + '/Engine/nn_data/white/model.json',
                        weights_path=parent + '/Engine/nn_data/white/model.h5')
        engine_move = engine.make_move()
        # find (row, col, row, col) coordinate of piece and target and print to stdout
        # opponent_coord_move = ChessLogic.get_move_coordinates_from_algebraic_move(engine_move, opponent_color, game_board)
        game_board.read_and_update(engine_move)
        # sys.stderr.write(opponent_coord_move)
        sys.stdout.write(Board.get_board_state_str(game_board) + '\n')
        sys.stdout.flush()

    else:
        opponent_color = 'b'
        engine = Engine(model_path=parent + '/Engine/nn_data/black/model.json',
                        weights_path=parent + '/Engine/nn_data/black/model.h5')
        sys.stderr.write('opponent is black\n')
        sys.stderr.flush()
    # !! is a character meaning that a player has made a move, otherwise it is a query of possible moves for piece at
    # "row,col"
    player_move = ''
    while 'quit' not in player_move:
        player_move = sys.stdin.readline()
        sys.stderr.write(player_move)
        sys.stderr.flush()
        # This checks if the gui is merely wishing for possible moves for a given piece
        if "!!" not in player_move:
            terms = player_move.split(',')
            row = int(terms[0])
            col = int(terms[1])
            moves = game_board.board[row][col].get_moves(game_board, ignore_check=False)
            for move in moves:
                sys.stderr.write(move + ',')
            sys.stderr.write('\n')
            sys.stderr.flush()

            moves = ChessLogic.get_target_coordinate_from_algebraic_moves(moves, player_color)
            for move in moves:
                sys.stdout.write(move)
                sys.stderr.write(move)
            sys.stdout.write('\n')
            sys.stdout.flush()
            sys.stderr.write('\n')
            sys.stderr.flush()
            continue

        # time.sleep(5)
        # otherwise get move in row,col,row,col!! form where first two are piece, second two are target location
        coords = player_move.split('!!')[0]
        coords = coords.split(',')
        piece = game_board.board[int(coords[0])][int(coords[1])]
        move = piece.get_move(board=game_board, i=int(coords[2]), j=int(coords[3]), ignore_check=True)
        sys.stderr.write('opponent read move as ' + move + '\n')
        sys.stderr.flush()
        game_board.read_and_update(move)
        engine.update_opponent_move(move)
        sys.stdout.write(Board.get_board_state_str(game_board) + '\n')
        sys.stdout.flush()
        sys.stderr.write(Board.get_board_state_str(game_board) + '\n' + Board.get_board_str(game_board))
        sys.stderr.flush()

        is_opponent_ready = sys.stdin.readline()
        if 'ready' in is_opponent_ready:
            # have engine move and convert algebraic move to coordinate to pass to gui
            engine_move = engine.make_move()
            game_board.read_and_update(engine_move)
            sys.stderr.write('AI made move: %s\n' % (engine_move))
            sys.stdout.write(Board.get_board_state_str(game_board) + '\n')
            sys.stdout.flush()
            sys.stderr.write(Board.get_board_state_str(game_board) + '\n' + Board.get_board_str(game_board))
            sys.stderr.flush()
        else:
            sys.stderr.write('Error from gui: not ready to read board state')
            sys.stderr.flush()


else:
    exit(-1)
