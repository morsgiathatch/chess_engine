import copy
from Board import Pieces
from Board import ChessLogic
import re


# Chess board is initialized in the following format
# 7 r n b q k b n r    Black side
# 6 p p p p p p p p
# 5 - - - - - - - -
# 4 - - - - - - - -
# 3 - - - - - - - -
# 2 - - - - - - - -
# 1 p p p p p p p p
# 0 r n b q k b n r
#   0 1 2 3 4 5 6 7    White side

class Board:
    algebra_to_index_map = {'a': 0, '1': 0, 'b': 1, '2': 1, 'c': 2, '3': 2, 'd': 3, '4': 3, 'e': 4, '5': 4, 'f': 5,
                            '6': 5, 'g': 6, '7': 6, 'h': 7, '8': 7}
    col_index_to_algebra = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h'}
    row_index_to_algebra = {0: '1', 1: '2', 2: '3', 3: '4', 4: '5', 5: '6', 6: '7', 7: '8'}

    def __init__(self, blank=True, vectorized_board=None):
        self.turn_number = 0
        # Initialize board with empty pieces
        self.board = []
        for i in range(0, 8):
            board_row = []
            for j in range(0, 8):
                board_row.append(Pieces.NullPiece(i, j, 1))
            self.board.append(board_row)

        # Create list of references for quick game updates
        self.white_pawns = []
        self.black_pawns = []
        self.white_rooks = []
        self.black_rooks = []
        self.white_knights = []
        self.black_knights = []
        self.white_bishops = []
        self.black_bishops = []
        self.white_queens = []
        self.black_queens = []
        self.white_king = []
        self.black_king = []
        self.vector = [0] * 256

        if blank:
            self.set_blank_board()
        else:
            for k in range(0, 256, 4):
                self.set_piece(Pieces.get_piece_from_binary_format(k, vectorized_board[k: k + 4]))

        self.set_references()

    # Read chess algebra and update board
    def read_and_update(self, algebraic_move):
        color = self.turn_number % 2
        # Move pawn
        if str(algebraic_move[0]).islower():
            ChessLogic.move_pawn(algebraic_move, self, color, turn_number=self.turn_number)

        # Move bureaucratic piece
        elif re.match('[NBRQK]', algebraic_move[0]):
            ChessLogic.move_bureaucratic_piece(algebraic_move=algebraic_move, board=self, color=color,
                                               turn_number=self.turn_number)

        # Castle
        elif algebraic_move[0] == 'O':
            ChessLogic.castle(algebraic_move=algebraic_move, board=self, color=color, turn_number=self.turn_number)

        # Parse error?
        else:
            raise ValueError('Invalid algebraic notation')

        self.turn_number += 1
        self.vectorize()

    # Update vectorization of board
    def vectorize(self):
        for i in range(0, 8):
            for j in range(0, 8):
                self.vector[i >> 5 + j >> 2: i >> 5 + j >> 2 + 4] = self.board[i][j].binary_format

    # Helper in constructing new board from vectorization.
    # Not to be confused with update which represents changes in board state.
    def set_piece(self, piece):
        self.board[piece.i][piece.j] = copy.deepcopy(piece)

    # Helper to set blank board
    def set_blank_board(self):
        # Add pawns
        for i in range(0, 8):
            self.board[1][i] = Pieces.Pawn(1, i, 0)
            self.board[6][i] = Pieces.Pawn(6, i, 1)

        # Add rooks
        self.board[0][0] = Pieces.Rook(0, 0, 0)
        self.board[0][7] = Pieces.Rook(0, 7, 0)
        self.board[7][0] = Pieces.Rook(7, 0, 1)
        self.board[7][7] = Pieces.Rook(7, 7, 1)

        # Add knights
        self.board[0][1] = Pieces.Knight(0, 1, 0)
        self.board[0][6] = Pieces.Knight(0, 6, 0)
        self.board[7][1] = Pieces.Knight(7, 1, 1)
        self.board[7][6] = Pieces.Knight(7, 6, 1)

        # Add bishops
        self.board[0][2] = Pieces.Bishop(0, 2, 0)
        self.board[0][5] = Pieces.Bishop(0, 5, 0)
        self.board[7][2] = Pieces.Bishop(7, 2, 1)
        self.board[7][5] = Pieces.Bishop(7, 5, 1)

        # Add queens
        self.board[0][3] = Pieces.Queen(0, 3, 0)
        self.board[7][3] = Pieces.Queen(7, 3, 1)

        # Add Kings
        self.board[0][4] = Pieces.King(0, 4, 0)
        self.board[7][4] = Pieces.King(7, 4, 1)
        self.vectorize()

    # Helper to set references
    def set_references(self):
        # Set references
        for row in self.board:
            for piece in row:
                if isinstance(piece, Pieces.Pawn):
                    if piece.color == 0:
                        self.white_pawns.append(piece)
                    else:
                        self.black_pawns.append(piece)
                elif isinstance(piece, Pieces.Rook):
                    if piece.color == 0:
                        self.white_rooks.append(piece)
                    else:
                        self.black_rooks.append(piece)
                elif isinstance(piece, Pieces.Knight):
                    if piece.color == 0:
                        self.white_knights.append(piece)
                    else:
                        self.black_knights.append(piece)
                elif isinstance(piece, Pieces.Bishop):
                    if piece.color == 0:
                        self.white_bishops.append(piece)
                    else:
                        self.black_bishops.append(piece)
                elif isinstance(piece, Pieces.Queen):
                    if piece.color == 0:
                        self.white_queens.append(piece)
                    else:
                        self.black_queens.append(piece)
                elif isinstance(piece, Pieces.King):
                    if piece.color == 0:
                        self.white_king.append(piece)
                    else:
                        self.black_king.append(piece)

    def delete_piece_from_references(self, i, j, color):
        if color == 0:
            if isinstance(self.board[i][j], Pieces.Pawn):
                self.white_pawns.remove(self.board[i][j])
            elif isinstance(self.board[i][j], Pieces.Rook):
                self.white_rooks.remove(self.board[i][j])
            elif isinstance(self.board[i][j], Pieces.Knight):
                self.white_knights.remove(self.board[i][j])
            elif isinstance(self.board[i][j], Pieces.Bishop):
                self.white_bishops.remove(self.board[i][j])
            elif isinstance(self.board[i][j], Pieces.Queen):
                self.white_queens.remove(self.board[i][j])
        else:
            if isinstance(self.board[i][j], Pieces.Pawn):
                self.black_pawns.remove(self.board[i][j])
            elif isinstance(self.board[i][j], Pieces.Rook):
                self.black_rooks.remove(self.board[i][j])
            elif isinstance(self.board[i][j], Pieces.Knight):
                self.black_knights.remove(self.board[i][j])
            elif isinstance(self.board[i][j], Pieces.Bishop):
                self.black_bishops.remove(self.board[i][j])
            elif isinstance(self.board[i][j], Pieces.Queen):
                self.black_queens.remove(self.board[i][j])

        self.board[i][j] = Pieces.NullPiece(i, j, 1)

    def get_piece_that_can_move_to_index(self, list_of_pieces, i, j, pos_args=None, end_args=None):
        # end_args are args that specify check or checkmate. May not be useful here.
        # pos_args are args that specify position clarification
        pieces_that_can_move_to_index = []
        for piece in list_of_pieces:
            if self.can_move_without_self_check(piece, i, j):
                pieces_that_can_move_to_index.append(piece)

        if len(pieces_that_can_move_to_index) == 1:
            return pieces_that_can_move_to_index[0]

        # Now need to use pos_args to trim pieces_that_can_move_to_index
        for piece in pieces_that_can_move_to_index:
            if pos_args in (str(Board.col_index_to_algebra[piece.j]) + str(Board.row_index_to_algebra[piece.i])):
                return piece

        # This should not occur maybe?
        return Pieces.NullPiece(i, j, 1)

    def get_promoted_piece(self, piece_type, i, j, color, turn_number):
        if piece_type == 'N':
            piece = Pieces.Knight(i, j, color)
            if color == 0:
                self.white_knights.append(piece)
            else:
                self.black_knights.append(piece)
        elif piece_type == 'B':
            piece = Pieces.Bishop(i, j, color)
            if color == 0:
                self.white_bishops.append(piece)
            else:
                self.black_bishops.append(piece)
        elif piece_type == 'Q':
            piece = Pieces.Queen(i, j, color)
            if color == 0:
                self.white_queens.append(piece)
            else:
                self.black_queens.append(piece)
        elif piece_type == 'R':
            piece = Pieces.Rook(i, j, color)
            if color == 0:
                self.white_rooks.append(piece)
            else:
                self.black_rooks.append(piece)
        else:
            raise ValueError('Invalid type of object to be promoted')
        self.board[i][j] = piece
        piece.turn_number = turn_number

    def get_references(self, piece_type, color):
        if color == 0:
            if piece_type == 'p':
                return self.white_pawns
            elif piece_type == 'N':
                return self.white_knights
            elif piece_type == 'B':
                return self.white_bishops
            elif piece_type == 'R':
                return self.white_rooks
            elif piece_type == 'Q':
                return self.white_queens
            elif piece_type == 'K':
                return self.white_king
            else:
                raise ValueError('Invalid piece type')
        else:
            if piece_type == 'p':
                return self.black_pawns
            elif piece_type == 'N':
                return self.black_knights
            elif piece_type == 'B':
                return self.black_bishops
            elif piece_type == 'R':
                return self.black_rooks
            elif piece_type == 'Q':
                return self.black_queens
            elif piece_type == 'K':
                return self.black_king
            else:
                raise ValueError('Invalid piece type')

    # If piece moves to [i][j], does this cause self_check?
    def can_move_without_self_check(self, piece, i, j):
        color = piece.color

        # See if piece can move
        if not piece.can_move(self, i, j):
            return False

        # Make temporary copy of board, move piece and see if opponent can check
        temp_board_copy = update_move_and_get_board_copy(self, piece, i, j)
        if color == 0:
            king = temp_board_copy.white_king[0]
        else:
            king = temp_board_copy.black_king[0]

        for row in temp_board_copy.board:
            for piece in row:
                if isinstance(piece, Pieces.NullPiece):
                    continue
                if piece.color != color and piece.can_move(temp_board_copy, king.i, king.j):
                    return False

        return True

    def set_empty(self, i, j):
        self.board[i][j] = Pieces.NullPiece(i, j, 1)

    def get_compact_vector_string(self, vec_str=None):

        if vec_str is None:
            vec_str = str(self.vector)
            vec_str = vec_str.replace('[', '')
            vec_str = vec_str.replace(']', '')
            vec_str = vec_str.replace(',', '')
            vec_str = vec_str.replace(' ', '')

        ret_str = ''
        for k in range(0, 8):
            ret_str += str(int(vec_str[k * 32: (k + 1) * 32], 2))
            if k != 7:
                ret_str += ':'

        return ret_str

    def get_list_of_possible_moves_in_coordinate_form(self, ignore_check):
        possible_moves = []
        for row in self.board:
            for piece in row:
                if not isinstance(piece, Pieces.NullPiece) and piece.color == self.turn_number % 2:
                    possible_moves += piece.get_moves(self, ignore_check)

        return possible_moves

    def get_list_of_possible_moves_in_algebraic_form(self):
        list_of_possible_moves_in_coordinate_form = self.get_list_of_possible_moves_in_coordinate_form(ignore_check=False)
        return ChessLogic.convert_coordinate_form_to_algebraic_form(list_of_possible_moves_in_coordinate_form)

    # Return 2 if checkmate, 1 if just check, 0 if nothing
    def move_is_check_or_checkmate(self, piece, i, j):
        color = piece.color
        board_copy = update_move_and_get_board_copy(self, piece, i, j)

        if color == 0:
            king = board_copy.black_king[0]
        else:
            king = board_copy.white_king[0]

        # First check for check
        is_check = False
        for row in board_copy.board:
            for piece in row:
                if isinstance(piece, Pieces.NullPiece):
                    continue
                if piece.color == color and piece.can_move(board_copy, king.i, king.j):
                    is_check = True

        # now check for mate
        if is_check:
            available_moves = board_copy.get_list_of_possible_moves_in_coordinate_form(ignore_check=True)
            # checkmate
            if len(available_moves) == 0:
                return 2
            # check
            else:
                return 1
        else:
            return 0


