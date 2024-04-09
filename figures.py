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
                              ['a1', 'b1', 'c1', 'd1', 'e1', 'f1', 'g1', 'h1'],]


    def load_figures(self):
        white = {"pw": QPixmap("assets/white/pawn.png"),
                 "rw": QPixmap("assets/white/rook.png"),
                 "knw":QPixmap("assets/white/knight.png"),
                 "bw": QPixmap("assets/white/bishop.png"),
                 "qw": QPixmap("assets/white/queen.png"),
                 "kw": QPixmap("assets/white/king.png")
                 }

        black = {"pb":QPixmap("assets/black/pawn.png"),
                "rb": QPixmap("assets/black/rook.png"),
                 "knb":QPixmap("assets/black/knight.png"),
                 "bb": QPixmap("assets/black/bishop.png"),
                 "qb": QPixmap("assets/black/queen.png"),
                 "kb": QPixmap("assets/black/king.png")
                 }

        return white, black


    def white_movement(self, item_select, item_data, pos, move,arr):
        if move % 2 == 0 and item_select in arr:
            item_select.setPos(*pos)
            return True


    def black_movement(self, item_select, item_data, pos, move,arr):
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
