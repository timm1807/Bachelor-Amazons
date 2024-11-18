import random
import numpy as np
import copy
from collections import deque

np.seterr(invalid='ignore')

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
        
    def current_player_random_moves_faster(self):
        """
        Überprüft ob der aktuelle Spieler noch legale Züge hat und gibt
        eine Liste mit allen legalen Zügen aus.

        Returns
        ----------
        Eine Liste legalMoves mit allen möglichen und legallen Zügen für den aktuellen Spieler
        Liste: [ (zug1) , (zug2) , (zug3) ]
        Zug: (start_pos), (end_pos), (arrow_pos)
        """
        amazon = self.amazons[self.current_player][random.randint(0,3)]
        return self.calculate_moves_for_amazon(amazon[0], amazon[1])
    
    ########################################################################
    ######################### EVALUATION FUNCTION ##########################

    def count_occupied_fields(self):
        """
        Zählt die Anzahl der belegten Felder auf dem Spielfeld.
        Belegte Felder sind Amazonen von Spieler 1, Spieler 2 oder Pfeile ("X").

        Returns
        -------
        occupied_count : int
            Die Anzahl der belegten Felder.
        """
        occupied_count = 0
        for row in self.board:
            for cell in row:
                if cell != 0:  # Ein Feld ist belegt, wenn es nicht 0 ist (0 = leeres Feld)
                    occupied_count += 1
        return occupied_count

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

        """
        # Gewichtungsfaktor w zur Mischung der Bewertungen
        w = sum(2 ** -abs(D1_1[x, y] - D2_1[x, y]) for x in range(10) for y in range(10) if D1_1[x, y] < np.inf and D2_1[x, y] < np.inf)


        f1 = lambda w: max(0, 1 - (w - 10) / 40)
        f2 = lambda w: min(1, (w - 10) / 40)
        f3 = lambda w: (1 - f1(w) - f4(w)) / 2
        f4 = lambda w: f2(w)

        # Kombinierte Bewertung aus territorialen und positionsabhängigen Faktoren
        t = f1(w) * t1 + f2(w) * c1 + f3(w) * c2 + f4(w) * t2
        """
        
        proportion_occupied_fields = self.count_occupied_fields()/100
        v = 0.7

        f1 = v*proportion_occupied_fields
        f2 = (1-v)*proportion_occupied_fields
        f3 = v*(1-proportion_occupied_fields)
        f4 = (1-v)*(1-proportion_occupied_fields)

        t = f1 * t1 + f2 * c1 + f3 * c2 + f4 * t2
        
        m1 = self.mobility_evaluation(1)
        m2 = self.mobility_evaluation(2)

        m = m1 - m2 # Mobilitätsdifferenz

        return t + m