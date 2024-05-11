import time
import utilis
from figures import Figure
from game import Game
from addons import Addons
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

        self.game = Game(self)
        self.addons = Addons(self)
        self.input = ''

        self.timer, self.turn_timer, self.ai_timer, self.serv_client = self.create_timers()

        self.create_window()

    '''
    
    interface setup:
        - creating window
        - board
        - placing figures
        - timers
    
    '''

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

    def create_timers(self):
        timer = QTimer()
        timer.timeout.connect(self.addons.update_time)
        timer.start(1000)

        turn_timer = QTimer()
        turn_timer.timeout.connect(self.addons.update_turn)
        turn_timer.start(1000)

        ai_timer = None
        serv_client = None

        if self.game.opponent == 'ai':
            ai_timer = QTimer()
            ai_timer.timeout.connect(self.game.ai_move)
            ai_timer.start(2000)

        elif self.game.opponent == 'player':
            serv_client = QTimer()
            serv_client.timeout.connect(self.game.manage_communication)
            serv_client.start(1000)

        return timer, turn_timer, ai_timer, serv_client


    '''
    
    interface events: 
        - retrieving text from input window
        - key events
        - dragging, moving, releasing
    
    '''

    def retrieve_text(self):
        text = self.addons.text_edit.toPlainText()
        print("Retrieved text:", text)
        self.addons.text_edit.clear()
        self.input_move(text[:2], text[3:])

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            if self.game.opponent == 'player':
                self.game.send_data()

            elif self.game.opponent == 'ai':
                self.retrieve_text()
        else:
            super().keyPressEvent(event)


    def drag(self, event):
        pos = event.scenePos()

        self.game.start_time = time.time()

        item_clicked = self.scene.itemAt(pos, self.transform())
        self.addons.update_label()

        try:
            item_data = item_clicked.data(Qt.UserRole)
            if (self.game.move % 2 == 0 and item_data[-1] == 'w')\
                    or (self.game.move % 2 == 1 and item_data[-1] == 'b'):

                x, y, pos_x, pos_y = self.convert_pos(pos.x(), pos.y())

                self.highlight(item_data, x, y)
                self.dragging_item = item_clicked
                self.figures.change_fig_pos(None, pos_y, pos_x)

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


    def release(self, event):
        pos = event.scenePos()

        rect = self.scene.itemAt(pos, self.transform())

        if rect.type() == 3:
            x, y, pos_x, pos_y = self.convert_pos(pos.x(), pos.y())

            if (self.check_existence(x, y) and self.check_if_empty(pos_y, pos_x)) or self.check_attack_exist(x, y):
                if self.check_attack_exist(x, y):
                    self.delete_attacked(x, y)

                new_pos = (x, y)

                status, temp_pos = self.move_for_castling(pos_x,x,y)
                if status: new_pos=temp_pos
                chess_pos = self.figures.pos_board[pos_y][pos_x]

                self.game.queue.put(f" new pos {chess_pos}\n")
                self.game.game_history[-1] += f"{chess_pos}"

                self.dragging_item.setPos(*new_pos)
                figure = self.dragging_item.data(Qt.UserRole)
                self.figures.change_fig_pos(figure, pos_y, pos_x)

                self.highlight(self.dragging_item.data(Qt.UserRole), x, y)
                self.check_mate()
                self.remove_highlights()

                self.dragging_item = None
                self.game.move += 1


            elif not self.check_existence(x, y):
                return

            self.addons.update_turn()

    '''
    
    interface changes:
        - highlighting
    
    '''

    def highlight(self, key: str, x: float, y: float):

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


    def highlight_rect(self,rect: QRectF, color: str):
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

    def highlight_current(self, x: float, y: float, size_w: float, size_h: float):
        color = QColor(utilis.FIG_POS_COLOR)
        rect_fig = QGraphicsRectItem(x, y, size_w, size_h)
        rect_fig.setBrush(color)
        rect_fig.setZValue(0)

        self.scene.addItem(rect_fig)
        self.highlights.append(rect_fig)


    '''
    
    game-interface related actions:
        - defining object at certain position
        - defining coords of figure on board
        - checking slot, availability, if it is highlighted
        - removing figure
        - checking if position is under attack
        - moving figures based on instructions from input window
        
    '''


    def define_objects_at(self, x: float, y: float, size_x: int, size_y: int):
        items = self.scene.items(QRectF(x, y, size_x, size_y))
        return items

    def convert_pos(self, x: float, y: float):
        pos_x = int(x / self.slot_w) * self.slot_w + 8
        pos_y = int(y / self.slot_h) * self.slot_h + 8
        idx_x = int(x / self.slot_w)
        idx_y = int(y / self.slot_h)
        return pos_x, pos_y, idx_x, idx_y

    def check_if_empty(self, idx_x: int, idx_y: int):
        if self.figures.figures_board[idx_x][idx_y] is None:
            return True
        else:
            return False

    def check_existence(self, x: float, y:float):
        for rect in self.highlights:
            if rect.rect().contains(QPointF(x, y)):
                return True

    def delete_attacked(self, x: float, y:float):

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

    def check_attack(self, x: float, y: float, key: str):
        fig2 = self.define_objects_at(x + 38, y + 38, 1, 1)

        color2 = fig2[0].data(Qt.UserRole)[-1]
        if key[-1] != color2:
            rect1 = QGraphicsRectItem(x, y, self.slot_w, self.slot_h)
            color = QColor(utilis.ATTACK_COLOR)
            rect1.setBrush(color)
            rect1.setZValue(0)
            self.scene.addItem(rect1)
            self.highlights_attack.append(rect1)

    def check_attack_exist(self, x, y):
        if len(self.highlights_attack) == 0: return False
        for rect in self.highlights_attack:
            if rect.rect().contains(QPointF(x, y)):
                return True

    '''
    
    input actions
    
    '''
    def input_move(self,pos_s: tuple, pos_e: tuple):
        x_s, y_s = self.find_pos(pos_s)
        x_e, y_e = self.find_pos(pos_e)

        if not self.validate_positions(x_s, y_s, x_e, y_e):
            return

        key = self.figures.figures_board[x_s][y_s]
        if not self.validate_turn(key, self.game.move):
            return

        x, y = self.calculate_item_pos(x_s, y_s)
        self.highlight(key, x, y)
        xe, ye = self.calculate_item_pos(x_e, y_e)

        if self.check_move_validity(xe, ye):
            self.perform_move(y_s, x_s, y_e, x_e, key)
            self.game.move += 1
        self.remove_highlights()


    def validate_positions(self, x_s: int, y_s: int, x_e: int, y_e: int):
        if (x_s is None and y_s is None) or (x_e is None and y_e is None):
            return False
        return True

    def validate_turn(self, key, move):
        if key is None: return
        if move % 2 == 0 and key[-1] != 'w':
            return False
        elif move % 2 == 1 and key[-1] != 'b':
            return False
        return True


    def find_pos(self, pos: tuple):
        for i, row in enumerate(self.figures.pos_board):
            for j, element in enumerate(row):
                if element == pos:
                    return i, j
        return None, None

    def calculate_item_pos(self, x: int, y: int):
        return y * 75 + 8, x * 75 + 8

    def check_move_validity(self, x_e: int, y_e: int):
        return self.check_existence(x_e, y_e) or self.check_attack_exist(x_e, y_e)

    def perform_move(self,x_s: int, y_s: int, x_e: int, y_e: int, key: str):
        self.figures.change_fig_pos(None, y_s, x_s)
        item = self.scene.itemAt(x_s * 75 + 8 + 30, y_s * 75 + 8 + 30, self.transform())


        if not self.check_if_empty(y_e, x_e):
            key_e = self.figures.figures_board[y_e][x_e]
            if key[-1]!=key_e[-1]:
                item_e = self.scene.itemAt(x_e * 75 + 8 + 30, y_e * 75 + 8 + 30, self.transform())
                self.scene.removeItem(item_e)

        item.setPos(x_e * 75 + 8, y_e * 75 + 8)
        self.figures.change_fig_pos(key, y_e, x_e)




    '''
    
    game-interface related actions:
        - all functions with defining what to highlight: attacks and moves
    
    '''

    def execute_pawn_move(self, curr_x: int,curr_y: int,color: str,key: str):
        moves, attacks = self.figures.define_pawn_moves(self.slots, curr_x, curr_y, key)

        for move_x, move_y in moves:
            if self.check_if_empty(move_y, move_x):
                rect = QGraphicsRectItem(move_x * self.slot_w, move_y * self.slot_h, self.slot_w, self.slot_h)
                self.highlight_rect(rect, color)

        for attack_x, attack_y in attacks:
            if not self.check_if_empty(attack_y, attack_x):
                self.check_attack(attack_x * self.slot_w, attack_y * self.slot_h, key)

    def execute_rook_move(self,curr_x: int,curr_y: int,color: str,key: str):
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

    def execute_bishop_move(self,curr_x: int,curr_y: int,color: str,key: str):
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

    def execute_knight_move(self,curr_x: int,curr_y: int,color: str,key: str):
        moves = self.figures.define_knight_moves(self.slots, curr_x, curr_y)

        for move_x, move_y in moves:
            if not self.check_if_empty(move_y, move_x):
                self.check_attack(move_x * self.slot_w, move_y * self.slot_h, key)
                continue
            rect = QGraphicsRectItem(move_x * self.slot_w, move_y * self.slot_h, self.slot_w, self.slot_h)
            self.highlight_rect(rect, color)

    def execute_king_move(self,curr_x: int,curr_y: int,color: str,key: str):
        moves = self.figures.define_king_moves(curr_x, curr_y)
        for side, side_moves in moves.items():
            for move_x, move_y in side_moves:
                if self.check_if_empty(move_y, move_x):
                    rect = QGraphicsRectItem(move_x * self.slot_w, move_y * self.slot_h, self.slot_w, self.slot_h)
                    self.highlight_rect(rect, color)
                else:
                    self.check_attack(move_x * self.slot_w, move_y * self.slot_h, key)
                    break


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


    def move_for_castling(self,pos_x: int,x: float,y: float):
        if self.dragging_item.data(Qt.UserRole)[0] == "k" and len(self.dragging_item.data(Qt.UserRole)) == 2:
            side = ''
            if pos_x > 4: side = 'r'
            elif pos_x < 4: side = 'l'
            if side == '': return

            if self.figures.do_castling(self.last_pos[1], side):
                mov, mov_r, r_pos = 0, 0, 0
                if side == 'l':
                    mov = 2
                    mov_r = 3

                elif side == 'r':
                    mov = 6
                    mov_r = 5
                    r_pos = 7

                new_pos = (mov * self.slot_h + 8, y)
                new_pos_rook = (mov_r * self.slot_h + 8, y)
                items = self.define_objects_at(r_pos * self.slot_h + 8 + 38, y + 38, 1, 1)

                if items[0].data(Qt.UserRole)[-1] == self.dragging_item.data(Qt.UserRole)[-1]:
                    self.dragging_item.setPos(*new_pos)
                    items[0].setPos(*new_pos_rook)
                    return True, new_pos

        return False, (None, None)
