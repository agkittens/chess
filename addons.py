import random
import time
from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import QColor, QFont, QPainterPath, QRegion, QPixmap, QImage
from PyQt5.QtWidgets import QLabel, QPushButton, QGraphicsEllipseItem, QGraphicsDropShadowEffect, \
    QGraphicsPixmapItem, QTextEdit, QRadioButton, QDialog, QVBoxLayout, \
    QCheckBox

import utilis
import sqlite3


class Addons:
    def __init__(self, window):
        self.window = window
        self.save = self.window.game.save
        self.queue = self.window.game.queue
        self.scene = self.window.scene
        self.is_loaded = False


    def mode1(self):
        self.window.game.mode=0
        self.window.game.max_time = 15
        self.max_time_label.setText(f'Max time : {self.window.game.max_time} min')

    def mode2(self):
        self.window.game.mode=1
        self.window.game.max_time = 5
        self.max_time_label.setText(f'Max time : {self.window.game.max_time} min')

    def mode3(self):
        self.window.game.mode=2
        self.window.game.max_time = 45
        self.max_time_label.setText(f'Max time : {self.window.game.max_time} min')



    def add_stuff(self):
        self.load_bg()
        self.label = QLabel()
        self.label.setText('Game history')
        self.label.resize(200,100)
        self.label.setStyleSheet(utilis.STYLE_LABEL)
        w = self.scene.addWidget(self.label)
        w.setPos(-500,100)
        self.scene.setBackgroundBrush(QColor(utilis.BG_COLOR))

        self.data_buttons()
        self.mode_info()
        self.turn_label()
        self.input_window()
        self.mode_buttons()
        self.save_buttons()
        self.circles()
        self.time_labels()

    def data_buttons(self):
        self.config_button = QPushButton("Config", self.window)
        self.config_button.resize(120,60)
        self.config_button.move(1350,100)
        self.config_button.clicked.connect(self.configuration_window)
        shadow_effect = QGraphicsDropShadowEffect()
        shadow_effect.setBlurRadius(15)
        shadow_effect.setColor(QColor(145, 90, 87, 127))
        shadow_effect.setOffset(0, 7)
        self.config_button.setGraphicsEffect(shadow_effect)

        self.load_button = QPushButton("Load", self.window)
        self.load_button.resize(120,60)
        self.load_button.move(1500,100)
        self.load_button.clicked.connect(self.load_data)
        shadow_effect_l = QGraphicsDropShadowEffect()
        shadow_effect_l.setBlurRadius(15)
        shadow_effect_l.setColor(QColor(145, 90, 87, 127))
        shadow_effect_l.setOffset(0, 7)
        self.load_button.setGraphicsEffect(shadow_effect_l)

        self.connect_button = QPushButton("Connect", self.window)
        self.connect_button.resize(120,60)
        self.connect_button.move(1650,100)
        self.connect_button.clicked.connect(self.window.game.server_connect)
        shadow_effect_c = QGraphicsDropShadowEffect()
        shadow_effect_c.setBlurRadius(15)
        shadow_effect_c.setColor(QColor(145, 90, 87, 127))
        shadow_effect_c.setOffset(0, 7)
        self.connect_button.setGraphicsEffect(shadow_effect_c)

    def mode_info(self):
        self.max_time_label = QLabel()
        self.max_time_label.setText(f'Max time : {self.window.game.max_time} min')
        self.max_time_label.setFont(QFont("Arial", 12,weight=QFont.Bold))
        self.max_time_label.resize(200, 60)
        self.max_time_label.setAutoFillBackground(True)
        palette = self.max_time_label.palette()
        palette.setColor(self.max_time_label.backgroundRole(), QColor("#f2e5dd"))
        self.max_time_label.setPalette(palette)
        path = QPainterPath()
        rect = QRectF(self.max_time_label.rect())
        path.addRoundedRect(rect, 10, 10)
        polygon = path.toFillPolygon().toPolygon()
        self.max_time_label.setMask(QRegion(polygon))

        self.max_time_label.setStyleSheet(utilis.STYLE_LABEL)
        self.max_time_label.setAlignment(Qt.AlignCenter)

        t = self.scene.addWidget(self.max_time_label)
        t.setPos(200, 720)

    def load_bg(self):
        background_image = QImage("assets/bg1.jpg")

        background_pixmap = QGraphicsPixmapItem(QPixmap.fromImage(background_image))
        background_pixmap.setTransformationMode(Qt.TransformationMode.SmoothTransformation)
        background_pixmap.setPos(-600, -200)
        self.scene.addItem(background_pixmap)
        background_pixmap.setZValue(-1)

    def turn_label(self):
        self.turn = QLabel()
        self.turn.setFont(QFont("Arial", 12,weight=QFont.Bold))
        self.turn.resize(200, 60)

        self.turn.setAutoFillBackground(True)
        palette = self.turn.palette()
        palette.setColor(self.turn.backgroundRole(), QColor("#476a66"))
        self.turn.setPalette(palette)

        path = QPainterPath()
        rect = QRectF(self.turn.rect())
        path.addRoundedRect(rect, 10, 10)
        polygon = path.toFillPolygon().toPolygon()
        self.turn.setMask(QRegion(polygon))


        self.turn.setStyleSheet(utilis.STYLE_LABEL3)
        self.turn.setAlignment(Qt.AlignCenter)


        turn = self.scene.addWidget(self.turn)
        turn.setPos(200, -100)

    def input_window(self):
        self.text_edit = QTextEdit()
        text = self.scene.addWidget(self.text_edit)
        text.setPos(700,0)

    def update_turn(self):
        if self.window.game.move %2 == 0:
            self.turn.setText("WHITE'S TURN")
        elif self.window.game.move %2 == 1:
            self.turn.setText("BLACK'S TURN")


    def mode_buttons(self):
        self.mode1_button = QPushButton("Rapid", self.window)
        self.mode2_button = QPushButton("Blitz", self.window)
        self.mode3_button = QPushButton("Classic", self.window)

        self.mode1_button.resize(120, 60)
        self.mode2_button.resize(120, 60)
        self.mode3_button.resize(120, 60)

        self.mode1_button.clicked.connect(self.mode1)
        self.mode2_button.clicked.connect(self.mode2)
        self.mode3_button.clicked.connect(self.mode3)

        self.mode1_button.move(750, 850)
        self.mode2_button.move(900, 850)
        self.mode3_button.move(1050, 850)

        shadow_effect1 = QGraphicsDropShadowEffect()
        shadow_effect1.setBlurRadius(15)
        shadow_effect1.setColor(QColor(145, 90, 87, 127))
        shadow_effect1.setOffset(0, 7)
        self.mode1_button.setGraphicsEffect(shadow_effect1)

        shadow_effect2 = QGraphicsDropShadowEffect()
        shadow_effect2.setBlurRadius(15)
        shadow_effect2.setColor(QColor(145, 90, 87, 127))
        shadow_effect2.setOffset(0, 7)
        self.mode2_button.setGraphicsEffect(shadow_effect2)

        shadow_effect3 = QGraphicsDropShadowEffect()
        shadow_effect3.setBlurRadius(15)
        shadow_effect3.setColor(QColor(145, 90, 87, 127))
        shadow_effect3.setOffset(0, 7)
        self.mode3_button.setGraphicsEffect(shadow_effect3)

        self.window.setStyleSheet(utilis.STYLE_BUTTON)

    def circles(self):
        circle_color = QColor(utilis.CIRCLE_COLOR)
        shadow_effect = QGraphicsDropShadowEffect()
        shadow_effect.setBlurRadius(15)
        shadow_effect.setColor(QColor(49, 81, 92, 127))
        shadow_effect.setOffset(0,7)

        circle_radius = 150
        circle_center = -250, 420

        circle = QGraphicsEllipseItem(circle_center[0] - circle_radius, circle_center[1] - circle_radius, circle_radius * 2, circle_radius * 2)
        circle.setBrush(circle_color)
        circle.setGraphicsEffect(shadow_effect)

        self.scene.addItem(circle)

        circle_center = 850, 420
        shadow_effect = QGraphicsDropShadowEffect()
        shadow_effect.setBlurRadius(15)
        shadow_effect.setColor(QColor(49, 81, 92, 127))
        shadow_effect.setOffset(0, 7)

        circle = QGraphicsEllipseItem(circle_center[0] - circle_radius, circle_center[1] - circle_radius, circle_radius * 2, circle_radius * 2)
        circle.setBrush(circle_color)
        circle.setGraphicsEffect(shadow_effect)

        self.scene.addItem(circle)


    def time_labels(self):
        self.white_time_label = QLabel()
        self.white_time_label.setText('WHITE\n')
        self.white_time_label.setFont(QFont("Arial", 15,weight=QFont.Bold))
        self.white_time_label.resize(200,60)
        self.white_time_label.setStyleSheet(utilis.STYLE_LABEL2)
        wt = self.scene.addWidget(self.white_time_label)
        wt.setPos(-180 - self.white_time_label.width()/2, 420 - self.white_time_label.height() / 2)

        self.black_time_label = QLabel()
        self.black_time_label.setText('BLACK\n')
        self.black_time_label.setFont(QFont("Arial", 15,weight=QFont.Bold))
        self.black_time_label.resize(200, 60)
        self.black_time_label.setStyleSheet(utilis.STYLE_LABEL2)
        bt = self.scene.addWidget(self.black_time_label)
        bt.setPos(915 - self.black_time_label.width() / 2, 420 - self.black_time_label.height() / 2)


    def update_label(self):
        if not self.queue.empty():
            self.save.append(self.queue.get())

            self.label.setText('\n'.join(self.save))
            self.label.resize(200, 100)


    def update_time(self):
        end_time = time.time() - self.window.game.start_time

        if self.window.dragging_item is None: return
        if self.window.dragging_item.data(Qt.UserRole)[-1] == 'w':
            self.window.game.white_time += end_time

        if self.window.dragging_item.data(Qt.UserRole)[-1] == 'b':
            self.window.game.black_time += end_time

        w_m = int(self.window.game.white_time // 60)
        w_s = int(self.window.game.white_time % 60)
        self.white_time_label.setText('WHITE\n' + f'{w_m}' + ':' + f'{w_s} ')

        b_m = int(self.window.game.black_time // 60)
        b_s = int(self.window.game.black_time % 60)
        self.black_time_label.setText('BLACK\n' + f'{b_m}' + ':' + f'{b_s} ')

        self.window.game.start_time = time.time()


    def save_buttons(self):
        self.mode4_button = QPushButton("SQL", self.window)
        self.mode5_button = QPushButton("XML", self.window)
        self.mode6_button = QPushButton("JSON", self.window)

        self.mode4_button.resize(120, 60)
        self.mode5_button.resize(120, 60)
        self.mode6_button.resize(120, 60)

        self.mode4_button.clicked.connect(self.window.game.save_to_sql)
        self.mode5_button.clicked.connect(self.window.game.save_to_xml)
        self.mode6_button.clicked.connect(self.window.game.save_to_json)

        self.mode4_button.move(100, 100)
        self.mode5_button.move(250, 100)
        self.mode6_button.move(400, 100)

        shadow_effect4 = QGraphicsDropShadowEffect()
        shadow_effect4.setBlurRadius(15)
        shadow_effect4.setColor(QColor(145, 90, 87, 127))
        shadow_effect4.setOffset(0, 7)
        self.mode4_button.setGraphicsEffect(shadow_effect4)

        shadow_effect5 = QGraphicsDropShadowEffect()
        shadow_effect5.setBlurRadius(15)
        shadow_effect5.setColor(QColor(145, 90, 87, 127))
        shadow_effect5.setOffset(0, 7)
        self.mode5_button.setGraphicsEffect(shadow_effect5)

        shadow_effect6 = QGraphicsDropShadowEffect()
        shadow_effect6.setBlurRadius(15)
        shadow_effect6.setColor(QColor(145, 90, 87, 127))
        shadow_effect6.setOffset(0, 7)
        self.mode6_button.setGraphicsEffect(shadow_effect6)

        self.window.setStyleSheet(utilis.STYLE_BUTTON)



    def configuration_window(self):
        popup = PopUp()
        if popup.exec_() == QDialog.Accepted:
            self.window.game.opponent = popup.select_option()
            self.window.game.ip, self.window.game.port = popup.get_address()

            self.window.game.status_tcpip = popup.select_type()
            print(self.window.game.status_tcpip)

            if self.window.game.status_tcpip!="" and self.window.game.opponent=='player':
                self.window.connect()


    def load_data(self):
        conn = sqlite3.connect('gameplay.db')
        cursor = conn.cursor()

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()

        if not tables:
            return

        random_table = random.choice(tables)[0]

        cursor.execute(f"SELECT white, black FROM {random_table}")
        data = cursor.fetchall()
        conn.close()

        if data:
            self.window.stream_data = data
            self.is_loaded = True
        else:
            pass


class PopUp(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout()

        self.radio_button1 = QRadioButton("with player")
        self.radio_button2 = QRadioButton("with ai")
        self.radio_button3 = QCheckBox("server")
        layout.addWidget(self.radio_button1)
        layout.addWidget(self.radio_button2)
        layout.addWidget(self.radio_button3)

        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.accept)
        layout.addWidget(self.ok_button)

        self.ip = QTextEdit()
        layout.addWidget(self.ip)

        self.port = QTextEdit()
        layout.addWidget(self.port)
        self.setLayout(layout)

    def select_option(self):
        if self.radio_button1.isChecked():
            return 'player'
        if self.radio_button2.isChecked():
            return 'ai'
        else: return 'player'

    def select_type(self):
        if self.radio_button3.isChecked():
            return 'server'
        else: return 'client'


    def get_address(self):
        ip = self.ip.toPlainText()
        port = self.port.toPlainText()
        self.ip.clear()
        self.port.clear()

        return ip,port


