TILE_COLOR_1 = "#f6e7e0"
TILE_COLOR_2 = "#7d9190"
ATTACK_COLOR = "#d27d69"
HIGHLIGHT_COLOR = '#daa293'
FIG_POS_COLOR = '#dfbab0'
BG_COLOR = "#e6e5d3"
CIRCLE_COLOR = "#899893"
BORDER_COLOR = "#365357"

STYLE_BUTTON = """
            QPushButton {
                background-color: #ab726b;
                border: none;
                color: white;
                padding: 10px 24px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 16px;
                margin: 4px 2px;
                transition-duration: 0.4s;
                cursor: pointer;
                border-radius: 12px;
            }
            QPushButton:hover {
                background-color: #8a504e;
                color: white;
            }
        """
STYLE_LABEL = "color: #2f484d;" \
              "border: 2px solid white;" \
              "font-size: 15px;" \
              "border-radius: 10px;" \

STYLE_LABEL2 = "background-color: transparent;" \
              "color: white;" \
              "font-size: 18px;"

STYLE_LABEL3 = "color: white;" \
              "font-size: 16px;" \

#1pkt szachownica, figury
#1pkt klasa figury QGraphicsItem
#2pkt mozliwosc ruchu
#1pkt graficzna zmiana podcas wyboru

#2pkt okienko do wyswietlania logow -> mechanizm musi byc bezpieczny? np ruchy pol
#2pkt weryfikacja ruchu figur, z roszada
#1pkt przemiennosc gry

#1pkt bicia
#1pkt werfikacja konca gry
#2pkt zegar - 1pkt pojawienie, 1pkt tryby
#1pkt notacja szachowa - okienko i sterowanie

#0.5pkt tryb rozgrywki: przeciwnik ai lub gracz radiobuttons
#0.5pkt komunikacja po sieci - miejsce: adres ip, port
#1pkt zapis historii gry w bazie danych
#1pkt zapis w formacie xml
#1pkt zapis opcji w json
#1pkt odczyt i playback historii rozgrywki


#2pkt serwer, klient - jeden serwer drugi klient
#2pkt przesylanie ruchow po tcp/ip komend, weryfikacja poprawnowsci ruchu, koniec gry
#1pkt messenger (serwer,klient)

#2pkt sterowanie pionkami i bicie
#3pkt algorytm min max z cieciem alpha beta, wagi pionow
