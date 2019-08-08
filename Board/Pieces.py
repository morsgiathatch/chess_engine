from Board import Board
import sys


class Pawn:
    def __init__(self, i, j, color):
        self.i = i
        self.j = j
        self.color = color
        self.binary_format = [self.color, 0, 0, 0]
        self.last_turn_moved = -1
        self.jumped_two = False
        self.symbol = 'p'

    def get_moves(self, board, ignore_check):
        moves = []
        if self.color == 0:
            moves.append(self.get_move(board, self.i + 1, self.j, ignore_check))
            moves.append(self.get_move(board, self.i + 1, self.j + 1, ignore_check))
            moves.append(self.get_move(board, self.i + 1, self.j - 1, ignore_check))
            moves.append(self.get_move(board, self.i + 2, self.j, ignore_check))
        else:
            moves.append(self.get_move(board, self.i - 1, self.j, ignore_check))
            moves.append(self.get_move(board, self.i - 1, self.j + 1, ignore_check))
            moves.append(self.get_move(board, self.i - 1, self.j - 1, ignore_check))
            moves.append(self.get_move(board, self.i - 2, self.j, ignore_check))
        return [x for x in moves if x is not None]

    def get_move(self, board, i, j, ignore_check):
        if board.can_move_without_self_check(self, i, j):
            if not isinstance(board.board[i][j], NullPiece) or self.is_en_passant(board, i, j):
                return get_coordinate_move(self, i, j, capture=True, board=board, ignore_check=ignore_check)
            else:
                return get_coordinate_move(self, i, j, capture=False, board=board, ignore_check=ignore_check)
        return None

    # Can move returns a boolean if the piece can move to the square dependent on board state
    def can_move(self, board, i, j):
        if i > 7 or j > 7 or i < 0 or j < 0:
            return False

        if self.i == i and self.j == j:
            return False

        # jump two on first move and cannot jump pieces
        if self.color == 0 and self.i == 1 and i == 3 and isinstance(board.board[i][j], NullPiece) and j == self.j:
            if isinstance(board.board[2][j], NullPiece):
                return True
        if self.color == 1 and self.i == 6 and i == 4 and isinstance(board.board[i][j], NullPiece) and j == self.j:
            if isinstance(board.board[5][j], NullPiece):
                return True

        # move forward 1 to empty space
        if self.color == 0 and i == self.i + 1 and isinstance(board.board[i][j], NullPiece) and j == self.j:
            return True
        if self.color == 1 and i == self.i - 1 and isinstance(board.board[i][j], NullPiece) and j == self.j:
            return True

        # Capture diagonally
        if self.color == 0 and i == self.i + 1 and (j == self.j + 1 or j == self.j - 1) and \
                not isinstance(board.board[i][j], NullPiece) and board.board[i][j].color == 1:
            return True
        if self.color == 1 and i == self.i - 1 and (j == self.j + 1 or j == self.j - 1) and \
                not isinstance(board.board[i][j], NullPiece) and board.board[i][j].color == 0:
            return True

        # en passant
        if self.color == 0 and i == self.i + 1 and self.i == 4 and (j == self.j + 1 or j == self.j - 1) and \
                isinstance(board.board[i][j], NullPiece) and isinstance(board.board[i - 1][j], Pawn) and \
                board.board[i - 1][j].color == 1 and board.board[i - 1][j].last_turn_moved == board.turn_number - 1:
            return True
        if self.color == 1 and i == self.i - 1 and self.i == 3 and (j == self.j + 1 or j == self.j - 1) and \
                isinstance(board.board[i][j], NullPiece) and isinstance(board.board[i + 1][j], Pawn) and \
                board.board[i + 1][j].color == 0 and board.board[i + 1][j].last_turn_moved == board.turn_number - 1:
            return True

        return False

    def is_en_passant(self, board, i, j):
        if self.i == i and self.j == j:
            return False

        # jump two on first move and cannot jump pieces
        if self.color == 0 and self.i == 1 and i == 3 and isinstance(board.board[i][j], NullPiece) and j == self.j:
            if isinstance(board.board[2][j], NullPiece):
                return False
        if self.color == 1 and self.i == 6 and i == 4 and isinstance(board.board[i][j], NullPiece) and j == self.j:
            if isinstance(board.board[5][j], NullPiece):
                return False

        # move forward 1 to empty space
        if self.color == 0 and i == self.i + 1 and isinstance(board.board[i][j], NullPiece) and j == self.j:
            return False
        if self.color == 1 and i == self.i - 1 and isinstance(board.board[i][j], NullPiece) and j == self.j:
            return False

        # Capture diagonally
        if self.color == 0 and i == self.i + 1 and (j == self.j + 1 or j == self.j - 1) and \
                not isinstance(board.board[i][j], NullPiece) and board.board[i][j].color == 1:
            return False
        if self.color == 1 and i == self.i - 1 and (j == self.j + 1 or j == self.j - 1) and \
                not isinstance(board.board[i][j], NullPiece) and board.board[i][j].color == 0:
            return False

        # en passant
        if self.color == 0 and i == self.i + 1 and self.i == 4 and (j == self.j + 1 or j == self.j - 1) and \
                isinstance(board.board[i][j], NullPiece) and isinstance(board.board[i - 1][j], Pawn) and \
                board.board[i - 1][j].color == 1 and board.board[i - 1][j].last_turn_moved == board.turn_number - 1 and \
                board.board[i - 1][j].jumped_two:
            return True
        if self.color == 1 and i == self.i - 1 and self.i == 3 and (j == self.j + 1 or j == self.j - 1) and \
                isinstance(board.board[i][j], NullPiece) and isinstance(board.board[i + 1][j], Pawn) and \
                board.board[i + 1][j].color == 0 and board.board[i + 1][j].last_turn_moved == board.turn_number - 1 and \
                board.board[i + 1][j].jumped_two:
            return True

        return False


