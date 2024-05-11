import json
import socket
import sqlite3
import threading
from queue import Queue
import random

import xml.etree.ElementTree as ET
from datetime import datetime

STOP = False

class Game:
    def __init__(self, window):
        self.window = window
        self.queue = Queue()
        self.queue.put("")
        self.status_tcpip = None
        self.client_connection = None
        self.server_connection = None
        self.client = None
        self.white_time = 0
        self.black_time = 0
        self.start_time = 0
        self.mode = 0
        self.max_time = 15

        self.opponent = 'ai'
        self.ip = 'localhost'
        self.port = 8888
        self.stream_data = []
        self.move = 0
        self.save = [""]
        self.game_history = [""]
        self.last_db = ""



    def connect(self):
        if self.status_tcpip == 'server':
            self.server_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_connection.bind((self.ip, int(self.port)))
            self.server_connection.listen(1)

        elif self.status_tcpip == 'client':
            self.client_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_connection = socket.create_connection((self.ip, int(self.port)))
            self.client_connection.setblocking(False)

    def server_connect(self):
        if self.status_tcpip == 'server':
            try:
                #server oczekuje na polaczenie i sie zawiesza
                connection, client = self.server_connection.accept()
                self.client = connection
                print("connected with", client)
                thread_recv = threading.Thread(target=self.receive_data, args=(connection, client,))
                thread_recv.start()
            except Exception: pass


    def manage_communication(self):
        if self.opponent == 'player':
            if self.status_tcpip == 'client':
                try:
                    self.receive_data(self.client_connection, None)
                except Exception: pass

    def send_data(self):
        if self.opponent == 'player':
            if self.status_tcpip == 'server':
                text = self.window.addons.text_edit.toPlainText()
                if text == "": return
                self.window.addons.text_edit.clear()
                self.window.input_move(text[:2], text[3:])

                text = text.encode()
                self.client.sendall(text)
                print("s send")


            elif self.status_tcpip == 'client':
                text = self.window.addons.text_edit.toPlainText()
                if text == "": return
                self.window.addons.text_edit.clear()
                self.window.input_move(text[:2], text[3:])

                text = text.encode()
                self.client_connection.sendall(text)
                print("c send")


    def receive_data(self, connection, client):
        if self.opponent == 'player':
            if self.status_tcpip == 'server':
                while not STOP:
                    data = connection.recv(1024).decode()
                    if data:
                        print(f"received from {client}: \n", data)
                        self.game_history.append(data)
                        self.queue.put(f"{data}")

                        self.window.input_move(data[:2], data[3:])
                        self.client = connection


            elif self.status_tcpip == 'client':
                data = connection.recv(1024).decode()

                if data:
                    self.game_history.append(data)
                    self.queue.put(f"{data}")

                    print(f"\nreceived: ", data)
                    self.window.input_move(data[:2], data[3:])


    def end_game(self):
        king_w = False
        king_b = False
        for row in self.window.figures.figures_board:
            for piece in row:
                if piece == 'kw':
                    king_w = True
                elif piece == 'kb':
                    king_b = True
        return king_w and king_b

    def ai_move(self):
        if self.opponent!='player':
            while self.move%2==1:
                idx_x = random.randint(0,7)
                idx_y = random.randint(0,7)
                random_x = self.window.figures.pos_board[idx_x][idx_y]
                key_s = self.window.figures.figures_board[idx_x][idx_y]

                idx_x = random.randint(0,7)
                idx_y = random.randint(0,7)
                random_y = self.window.figures.pos_board[idx_x][idx_y]

                key_e = self.window.figures.figures_board[idx_x][idx_y]
                # random_positions = random.sample(self.figures.pos_board, 2)
                num = random.randint(0,10)

                if num < 9 and key_e is not None and key_s is not None and key_e[-1]!=key_s[-1]:
                    self.window.input_move(random_x, random_y)
                elif num <=2:
                    self.window.input_move(random_x, random_y)

    def save_to_json(self):
        data = {
                "opponent": self.opponent,
                "ip": self.ip,
                "port": self.port,
                "mode": self.max_time}

        with open("gameplay_config.json", "w") as file:
            json.dump(data, file)

    def save_to_xml(self):
        with open("gameplay.xml", "w") as xml_file:

            game_element = ET.Element("last game")
            for move in self.game_history[1:]:
                move_element = ET.SubElement(game_element, "move")
                sub_element = ET.SubElement(move_element, move[:2])
                sub_element.text = move[3:]

            xml_file.write(ET.tostring(game_element, encoding="unicode", method="xml"))


    def save_to_sql(self):
        try:
            conn = sqlite3.connect('gameplay.db')
            cursor = conn.cursor()
            date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            table_name = f'gameplay_{date.replace("-", "_").replace(":", "_").replace(" ", "_")}'
            self.last_db = table_name
            create_table_query = f'''
            CREATE TABLE IF NOT EXISTS {table_name} (
                id INTEGER PRIMARY KEY,
                white TEXT,
                black TEXT
            )'''

            cursor.execute(create_table_query)

            for value in self.game_history[1:]:
                if value[1] == 'w':
                    cursor.execute(f"INSERT INTO {table_name} (white, black) VALUES (?,?)", (value[4:],''))
                if value[1] == 'b':
                    cursor.execute(f"INSERT INTO {table_name} (white, black) VALUES (?,?)", ('',value[4:]))
            conn.commit()
            conn.close()

            print("saved")

        except sqlite3.Error as e:
            print('error', e)


