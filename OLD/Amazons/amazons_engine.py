import random
import numpy as np
import copy
from collections import deque

class AmazonsGame:
    def __init__(self):
        self.board = [[0]*10 for _ in range(10)]
        self.amazons = {1: [], 2: []}
        self.initialize_amazons()
        self.current_player = 1
        self.prev_move = None

    def initialize_amazons(self):
        # Positioniere die Amazonen anfangs auf den Standardpositionen
        positions = [(0, 3), (0, 6), (3, 0), (3, 9), (6, 0), (6, 9), (9, 3), (9, 6)]
        for i, pos in enumerate(positions):
            player = 1 if i < 4 else 2
            self.board[pos[0]][pos[1]] = player  # Spieler 1 und Spieler 2
            self.amazons[player].append(pos)

    def print_board(self):
        # Gibt das aktuelle Brett mit Achsenbeschriftungen auf der Konsole aus
        print("   " + " ".join(str(i) for i in range(10)))
        print("  +" + "---"*7 + "+")
        for i, row in enumerate(self.board):
            print(f"{i} |" + " ".join(str(x) for x in row) + "|")
        print("  +" + "---"*7 + "+")
    
    def update_amazon_positions(self, start, end):
        """
        Updated das Attribut game.amazons indem die Startposition der jeweiligen zu bewegenden Amazone removed wird und 
        die Endposition als neuer aktueller Standort hinzugefügt wird.

        Parameters
        ----------
        start : int
            the start position of the amazon
        end : int
            the end position of the amazon
            
        Uses
        ----------
        amazons : Dictionary
        - Speichert die aktuellen Positionen der Amazonen vom Spieler 1 und 2

        amazons = {
                1: [(x-Pos,y-Pos),(x,y),(x,y),(x,y)]
                2: [(x-Pos,y-Pos),(x,y),(x,y),(x,y)]
            }
        """
        # Entfernt die alte Position und fügt die neue hinzu
        #print("Player: ",self.current_player)
        #print("Amazons: ",self.amazons)
        #print("Remove: ",start)
        #print("Append: ",end)
        self.amazons[self.current_player].remove((start[0], start[1]))
        self.amazons[self.current_player].append((end[0], end[1]))

    def is_within_bounds(self, x, y):
        """
        Überprüft ob die gegebene Koordinate innerhalb der Bounds ist

        Parameters
        ----------
        x : int
            x-Coordinate of the position
        y : int
            y-Coordinate of the position
        """
        return 0 <= x <= 9 and 0 <= y <= 9

    def is_move_legal(self, start, end, arrow):
        """
        Überprüft ob der gegebene Zug legal ist. 
        Überprüft wird folgendes (der Reihe nach):
        - Ist der Zug innerhalb des Boards?
        - Spieler versucht ein leeres Feld (eine 0) zu bewegen
        - Falscher Spieler versucht einen Zug zu machen
        - Spieler versucht eine Amazone auf ein besetztes Feld zu bewegen
        - Spieler schießt ein Pfeil auf ein besetztes Feld
        - Spieler versucht Amazone oder Pfeil durch andere Amazonen oder Pfeile zu bewegen

        Parameters
        ----------
        start : tupel(int,int)
            Startposition ein Tupel bestehend aus x und y Koordinate (x,y)
        end : tupel(int,int)
            Endposition ein Tupel bestehend aus x und y Koordinate (x,y)
        arrow : tupel(int,int)
            Pfeilposition ein Tupel bestehend aus x und y Koordinate (x,y)
            
        Returns
        ----------
        True: wenn der Zug legal ist nach den geprüften Kriterien
        False: wenn nicht
        """
        # Überprüft, ob der Zug legal ist (Amazonenbewegung + Pfeilwurf)
        if not all([self.is_within_bounds(x, y) for x, y in [(start[0], start[1]), (end[0], end[1]), (arrow[0], arrow[1])]]):
            print("Out of bounds - Move: ",start, end, arrow)
            raise Exception(".")
            return False
        if self.board[start[0]][start[1]] == 0:
            print(f"Player {self.current_player} wants to move an empty field 0 - Move: ",start, end, arrow)
            self.print_board()
            print("amazons: ",self.amazons)
            raise Exception(".")
            return False
        if self.board[start[0]][start[1]] != self.current_player:
            print("Wrong turnplayer")
            raise Exception(".")
            return False
        if self.board[end[0]][end[1]] != 0:
            print("Player wants to move to an occupied field:", self.board[end[0]][end[1]]," - Move: ",start, end, arrow)
            raise Exception(".")
            return False
        
        self.board[start[0]][start[1]] = 0
        self.board[end[0]][end[1]] = self.current_player
        if self.board[arrow[0]][arrow[1]] != 0:
            if start != arrow or end == arrow: # Wenn der Pfeil auf die eigene Anfangsposition geschossen werden soll ist das erlaubt
                print("Shooting arrow on occupied field", self.board[arrow[0]][arrow[1]]," - Move: ",start, end, arrow)
                self.board[start[0]][start[1]] = self.current_player
                self.board[end[0]][end[1]] = 0
                raise Exception(".")
                return False
        self.board[start[0]][start[1]] = self.current_player
        self.board[end[0]][end[1]] = 0
        
        # Zug wird provisorisch durchgeführt damit er sich nicht selber im Weg stehen kann, was nicht möglich ist
        self.board[start[0]][start[1]] = 0
        self.board[end[0]][end[1]] = self.current_player
        if not self.is_path_clear(start[0], start[1], end[0], end[1]) or not self.is_path_clear(end[0], end[1], arrow[0], arrow[1]):
            print("Path is not clear", (start[0], start[1]), (end[0], end[1]) , " oder ", (end[0], end[1]), (arrow[0], arrow[1]))
            self.board[start[0]][start[1]] = self.current_player
            self.board[end[0]][end[1]] = 0
            raise Exception(".")
            return False
        
        return True

    def is_path_clear(self, x1, y1, x2, y2):
        """
        Überprüft ob der gegebene Pfad zwischen zwei Punkten leer ist bzw ob etwas im Weg ist.

        Parameters
        ----------
        x1 : int
            x-Koordinate des 1. Punktes
        y1 : tupel(int,int)
            y-Koordinate des 1. Punktes
        x2 : tupel(int,int)
            x-Koordinate des 2. Punktes
        y2 : tupel(int,int)
            x-Koordinate des 2. Punktes
            
        Returns
        ----------
        True: wenn der Pfad zwischen den 2 Punkten leer ist
        False: wenn nicht
        """
        # Prüft, ob der Pfad zwischen zwei Punkten frei ist
        step_x = 0 if x1 == x2 else 1 if x2 > x1 else -1
        step_y = 0 if y1 == y2 else 1 if y2 > y1 else -1
        x, y = x1 + step_x, y1 + step_y
        while (x, y) != (x2, y2):
            if self.board[x][y] != 0:
                return False
            x += step_x
            y += step_y
        return True

    def make_move(self, start, end, arrow):
        """
        Macht den übergebenen Zug überprüft aber vorher ob der Zug legal ist und wenn ja wird das Board geupdated und die Amazonenposition auch geupdated in Amazons

        Parameters
        ----------
        start : tupel(int,int)
            Startposition ein Tupel bestehend aus x und y Koordinate (x,y)
        end : tupel(int,int)
            Endposition ein Tupel bestehend aus x und y Koordinate (x,y)
        arrow : tupel(int,int)
            Pfeilposition ein Tupel bestehend aus x und y Koordinate (x,y)
        
        Returns
        ----------
        True: wenn der Zug erfolgreich durchgeführt wurde
        False: wenn nicht
        """

        #print("Current Player that makes the move: ",self.current_player)
        # Führt einen legalen Zug aus
        if self.is_move_legal(start, end, arrow):
            self.board[start[0]][start[1]] = 0
            self.board[end[0]][end[1]] = self.current_player
            self.board[arrow[0]][arrow[1]] = "X"  # 3 repräsentiert einen Pfeil
            self.update_amazon_positions(start, end)
            #self.current_player = 3 - self.current_player  # Wechsel der Spieler
            #print("THE MOVE: Start:",start,"Ende:",end,"Pfeil:",arrow)
            return True
        return False

    def undo_move(self, start, end, arrow):
        """
        Macht den übergebenen Zug wieder rückgängig sowohl auf dem Board als auch die Amazonen inder amazons Liste werden geupdated

        Parameters
        ----------
        start : tupel(int,int)
            Startposition ein Tupel bestehend aus x und y Koordinate (x,y)
        end : tupel(int,int)
            Endposition ein Tupel bestehend aus x und y Koordinate (x,y)
        arrow : tupel(int,int)
            Pfeilposition ein Tupel bestehend aus x und y Koordinate (x,y)

        """

        # Macht den vorherigen Zug rückgängig
        #print("player: ",self.current_player)
        #print("undo the move",start, " to ", end)
        #self.current_player = 3 - self.current_player # Spieler wird zurückgewechselt
        if self.board[end[0]][end[1]] != self.current_player:
            self.current_player = self.board[end[0]][end[1]]
        self.board[arrow[0]][arrow[1]] = 0
        self.board[start[0]][start[1]] = self.current_player
        self.board[end[0]][end[1]] = 0
        self.update_amazon_positions(end, start)

    def current_player_has_legal_moves(self):
        """
        Überprüft ob der aktuelle Spieler noch legale Züge hat und gibt
        eine Liste mit allen legalen Zügen aus.

        Returns
        ----------
        Eine Liste legalMoves mit allen möglichen und legallen Zügen für den aktuellen Spieler
        Liste: [ (zug1) , (zug2) , (zug3) ]
        Zug: (start_pos), (end_pos), (arrow_pos)
        """

        legalMoves = []
        for amazon in self.amazons[self.current_player]:
            moves = self.calculate_moves_for_amazon(amazon[0], amazon[1])
            if moves:
                # moves: ( ((sx, sy), (tx, ty), (ax, ay)) , ((sx, sy), (tx, ty), (ax, ay)) , ... )
                legalMoves.extend(moves)
        #print("legalMoves: ",legalMoves)
        return legalMoves
    
    def calculate_moves_for_amazon(self, x, y):
        """
        Berechnet alle möglichen und legalen Züge für eine Amazone der Position (x, y). 

        Parameters
        ----------
        x : int
            x-Coordinate von der Amazone
        y : int
            y - Coordinate von der Amazone

        Returns
        ----------
        Eine Liste moves mit allen möglichen und legallen Zügen für die übergebene Amazone
        Liste: ( ((start_pos) , (end_pos) , (arrow_pos)) , ((start_pos) , (end_pos) , (arrow_pos)) , ... )
        """
        moves = []
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            while self.is_within_bounds(nx, ny) and self.board[nx][ny] == 0:
                # Move wird provisorisch durchgeführt
                self.board[x][y] = 0
                self.board[nx][ny] = self.current_player
                # Überprüfe alle möglichen Orte, um einen Pfeil zu schießen
                for adx, ady in directions:
                    ax, ay = nx + adx, ny + ady
                    while self.is_within_bounds(ax, ay) and self.board[ax][ay] == 0:
                        if self.is_path_clear(nx, ny, ax, ay):
                            # Move wird provisorisch durchgeführt
                            self.board[x][y] = self.current_player
                            self.board[nx][ny] = 0
                            if self.is_move_legal((x, y), (nx, ny), (ax, ay)):
                                moves.append(((x, y), (nx, ny), (ax, ay)))
                        ax += adx
                        ay += ady
                # Move rückgängig machen
                self.board[x][y] = self.current_player
                self.board[nx][ny] = 0
                nx += dx
                ny += dy
        return moves
    
    ########### ADDED FOR MCTS ###########

    def deepcopy(self):
        new_game = AmazonsGame()
        new_game.board = copy.deepcopy(self.board)
        new_game.amazons = {1: copy.deepcopy(self.amazons[1]), 2: copy.deepcopy(self.amazons[2])}
        new_game.current_player = self.current_player
        new_game.prev_move = copy.deepcopy(self.prev_move)
        return new_game

    def copy(self):
        new_game = AmazonsGame()
        new_game.board = [row[:] for row in self.board]
        new_game.amazons = {player: positions[:] for player, positions in self.amazons.items()}
        new_game.current_player = self.current_player
        new_game.prev_move = self.prev_move
        return new_game
    
    def is_terminal(self):
        return not self.current_player_has_legal_moves()
    
    def is_game_over(self):
        return not self.current_player_has_legal_moves()
    
    def get_result(self):
        if self.is_terminal():
            if self.current_player_has_legal_moves():
                return 1 if self.current_player == 1 else -1
            else:
                return -1 if self.current_player == 1 else 1
        return 0
        
    def game_result(self):
        score = self.evaluate_position()

        # Annahme: Positive Werte bedeuten Vorteil für den aktuellen Spieler,
        # negative Werte bedeuten Vorteil für den Gegner
        if score > 0:
            return 1  # Sieg für Spieler 1
        elif score < 0:
            return -1  # Niederlage für Spieler 2
        else:
            return 0  # Unentschieden oder unklare Situation

    ########################################################################
    ############################ MOVE ORDERING #############################
    
    def move_blocks_opponent(self, move):
        #print("move_blocks_opponent")
        """
        Überprüft, wie viele gegnerische Amazonen, durch die Amazone selbst blockiert werden (horizontal, vertikal, diagonal)
        - (0,1,2,>=3)

        Parameters
        ----------
        move : tupel
            ((start_position), (end_position), (arrow_position))

        Returns
        ----------
        0: wenn die Amazone *KEINE* gegnerische Amazone blockiert
        1: wenn die Amazone *EINE* gegnerische Amazone blockiert
        2: wenn die Amazone *ZWEI* gegnerische Amazonen blockiert
        >=3: wenn die Amazone mind. *DREI* gegnerische Amazonen blockiert
        """

        # move ist ein Tupel (start_position, end_position, arrow_position)
        _, end_position, arrow_position = move
        ex, ey = end_position
        ax, ay = arrow_position
        opponent = 3 - self.current_player  # Nimmt an, dass es nur Spieler 1 und 2 gibt
        
        # Richtungen: Horizontal, Vertikal, Diagonal
        directions = [
            (1, 0),  # Rechts
            (-1, 0), # Links
            (0, 1),  # Unten
            (0, -1), # Oben
            (1, 1),  # Rechts unten
            (-1, -1),# Links oben
            (1, -1), # Rechts oben
            (-1, 1)  # Links unten
        ]

        self.board[ax][ay] = "X"

        blocked_opponents = 0

        # Überprüfe jede Richtung auf gegnerische Amazonen
        for dx, dy in directions:
            nx, ny = ex + dx, ey + dy
            while 0 <= nx < len(self.board) and 0 <= ny < len(self.board[0]) and self.board[nx][ny] == 0:
                nx += dx
                ny += dy
            # Überprüfe, ob am Ende eine gegnerische Amazone steht
            if 0 <= nx < len(self.board) and 0 <= ny < len(self.board[0]) and self.board[nx][ny] == opponent:
                if AmazonsGame.is_path_clear(self, ex, ey, nx, ny):
                    blocked_opponents += 1

        self.board[ax][ay] = 0
        return blocked_opponents
    
    def arrow_blocks_opponent(self, move):
        #print("arrow_blocks_opponent")
        """
        Überprüft, wie viele gegnerische Amazonen, durch den Pfeil blockiert werden (horizontal, vertikal, diagonal)
        - (0,1,2,>=3)

        Parameters
        ----------
        move : tupel
            ((start_position), (end_position), (arrow_position))

        Returns
        ----------
        0: wenn der Pfeil *KEINE* gegnerische Amazone blockiert
        1: wenn der Pfeil *EINE* gegnerische Amazone blockiert
        2: wenn der Pfeil *ZWEI* gegnerische Amazonen blockiert
        >=3: wenn der Pfeil mind. *DREI* gegnerische Amazonen blockiert
        """

        # move ist ein Tupel (start_position, end_position, arrow_position)
        _, end_position, arrow_position = move
        ax, ay = arrow_position
        ex, ey = end_position
        opponent = 3 - self.current_player  # Nimmt an, dass es nur Spieler 1 und 2 gibt
        
        # Richtungen: Horizontal, Vertikal, Diagonal
        directions = [
            (1, 0),  # Rechts
            (-1, 0), # Links
            (0, 1),  # Unten
            (0, -1), # Oben
            (1, 1),  # Rechts unten
            (-1, -1),# Links oben
            (1, -1), # Rechts oben
            (-1, 1)  # Links unten
        ]

        self.board[ex][ey] = self.current_player

        blocked_opponents = 0

        # Überprüfe jede Richtung auf gegnerische Amazonen
        for dx, dy in directions:
            nx, ny = ax + dx, ay + dy
            while 0 <= nx < len(self.board) and 0 <= ny < len(self.board[0]) and self.board[nx][ny] == 0:
                nx += dx
                ny += dy
            # Überprüfe, ob am Ende eine gegnerische Amazone steht
            if 0 <= nx < len(self.board) and 0 <= ny < len(self.board[0]) and self.board[nx][ny] == opponent:
                if AmazonsGame.is_path_clear(self, ax, ay, nx, ny):
                    blocked_opponents += 1

        self.board[ex][ey] = 0
        return blocked_opponents
    
    def move_adjacent_to_opponent(self, move):
        #print("move_adjacent_to_opponent")
        """
        Überprüft, ob bei dem Zug die zu bewegende Amazone auf ein benachbartes Feld einer gegnerischen Amazone bewegt wird

        Parameters
        ----------
        move : tupel
            ((start_position), (end_position), (arrow_position))

        Returns
        ----------
        True: wenn die Amazone auf *EIN* benachbartes Feld einer gegnerischen Amazone bewegt wird
        False: wenn die Amazone auf *KEIN* benachbartes Feld einer gegnerischen Amazone bewegt wird
        """

        # move ist ein Tupel (start_position, end_position, arrow_position)
        _, end_position, _ = move
        ex, ey = end_position
        opponent = 3 - self.current_player  # Gegenspieler identifizieren

        # Überprüfe alle angrenzenden Felder
        adjacent_positions = [
            (ex + 1, ey), 
            (ex - 1, ey), 
            (ex, ey + 1), 
            (ex, ey - 1),
            (ex + 1, ey + 1), 
            (ex - 1, ey - 1), 
            (ex + 1, ey - 1), 
            (ex - 1, ey + 1)
        ]
        for nx, ny in adjacent_positions:
            if 0 <= nx < len(self.board) and 0 <= ny < len(self.board[0]):
                if self.board[nx][ny] == opponent:
                    return True
        return False
    
    def arrow_adj_to_opponent(self, move):
        #print("arrow_adj_to_opponent")
        """
        Überprüft, ob bei dem Zug der zu verschießende Pfeil auf ein benachbartes Feld einer gegnerischen Amazone geschossen wird

        Parameters
        ----------
        move : tupel
            ((start_position), (end_position), (arrow_position))

        Returns
        ----------
        True: wenn der Pfeil auf *EIN* benachbartes Feld einer gegnerischen Amazone geschossen wird
        False: wenn der Pfeil auf *KEIN* benachbartes Feld einer gegnerischen Amazone geschossen wird
        """

        # move ist ein Tupel (start_position, end_position, arrow_position)
        _, _, arrow_position = move
        ax, ay = arrow_position
        opponent = 3 - self.current_player  # Gegenspieler identifizieren

        # Überprüfe alle angrenzenden Felder um die Pfeilposition
        adjacent_positions = [
            (ax + 1, ay), 
            (ax - 1, ay), 
            (ax, ay + 1), 
            (ax, ay - 1),
            (ax + 1, ay + 1), 
            (ax - 1, ay - 1), 
            (ax + 1, ay - 1), 
            (ax - 1, ay + 1)
        ]
        for nx, ny in adjacent_positions:
            if 0 <= nx < len(self.board) and 0 <= ny < len(self.board[0]):
                if self.board[nx][ny] == opponent:
                    return True
        return False
    
    def blocking_amazon_multiple_ways(self, move):
        #print("blocking_amazon_multiple_ways")
        """
        Überprüft, ob der Zug mithilfe der Amazone selbst und dem Pfeil die ein und dieselbe gegnerische Amazone blockiert

        Parameters
        ----------
        move : tupel
            ((start_position), (end_position), (arrow_position))

        Returns
        ----------
        True: wenn der Zug mit der Amazone selbst und dem Pfeil dieselbe Amazone blockieren
        False: wenn der Zug mit der Amazone selbst und dem Pfeil *NICHT* dieselbe Amazone blockieren
        """

        # move ist ein Tupel (start_position, end_position, arrow_position)
        start_position, end_position, arrow_position = move
        sx, sy = start_position
        ex, ey = end_position
        ax, ay = arrow_position
        opponent = 3 - self.current_player

        # Richtungen für die Überprüfung der Bewegungsfreiheit
        directions = [
            (1, 0),  # Rechts
            (-1, 0), # Links
            (0, 1),  # Oben
            (0, -1), # Unten
            (1, 1),  # Diagonal rechts oben
            (-1, -1),# Diagonal links unten
            (1, -1), # Diagonal rechts unten
            (-1, 1)  # Diagonal links oben
        ]

        # Funktion, die überprüft, ob eine bestimmte Position eine gegnerische Amazone blockiert
        def blocks_opponent(position):
            for dx, dy in directions:
                nx, ny = position[0] + dx, position[1] + dy
                while 0 <= nx < len(self.board) and 0 <= ny < len(self.board[0]) and self.board[nx][ny] == 0:
                    nx += dx
                    ny += dy
                if 0 <= nx < len(self.board) and 0 <= ny < len(self.board[0]) and self.board[nx][ny] == opponent:
                    if AmazonsGame.is_path_clear(self, position[0], position[1], nx, ny):
                        return True
            return False
        
        self.board[sx][sy] = 0
        self.board[ex][ey] = self.current_player
        self.board[ax][ay] = "X"

        # Überprüfe, ob sowohl die Endposition der Amazone als auch die Pfeilposition die gleiche gegnerische Amazone blockieren
        if blocks_opponent(end_position) and blocks_opponent(arrow_position):
            self.board[sx][sy] = self.current_player
            self.board[ex][ey] = 0
            self.board[ax][ay] = 0
            return True

        self.board[sx][sy] = self.current_player
        self.board[ex][ey] = 0
        self.board[ax][ay] = 0
        return False
    
    def move_prev_blocked_amazon(self, move):
        #print("move_prev_blocked_amazon")
        """
        Überprüft, ob bei der aktuellen Amazone, im vorherigen Zug vom Gegner die Dame oder der verschossene Pfeil die aktuelle Amazone blockiert 
        (Pfeil und/oder Amazone selbst oder weder noch - 0,1,2)

        Parameters
        ----------
        move : tupel
            ((start_position), (end_position), (arrow_position))

        Returns
        ----------
        0: wenn die aktuelle Amazone, vom Gegner durch den Zug davor, *NICHT* blockiert wird
        1: wenn die aktuelle Amazone ,vom Gegner durch den Zug davor, blockiert wird (entweder durch Pfeil oder Amazone)
        2: wenn die aktuelle Amazone ,vom Gegner durch den Zug davor, blockiert wird (durch Pfeil und Amazone selbst)
        """

        if self.prev_move == None:
            return 0

        # Entpacke den aktuellen und vorherigen Zug
        start_position, _, _ = move
        _, prev_end_position, prev_arrow_position = self.prev_move
        
        directions = [
            (1, 0),  # Horizontal rechts
            (-1, 0), # Horizontal links
            (0, 1),  # Vertikal oben
            (0, -1), # Vertikal unten
            (1, 1),  # Diagonal rechts oben
            (-1, -1),# Diagonal links unten
            (1, -1), # Diagonal rechts unten
            (-1, 1)  # Diagonal links oben
        ]
        
        def check_blockade_from(position):
            # Überprüfe, ob von dieser Position eine Blockade in irgendeiner Richtung besteht
            for dx, dy in directions:
                nx, ny = start_position[0] + dx, start_position[1] + dy
                while 0 <= nx < len(self.board) and 0 <= ny < len(self.board[0]):
                    if (nx, ny) == position:
                        return True
                    if self.board[nx][ny] != 0:  # Ein Hindernis auf dem Weg
                        break
                    nx += dx
                    ny += dy
            return False

        # Zähle, wie oft die aktuell zu bewegende Amazone durch die vorige Bewegung oder den Pfeil blockiert wird
        blockade_count = 0
        if check_blockade_from(prev_end_position):
            blockade_count += 1
        if check_blockade_from(prev_arrow_position):
            blockade_count += 1

        return blockade_count
    
    def move_amazon_to_which_enemy_amazon_moved_adj(self, move):
        #print("move_amazon_to_which_enemy_amazon_moved_adj")
        """
        Überprüft, ob bei der aktuellen Amazone, im vorherigen Zug vom Gegner die Dame auf ein benachbartes Feld bewegt wurde

        Parameters
        ----------
        move : tupel
            ((start_position), (end_position), (arrow_position))

        Returns
        ----------
        True: wenn die Amazone im letzten Zug vom Gegner auf ein benachbartes Feld dieser Amazone bewegt wurde
        False: wenn die Amazone *NICHT* im letzten Zug vom Gegner auf ein benachbartes Feld dieser Amazone bewegt wurde
        """

        if self.prev_move == None:
            return False

        # Der aktuelle Zug beinhaltet die Startposition der Amazone, die bewegt wird
        start_position, _, _ = move
        # Der vorherige Zug beinhaltet die Endposition der gegnerischen Amazone
        _, prev_end_position, _ = self.prev_move
        
        # Berechne die Differenz in den Koordinaten
        diff_x = abs(start_position[0] - prev_end_position[0])
        diff_y = abs(start_position[1] - prev_end_position[1])
        
        # Überprüfe, ob die Positionen benachbart sind
        if (diff_x <= 1 and diff_y <= 1) and (start_position != prev_end_position):
            return True
        return False
    
    def move_amazon_to_which_enemy_arrow_moved_adj(self, move):
        #print("move_amazon_to_which_enemy_arrow_moved_adj")
        """
        Überprüft, ob bei der aktuellen Amazone, im vorherigen Zug vom Gegner ein Pfeil auf ein benachbartes Feld geschossen wurde

        Parameters
        ----------
        move : tupel
            ((start_position), (end_position), (arrow_position))

        Returns
        ----------
        True: wenn *EIN* Pfeil im letzten Zug vom Gegner auf ein benachbartes Feld dieser Amazone geschossen wurde
        False: wenn *KEIN* Pfeil im letzten Zug vom Gegner auf ein benachbartes Feld dieser Amazone geschossen wurde
        """

        if self.prev_move == None:
            return False

        # Der aktuelle Zug beinhaltet die Startposition der Amazone, die bewegt wird
        start_position, _, _ = move
        # Der vorherige Zug beinhaltet die Endposition des gegnerischen Pfeils
        _, _, prev_arrow_position = self.prev_move
        
        # Berechne die Differenz in den Koordinaten
        diff_x = abs(start_position[0] - prev_arrow_position[0])
        diff_y = abs(start_position[1] - prev_arrow_position[1])
        
        # Überprüfe, ob die Positionen benachbart sind
        if (diff_x <= 1 and diff_y <= 1) and (start_position != prev_arrow_position):
            return True
        return False
    
    def block_amazon_from_prev_move(self, move):
        #print("block_amazon_from_prev_move")
        """
        Überprüft ob der aktuelle Zug der Amazone, die vom Gegner zuletzt bewegte Amazone blockiert (durch Pfeil oder Amazone selbst)

        Parameters
        ----------
        move : tupel
            ((start_position), (end_position), (arrow_position))

        Returns
        ----------
        True: wenn die gegnerische Dame vom Zug davor blockiert wird
        False: wenn die gegnerische Dame *NICHT* vom Zug davor blockiert wird
        """

        if self.prev_move == None:
            return False

        # Endposition der Amazone und Pfeilposition aus dem aktuellen Zug
        _, end_position, arrow_position = move
        # Endposition der Amazone aus dem vorherigen Zug
        _, prev_end_position, _ = self.prev_move
        
        directions = [
            (1, 0),  # Horizontal rechts
            (-1, 0), # Horizontal links
            (0, 1),  # Vertikal oben
            (0, -1), # Vertikal unten
            (1, 1),  # Diagonal rechts oben
            (-1, -1),# Diagonal links unten
            (1, -1), # Diagonal rechts unten
            (-1, 1)  # Diagonal links oben
        ]
        
        def is_blocking_path(position):
            # Überprüft, ob die Position die gegnerische Amazone in einer Linie blockiert
            for dx, dy in directions:
                nx, ny = prev_end_position[0] + dx, prev_end_position[1] + dy
                while 0 <= nx < len(self.board) and 0 <= ny < len(self.board[0]):
                    if (nx, ny) == position:  # Position blockiert die Linie
                        return True
                    if self.board[nx][ny] != 0:  # Ein Hindernis unterbricht die Linie
                        break
                    nx += dx
                    ny += dy
            return False

        # Überprüfe, ob die aktuelle Amazone oder der Pfeil die gegnerische Amazone blockiert
        if is_blocking_path(end_position) or is_blocking_path(arrow_position):
            return True
        
        return False
    
    def move_not_blocking_any_opponent(self, move):
        #print("move_not_blocking_any_opponent")
        """
        Überprüft ob die aktuelle Amazone durch einen Gegner blockiert wird oder nicht

        Parameters
        ----------
        move : tupel
            ((start_position), (end_position), (arrow_position))

        Returns
        ----------
        True: wenn *KEINE* gegnerische Amazone blockiert
        False: wenn *EINE* gegnerische Amazone blockiert
        """
        # Startposition der aktuellen Amazone aus dem move extrahieren
        start_position, _, _ = move
        sx, sy = start_position
        
        directions = [
            (1, 0),  # Horizontal rechts
            (-1, 0), # Horizontal links
            (0, 1),  # Vertikal oben
            (0, -1), # Vertikal unten
            (1, 1),  # Diagonal rechts oben
            (-1, -1),# Diagonal links unten
            (1, -1), # Diagonal rechts unten
            (-1, 1)  # Diagonal links oben
        ]
        
        def is_blocked_by_opponent(position, direction):
            # Überprüft in der gegebenen Richtung auf gegnerische Amazonen
            nx, ny = position[0] + direction[0], position[1] + direction[1]
            while 0 <= nx < len(self.board) and 0 <= ny < len(self.board[0]):
                if self.board[nx][ny] != 0:
                    if self.board[nx][ny] == 3 - self.current_player:  # Gegnerische Amazone gefunden
                        return True
                    else:
                        break  # Ein Hindernis, das die Sicht blockiert
                nx += direction[0]
                ny += direction[1]
            return False

        # Überprüfe alle Richtungen, um zu sehen, ob die Amazone blockiert wird
        for direction in directions:
            if is_blocked_by_opponent((sx, sy), direction):
                return False  # Die Amazone wird von einer gegnerischen Amazone blockiert

        return True  # Keine Blockierung durch eine gegnerische Amazone gefunden
    
    def categorize_move(self, move):
        """
        Kategorisiert den übergebenen Zug

        Parameters
        ----------
        move : tupel
            ((start_position), (end_position), (arrow_position))

        Returns
        ----------
        Ein Dictionary mit den Keys: 1-10 und der jeweiligen Value: die jeweiligen Werte der überprüften Kategorien
        
        categories = {
            1: 2
            2: True
            3: False
            ...
            10: 0
        }
        """
        categories = {
            1: self.move_blocks_opponent(move),
            2: self.arrow_blocks_opponent(move),
            3: self.move_adjacent_to_opponent(move),
            4: self.arrow_adj_to_opponent(move),
            5: self.blocking_amazon_multiple_ways(move),
            6: self.move_prev_blocked_amazon(move),
            7: self.move_amazon_to_which_enemy_amazon_moved_adj(move),
            8: self.move_amazon_to_which_enemy_arrow_moved_adj(move),
            9: self.block_amazon_from_prev_move(move),
            10: self.move_not_blocking_any_opponent(move)
        }
        return categories
    
    def evaluate_move(self, move):
        """
        Bewertet den übergebenen Move anhand von 10 Kategorien und errechnet so einen Score

        Parameters
        ----------
        move : tupel
            ((start_position), (end_position), (arrow_position))

        Returns
        ----------
        Score den der übergeben Zug anhand der Kategorien erzielt hat
        """
        # Bewerten Sie den Zug basierend auf den zugeordneten Kategorien
        categories = self.categorize_move(move)
        score = 0
        for category in categories:
            if category == 1: # move_blocks_opponent
                if categories[category] == 0:
                    score += 33.1
                elif categories[category] == 1:
                    score += 56.9
                elif categories[category] == 2:
                    score += 13.1
                elif categories[category] >= 3:
                    score += 6.6
            if category == 2: # arrow_blocks_opponent
                if categories[category] == 0:
                    score += 14.9
                elif categories[category] == 1:
                    score += 71.4
                elif categories[category] == 2:
                    score += 17.2
                elif categories[category] >= 3:
                    score += 5.3
            if category == 3: # move_adjacent_to_opponent
                if categories[category] == True:
                    score += 52.3
            if category == 4: # arrow_adj_to_opponent
                if categories[category] == True:
                    score += 72.3
            if category == 5: # blocking_amazon_multiple_ways
                if categories[category] == True:
                    score += 36.2
            if category == 6: # move_prev_blocked_amazon
                if categories[category] == 0:
                    score += 56.0 # ???
                elif categories[category] == 1:
                    score += 49.0
                elif categories[category] == 2:
                    score += 33.9
            if category == 7: # move_amazon_to_which_enemy_amazon_moved_adj
                if categories[category] == True:
                    score += 32.8 
            if category == 8: # move_amazon_to_which_enemy_arrow_moved_adj
                if categories[category] == True:
                    score += 34.5
            if category == 9: # block_amazon_from_prev_move
                if categories[category] == True:
                    score += 50.6
            if category == 10: # move_not_blocking_any_opponent
                if categories[category] == True:
                    score += 45.6
            
        return score

    def get_sorted_moves(self, player):
        """
        Sortiert die von dem übergebenen Spieler aktuellen möglichen Züge nach bestimmten Kriterien von asc -> desc

        Parameters
        ----------
        player : int
            1 für Spieler 1 | 2 für Spieler 2

        Returns
        ----------
        sortierte Liste von den Zügen
        """
        moves = []
        for amazon in self.amazons[player]:
            moves.extend(self.calculate_moves_for_amazon(amazon[0], amazon[1]))
        
        # Bewerten und sortieren der Züge
        moves = [(move, self.evaluate_move(move)) for move in moves]
        moves.sort(key=lambda x: x[1], reverse=True)  # Sortieren nach Bewertung, höchste zuerst
        return [move for move, score in moves]
    
    def random_play(self):
        movesCount = 0
        while self.current_player_has_legal_moves():
            possible_moves_for_current_player = self.current_player_has_legal_moves()

            if possible_moves_for_current_player:
                possible_Moves_for_Amazon = random.choice(possible_moves_for_current_player)
                self.make_move(*random.choice(possible_Moves_for_Amazon))
                movesCount += 1
                self.print_board()
                print("---------------------------------------------------------------------")
            else:
                break
        print(f"Spieler {self.current_player} hat keine legalen Züge mehr.")
        print("Game over")
        print("Anzahl gespielter Züge: ",movesCount)

    def random_Move(self):
        possible_moves_for_current_player = self.current_player_has_legal_moves()
        possible_Moves_for_Amazon = random.choice(possible_moves_for_current_player)
        self.make_move(*random.choice(possible_Moves_for_Amazon))
    
    def test_WrongMoves(self):
        # Beispielzug: Spieler 1 bewegt von (3, 0) zu (5, 2) und schießt Pfeil nach (7, 4)
        if self.make_move(start=(3, 0), end=(5, 2), arrow=(7, 4)):
            self.print_board()
        if self.make_move(start=(6, 0), end=(9, 0), arrow=(9, 1)):
            self.print_board()
        # Out of bounds
        if self.make_move(start=(5, 2), end=(10, 2), arrow=(8, 2)):
            self.print_board()
        # Wrong player
        if self.make_move(start=(9, 0), end=(8, 0), arrow=(8, 2)):
            self.print_board()
        # Path not clear
        if self.make_move(start=(3, 9), end=(7, 9), arrow=(9, 9)):
            self.print_board()
        # Moving an empty field
        if self.make_move(start=(0, 0), end=(0, 1), arrow=(0, 0)):
            self.print_board()
        # Player wants to move to an occupied field
        if self.make_move(start=(0, 3), end=(0, 6), arrow=(0, 0)):
            self.print_board()
        # Shooting arrow on occupied field
        if self.make_move(start=(0, 3), end=(0, 4), arrow=(0, 6)):
            self.print_board()

    def missing_1_or_2(self):
        # Initialisieren der Zähler
        count_1 = 0
        count_2 = 0

        # Durchlaufen des Objekts und Zählen der 1 und 2
        for row in self.board:
            count_1 += row.count(1)
            count_2 += row.count(2)

        if count_1 < 4 or count_2 < 4:
            print(count_1)
            print(count_2)
            return True
        return False

    def find_positions(self):
        positions = {1: [], 2: []}  # Initialisiert ein Dictionary für die Positionen von 1 und 2
        
        # Durchläuft jede Zeile und jede Spalte des Bretts
        for row_index, row in enumerate(self.board):
            for col_index, value in enumerate(row):
                if value == 1 or value == 2:
                    # Fügt die Koordinaten der Werte 1 und 2 ihren entsprechenden Listen hinzu
                    positions[value].append((row_index, col_index))
        
        return positions
    
    ########################################################################
    ######################### EVALUATION FUNCTION ##########################

    def calculate_distances(self, player):
        """
        Berechnet die minimalen Distanzen von jeder Zelle auf dem Brett zu den Amazonen eines Spielers.

        Parameters
        ----------
        player : int
            Der Spieler (1 oder 2), für den die Distanzen berechnet werden.

        Returns
        ----------
        D1 : np.ndarray
            Eine 10x10-Matrix mit den minimalen Königinnen-Distanzen zu den Amazonen des Spielers.
        D2 : np.ndarray
            Eine 10x10-Matrix mit den minimalen Königsdistanzen zu den Amazonen des Spielers.
        """

        D1 = np.full((10, 10), np.inf)
        D2 = np.full((10, 10), np.inf)
        
        for amazon in self.amazons[player]:
            self.update_distances(amazon, D1, D2)
        
        return D1, D2

    def update_distances(self, amazon, D1, D2):
        """
        Berechnet die minimalen Distanzen von jeder Zelle auf dem Brett zu den Amazonen eines Spielers.

        Parameters
        ----------
        player : int
            Der Spieler (1 oder 2), für den die Distanzen berechnet werden.

        Returns
        ----------
        D1 : np.ndarray
            Eine 10x10-Matrix mit den minimalen Königinnen-Distanzen zu den Amazonen des Spielers.
        D2 : np.ndarray
            Eine 10x10-Matrix mit den minimalen Königsdistanzen zu den Amazonen des Spielers.
        """

        queue = [amazon]
        D1[amazon] = 0
        D2[amazon] = 0
        
        while queue:
            x, y = queue.pop(0)
            for dx, dy in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
                nx, ny = x + dx, y + dy
                if self.is_within_bounds(nx, ny):
                    if self.board[nx][ny] == 0:
                        if D2[nx, ny] > D2[x, y] + 1:
                            D2[nx, ny] = D2[x, y] + 1
                            queue.append((nx, ny))
                    if abs(dx) + abs(dy) <= 1:
                        if D1[nx, ny] > D1[x, y] + 1:
                            D1[nx, ny] = D1[x, y] + 1
                            queue.append((nx, ny))

    def territorial_evaluation(self, D1, D2):
        """
        Bewertet die territoriale Kontrolle basierend auf den minimalen Königinnen-Distanzen.

        Parameters
        ----------
        D1 : np.ndarray
            Die 10x10-Matrix der minimalen Königinnen-Distanzen für Spieler 1.
        D2 : np.ndarray
            Die 10x10-Matrix der minimalen Königinnen-Distanzen für Spieler 2.

        Returns
        ----------
        t1 : int
            Die territoriale Bewertung. Positive Werte deuten auf einen Vorteil für Spieler 1 hin,
            negative Werte deuten auf einen Vorteil für Spieler 2 hin.
        """

        t1 = 0
        for x in range(10):
            for y in range(10):
                if D1[x, y] < D2[x, y]:
                    t1 += 1 # Spieler 1 hat bessere Kontrolle
                elif D1[x, y] > D2[x, y]:
                    t1 -= 1 # Spieler 2 hat bessere Kontrolle
        return t1
    
    def mobility_of_amazon(self, amazon):
        """
        Berechnet die Mobilität einer einzelnen Amazone.

        Parameters
        ----------
        amazon : tuple
            Die Position der Amazone als (x, y).

        Returns
        ----------
        mobility : int
            Die Anzahl der Felder, die die Amazone erreichen kann.
        """

        x, y = amazon
        mobility = 0
        for dx, dy in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
            nx, ny = x + dx, y + dy
            while self.is_within_bounds(nx, ny) and self.board[nx][ny] == 0:
                mobility += 1
                nx += dx
                ny += dy
        return mobility

    def mobility_evaluation(self, player):
        """
        Summiert die Mobilität aller Amazonen eines Spielers.

        Parameters
        ----------
        player : int
            Der Spieler (1 oder 2), dessen Amazonen bewertet werden.

        Returns
        ----------
        m : int
            Die Gesamtmobilität der Amazonen des Spielers.
        """
        
        m = 0
        for amazon in self.amazons[player]:
            m += self.mobility_of_amazon(amazon)
        return m

    def evaluate_position(self):
        """
        Bewertet die aktuelle Position des Spiels unter Berücksichtigung der territorialen Kontrolle und der Mobilität.

        Returns
        ----------
        evaluation : float
            Die Gesamtbewertung der Position. Positive Werte deuten auf einen Vorteil für Spieler 1 hin,
            negative Werte deuten auf einen Vorteil für Spieler 2 hin.
        """
        # D[Spieler(j)] _ [i]
    	
        D1_1, D1_2 = self.calculate_distances(1) # Spieler 1
        D2_1, D2_2 = self.calculate_distances(2) # Spieler 2

        t1 = self.territorial_evaluation(D1_1, D2_1) # Bewertung der Territorial Position Königinnenzüge D1 | Bei > 0 => Vorteil Spieler 1 else (<0) Spieler 2
        t2 = self.territorial_evaluation(D1_2, D2_2) # Bewertung der Territorial Position Königszüge D2     | Bei > 0 => Vorteil Spieler 1 else (<0) Spieler 2
        
        # Lokale Bewertung, die die Kontrolle über Felder basierend auf den minimalen *Königin*-Distanzen D1 widerspiegelt
        # Felder die näher an den Amazonen eines Spielers leigen, sind für diesen vorteilhafter
        c1 = 0
        for x in range(10):
            for y in range(10):
                c1 += 2 ** (-D1_1[x, y]) - 2 ** (-D2_1[x, y]) # Gewichtung basierend auf Distanzwerten
        c1 = 2 * c1
        
        # Lokale Bewertung, die die Kontrolle über Felder basierend auf den minimalen *Königs*-Distanzen D2 widerspiegelt
        # Felder die näher an den Amazonen eines Spielers leigen, sind für diesen vorteilhafter
        c2 = 0
        for x in range(10):
            for y in range(10):
                c2 += min(1, max(-1, ((D2_2[x, y] - D1_2[x, y]) / 6))) # Bewertung basierend auf D2-Differenzen

        # Gewichtungsfaktor w zur Mischung der Bewertungen
        w = sum(2 ** -abs(D1_1[x, y] - D2_1[x, y]) for x in range(10) for y in range(10) if D1_1[x, y] < np.inf and D2_1[x, y] < np.inf)


        f1 = lambda w: max(0, 1 - (w - 10) / 40)
        f2 = lambda w: min(1, (w - 10) / 40)
        f3 = lambda w: (1 - f1(w) - f4(w)) / 2
        f4 = lambda w: f2(w)
        
        # Kombinierte Bewertung aus territorialen und positionsabhängigen Faktoren
        t = f1(w) * t1 + f2(w) * c1 + f3(w) * c2 + f4(w) * t2
        
        m1 = self.mobility_evaluation(1)
        m2 = self.mobility_evaluation(2)

        m = m1 - m2 # Mobilitätsdifferenz

        #print(f"t1: {t1}, t2: {t2}, c1: {c1}, c2: {c2}, w: {w}, f1(w): {f1(w)}, f2(w): {f2(w)} t: {t}, m1: {m1}, m2: {m2}, evaluation: {t+m}")
        return t + m
    
    """
    def mobility_evaluation(self,  player):
    
        Berechnet, wie viele legale Züge der Spieler hat.

        Returns
        ----------
        Score den die aktuelle Position hat - sprich wie viele mögliche Züge der aktuelle Spiler mit der aktuellen Position hat

        self.current_player = player
        m = 0
        for amazon in self.game.amazons[player]:
            m += len(self.calculate_moves_for_amazon(amazon[0], amazon[1]))
        
        self.current_player = 3 - player
        return m
    """

    """
    def evaluate_position(self):
        m = 0
        for amazon in self.amazons[self.current_player]:
            m += len(self.calculate_moves_for_amazon(amazon[0], amazon[1]))
        
        return m
    """