class Bishop:
    def __init__(self, i, j, color):
        self.i = i
        self.j = j
        self.color = color
        self.binary_format = [self.color, 0, 1, 1]
        self.last_turn_moved = -1
        self.symbol = 'B'

    def get_moves(self, board, ignore_check):
        return get_diagonal_moves(self, board, ignore_check)

    def get_move(self, board, i, j, ignore_check):
        if board.can_move_without_self_check(self, i, j):
            if not isinstance(board.board[i][j], NullPiece):
                return 'B' + get_coordinate_move(self, i, j, capture=True, board=board, ignore_check=ignore_check)
            else:
                return 'B' + get_coordinate_move(self, i, j, capture=False, board=board, ignore_check=ignore_check)
        return None

    def can_move(self, board, i, j):
        if i > 7 or j > 7 or i < 0 or j < 0:
            return False

        if self.i == i and self.j == j:
            return False

        # Check that it lies on diagonal
        if abs(self.i - i) != abs(self.j - j):
            return False

        # Make sure that piece at i, j is not of same color
        if board.board[i][j].color == self.color and not isinstance(board.board[i][j], NullPiece):
            return False

        return can_move_diagonally(self, board, i, j)


class Knight:
    def __init__(self, i, j, color):
        self.i = i
        self.j = j
        self.color = color
        self.binary_format = [self.color, 0, 1, 0]
        self.last_turn_moved = -1
        self.symbol = 'N'

    def get_moves(self, board, ignore_check):
        moves = [self.get_move(board, self.i + 2, self.j + 1, ignore_check), self.get_move(board, self.i + 2, self.j - 1, ignore_check),
                 self.get_move(board, self.i + 1, self.j - 2, ignore_check), self.get_move(board, self.i - 1, self.j - 2, ignore_check),
                 self.get_move(board, self.i - 2, self.j - 1, ignore_check), self.get_move(board, self.i - 2, self.j + 1, ignore_check),
                 self.get_move(board, self.i - 1, self.j + 2, ignore_check), self.get_move(board, self.i + 1, self.j + 2, ignore_check)]
        return [x for x in moves if x is not None]

    def get_move(self, board, i, j, ignore_check):
        if board.can_move_without_self_check(self, i, j):
            if not isinstance(board.board[i][j], NullPiece):
                return 'N' + get_coordinate_move(self, i, j, capture=True, board=board, ignore_check=ignore_check)
            else:
                return 'N' + get_coordinate_move(self, i, j, capture=False, board=board, ignore_check=ignore_check)
        return None

    def can_move(self, board, i, j):
        if i > 7 or j > 7 or i < 0 or j < 0:
            return False

        if self.i == i and self.j == j:
            return False

        # Cannot move to same piece color
        if board.board[i][j].color == self.color and not isinstance(board.board[i][j], NullPiece):
            return False

        # Now check that it is a legal move
        if (i == self.i + 2 and j == self.j + 1) or (i == self.i + 2 and j == self.j - 1) or (i == self.i + 1 and
            j == self.j - 2) or (i == self.i - 1 and j == self.j - 2) or (i == self.i - 2 and j == self.j - 1) or \
            (i == self.i - 2 and j == self.j + 1) or (i == self.i - 1 and j == self.j + 2) or (i == self.i + 1 and
            j == self.j + 2):
            return True

        return False


