import time

import utilis
from figures import Figure
from game import Game

from PyQt5.QtWidgets import QGraphicsScene, QGraphicsView, QGraphicsRectItem
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt, QPointF, QRectF, QTimer


class Window(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.figures = Figure()
        self.img_w, self.img_b = self.figures.load_figures()
        self.white = []
        self.black = []

        self.title = "Chess"
        self.width = self.height = 600
        self.slots = 8
        self.scene = QGraphicsScene()

        self.highlights = []
        self.highlights_attack = []
        self.last_pos = []
        self.slot_w = self.width / self.slots
        self.slot_h = self.height / self.slots

        self.board = [[0, 1, 0, 1, 0, 1, 0, 1],
                      [1, 0, 1, 0, 1, 0, 1, 0],
                      [0, 1, 0, 1, 0, 1, 0, 1],
                      [1, 0, 1, 0, 1, 0, 1, 0],
                      [0, 1, 0, 1, 0, 1, 0, 1],
                      [1, 0, 1, 0, 1, 0, 1, 0],
                      [0, 1, 0, 1, 0, 1, 0, 1],
                      [1, 0, 1, 0, 1, 0, 1, 0]]
        self.dragging_item = None

        from addons import Addons
        self.game = Game(self)

        self.addons = Addons(self)
        self.input = ''

        self.timer = QTimer()
        self.timer.timeout.connect(self.addons.update_time)
        self.timer.start(1000)
        self.start_time = time.time()

        self.serv_client = QTimer()
        self.serv_client.timeout.connect(self.game.manage_communication)
        self.serv_client.start(1000)

        self.turn_timer = QTimer()
        self.turn_timer.timeout.connect(self.addons.update_turn)
        self.turn_timer.start(1000)

        self.ai_timer = QTimer()
        self.ai_timer.timeout.connect(self.game.ai_move)
        self.ai_timer.start(1000)

        self.create_window()

    def create_window(self):

        self.setWindowTitle(self.title)
        self.setGeometry(0, 0, self.width, self.height)

        self.setSceneRect(0, 0, self.width, self.height)
        self.setScene(self.scene)

        self.create_chessboard()
        self.figures.reset_board()
        self.show_figures()

        self.scene.mousePressEvent = self.drag
        self.scene.mouseMoveEvent = self.move_img
        self.scene.mouseReleaseEvent = self.release

        self.addons.add_stuff()
        self.addons.update_time()
        self.addons.update_turn()

        self.show()

    def create_chessboard(self):

        color1 = QColor(utilis.TILE_COLOR_1)
        color2 = QColor(utilis.TILE_COLOR_2)

        for i in range(self.slots):
            for j in range(self.slots):
                rect_item = QGraphicsRectItem(0 + i * self.slot_w, 0 + j * self.slot_h, self.slot_w, self.slot_h)

                if self.board[i][j] == 0:
                    rect_item.setBrush(color2)
                elif self.board[i][j] == 1:
                    rect_item.setBrush(color1)

                self.scene.addItem(rect_item)

    def retrieve_text(self):
        text = self.addons.text_edit.toPlainText()
        print("Retrieved text:", text)
        self.addons.text_edit.clear()
        self.game.input_move(text[:2], text[3:])

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            if self.game.opponent == 'player':
                self.game.send_data()

            elif self.game.opponent == 'ai':
                self.retrieve_text()
        else:
            super().keyPressEvent(event)



    def find_pos(self, pos):
        for i, row in enumerate(self.figures.pos_board):
            for j, element in enumerate(row):
                if element == pos:
                    return i, j
        return None, None

    def show_figures(self):
        for i in range(len(self.figures.figures_board)):
            for j in range(len(self.figures.figures_board[0])):

                key = self.figures.figures_board[i][j]

                if key in self.img_b:
                    item = self.scene.addPixmap(self.img_b[f'{key}'])
                    item.setPos(8 + j * 75, 8 + i * 75)
                    item.setData(Qt.UserRole, key)
                    item.setZValue(1)
                    self.black.append(item)

                elif key in self.img_w:
                    item = self.scene.addPixmap(self.img_w[f'{key}'])
                    item.setPos(8 + j * 75, 8 + i * 75)
                    item.setData(Qt.UserRole, key)
                    item.setZValue(1)
                    self.white.append(item)

    def define_objects_at(self, x, y, size_x, size_y):
        items = self.scene.items(QRectF(x, y, size_x, size_y))
        return items

    def check_attack(self, x, y, key):
        fig2 = self.define_objects_at(x + 38, y + 38, 1, 1)

        color2 = fig2[0].data(Qt.UserRole)[-1]
        if key[-1] != color2:
            rect1 = QGraphicsRectItem(x, y, self.slot_w, self.slot_h)
            color = QColor(utilis.ATTACK_COLOR)
            rect1.setBrush(color)
            rect1.setZValue(0)
            self.scene.addItem(rect1)
            self.highlights_attack.append(rect1)

    def delete_attacked(self, x, y):

        figures = self.define_objects_at(x + 30, y + 30, 1, 1)

        if self.game.move % 2 == 0:
            for figure in figures:
                if figure.data(Qt.UserRole) is None:
                    pass
                elif figure.data(Qt.UserRole)[-1] == 'b':
                    self.scene.removeItem(figure)

        elif self.game.move % 2 == 1:
            for figure in figures:
                if figure.data(Qt.UserRole) is None:
                    pass

                elif figure.data(Qt.UserRole)[-1] == 'w':
                    self.scene.removeItem(figure)

    def check_mate(self):
        key = 'kb'
        if self.game.move % 2 == 0: key = 'kw'

        slot = (0, 0)
        for row_idx, row in enumerate(self.figures.figures_board):
            for piece_idx, piece in enumerate(row):
                if piece == key:
                    slot = (8 + piece_idx * 75, 8 + row_idx * 75)
                    break

        for highlight in self.highlights_attack:
            if highlight.rect().contains(QPointF(*slot)):
                pass

    def end_game(self):
        king_w = False
        king_b = False
        for row in self.figures.figures_board:
            for piece in row:
                if piece == 'kw':
                    king_w = True
                elif piece == 'kb':
                    king_b = True
        return king_w and king_b

    def check_existance(self, x, y):
        for rect in self.highlights:
            if rect.rect().contains(QPointF(x, y)):
                return True

    def check_attack_exist(self, x, y):
        if len(self.highlights_attack) == 0: return False
        for rect in self.highlights_attack:
            if rect.rect().contains(QPointF(x, y)):
                return True

    def check_if_empty(self, idx_x, idx_y):
        if self.figures.figures_board[idx_x][idx_y] is None:
            return True
        else:
            return False

    def change_fig_pos(self, fig, idx_x, idx_y):
        self.figures.figures_board[idx_x][idx_y] = fig

    def convert_pos(self, x, y):
        pos_x = int(x / self.slot_w) * self.slot_w + 8
        pos_y = int(y / self.slot_h) * self.slot_h + 8
        idx_x = int(x / self.slot_w)
        idx_y = int(y / self.slot_h)
        return pos_x, pos_y, idx_x, idx_y

    def drag(self, event):
        # self.loaded_input()

        pos = event.scenePos()

        x, y, pos_x, pos_y = self.convert_pos(pos.x(), pos.y())

        self.start_time = time.time()

        item_clicked = self.scene.itemAt(pos, self.transform())
        self.addons.update_label()

        if item_clicked.type() == 3:
            pass

        if item_clicked.type() == 12:
            pass

        else:
            try:
                item_data = item_clicked.data(Qt.UserRole)
                if self.game.move % 2 == 0 and item_data[-1] == 'w':

                    self.highlight(item_data, x, y)
                    self.dragging_item = item_clicked
                    self.change_fig_pos(None, pos_y, pos_x)

                    self.last_pos = [int(self.dragging_item.x() / self.slot_w),
                                     int(self.dragging_item.y() / self.slot_h)]

                    chess_pos = self.figures.pos_board[self.last_pos[1]][self.last_pos[0]]
                    self.game.queue.put(f"last pos {chess_pos}\n")
                    self.game.game_history.append(f"{item_data}: {chess_pos} ")

                elif self.game.move % 2 == 1 and item_data[-1] == 'b':

                    self.highlight(item_data, x, y)
                    self.dragging_item = item_clicked
                    self.change_fig_pos(None, pos_y, pos_x)

                    self.last_pos = [int(self.dragging_item.x() / self.slot_w),
                                     int(self.dragging_item.y() / self.slot_h)]

                    chess_pos = self.figures.pos_board[self.last_pos[1]][self.last_pos[0]]
                    self.game.queue.put(f"last pos {chess_pos}\n")
                    self.game.game_history.append(f"{item_data}: {chess_pos} ")

            except TypeError:
                pass

    def move_img(self, event):
        if self.dragging_item:
            pos = event.scenePos()
            new_pos = pos

            if new_pos.x() < 0 or new_pos.y() < 0 or new_pos.x() > (self.width - 70) or new_pos.y() > (
                    self.height - 70):
                new_pos.setX(min(max(0, pos.x()), self.width - 70))
                new_pos.setY(min(max(0, pos.y()), self.height - 70))

            self.dragging_item.setPos(new_pos)

    def swap(self, x, side):
        if x != 7 and x != 0:
            return False

        num1 = 1
        num2 = 4

        if side == 'r':
            num1 = 5
            num2 = 7

        for i in range(num1, num2):
            if self.figures.figures_board[x][i] is not None: return False

        if self.figures.figures_board[x][0][0] != 'r' or self.figures.figures_board[x][7][0] != 'r':
            return False

        return True

    def release(self, event):
        pos = event.scenePos()

        rect = self.scene.itemAt(pos, self.transform())

        if rect.type() == 3:
            x, y, pos_x, pos_y = self.convert_pos(pos.x(), pos.y())

            if (self.check_existance(x, y) and self.check_if_empty(pos_y, pos_x)) or self.check_attack_exist(x, y):
                if self.check_attack_exist(x, y):
                    self.delete_attacked(x, y)

                new_pos = (x, y)

                if self.dragging_item.data(Qt.UserRole)[0] == "k" and len(self.dragging_item.data(Qt.UserRole)) == 2:
                    print(2)
                    side = ''
                    if pos_x > 4:
                        side = 'r'

                    elif pos_x < 4:
                        side = 'l'

                    if side != '':
                        if self.swap(self.last_pos[1], side):
                            mov = 0
                            mov_r = 0
                            r_pos = 0

                            if side == 'l':
                                mov = 2
                                mov_r = 3

                            elif side == 'r':
                                mov = 6
                                mov_r = 5
                                r_pos = 7

                            new_pos = (mov * self.slot_h + 8, y)
                            new_pos_r = (mov_r * self.slot_h + 8, y)
                            items = self.define_objects_at(r_pos * self.slot_h + 8 + 38, y + 38, 1, 1)

                            if items[0].data(Qt.UserRole)[-1] != self.dragging_item.data(Qt.UserRole)[-1]:
                                new_pos = (x, y)
                            else:
                                items[0].setPos(*new_pos_r)

                chess_pos = self.figures.pos_board[pos_y][pos_x]

                self.game.queue.put(f" new pos {chess_pos}\n")
                self.game.game_history[-1] += f"{chess_pos}"

                self.dragging_item.setPos(*new_pos)
                figure = self.dragging_item.data(Qt.UserRole)
                self.change_fig_pos(figure, pos_y, pos_x)

                self.highlight(self.dragging_item.data(Qt.UserRole), x, y)
                self.check_mate()
                self.remove_highlights()

                self.dragging_item = None
                self.game.move += 1


            elif not self.check_existance(x, y):
                return

            self.addons.update_turn()

    def highlight(self, key, x, y):

        x -= 8
        y -= 8

        color = QColor(utilis.HIGHLIGHT_COLOR)

        curr_x = int(x / self.slot_w)
        curr_y = int(y / self.slot_h)

        self.highlight_current(x, y, self.slot_w, self.slot_h)

        if (key == 'pw' or key == 'pb'):
            self.execute_pawn_move(curr_x, curr_y, color, key)

        if key == 'rw' or key == 'rb' or key == "qw" or key == "qb":
            self.execute_rook_move(curr_x, curr_y, color, key)

        if key == 'bw' or key == 'bb' or key == "qw" or key == "qb":
            self.execute_bishop_move(curr_x, curr_y, color, key)

        if key == 'knw' or key == 'knb':
            self.execute_knight_move(curr_x, curr_y, color, key)

        if key == "kw" or key == "kb":
            self.execute_king_move(curr_x, curr_y, color, key)

    def execute_pawn_move(self,curr_x,curr_y,color,key):
        moves, attacks = self.figures.define_pawn_moves(self.slots, curr_x, curr_y, key)

        for move_x, move_y in moves:
            if self.check_if_empty(move_y, move_x):
                rect = QGraphicsRectItem(move_x * self.slot_w, move_y * self.slot_h, self.slot_w, self.slot_h)
                self.highlight_rect(rect, color)

        for attack_x, attack_y in attacks:
            if not self.check_if_empty(attack_y, attack_x):
                self.check_attack(attack_x * self.slot_w, attack_y * self.slot_h, key)

    def execute_rook_move(self,curr_x,curr_y,color,key):
        moves = self.figures.define_rook_moves(self.slots, curr_x, curr_y)
        for side, side_moves in moves.items():
            for move_x, move_y in side_moves:
                if self.check_if_empty(move_y, move_x):
                    rect = QGraphicsRectItem(self.slot_w * move_x, self.slot_h * move_y, self.slot_w,
                                             self.slot_h)
                    self.highlight_rect(rect, color)
                else:

                    self.check_attack(move_x * self.slot_w, move_y * self.slot_h, key)
                    break

    def execute_bishop_move(self,curr_x,curr_y,color,key):
        moves = self.figures.define_bishop_moves(self.slots, curr_x, curr_y)
        for side, side_moves in moves.items():
            for move_x, move_y in side_moves:
                if self.check_if_empty(move_y, move_x):
                    rect = QGraphicsRectItem(self.slot_w * move_x, self.slot_h * move_y, self.slot_w,
                                             self.slot_h)
                    self.highlight_rect(rect, color)
                else:

                    self.check_attack(move_x * self.slot_w, move_y * self.slot_h, key)
                    break

    def execute_knight_move(self,curr_x,curr_y,color,key):
        moves = self.figures.define_knight_moves(self.slots, curr_x, curr_y)

        for move_x, move_y in moves:
            if not self.check_if_empty(move_y, move_x):
                self.check_attack(move_x * self.slot_w, move_y * self.slot_h, key)
                continue
            rect = QGraphicsRectItem(move_x * self.slot_w, move_y * self.slot_h, self.slot_w, self.slot_h)
            self.highlight_rect(rect, color)

    def execute_king_move(self,curr_x,curr_y,color,key):
        moves = self.figures.deine_king_moves(curr_x, curr_y)
        for side, side_moves in moves.items():
            for move_x, move_y in side_moves:
                if self.check_if_empty(move_y, move_x):
                    rect = QGraphicsRectItem(move_x * self.slot_w, move_y * self.slot_h, self.slot_w, self.slot_h)
                    self.highlight_rect(rect, color)
                else:
                    self.check_attack(move_x * self.slot_w, move_y * self.slot_h, key)
                    break

    def highlight_rect(self,rect, color):
        rect.setBrush(color)
        rect.setZValue(0)
        self.scene.addItem(rect)
        self.highlights.append(rect)

    def remove_highlights(self):
        if len(self.highlights) > 0:
            for highlight in self.highlights:
                self.scene.removeItem(highlight)
            self.highlights = []

        if len(self.highlights_attack) > 0:
            for highlight in self.highlights_attack:
                self.scene.removeItem(highlight)
            self.highlights_attack = []

    def highlight_current(self, x, y, size_w, size_h):
        color = QColor(utilis.FIG_POS_COLOR)
        rect_fig = QGraphicsRectItem(x, y, size_w, size_h)
        rect_fig.setBrush(color)
        rect_fig.setZValue(0)

        self.scene.addItem(rect_fig)
        self.highlights.append(rect_fig)
