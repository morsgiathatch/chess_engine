from Board import Board
from Engine.Engine import Engine
import os

if __name__ == '__main__':
    # Build blank board
    game_board = Board.Board()
    cwd = os.getcwd()
    parent = os.path.join(cwd, os.path.join(os.path.dirname(__file__)))
    player_color = input('Are you playing as white or black? w/b\n')
    print(Board.get_board_str(game_board))
    if player_color == 'b':
        engine = Engine(model_path=parent + '/../Engine/nn_data/white/model.json',
                        weights_path=parent + '/../Engine/nn_data/white/model.h5')
        engine_move = engine.make_move()
        game_board.read_and_update(engine_move)
        print("\nTurn %d: %s" % (game_board.turn_number, engine_move))
        print(Board.get_board_str(game_board))
    else:
        engine = Engine(model_path=parent + '/../Engine/nn_data/black/model.json',
                        weights_path=parent + '/../Engine/nn_data/black/model.h5')
    player_move = input('Enter next move in algebraic form\n')
    while player_move != 'quit':
        game_board.read_and_update(player_move)
        print("\nTurn %d: %s" % (game_board.turn_number, player_move))
        print(Board.get_board_str(game_board))
        engine.update_opponent_move(player_move)
        engine_move = engine.make_move()
        game_board.read_and_update(engine_move)
        print("\nTurn %d: %s" % (game_board.turn_number, engine_move))
        print(Board.get_board_str(game_board))
        player_move = input('Enter next move in algebraic form\n')

else:
    exit(-1)