class Rook:
    def __init__(self, i, j, color):
        self.i = i
        self.j = j
        self.color = color
        self.binary_format = [self.color, 0, 0, 1]
        self.last_turn_moved = -1
        self.symbol = 'R'

    def get_moves(self, board, ignore_check):
        return get_forward_and_sideways_moves(self, board, ignore_check=ignore_check)

    def get_move(self, board, i, j, ignore_check):
        if board.can_move_without_self_check(self, i, j):
            if not isinstance(board.board[i][j], NullPiece):
                return 'R' + get_coordinate_move(self, i, j, capture=True, board=board, ignore_check=ignore_check)
            else:
                return 'R' + get_coordinate_move(self, i, j, capture=False, board=board, ignore_check=ignore_check)
        return None

    def can_move(self, board, i, j):
        if i > 7 or j > 7 or i < 0 or j < 0:
            return False

        if self.i == i and self.j == j:
            return False

        # Cannot move to space with same color
        if board.board[i][j].color == self.color and not isinstance(board.board[i][j], NullPiece):
            return False

        # narrow down false moves
        if self.i != i and self.j != j:
            return False

        return can_move_forward_and_sideways(self, board, i, j)


class Queen:
    def __init__(self, i, j, color):
        self.i = i
        self.j = j
        self.color = color
        self.binary_format = [self.color, 1, 0, 0]
        self.last_turn_moved = -1
        self.symbol = 'Q'

    def get_moves(self, board, ignore_check):
        return get_forward_and_sideways_moves(self, board, ignore_check) + get_diagonal_moves(self, board, ignore_check)

    def get_move(self, board, i, j, ignore_check):
        if board.can_move_without_self_check(self, i, j):
            if not isinstance(board.board[i][j], NullPiece):
                return 'Q' + get_coordinate_move(self, i, j, capture=True, board=board, ignore_check=ignore_check)
            else:
                return 'Q' + get_coordinate_move(self, i, j, capture=False, board=board, ignore_check=ignore_check)
        return None

    def can_move(self, board, i, j):
        if i > 7 or j > 7 or i < 0 or j < 0:
            return False

        if self.i == i and self.j == j:
            return False

        # Cannot move to space with same color
        if board.board[i][j].color == self.color and not isinstance(board.board[i][j], NullPiece):
            return False

        # narrow down false moves. Mere combination of bishop and rook stuff
        if (self.i != i and self.j != j) and abs(self.i - i) != abs(self.j - j):
            return False

        return can_move_forward_and_sideways(self, board, i, j) or can_move_diagonally(self, board, i, j)