# Get new board from vectorization
def devectorize(vectorized_board):
    return Board(blank=False, vectorized_board=vectorized_board)


def get_board_str(board):
    print_str = '_________________________________\n'
    for i in reversed(range(0, 8)):
        for j in range(0, 8):
            print_str += '|_%s_' % board.board[i][j].symbol
            if j == 7:
                print_str += '|\n'

    return print_str


def update_move_and_get_board_copy(board, piece, i, j):
    color = piece.color
    temp_board_copy = copy.deepcopy(board)
    piece_copy = temp_board_copy.board[piece.i][piece.j]
    if not isinstance(temp_board_copy.board[i][j], Pieces.NullPiece):
        ChessLogic.update_capture_piece(board=temp_board_copy, attk_piece=piece_copy,
                                        def_piece=temp_board_copy.board[i][j])
    else:
        # Check if not en passant
        if isinstance(piece_copy, Pieces.Pawn) and piece_copy.is_en_passant(board=temp_board_copy, i=i, j=j):
            if color == 0:
                ChessLogic.update_en_passant(board=temp_board_copy, attk_piece=piece_copy,
                                             def_piece=temp_board_copy.board[i - 1][j], color=color)
            else:
                ChessLogic.update_en_passant(board=temp_board_copy, attk_piece=piece_copy,
                                             def_piece=temp_board_copy.board[i + 1][j], color=color)

        else:
            ChessLogic.update_move_piece(board=temp_board_copy, piece=piece_copy, i=i, j=j)
    return temp_board_copy


# This returns a string in the format '10010110101...', not '1, 0, 0, 1, 0, ...'
def convert_compact_string_to_normal(vec_str):
    terms = vec_str.split(':')
    true_terms = ''
    for term in terms:
        true_term = bin(int(term))[2:]
        while len(true_term) != 32:
            true_term = '0' + true_term

        true_terms += true_term

    return true_terms
