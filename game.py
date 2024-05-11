import socket
import threading
from queue import Queue
import random

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

