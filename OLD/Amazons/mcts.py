import math
import random
import copy
import logging

logging.basicConfig(level=logging.DEBUG)

class MCTSNode:
    def __init__(self, game, parent=None, move=None):
        self.game = game
        self.parent = parent
        self.move = move
        self.children = []
        self.wins = 0
        self.visits = 0
        self.untried_moves = game.current_player_has_legal_moves()

    def is_fully_expanded(self):
        return len(self.untried_moves) == 0

    def best_child(self, exploration_value=1.4):
        choices_weights = [
            (child.wins / child.visits) + exploration_value * math.sqrt((2 * math.log(self.visits) / child.visits))
            for child in self.children
        ]
        logging.debug(f'Best Child: {self.children[choices_weights.index(max(choices_weights))]}')
        return self.children[choices_weights.index(max(choices_weights))]

    def expand(self):
        move = random.choice(self.untried_moves)
        self.untried_moves.pop(self.untried_moves.index(move)) ####
        next_game = self.game.copy()
        next_game.make_move(*move)
        child_node = MCTSNode(next_game, parent=self, move=move)
        self.children.append(child_node)
        return child_node

    def update(self, result):
        self.visits += 1
        self.wins += result
        logging.debug(f'Updated node: Wins={self.wins}, Visits={self.visits}, Result={result}')

def mcts(root, itermax, exploration_value=1.4):
    for _ in range(itermax):
        node = root
        game = copy.deepcopy(root.game)

        # Selection:
        # Wählt iterativ den besten Kinderknoten basierend auf UCB1 aus, bis ein Knoten erreicht wird, 
        # der nicht vollständig expandiert ist
        while node.is_fully_expanded() and node.children:
            node = node.best_child(exploration_value) # Kind mit höchsten UCB1 Score
            game.make_move(*node.move)
            logging.debug(f'Move made: {node.move}, New Node: {node}')

        # Expansion:
        # Expandiert den ausgewählten Knoten, indem ein noch nicht ausprobierter Zug ausgeführt wird
        if node.untried_moves:
            node = node.expand()
            game.make_move(*node.move)
            logging.debug(f'Expanded: {node.move}, New Node: {node}')

        # Simulation: 
        # Führt eine zufällige Simulation vom expandierten Knoten aus, bis das Spiel endet
        while game.current_player_has_legal_moves():
            move = random.choice(game.current_player_has_legal_moves())
            game.make_move(*move)

        # Backpropagation: 
        # Aktualisiert die Knoten entlang des Pfades vom expandierten Knoten zum Wurzelknoten 
        # basierend auf dem Ergebnis der Simulation
        result = game.get_game_result()  # Adjust this to return 1 for win, 0 for loss, and 0.5 for draw
        while node is not None:
            node.update(result)
            node = node.parent

    best_move = max(root.children, key=lambda c: c.visits).move
    logging.debug(f'Best move: {best_move}')
    return best_move