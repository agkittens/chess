from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QGraphicsItem


class Figure(QGraphicsItem):
    def __init__(self):
        super().__init__()

        self.figures_board = [['rb', 'knb', 'bb', 'qb', 'kb', 'bb', 'knb', 'rb'],
                              ['pb', 'pb', 'pb', 'pb', 'pb', 'pb', 'pb', 'pb'],
                              [None, None, None, None, None, None, None, None],
                              [None, None, None, None, None, None, None, None],
                              [None, None, None, None, None, None, None, None],
                              [None, None, None, None, None, None, None, None],
                              ['pw', 'pw', 'pw', 'pw', 'pw', 'pw', 'pw', 'pw'],
                              ['rw', 'knw', 'bw', 'qw', 'kw', 'bw', 'knw', 'rw']
                              ]

        self.pos_board = [['a8', 'b8', 'c8', 'd8', 'e8', 'f8', 'g8', 'h8'],
                          ['a7', 'b7', 'c7', 'd7', 'e7', 'f7', 'g7', 'h7'],
                          ['a6', 'b6', 'c6', 'd6', 'e6', 'f6', 'g6', 'h6'],
                          ['a5', 'b5', 'c5', 'd5', 'e5', 'f5', 'g5', 'h5'],
                          ['a4', 'b4', 'c4', 'd4', 'e4', 'f4', 'g4', 'h4'],
                          ['a3', 'b3', 'c3', 'd3', 'e3', 'f3', 'g3', 'h3'],
                          ['a2', 'b2', 'c2', 'd2', 'e2', 'f2', 'g2', 'h2'],
                          ['a1', 'b1', 'c1', 'd1', 'e1', 'f1', 'g1', 'h1'], ]

    def load_figures(self):
        white = {"pw": QPixmap("assets/white/pawn.png"),
                 "rw": QPixmap("assets/white/rook.png"),
                 "knw": QPixmap("assets/white/knight.png"),
                 "bw": QPixmap("assets/white/bishop.png"),
                 "qw": QPixmap("assets/white/queen.png"),
                 "kw": QPixmap("assets/white/king.png")
                 }

        black = {"pb": QPixmap("assets/black/pawn.png"),
                 "rb": QPixmap("assets/black/rook.png"),
                 "knb": QPixmap("assets/black/knight.png"),
                 "bb": QPixmap("assets/black/bishop.png"),
                 "qb": QPixmap("assets/black/queen.png"),
                 "kb": QPixmap("assets/black/king.png")
                 }

        return white, black

    def white_movement(self, item_select, item_data, pos, move, arr):
        if move % 2 == 0 and item_select in arr:
            item_select.setPos(*pos)
            return True

    def black_movement(self, item_select, item_data, pos, move, arr):
        if move % 2 == 1 and item_select in arr:
            item_select.setPos(*pos)

            return True

    def reset_board(self):
        self.figures_board = [['rb', 'knb', 'bb', 'qb', 'kb', 'bb', 'knb', 'rb'],
                              ['pb', 'pb', 'pb', 'pb', 'pb', 'pb', 'pb', 'pb'],
                              [None, None, None, None, None, None, None, None],
                              [None, None, None, None, None, None, None, None],
                              [None, None, None, None, None, None, None, None],
                              [None, None, None, None, None, None, None, None],
                              ['pw', 'pw', 'pw', 'pw', 'pw', 'pw', 'pw', 'pw'],
                              ['rw', 'knw', 'bw', 'qw', 'kw', 'bw', 'knw', 'rw']
                              ]


    def change_fig_pos(self, fig, idx_x, idx_y):
        self.figures_board[idx_x][idx_y] = fig

    def do_castling(self, x, side):
        if x != 7 and x != 0:
            return False

        num1 = 1
        num2 = 4

        if side == 'r':
            num1 = 5
            num2 = 7

        for i in range(num1, num2):
            if self.figures_board[x][i] is not None: return False

        if self.figures_board[x][0][0] != 'r' or self.figures_board[x][7][0] != 'r':
            return False

        return True


    @staticmethod
    def define_pawn_moves(slots, curr_x, curr_y, key):
        val = -1 if key[-1] == 'w' else 1
        moves = []
        attacks = []

        if 0 <= curr_y + val < slots:
            moves.append((curr_x, curr_y + val))

            if ((curr_y == 1 and key[-1] == 'b') or (curr_y == 6 and key[-1] == 'w')) and 0 <= curr_y + 2 * val < slots:
                moves.append((curr_x, curr_y + 2 * val))

            for dx in [-1, 1]:
                if 0 <= curr_x + dx < 8 and 0 <= curr_y + val < 8:
                    attacks.append((curr_x + dx, curr_y + val))
        return moves, attacks

    @staticmethod
    def define_bishop_moves(slots, curr_x, curr_y):
        moves = {
            'top_left': [],
            'top_right': [],
            'bottom_left': [],
            'bottom_right': []
        }

        offsets = [(1, -1), (1, 1), (-1, -1), (-1, 1)]

        for i, (offset_x, offset_y) in enumerate(offsets):
            for distance in range(1, slots):
                new_x, new_y = curr_x + offset_x * distance, curr_y + offset_y * distance
                if 0 <= new_x < slots and 0 <= new_y < slots:
                    moves[list(moves.keys())[i]].append((new_x, new_y))
                else:
                    break
        return moves

    @staticmethod
    def define_rook_moves(slots, curr_x, curr_y):
        moves = {
            'top': [],
            'right': [],
            'left': [],
            'bottom': []
        }
        offsets = [(0, 1), (1, 0), (-1, 0), (0, -1)]

        for i, (offset_x, offset_y) in enumerate(offsets):
            for distance in range(1, slots):
                new_x, new_y = curr_x + offset_x * distance, curr_y + offset_y * distance
                if 0 <= new_x < slots and 0 <= new_y < slots:
                    moves[list(moves.keys())[i]].append((new_x, new_y))
                else:
                    break
        return moves

    @staticmethod
    def define_knight_moves(slots, curr_x, curr_y):
        moves = []
        offsets = [
            (1, 2), (2, 1), (2, -1), (1, -2),
            (-1, -2), (-2, -1), (-2, 1), (-1, 2)
        ]
        for offset_x, offset_y in offsets:
            new_x, new_y = curr_x + offset_x, curr_y + offset_y
            if 0 <= new_x < slots and 0 <= new_y < slots:
                moves.append((new_x, new_y))
        return moves

    @staticmethod
    def deine_king_moves(curr_x, curr_y):
        moves = {
            'top': [],
            'right': [],
            'left': [],
            'bottom': [],
            'top_left': [],
            'top_right': [],
            'bottom_left': [],
            'bottom_right': []
        }
        offsets = [(0, 1), (1, 0), (-1, 0), (0, -1), (1, -1), (1, 1), (-1, -1), (-1, 1)]

        for i, (offset_x, offset_y) in enumerate(offsets):
            new_x, new_y = curr_x + offset_x, curr_y + offset_y
            if 0 <= new_x < 8 and 0 <= new_y < 8:
                moves[list(moves.keys())[i]].append((new_x, new_y))
        return moves
