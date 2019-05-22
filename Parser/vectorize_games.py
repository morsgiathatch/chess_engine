from Board import Board
import os
import sys


if __name__ == '__main__':
    cwd = os.getcwd()
    parent = os.path.join(cwd, os.path.join(os.path.dirname(__file__)))
    game_path = parent + "/parsed_games/white_games_won/white_games_won.txt"
    # game_path = parent + "/parsed_games/black_games_won/black_games_won.txt"
    # game_path = parent + "/parsed_games/tied_games/tie.txt"

    games = []
    with open(game_path, 'r') as f:
        lines = f.readlines()
        for line in lines:
            game = line.rstrip('\n')
            moves = game.split(',')
            games.append(moves)
    f.close()
    for k, moves in enumerate(games):
        board = Board.Board()
        sys.stdout.write('\rVectorizing games: %d / %d' % (k + 1, len(games)))

        vectorized_game_str = ''
        with open(parent + "/vectorized_games/white_games_won/white_games_won.txt", 'a+') as f:
        # with open(parent + "/vectorized_games/black_games_won/black_games_won.txt", 'a+') as f:
        # with open(parent + "/vectorized_games/tied_games/tied_games.txt", 'a+') as f:

            for i, move in enumerate(moves):
                board.read_and_update(algebraic_move=move)
                vectorized_board_str = board.get_compact_vector_string()
                vectorized_game_str += vectorized_board_str
                # Check that composing vectorization with inverse operation results in original string
                if vectorized_board_str != board.get_compact_vector_string(board.convert_compact_string_to_normal(vectorized_board_str)):
                    raise ValueError('Invalid vectorization')
                if i != len(moves) - 1:
                    vectorized_game_str += ','
            del board
            f.write(vectorized_game_str + '\n')
else:
    exit(-1)
