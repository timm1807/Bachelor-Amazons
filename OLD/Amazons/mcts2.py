import random, math
import time

class MCTSNode:
    def __init__(self, game, player, parent=None, move=None):
        self.mcts_player = player
        self.game = game
        self.player = player
        self.parent = parent
        self.move = move
        self.children = []
        self.wins = 0
        self.visits = 0
        self.untried_moves = game.current_player_has_legal_moves()

    def expandRoot(self, top_x=100):
        """
        Erweitert die Wurzel um die Top-x-Züge basierend auf einer Bewertungsfunktion.

        Parameters
        ----------
        top_x : int
            Die Anzahl der besten Züge, die als Kindknoten erweitert werden sollen.
        """
        # Bewertet alle möglichen Züge
        evaluated_moves = []
        for move in self.untried_moves:
            simulated_game = self.game.copy()
            simulated_game.make_move(*move)
            evaluation = simulated_game.evaluate_position()
            evaluated_moves.append((evaluation, move))
        
        # Sortiert die Züge nach Bewertung, um die besten zu ermitteln
        evaluated_moves.sort(reverse=True, key=lambda x: x[0])
        
        # Erweitert die Wurzel um die Top-x-Züge
        for _, move in evaluated_moves[:top_x]:
            next_game = self.game.copy()
            next_game.make_move(*move)
            child_node = MCTSNode(next_game, self.player, parent=self, move=move)
            self.children.append(child_node)
        
        return

    def expand(self, expand_ratio=100):
        """
        Fügt dem aktuellen (Eltern)knoten *expand_ratio* Kindknoten hinzu

        Returns
        ----------
        Ein Kindknoten mit dem random Move als Game-state und gewechseltem Spieler
        """
        for _ in range(expand_ratio):
            if self.untried_moves:
                move = random.choice(self.untried_moves)
                self.untried_moves.pop(self.untried_moves.index(move))
                next_game = self.game.copy()
                next_game.make_move(*move)
                child_node = MCTSNode(next_game, (3 - self.player), parent=self, move=move)
                self.children.append(child_node)
                # Spielerwechsel
                #self.game.current_player = 3 - self.game.current_player
        return child_node
    
    def expanded(self):
        return len(self.children) > 0
    
    def best_child(self, exploration_value=1.4):
        choices_weights = []
        for child in self.children:
            if child.visits == 0:
                choices_weights.append(float('inf'))
            else:
                # Priorisiere Züge basierend auf der Bewertung des resultierenden Spielzustands
                move_priority = child.game.evaluate_position()  # Evaluierung des aktuellen Game-States
                priority_bonus = move_priority / (1 + child.visits)  # Bonus basierend auf der Evaluierung und der Anzahl der Besuche
                choices_weights.append(
                    (child.wins / child.visits) + exploration_value * math.sqrt((2 * math.log(self.visits) / child.visits)) + priority_bonus
                )
        return self.children[choices_weights.index(max(choices_weights))]
    
    def simulate(self, max_depth=6, move_range=100):
        #move = random.choice(self.game.current_player_has_legal_moves())
        #self.game.make_move(*move)
        #self.game.current_player = 3 - self.game.current_player
        """
        Simuliert das Spiel bis zum Ende unter Verwendung der Evaluationsfunktion,
        um nicht zufällige, sondern strategisch sinnvolle Züge durchzuführen.

        Es werden *max_depth* Züge gespielt und für jeden Zug wird jeweils der nach der Evaluierungsfunktion aus *move_range* zufälligen
        möglichen Zügen der best bewerteste Zug ausgewählt und in der Simulation gespielt.

        Parameters
        ----------
        max_depth : int
            Die maximale Tiefe, bis zu der simuliert wird. Standardwert ist 10.

        Returns
        ----------
        int : Die Bewertung der Simulation
        """
        depth = 0

        while depth < max_depth:
            legal_moves = self.game.current_player_has_legal_moves()
        
            if not legal_moves:
                break
        
            # Wähle den besten Zug basierend auf der Evaluationsfunktion
            best_move = None
            best_evaluation = float('-inf') if self.game.current_player == self.mcts_player else float('inf')
            
            #for move in legal_moves:
            for _ in range(move_range):
                if not legal_moves:
                    break
                move = random.choice(legal_moves)
                legal_moves.pop(legal_moves.index(move))
                #move = random.choice(legal_moves)
                simulated_game = self.game.copy()
                simulated_game.make_move(*move)
                evaluation = simulated_game.evaluate_position()
                
                if self.game.current_player == self.mcts_player:
                    # Maximieren
                    if evaluation > best_evaluation:
                        best_evaluation = evaluation
                        best_move = move
                else:
                    # Minimieren
                    if evaluation < best_evaluation:
                        best_evaluation = evaluation
                        best_move = move
        
            # Führe den besten Zug durch
            self.game.make_move(*best_move)
            self.game.current_player = 3 - self.game.current_player
            depth += 1
        
        return self.game.get_game_result()

    def update(self, result):
        # Wenn der aktuelle Knoten einen von mir als MCTS Spieler repräsentiert
        if self.player == self.mcts_player:
            self.wins += result
            self.visits += 1
        else:
            self.wins = 0
            self.visits += 1

def mcts2(game, player, num_sim=20, exploration_value=1.4, time_limit=60):
    root = MCTSNode(game, player)
    
    start_time = time.time()

    start1 = time.time()
    # Expand Root -> ~7 Sekunden Calc Time
    root.expandRoot(top_x=50)
    end1 = time.time()
    #print("expand root time: ",end1-start1)

    for _ in range(num_sim):
        if game.is_game_over():
            break
        node = root

        if time.time() - start_time > time_limit:
            print("Zeitlimit erreicht, breche Berechnung ab.")
            break
        
        # Selection - wähle einen Node aus, der noch nicht erweitert wurde (keine Kinderknoten hat)
        # -> ~0 Sekunden Calc Time
        start2 = time.time()
        while node.expanded():
            #print("---select")
            node = node.best_child(exploration_value)
        end2 = time.time()
        #print("selection time: ",end2-start2)

        # Expansion - füge dem ausgewählten Knoten Kinderknoten hinzu
        # -> ~0.3 Sekunden Calc Time
        start3 = time.time()
        if not node.game.is_game_over():
            #print("------expand")
            node.expand(expand_ratio=50)
        end3 = time.time()
        #print("expansion time: ",end3-start3)

        # Simulation -> ~48 Sekunden Calc Time
        #while not node.game.is_game_over():
        #print("--------simulate")
        start5 = time.time()
        for child in node.children:
            #print("--------simulate child") 
            result = child.simulate(max_depth=6, move_range=50)
            # Backpropagation -> ~0 Sekunden Calc Time
            #print("---------------backropagate")
            start4 = time.time()
            while child is not None:
                child.update(result)
                child = child.parent
            end4 = time.time()
            #print("backpropagation time: ",end4-start4)
        end5 = time.time()
        #print("overall simulation time: ",(end5-start5)-(end4-start4))

        """
        # Backpropagation
        result = node.game.get_game_result()
        #print("RESULT: ",result)
        while node is not None:
            #print("backropagate")
            node.update(result)
            node = node.parent
        """

    best_move = max(root.children, key=lambda c: c.visits).move
    return best_move if best_move else None