class King:
    def __init__(self, i, j, color):
        self.i = i
        self.j = j
        self.color = color
        self.binary_format = [self.color, 1, 0, 1]
        self.last_turn_moved = -1
        self.symbol = 'K'

    def get_moves(self, board, ignore_check):
        moves = [self.get_move(board, self.i + 1, self.j, ignore_check), self.get_move(board, self.i, self.j + 1, ignore_check),
                 self.get_move(board, self.i + 1, self.j + 1, ignore_check), self.get_move(board, self.i + 1, self.j - 1, ignore_check),
                 self.get_move(board, self.i - 1, self.j, ignore_check), self.get_move(board, self.i, self.j - 1, ignore_check),
                 self.get_move(board, self.i - 1, self.j - 1, ignore_check), self.get_move(board, self.i - 1, self.j + 1, ignore_check)]
        if self.can_castle_kingside(board):
            moves.append('O-O')
        if self.can_castle_queenside(board):
            moves.append('O-O-O')
        return [x for x in moves if x is not None]

    def get_move(self, board, i, j, ignore_check):
        if board.can_move_without_self_check(self, i, j):
            if not isinstance(board.board[i][j], NullPiece):
                return 'K' + get_coordinate_move(self, i, j, capture=True, board=board, ignore_check=ignore_check)
            else:
                # check for queenside castle
                if self.j - j == 2:
                    return 'O-O-O'
                elif j - self.j == 2:
                    return 'O-O'
                return 'K' + get_coordinate_move(self, i, j, capture=False, board=board, ignore_check=ignore_check)
        return None

    def can_move(self, board, i, j):
        if i > 7 or j > 7 or i < 0 or j < 0:
            return False

        if self.i == i and self.j == j:
            return False

        # Cannot move to space with same color
        if board.board[i][j].color == self.color and not isinstance(board.board[i][j], NullPiece):
            return False

        # check for castling
        if self.i == i and self.j - j == 2:
            if self.can_castle_queenside(board):
                return True

        if i == self.i and j - self.j == 2:
            if self.can_castle_kingside(board):
                return True

        # narrow down false moves. Mere combination of bishop and rook stuff
        if abs(self.i - i) > 1 or abs(self.j - j) > 1:
            return False

        return can_move_forward_and_sideways(self, board, i, j) or can_move_diagonally(self, board, i, j)

    def can_castle_kingside(self, board):
        if self.last_turn_moved == -1 and board.board[self.i][self.j + 3].last_turn_moved == -1:
            if board.move_is_check_or_checkmate(piece=self, i=self.i, j=self.j) != 0:
                return False
            for k in range(1, 3):
                if not isinstance(board.board[self.i][self.j + k], NullPiece):
                    return False
                if board.move_is_check_or_checkmate(piece=self, i=self.i, j=self.j + k) != 0:
                    return False
            return True
        return False

    def can_castle_queenside(self, board):
        if self.last_turn_moved == -1 and board.board[self.i][self.j - 4].last_turn_moved == -1:
            if board.move_is_check_or_checkmate(piece=self, i=self.i, j=self.j) != 0:
                return False
            for k in range(1, 4):
                if not isinstance(board.board[self.i][self.j - k], NullPiece):
                    return False
                if board.move_is_check_or_checkmate(piece=self, i=self.i, j=self.j - k) != 0:
                    return False
            return True
        return False

class NullPiece:
    def __init__(self, i, j, color):
        self.i = i
        self.j = j
        self.color = color
        self.binary_format = [1, 1, 1, 1]
        self.last_turn_moved = -1
        self.symbol = '_'

    def get_moves(self, board, ignore_check):
        return []

    def get_move(self, board, i, j, ignore_check):
        return None

    def can_move(self, board, i, j):
        return False


def get_piece_from_binary_format(k, binary_format):
    if k >= 256:
        raise ValueError('Incorrect vectorization index')
    i = k // 8
    j = k % 8
    color = binary_format[0]
    # Return null piece
    if binary_format[1:4] == [1, 1, 1] and color == 1:
        return NullPiece(i, j, color)
    # Return pawn
    elif binary_format[1:4] == [0, 0, 0]:
        return Pawn(i, j, color)
    # Return knight
    elif binary_format[1:4] == [0, 1, 0]:
        return Knight(i, j, color)
    # Return bishop
    elif binary_format[1:4] == [0, 1, 1]:
        return Bishop(i, j, color)
    # Return rook
    elif binary_format[1:4] == [0, 0, 1]:
        return Rook(i, j, color)
    # Return Queen
    elif binary_format[1:4] == [1, 0, 0]:
        return Queen(i, j, color)
    # Return King
    elif binary_format[1:4] == [1, 0, 1]:
        return King(i, j, color)
    else:
        raise ValueError('Incorrect binary format')


