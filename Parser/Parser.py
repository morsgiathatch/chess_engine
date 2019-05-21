import os
import re


def print_to_file(games, file_path):
    with open(file_path, 'w+') as f:
        for game in games:
            print(game, file=f)
    f.close()


def parse(file_path):
    """Parse pgn game file and return games

    :param file_path: path to pgn game file
    :type file_path: string
    :return: multiple python lists
    :rtype: list
    """
    tied_games_ = []
    white_games_won_ = []
    black_games_won_ = []
    with open(file_path, 'r') as f:
        line = f.readline()
        while line:
            if line[0] == '1':
                game_lines = ''
                while '1/2-1/2' not in line and '1-0' not in line and '0-1' not in line:
                    game_lines += line + ' '
                    line = f.readline()
                game_lines += line
                if '#' not in game_lines and '1/2-1/2' not in game_lines:
                    line = f.readline()
                    continue
                game_lines = game_lines.replace('\n', '')
                game_lines = re.sub(r'\s\d+\.\s', ',', game_lines)
                game_lines = re.sub(r'1\.\s', '', game_lines)
                game_lines = re.sub(r'\s', ',', game_lines)
                if "1/2-1/2" in line:
                    game_lines = re.sub('1/2-1/2', '', game_lines)
                    game_lines = game_lines[:-1]
                    tied_games_.append(game_lines)
                elif "1-0" in line:
                    game_lines = re.sub('1-0', '', game_lines)
                    game_lines = game_lines[:-1]
                    white_games_won_.append(game_lines)
                else:
                    game_lines = re.sub('0-1', '', game_lines)
                    game_lines = game_lines[:-1]
                    black_games_won_.append(game_lines)

            line = f.readline()
    f.close()

    return tied_games_, white_games_won_, black_games_won_


# Parser to parse game files
if __name__ == '__main__':
    cwd = os.getcwd()
    parent = os.path.join(cwd, os.path.join(os.path.dirname(__file__)))
    game_files = os.listdir(parent + "/games")
    for game_file in game_files:
        tied_games, white_games_won, black_games_won = parse(parent + "/games/" + game_file)

        print_to_file(tied_games, parent + "/parsed_games/tied_games/tie.txt")
        print_to_file(white_games_won, parent + "/parsed_games/white_games_won/white_games_won.txt")
        print_to_file(black_games_won, parent + "/parsed_games/black_games_won/black_games_won.txt")

else:
    exit(-1)
