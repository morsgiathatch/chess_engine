from Board import Board
import os


if __name__ == '__main__':
    printout = True
    cwd = os.getcwd()
    parent = os.path.join(cwd, os.path.join(os.path.dirname(__file__)))
    game_path = parent + "/Parser/parsed_games/black_games_won/black_games_won.txt"
    # game_path = parent + "/Parser/parsed_games/white_games_won/white_games_won.txt"
    # game_path = parent + "/Parser/parsed_games/tied_games/tie.txt"

    games = []
    with open(game_path, 'r') as f:
        lines = f.readlines()
        for line in lines:
            game = line.rstrip('\n')
            moves = game.split(',')
            games.append(moves)
    f.close()
    for k, moves in enumerate(games):
        if k != 1:
            continue

        board = Board.Board()
        board_str = Board.get_board_str(board)
        print('\n----- Beginning game %d -----\n' % k)
        if printout:
            if k % 2 == 0:
                player_color = 'White'
            else:
                player_color = 'Black'
            print("\n%s Turn %d: %s" % (player_color, board.turn_number, 'Begin game'))
            print(board_str)
        for i, move in enumerate(moves):
            possible_moves = board.get_list_of_possible_moves_in_algebraic_form()
            print('Possible moves for next move are ', possible_moves)
            board.read_and_update(algebraic_move=move, move_index=i)
            if printout:
                board_str = Board.get_board_str(board)
                print("\nTurn %d: %s" % (board.turn_number, move))
                print(board_str)
        del board