def can_move_diagonally(piece, board, i, j):
    if abs(piece.i - i) != abs(piece.j - j):
        return False

    # moving upper right diagonal
    if i > piece.i and j > piece.j:
        for k in range(1, abs(i - piece.i)):
            if not isinstance(board.board[piece.i + k][piece.j + k], NullPiece):
                return False

    # Moving upper left diagonal
    if i > piece.i and j < piece.j:
        for k in range(1, abs(i - piece.i)):
            if not isinstance(board.board[piece.i + k][piece.j - k], NullPiece):
                return False

    # Moving lower left diagonal
    if i < piece.i and j < piece.j:
        for k in range(1, abs(i - piece.i)):
            if not isinstance(board.board[piece.i - k][piece.j - k], NullPiece):
                return False

    # Moving lower right diagonal
    if i < piece.i and j > piece.j:
        for k in range(1, abs(i - piece.i)):
            if not isinstance(board.board[piece.i - k][piece.j + k], NullPiece):
                return False

    return True


def can_move_forward_and_sideways(piece, board, i, j):
    if piece.i != i and piece.j != j:
        return False

    # Moving up.
    if piece.j == j and piece.i < i:
        for k in range(1, abs(i - piece.i)):
            if not isinstance(board.board[piece.i + k][piece.j], NullPiece):
                return False

    # Moving down
    if piece.j == j and piece.i > i:
        for k in range(1, abs(i - piece.i)):
            if not isinstance(board.board[piece.i - k][piece.j], NullPiece):
                return False

    # Moving right
    if piece.i == i and piece.j < j:
        for k in range(1, abs(j - piece.j)):
            if not isinstance(board.board[piece.i][piece.j + k], NullPiece):
                return False

    # Moving left
    if piece.i == i and piece.j > j:
        for k in range(1, abs(j - piece.j)):
            if not isinstance(board.board[piece.i][piece.j - k], NullPiece):
                return False

    return True


def get_diagonal_moves(piece, board, ignore_check):
    moves = []
    k = 1
    while piece.i + k < 8 and piece.j + k < 8:
        moves.append(piece.get_move(board, piece.i + k, piece.j + k, ignore_check))
        k += 1

    k = 1
    while piece.i + k < 8 and piece.j - k >= 0:
        moves.append(piece.get_move(board, piece.i + k, piece.j - k, ignore_check))
        k += 1

    k = 1
    while piece.i - k >= 0 and piece.j - k >= 0:
        moves.append(piece.get_move(board, piece.i - k, piece.j - k, ignore_check))
        k += 1

    k = 1
    while piece.i - k >= 0 and piece.j + k < 8:
        moves.append(piece.get_move(board, piece.i - k, piece.j + k, ignore_check))
        k += 1
    return [x for x in moves if x is not None]


def get_forward_and_sideways_moves(piece, board, ignore_check):
    moves = []
    k = 1
    while piece.i + k < 8:
        moves.append(piece.get_move(board, piece.i + k, piece.j, ignore_check))
        k += 1

    k = 1
    while piece.i - k >= 0:
        moves.append(piece.get_move(board, piece.i - k, piece.j, ignore_check))
        k += 1

    k = 1
    while piece.j + k < 8:
        moves.append(piece.get_move(board, piece.i, piece.j + k, ignore_check))
        k += 1

    k = 1
    while piece.j - k >= 0:
        moves.append(piece.get_move(board, piece.i, piece.j - k, ignore_check))
        k += 1

    return [x for x in moves if x is not None]


def get_coordinate_move(piece, i, j, capture, board, ignore_check):
    move_str = ''

    if capture:
        move_str += str(Board.Board.col_index_to_algebra[piece.j]) + str(Board.Board.row_index_to_algebra[piece.i]) + 'x' + \
            str(Board.Board.col_index_to_algebra[j]) + str(Board.Board.row_index_to_algebra[i])
    else:
        move_str += str(Board.Board.col_index_to_algebra[piece.j]) + str(Board.Board.row_index_to_algebra[piece.i]) + \
               str(Board.Board.col_index_to_algebra[j]) + str(Board.Board.row_index_to_algebra[i])

    if not ignore_check:
        move_result = board.move_is_check_or_checkmate(piece, i, j)
        if move_result == 2:
            move_str += '#'
        elif move_result == 1:
            move_str += '+'

    return move_str
