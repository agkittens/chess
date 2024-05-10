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


        self.opponent = 'player'
        self.ip = 'localhost'
        self.port = 8888
        self.stream_data = []
        self.move = 0
        self.save = [""]
        self.game_history = [""]

    # def exec_move(self):
    #     if self.move_index < len(self.stream_data):
    #         moves = self.stream_data[self.move_index]
    #         for move in moves:
    #             if move != '':
    #                 self.input_move(move[:2], move[3:])
    #
    #         self.move_index += 1
    #         QTimer.singleShot(2000,self.exec_move)
    #
    #     else:
    #         self.addons.is_loaded = False


    def input_move(self,pos_s, pos_e):
        x_s,y_s = self.window.find_pos(pos_s)
        x_e,y_e = self.window.find_pos(pos_e)

        if x_s is None and y_s is None: return
        if x_e is None and y_e is None: return

        if not self.window.check_if_empty(x_s,y_s) and self.window.check_if_empty(x_e,y_e):
            key = self.window.figures.figures_board[x_s][y_s]
            if self.move%2==0 and key[-1]!='w': return
            elif self.move%2==1 and key[-1]!='b': return

            x,y = y_s*75+8, x_s*75+8
            self.window.highlight(key,x,y)
            xe,ye = y_e*75+8, x_e*75+8


            if self.window.check_existance(xe,ye) or self.window.check_attack_exist(xe,ye):
                self.window.change_fig_pos(None,x_s,y_s)
                item = self.window.scene.itemAt(x+30,y+30, self.window.transform())

                item.setPos(xe,ye)
                self.window.change_fig_pos(key,x_e,y_e)
                self.move+=1

            self.window.remove_highlights()

        elif not self.window.check_if_empty(x_s,y_s) and not self.window.check_if_empty(x_e,y_e):
            key = self.window.figures.figures_board[x_s][y_s]
            if self.move%2==0 and key[-1]!='w': return
            elif self.move%2==1 and key[-1]!='b': return

            x,y = y_s*75+8, x_s*75+8
            self.window.highlight(key,x,y)
            xe,ye = y_e*75+8, x_e*75+8

            if self.window.check_existance(xe,ye) or self.window.check_attack_exist(xe,ye):

                key_e = self.window.figures.figures_board[x_e][y_e]
                if key_e is None: return
                if key_e[-1]!=key[-1]:

                    item_e = self.window.scene.itemAt(xe + 30, ye + 30, self.window.transform())
                    self.window.scene.removeItem(item_e)

                    self.window.change_fig_pos(None, x_s, y_s)
                    item = self.window.scene.itemAt(x + 30, y + 30, self.window.transform())

                    item.setPos(xe,ye)
                    self.window.change_fig_pos(key,x_e,y_e)
                    self.move+=1

            self.window.remove_highlights()
            
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
                self.input_move(text[:2], text[3:])

                text = text.encode()
                self.client.sendall(text)
                print("s send")


            elif self.status_tcpip == 'client':
                text = self.window.addons.text_edit.toPlainText()
                if text == "": return
                self.window.addons.text_edit.clear()
                self.input_move(text[:2], text[3:])

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

                        self.input_move(data[:2], data[3:])
                        self.client = connection


            elif self.status_tcpip == 'client':
                data = connection.recv(1024).decode()

                if data:
                    self.game_history.append(data)
                    self.queue.put(f"{data}")

                    print(f"\nreceived: ", data)
                    self.input_move(data[:2], data[3:])



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
                    self.input_move(random_x, random_y)
                elif num <=2:
                    self.input_move(random_x, random_y)

