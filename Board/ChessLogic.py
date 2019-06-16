from Board import Pieces
from Board import Board
import re


def move_pawn(algebraic_move, board, color, turn_number):
    # Go case by case
    # Move pawn with no captures and no promotion
    if re.match('[a-h][1-8]', algebraic_move) and 'x' not in algebraic_move and '=' not in algebraic_move:
        i = Board.Board.algebra_to_index_map[algebraic_move[1]]
        j = Board.Board.algebra_to_index_map[algebraic_move[0]]
        piece = board.get_piece_that_can_move_to_index(board.get_references('p', color), i, j,
                                                       end_args=algebraic_move[2:])
        update_move_piece(board=board, piece=piece, i=i, j=j)

    # pawn capture with no promotion,
    elif re.match('[a-h]x[a-h][1-8]', algebraic_move[0: 4]) and '=' not in algebraic_move:
        i = Board.Board.algebra_to_index_map[algebraic_move[3]]
        j = Board.Board.algebra_to_index_map[algebraic_move[2]]

        pos_args = algebraic_move[0]
        end_args = algebraic_move[4:]
        piece = board.get_piece_that_can_move_to_index(board.get_references('p', color), i, j, end_args=end_args,
                                                       pos_args=pos_args)
        # Take into account en passant
        if color == 0 and isinstance(board.board[i][j], Pieces.NullPiece):
            update_en_passant(board=board, attk_piece=piece, def_piece=board.board[i - 1][j],
                              color=color)
        elif color == 1 and isinstance(board.board[i][j], Pieces.NullPiece):
            update_en_passant(board=board, attk_piece=piece, def_piece=board.board[i + 1][j],
                              color=color)
        else:
            update_capture_piece(board=board, attk_piece=piece, def_piece=board.board[i][j])

    # pawn promotion without capture
    elif re.match('[a-h][1-8]=', algebraic_move[0: 3]):
        i = Board.Board.algebra_to_index_map[algebraic_move[1]]
        j = Board.Board.algebra_to_index_map[algebraic_move[0]]
        piece = board.get_piece_that_can_move_to_index(board.get_references('p', color), i, j)
        board.board[piece.i][piece.j] = Pieces.NullPiece(piece.i, piece.j, 1)
        board.delete_piece_from_references(piece.i, piece.j, color)
        board.get_promoted_piece(algebraic_move[3], i, j, color, turn_number=turn_number)

    # Pawn promotion with capture
    elif re.match('[a-h]x[a-h][1-8]=', algebraic_move):
        i = Board.Board.algebra_to_index_map[algebraic_move[3]]
        j = Board.Board.algebra_to_index_map[algebraic_move[2]]
        pos_args = algebraic_move[0]
        end_args = algebraic_move[6:]
        piece = board.get_piece_that_can_move_to_index(board.get_references('p', color), i, j, end_args=end_args,
                                                       pos_args=pos_args)
        update_capture_piece(board=board, attk_piece=piece, def_piece=board.board[i][j])
        board.delete_piece_from_references(i, j, color)
        board.get_promoted_piece(algebraic_move[5], i, j, color, turn_number=turn_number)
        del piece


