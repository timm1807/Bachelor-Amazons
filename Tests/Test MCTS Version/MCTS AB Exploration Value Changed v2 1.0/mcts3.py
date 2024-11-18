import random, math
import time

debug = False
debugTimer = False

class MCTSNode:
    def __init__(self, game, mcts_player, is_to_move, parent=None, move=None):
        self.mcts_player = mcts_player
        self.game = game
        self.is_to_move = is_to_move
        self.parent = parent
        self.move = move
        self.children = []
        self.wins = 0
        self.visits = 0
        self.untried_moves = game.current_player_has_legal_moves()

    def expandRoot(self, top_x=50):
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
        evaluated_moves.sort(reverse=True, key=lambda x: x[0] if self.mcts_player == 1 else -x[0])
        top_moves = evaluated_moves[:top_x]
        random.shuffle(top_moves)
        
        # Erweitert die Wurzel um die Top-x-Züge
        for _, move in top_moves:
            next_game = self.game.copy()
            next_game.make_move(*move)
            child_node = MCTSNode(next_game, self.mcts_player, is_to_move=(3 - self.is_to_move), parent=self, move=move)
            self.children.append(child_node)

    def expand(self, expand_ratio=100):
        """
        Fügt dem aktuellen (Eltern)knoten *expand_ratio* Kindknoten hinzu

        Returns
        ----------
        Ein Kindknoten mit dem random Move als Game-state und gewechseltem Spieler
        """
        possible_moves = self.game.current_player_has_legal_moves()
        for _ in range(expand_ratio):
            if possible_moves:
                move = random.choice(possible_moves)
                possible_moves.pop(possible_moves.index(move))
                next_game = self.game.copy()
                next_game.make_move(*move)
                child_node = MCTSNode(next_game, self.mcts_player, is_to_move=(3 - self.is_to_move), parent=self, move=move)
                self.children.append(child_node)
        return child_node
    
    def expanded(self):
        return len(self.children) > 0
    
    def best_child(self, exploration_value=1.0):
        choices_weights = []
        for child in self.children:
            if child.visits == 0:
                if self.mcts_player == 1:
                    choices_weights.append(float('inf'))
                else:
                    choices_weights.append(float('-inf'))
            else:
                # Priorisiere Züge basierend auf der Bewertung des resultierenden Spielzustands
                move_priority = child.game.evaluate_position()

                # Berechne den Normalwert für die UCB1-Formel
                ucb1_value = (child.wins / child.visits) + exploration_value * math.sqrt((2 * math.log(self.visits) / child.visits))

                # UCB1 * -1 für Spieler 2
                if self.mcts_player == 2: ucb1_value = (ucb1_value * -1) 

                # Kombiniere UCB1 und move_priority unter Berücksichtigung der Korrelation
                if self.mcts_player == 1:
                    adjusted_value = ucb1_value + (move_priority / (1 + child.visits))
                else:
                    adjusted_value = ucb1_value - (move_priority / (1 + child.visits))

                choices_weights.append(adjusted_value)
                
                #choices_weights.append(ucb1_value)

        #return self.children[choices_weights.index(max(choices_weights))]

        if self.mcts_player == 1:
            return self.children[choices_weights.index(max(choices_weights))]
        else:
            return self.children[choices_weights.index(min(choices_weights))]
    
    def simulate(self, max_depth=6):
        """
        Simuliert das Spiel bis zum Ende unter Verwendung der Evaluationsfunktion,
        um nicht zufällige, sondern strategisch sinnvolle Züge durchzuführen.

        Es werden *max_depth* Züge gespielt und für jeden Zug wird jeweils der nach der Evaluierungsfunktion aus 50 zufälligen
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
        simulated_game = self.game.copy()
        while depth < max_depth:
            
            legal_moves = simulated_game.current_player_random_moves_faster()

            # Wähle den besten Zug basierend auf der Evaluationsfunktion
            best_move = None
            best_evaluation = float('-inf') if simulated_game.current_player == 1 else float('inf')
        
            if not legal_moves:
                break

            for move in legal_moves:
                if not legal_moves:
                    break
                
                legal_moves.pop(legal_moves.index(move))

                inner_sim = simulated_game.copy()
                inner_sim.make_move(*move)
                evaluation = inner_sim.evaluate_position()

                if inner_sim.current_player == 1:
                        # Maximieren
                        if evaluation > best_evaluation:
                            best_evaluation = evaluation
                            best_move = move
                else:
                    # Minimieren
                    if evaluation < best_evaluation:
                        best_evaluation = evaluation
                        best_move = move

            simulated_game.make_move(*best_move)
            simulated_game.current_player = 3 - simulated_game.current_player
            depth += 1
        
        return simulated_game.get_game_result()

    def update(self, result):
        # Wenn der aktuelle Knoten einen von mir als MCTS Spieler repräsentiert
        if self.mcts_player == 2: result = 1 - result
        if self.is_to_move == self.mcts_player:
            self.wins += result
            self.visits += 1
        else: 
            self.wins += 1 - result
            self.visits += 1

def mcts3(game, is_to_move, exploration_value=1.0, time_limit=120):
    root = MCTSNode(game, mcts_player=game.current_player, is_to_move=is_to_move)
    
    root.expandRoot(top_x=30)

    start_time = time.time()
    iteration_count = 0
    while time.time() - start_time < time_limit:

        if game.is_game_over():
            break

        node = root
        
        # Selection - wähle einen Node aus, der noch nicht erweitert wurde (keine Kinderknoten hat)
        while node.expanded():
            node = node.best_child(exploration_value)

        # Expansion - füge dem ausgewählten Knoten Kinderknoten hinzu
        if not node.game.is_game_over():
            node.expand(expand_ratio=1)

        # Simulation -> Führe für jeden dieser Kinderknoten eine Simulation durch ~48 Sekunden Calc Time
        for child in node.children:
            result = child.simulate()

            while child is not None:
                child.update(result)
                child = child.parent
        
        iteration_count += 1
        
    if not root.children: return None, iteration_count
    best_move = max(root.children, key=lambda c: c.visits).move
    return best_move, iteration_count