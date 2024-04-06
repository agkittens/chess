import time
from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import QColor, QPainter, QBrush, QPen, QFont, QPainterPath, QRegion, QPixmap, QImage
from PyQt5.QtWidgets import QLabel, QPushButton, QGraphicsView, QGraphicsEllipseItem, QGraphicsDropShadowEffect, \
    QGraphicsPixmapItem, QGraphicsRectItem, QApplication, QTextEdit

import utilis


class Addons:
    def __init__(self, window):
        self.window = window
        self.save = self.window.save
        self.queue = self.window.queue
        self.scene = self.window.scene


    def mode1(self):
        self.window.mode=0
        self.window.max_time = 15
        self.max_time_label.setText(f'Max time : {self.window.max_time} min')

    def mode2(self):
        self.window.mode=1
        self.window.max_time = 5
        self.max_time_label.setText(f'Max time : {self.window.max_time} min')

    def mode3(self):
        self.window.mode=2
        self.window.max_time = 45
        self.max_time_label.setText(f'Max time : {self.window.max_time} min')



    def add_stuff(self):
        self.load_bg()
        self.label = QLabel()
        self.label.setText('Game history')
        self.label.resize(200,200)
        self.label.setStyleSheet(utilis.STYLE_LABEL)
        w = self.scene.addWidget(self.label)
        w.setPos(-500,0)
        self.scene.setBackgroundBrush(QColor(utilis.BG_COLOR))

        self.mode_info()
        self.turn_label()
        self.input_window()
        self.mode_buttons()
        self.circles()
        self.time_labels()


    def mode_info(self):
        self.max_time_label = QLabel()
        self.max_time_label.setText(f'Max time : {self.window.max_time} min')
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
        if self.window.move %2 == 0:
            self.turn.setText("WHITE'S TURN")
        elif self.window.move %2 == 1:
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
            self.label.resize(200, 200)


    def update_time(self):
        end_time = time.time() - self.window.start_time

        if self.window.dragging_item is None: return
        if self.window.dragging_item.data(Qt.UserRole)[-1] == 'w':
            self.window.white_time += end_time

        if self.window.dragging_item.data(Qt.UserRole)[-1] == 'b':
            self.window.black_time += end_time

        w_m = int(self.window.white_time // 60)
        w_s = int(self.window.white_time % 60)
        self.white_time_label.setText('WHITE\n' + f'{w_m}' + ':' + f'{w_s} ')

        b_m = int(self.window.black_time // 60)
        b_s = int(self.window.black_time % 60)
        self.black_time_label.setText('BLACK\n' + f'{b_m}' + ':' + f'{b_s} ')

        self.window.start_time = time.time()