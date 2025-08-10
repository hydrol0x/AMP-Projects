from Player import Player, Hand
from typing import List, Dict, Tuple, Optional

class Game():
    def __init__(self):
        self.current_player = 0
        self.players = [Player(), Player()]
        self.winner: Optional[int] = None

    def start_game(self) -> None:
        self.current_player = 0
        self.winner = None
        self.players = [Player(), Player()]

    def valid_moves(self) -> List[Dict[str, any]]:
        moves = []
        current = self.players[self.current_player]
        opponent = self.players[1 - self.current_player]

        if current.left.alive and current.left.value > 0:
            if opponent.left.alive:
                moves.append({
                    'type': 'attack',
                    'from_hand': 'left',
                    'to_player': 1 - self.current_player,
                    'to_hand': 'left'
                })
            if opponent.right.alive:
                moves.append({
                    'type': 'attack',
                    'from_hand': 'left',
                    'to_player': 1 - self.current_player,
                    'to_hand': 'right'
                })

        if current.right.alive and current.right.value > 0:
            if opponent.left.alive:
                moves.append({
                    'type': 'attack',
                    'from_hand': 'right',
                    'to_player': 1 - self.current_player,
                    'to_hand': 'left'
                })
            if opponent.right.alive:
                moves.append({
                    'type': 'attack',
                    'from_hand': 'right',
                    'to_player': 1 - self.current_player,
                    'to_hand': 'right'
                })

        if current.left.alive and current.right.alive:
            total = current.left.value + current.right.value
            for left_value in range(total + 1):
                right_value = total - left_value
                if (left_value != current.left.value and
                    0 < left_value < 5 and 0 < right_value < 5):
                    if left_value < current.left.value:
                        amount = current.left.value - left_value
                        moves.append({
                            'type': 'split',
                            'left_to_right': True,
                            'amount': amount,
                            'left_value': left_value,
                            'right_value': right_value
                        })
                    else:
                        amount = left_value - current.left.value
                        moves.append({
                            'type': 'split',
                            'left_to_right': False,
                            'amount': amount,
                            'left_value': left_value,
                            'right_value': right_value
                        })

        elif current.left.alive and not current.right.alive and current.left.value > 1:
            for amount in range(1, current.left.value):
                if current.left.value - amount > 0 and amount > 0:
                    moves.append({
                        'type': 'split',
                        'left_to_right': True,
                        'amount': amount,
                        'left_value': current.left.value - amount,
                        'right_value': amount
                    })
        elif current.right.alive and not current.left.alive and current.right.value > 1:
            for amount in range(1, current.right.value):
                if current.right.value - amount > 0 and amount > 0:
                    moves.append({
                        'type': 'split',
                        'left_to_right': False,
                        'amount': amount,
                        'left_value': amount,
                        'right_value': current.right.value - amount
                    })

        return moves

    def make_move(self, move: Dict[str, any]) -> bool:
        if self.winner is not None:
            return False

        valid_moves = self.valid_moves()
        move_valid = False
        for valid_move in valid_moves:
            if move['type'] == valid_move['type']:
                if move['type'] == 'attack':
                    if (move.get('from_hand') == valid_move.get('from_hand') and
                        move.get('to_player') == valid_move.get('to_player') and
                        move.get('to_hand') == valid_move.get('to_hand')):
                        move_valid = True
                        break
                elif move['type'] == 'split':
                    if (move.get('left_to_right') == valid_move.get('left_to_right') and
                        move.get('amount') == valid_move.get('amount')):
                        move_valid = True
                        break

        if not move_valid:
            return False

        current = self.players[self.current_player]

        if move['type'] == 'attack':
            from_hand = current.left if move['from_hand'] == 'left' else current.right
            to_player = self.players[move['to_player']]
            to_hand = to_player.left if move['to_hand'] == 'left' else to_player.right

            to_hand.value += from_hand.value

            if to_hand.value >= 5:
                to_hand.value = to_hand.value % 5
                if to_hand.value == 0:
                    to_hand.alive = False

        elif move['type'] == 'split':
            current.split(move['left_to_right'], move['amount'])

            for hand in [current.left, current.right]:
                if hand.value >= 5:
                    hand.value = hand.value % 5
                    if hand.value == 0:
                        hand.alive = False
                elif hand.value > 0:
                    hand.alive = True
                else:
                    hand.value = 0
                    hand.alive = False

        opponent = self.players[1 - self.current_player]
        if not opponent.left.alive and not opponent.right.alive:
            self.winner = self.current_player

        self.current_player = 1 - self.current_player

        return True

    def get_game_state(self) -> Dict[str, any]:
        state = {
            'current_player': self.current_player,
            'winner': self.winner,
            'players': []
        }

        for i, player in enumerate(self.players):
            player_state = {
                'player_id': i,
                'left': {
                    'alive': player.left.alive,
                    'value': player.left.value
                },
                'right': {
                    'alive': player.right.alive,
                    'value': player.right.value
                }
            }
            state['players'].append(player_state)

        return state
