from Board import Board
import os


if __name__ == '__main__':
    printout = True
    cwd = os.getcwd()
    parent = os.path.join(cwd, os.path.join(os.path.dirname(__file__)))
    game_path = parent + "/../Parser/parsed_games/black_games_won/black_games_won.txt"
    # game_path = parent + "/../Parser/parsed_games/white_games_won/white_games_won.txt"
    # game_path = parent + "/../Parser/parsed_games/tied_games/tie.txt"

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
            print("\nTurn %d: %s" % (board.turn_number, 'Begin game'))
            print(board_str)
        for i, move in enumerate(moves):
            board.read_and_update(algebraic_move=move)
            temp_str = Board.get_board_str(board)
            if temp_str == board_str:
                print('Board game unchanged at turn %d, %s' % (board.turn_number, move))
                raise ValueError('Board game unchanged')
            board_str = temp_str
            if printout:
                print("\nTurn %d: %s" % (board.turn_number, move))
                print(board_str)
        del board