# Move any bureaucratic piece. I.e., N, B, R, Q, K
def move_bureaucratic_piece(algebraic_move, board, color):
    # Go case by case
    # Move piece with no capture and no ambiguity
    if re.match('[NBRQK][a-h][1-8]', algebraic_move) and len(algebraic_move) < 5 and 'x' not in algebraic_move:
        i = Board.Board.algebra_to_index_map[algebraic_move[2]]
        j = Board.Board.algebra_to_index_map[algebraic_move[1]]
        piece = board.get_piece_that_can_move_to_index(board.get_references(algebraic_move[0], color), i, j,
                                                       end_args=algebraic_move[3:])
        update_move_piece(board=board, piece=piece, i=i, j=j)

    # Move piece with simple ambiguity without capture
    elif re.match('[NBRQK][a-h][a-h][1-8]', algebraic_move) or re.match('[NBRQK][1-8][a-h][1-8]', algebraic_move):
        i = Board.Board.algebra_to_index_map[algebraic_move[3]]
        j = Board.Board.algebra_to_index_map[algebraic_move[2]]
        piece = board.get_piece_that_can_move_to_index(board.get_references(algebraic_move[0], color), i, j,
                                                       pos_args=algebraic_move[1],
                                                       end_args=algebraic_move[4:])
        update_move_piece(board=board, piece=piece, i=i, j=j)

    # Move piece with complex ambiguity without capture, this should almost never occur
    elif re.match('[NBRQK][a-h][1-8][a-h][1-8]', algebraic_move):
        i = Board.Board.algebra_to_index_map[algebraic_move[4]]
        j = Board.Board.algebra_to_index_map[algebraic_move[3]]
        piece = board.get_piece_that_can_move_to_index(board.get_references(algebraic_move[0], color), i, j,
                                                       pos_args=algebraic_move[1:3],
                                                       end_args=algebraic_move[5:])
        update_move_piece(board=board, piece=piece, i=i, j=j)

    # Move piece and capture with no ambiguity
    elif re.match('[NBRQK]x[a-h][1-8]', algebraic_move):
        i = Board.Board.algebra_to_index_map[algebraic_move[3]]
        j = Board.Board.algebra_to_index_map[algebraic_move[2]]

        end_args = algebraic_move[4:]
        piece = board.get_piece_that_can_move_to_index(board.get_references(algebraic_move[0], color), i, j,
                                                       end_args=end_args)
        update_capture_piece(board=board, attk_piece=piece, def_piece=board.board[i][j])

    # Move piece and capture with simple ambiguity
    elif re.match('[NBRQK][a-h]x[a-h][1-8]', algebraic_move) or re.match('[NBRQK][1-8]x[a-h][1-8]', algebraic_move):
        i = Board.Board.algebra_to_index_map[algebraic_move[4]]
        j = Board.Board.algebra_to_index_map[algebraic_move[3]]

        end_args = algebraic_move[5:]
        pos_args = algebraic_move[1]
        piece = board.get_piece_that_can_move_to_index(board.get_references(algebraic_move[0], color), i, j,
                                                       end_args=end_args, pos_args=pos_args)
        update_capture_piece(board=board, attk_piece=piece, def_piece=board.board[i][j])

    # Move piece and capture with complex ambiguity. Should also almost never happen
    elif re.match('[NBRQK][a-h][1-8]x[a-h][1-8]', algebraic_move):
        i = Board.Board.algebra_to_index_map[algebraic_move[4]]
        j = Board.Board.algebra_to_index_map[algebraic_move[3]]

        end_args = algebraic_move[6:]
        pos_args = algebraic_move[1:3]
        piece = board.get_piece_that_can_move_to_index(board.get_references(algebraic_move[0], color), i, j,
                                                       end_args=end_args, pos_args=pos_args)
        update_capture_piece(board=board, attk_piece=piece, def_piece=board.board[i][j])


def castle(algebraic_move, board, color):
    if color == 0:
        i = board.white_king[0].i
        j = board.white_king[0].j
    else:
        i = board.black_king[0].i
        j = board.black_king[0].j

    # Move king, then queenside rook
    if re.match('O-O-O', algebraic_move):
        update_move_piece(board=board, piece=board.board[i][j], i=i, j=j - 2)
        update_move_piece(board=board, piece=board.board[i][0], i=i, j=3)
    # Move king, then kingside rook
    else:
        update_move_piece(board=board, piece=board.board[i][j], i=i, j=j + 2)
        update_move_piece(board=board, piece=board.board[i][7], i=i, j=5, castled=True)


def update_move_piece(board, piece, i, j, castled=False):
    if isinstance(piece, Pieces.Pawn) and piece.i - i == 2:
        piece.jumped_two = True
    board.set_empty(piece.i, piece.j)
    board.board[i][j] = piece
    piece.i = i
    piece.j = j
    piece.last_turn_moved = board.turn_number
    if not castled:
        board.turn_number += 1


