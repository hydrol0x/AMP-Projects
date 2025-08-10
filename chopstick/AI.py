from typing import Dict, List, Tuple, Optional
from Game import Game
from Player import Player, Hand
import copy


class AI:
    def __init__(self):
        self.max_depth = 10
        self.cache = {}

    def get_best_move(self, game: Game) -> Optional[Dict[str, any]]:
        if game.winner is not None:
            return None

        valid_moves = game.valid_moves()
        if not valid_moves:
            return None

        best_move = None
        best_value = float('-inf')
        alpha = float('-inf')
        beta = float('inf')

        for move in valid_moves:
            game_copy = self._copy_game(game)
            game_copy.make_move(move)

            value = self._minimax(game_copy, self.max_depth - 1, alpha, beta, False)

            if value > best_value:
                best_value = value
                best_move = move

            alpha = max(alpha, value)

        return best_move

    def _minimax(self, game: Game, depth: int, alpha: float, beta: float, maximizing: bool) -> float:

        state_key = self._get_state_key(game)
        cache_key = (state_key, depth, maximizing)

        if cache_key in self.cache:
            return self.cache[cache_key]

        if game.winner is not None:
            result = 1000 if game.winner == 0 else -1000
            self.cache[cache_key] = result
            return result

        if depth == 0:
            eval_score = self._evaluate_position(game)
            self.cache[cache_key] = eval_score
            return eval_score

        valid_moves = game.valid_moves()
        if not valid_moves:
            self.cache[cache_key] = 0
            return 0

        if maximizing:
            max_eval = float('-inf')
            for move in valid_moves:
                game_copy = self._copy_game(game)
                game_copy.make_move(move)
                eval_score = self._minimax(game_copy, depth - 1, alpha, beta, False)
                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break
            self.cache[cache_key] = max_eval
            return max_eval
        else:
            min_eval = float('inf')
            for move in valid_moves:
                game_copy = self._copy_game(game)
                game_copy.make_move(move)
                eval_score = self._minimax(game_copy, depth - 1, alpha, beta, True)
                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break
            self.cache[cache_key] = min_eval
            return min_eval

    def _evaluate_position(self, game: Game) -> float:
        if game.winner == 0:
            return 1000
        elif game.winner == 1:
            return -1000

        score = 0

        p0 = game.players[0]
        p0_alive_hands = (1 if p0.left.alive else 0) + (1 if p0.right.alive else 0)
        p0_total_fingers = p0.left.value + p0.right.value

        p1 = game.players[1]
        p1_alive_hands = (1 if p1.left.alive else 0) + (1 if p1.right.alive else 0)
        p1_total_fingers = p1.left.value + p1.right.value

        score += (p0_alive_hands - p1_alive_hands) * 50

        score += (p0_total_fingers - p1_total_fingers) * 5

        if game.current_player == 0:
            for p0_hand in [p0.left, p0.right]:
                if p0_hand.alive:
                    for p1_hand in [p1.left, p1.right]:
                        if p1_hand.alive and (p0_hand.value + p1_hand.value) == 5:
                            score += 20
        else:
            for p1_hand in [p1.left, p1.right]:
                if p1_hand.alive:
                    for p0_hand in [p0.left, p0.right]:
                        if p0_hand.alive and (p1_hand.value + p0_hand.value) == 5:
                            score -= 20

        return score

    def _copy_game(self, game: Game) -> Game:
        new_game = Game()
        new_game.current_player = game.current_player
        new_game.winner = game.winner

        new_game.players = []
        for player in game.players:
            new_player = Player()
            new_player.left = Hand()
            new_player.left.value = player.left.value
            new_player.left.alive = player.left.alive
            new_player.right = Hand()
            new_player.right.value = player.right.value
            new_player.right.alive = player.right.alive
            new_game.players.append(new_player)

        return new_game

    def _get_state_key(self, game: Game) -> str:
        p0 = game.players[0]
        p1 = game.players[1]
        return f"{game.current_player}:{p0.left.value}{p0.left.alive}:{p0.right.value}{p0.right.alive}:{p1.left.value}{p1.left.alive}:{p1.right.value}{p1.right.alive}"

    def get_move_description(self, move: Dict[str, any]) -> str:
        if move['type'] == 'attack':
            return f"Attack: Use {move['from_hand']} hand to attack opponent's {move['to_hand']} hand"
        elif move['type'] == 'split':
            direction = "left to right" if move['left_to_right'] else "right to left"
            return f"Split: Move {move['amount']} from {direction} (Result: L={move['left_value']}, R={move['right_value']})"
        return "Unknown move"

    def analyze_position(self, game: Game) -> Dict[str, any]:
        best_move = self.get_best_move(game)

        if not best_move:
            return {
                'best_move': None,
                'description': "No moves available",
                'evaluation': 0,
                'winning': None
            }

        game_copy = self._copy_game(game)
        game_copy.make_move(best_move)

        evaluation = self._minimax(game_copy, self.max_depth - 1, float('-inf'), float('inf'), False)

        winning = None
        if abs(evaluation) > 900:
            winning = evaluation > 0

        return {
            'best_move': best_move,
            'description': self.get_move_description(best_move),
            'evaluation': evaluation,
            'winning': winning,
            'explanation': self._get_position_explanation(evaluation)
        }

    def _get_position_explanation(self, evaluation: float) -> str:
        if abs(evaluation) > 900:
            if evaluation > 0:
                return "This position is winning for the current player with best play."
            else:
                return "This position is losing for the current player with best play."
        elif abs(evaluation) > 50:
            if evaluation > 0:
                return "The current player has a significant advantage."
            else:
                return "The opponent has a significant advantage."
        elif abs(evaluation) > 20:
            if evaluation > 0:
                return "The current player has a slight advantage."
            else:
                return "The opponent has a slight advantage."
        else:
            return "The position is approximately equal."