def update_capture_piece(board, attk_piece, def_piece):
    board.delete_piece_from_references(def_piece.i, def_piece.j, def_piece.color)
    board.set_empty(attk_piece.i, attk_piece.j)
    board.board[def_piece.i][def_piece.j] = attk_piece
    attk_piece.i = def_piece.i
    attk_piece.j = def_piece.j
    attk_piece.last_turn_moved = board.turn_number
    del def_piece
    board.turn_number += 1


def update_en_passant(board, attk_piece, def_piece, color):
    board.delete_piece_from_references(def_piece.i, def_piece.j, def_piece.color)
    board.set_empty(attk_piece.i, attk_piece.j)
    board.set_empty(def_piece.i, def_piece.j)
    if color == 0:
        board.board[def_piece.i + 1][def_piece.j] = attk_piece
        attk_piece.i = def_piece.i + 1
        attk_piece.j = def_piece.j
    else:
        board.board[def_piece.i - 1][def_piece.j] = attk_piece
        attk_piece.i = def_piece.i - 1
        attk_piece.j = def_piece.j

    attk_piece.last_turn_moved = board.turn_number
    del def_piece
    board.turn_number += 1


def convert_coordinate_form_to_algebraic_form(coordinate_form_moves):
    algebraic_form_moves = []
    for coordinate_move in coordinate_form_moves:
        # First deal with pawn
        if coordinate_move[0].islower():
            if 'x' in coordinate_move:
                algebraic_form_moves.append(coordinate_move[0] + coordinate_move[2:])
            else:
                algebraic_form_moves.append(coordinate_move[2:])

        # Otherwise bureaucratic piece
        else:
            if 'O-O' in coordinate_move:
                algebraic_form_moves.append(coordinate_move)
                continue
            piece_type = coordinate_move[0]
            piece_coords = re.findall('[a-h][1-8]', coordinate_move)
            conflicting_moves = []
            # Get all conflicting moves
            for other_move in coordinate_form_moves:
                other_piece_coords = re.findall('[a-h][1-8]', other_move)
                if other_move[0] == piece_type and other_move != coordinate_move and \
                        piece_coords[1] == other_piece_coords[1]:
                    conflicting_moves.append(other_move)

            # No conflicting moves
            if len(conflicting_moves) == 0:
                algebraic_form_moves.append(coordinate_move[0] + coordinate_move[3:])

            # Only one conflicting move
            elif len(conflicting_moves) == 1:
                conflicting_move = conflicting_moves[0]
                conflicting_piece_coords = re.findall('[a-h][1-8]', conflicting_move)
                # if no column conflict
                if conflicting_piece_coords[0][0] != piece_coords[0][0]:
                    algebraic_form_moves.append(coordinate_move[0:2] + coordinate_move[3:])
                # else there can be no row conflict
                else:
                    algebraic_form_moves.append(coordinate_move[0] + coordinate_move[2:])

            # Multiple conflicting moves. This should almost never occur
            else:
                column_conflict_flag = False
                row_conflict_flag = False
                for conflicting_move in conflicting_moves:
                    conflicting_piece_coords = re.findall('[a-h][1-8]', conflicting_move)
                    if conflicting_piece_coords[0][0] == piece_coords[0][0]:
                        column_conflict_flag = True
                    if conflicting_piece_coords[0][1] == piece_coords[0][1]:
                        row_conflict_flag = True

                if column_conflict_flag and not row_conflict_flag:
                    algebraic_form_moves.append(coordinate_move[0] + coordinate_move[2:])
                elif not column_conflict_flag and row_conflict_flag:
                    algebraic_form_moves.append(coordinate_move[0:2] + coordinate_move[3:])
                elif column_conflict_flag and row_conflict_flag:
                    algebraic_form_moves.append(coordinate_move)
                else:
                    raise ValueError('Parse or logic error encountered')

    return algebraic_form_moves
