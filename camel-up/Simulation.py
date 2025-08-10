from Board import Board
from Camel import Color
from copy import deepcopy

class GameState:
    def __init__(self, board):
        self.board = deepcopy(board)

    def get_current_state(self):
        state = {}

        state['available_betting_cards'] = self._get_available_betting_cards()
        state['camel_positions'] = self._get_camel_positions()
        state['dice_remaining'] = self._get_dice_remaining()
        state['player_states'] = self._get_player_states()
        state['spectator_tiles'] = self._get_spectator_tiles()
        state['current_player'] = self._get_current_player_info()
        state['game_status'] = self._get_game_status()
        state['board_visualization'] = self._get_board_visualization()
        state['finish_cards'] = self._get_finish_cards()
        state['available_moves'] = self._get_available_moves()

        return state

    def _get_available_betting_cards(self):
        betting_cards = {}
        for color, cards in self.board.cards.return_bets().items():
            betting_cards[color.name] = deepcopy(cards)
        return betting_cards

    def _get_camel_positions(self):
        camel_positions = {}
        for camel in self.board.camels:
            camel_positions[camel.color.name] = {
                'position': camel.get_position(),
                'stacked_on_me': camel.stacked_on_me.color.name if camel.stacked_on_me else None,
                'stacked_below': self.board.stacked_below(camel).color.name if self.board.stacked_below(camel) else None
            }
        return camel_positions

    def _get_dice_remaining(self):
        return [color.name for color in self.board.pyramid.get_dice()]

    def _get_player_states(self):
        player_states = []
        for player in self.board.players:
            player_state = {
                'name': player.get_name(),
                'money': player.get_money(),
                'current_bets': [{'color': bet[0].name, 'value': bet[1]} for bet in player.current_bets],
                'spectator_card_played': player.spectator_card_played,
                'spectator_card_position': player.spectator_card_position,
                'spectator_card_value': player.spectator_card_value,
                'available_finish_cards': [color.name for color in player.get_availible_finish_cards()],
                'overall_winner_bets': [color.name for color in player.overall_winner],
                'overall_loser_bets': [color.name for color in player.overall_loser]
            }
            player_states.append(player_state)
        return player_states

    def _get_spectator_tiles(self):
        spectator_tiles = []
        for tile in self.board.spectators:
            spectator_tiles.append({
                'position': tile.tile_position(),
                'value': '+1' if tile.tile_value() else '-1'
            })
        return spectator_tiles

    def _get_current_player_info(self):
        current_player = self.board.get_current_player()
        return {
            'index': self.board.current_player,
            'name': current_player.get_name(),
            'money': current_player.get_money()
        }

    def _get_game_status(self):
        return {
            'is_game_over': self.board.is_game_over,
            'is_leg_over': self.board.is_leg_over(),
            'num_players': self.board.num_players
        }

    def _get_board_visualization(self):
        return self.board.visualize_board_1()

    def _get_finish_cards(self):
        finish_cards = {
            'winner_bets': [(color.name, player.get_name()) for color, player in self.board.finish_cards_winner],
            'loser_bets': [(color.name, player.get_name()) for color, player in self.board.finish_cards_loser]
        }
        return finish_cards

    def _get_available_moves(self):
        available_moves = ['ROLL']

        for color in Color:
            if not self.board.cards.is_empty(self.board.cards.bets[color]):
                available_moves.append(f'BET_{color.name}')

        if self.board.free_spaces():
            available_moves.append('PLACE_SPECTATOR_TILE')

        current_player = self.board.get_current_player()
        if current_player.get_availible_finish_cards():
            available_moves.append('BET_FINISH')

        return available_moves

    def simulate_leg(self):
        # i want to simulate till leg is over which is like all the dices have been rolled
        while not self.board.is_leg_over():
            roll_result = self.board.pyramid.roll_dice()
            if roll_result:
                color, number = roll_result
                self.board.handle_roll_dice(color, number)
            else:
                self.board.pyramid.reset_dice()
                break

        final_state = self.get_current_state()
        return final_state

    def rank_camels(self):
        camel_rankings = []
        for camel in self.board.camels:
            position = camel.get_position()

            stack_height = 0
            current = camel
            while self.board.stacked_below(current):
                stack_height += 1
                current = self.board.stacked_below(current)

            camel_rankings.append((camel.color.name, position, stack_height))
        camel_rankings.sort(key=lambda x: (x[1], x[2]), reverse=True)
        first_camel = camel_rankings[0]
        second_camel = camel_rankings[1]
        camel_rankings.remove(first_camel)
        camel_rankings.remove(second_camel)
        losing_camels = []
        for i in camel_rankings:
            losing_camels.append(i[0])
        winner_runner_up = (first_camel[0], second_camel[0])

        return winner_runner_up, losing_camels

    def multiple_simulations(self, n):
        win_counts = {}
        runner_up_counts = {}
        loser_counts = {}

        original_board = deepcopy(self.board)
        for camel in self.board.camels:
            win_counts[camel.color.name] = 0 # new dict for the camels
            runner_up_counts[camel.color.name] = 0
            loser_counts[camel.color.name] = 0

        for i in range(n):
            sim_game_state = GameState(original_board)
            sim_game_state.simulate_leg()
            winner_runner_up, losing_camels = sim_game_state.rank_camels()
            winner = winner_runner_up[0]
            runner_up = winner_runner_up[1]

            win_counts[winner] += 1
            runner_up_counts[runner_up] += 1

        for camel in self.board.camels:
            loser_counts[camel.color.name] = (n - (runner_up_counts[camel.color.name] + win_counts[camel.color.name]))

        return win_counts, runner_up_counts, loser_counts

    def expected_value(self, number_of_simulations, win_counts, runner_up_counts, loser_counts):
        colors = {'Y': 'YELLOW', 'G': 'GREEN', 'B': 'BLUE', 'R' : 'RED', 'P': 'PURPLE'}
        color_list = [i for i in colors.values()]
        color_keys = [i for i in colors.keys()]
        print(win_counts, runner_up_counts, loser_counts)

        available_cards = self._get_available_betting_cards()
        betting_values = {}

        for color_name, cards in available_cards.items():
            if cards:
                betting_values[color_name] = cards.pop()
            else:
                betting_values[color_name] = 0

        win_probability, runner_up_probability, lose_probability = {}, {}, {}

        for color in colors.values():
            win_probability[color] = (win_counts[color] / number_of_simulations)
            runner_up_probability[color] = (runner_up_counts[color] / number_of_simulations)
            lose_probability[color] = (loser_counts[color] / number_of_simulations)

        expected_values = {}
        for color in colors.values():
            print(color, betting_values[color], win_probability[color], runner_up_probability[color], lose_probability[color])
            expected_values[color] = round(betting_values[color] * win_probability[color] + runner_up_probability[color] - lose_probability[color], 2)
        expected_values['ROLL'] = 1

        return expected_values

    def hint(self, expected_values):
        sorted_moves = sorted(expected_values.items(), key=lambda x: x[1], reverse=True)

        best_move = sorted_moves[0]
        second_best_move = sorted_moves[1] if len(sorted_moves) > 1 else None

        return best_move, second_best_move



board = Board()
board.initialize_camels()
board._test_init_players()
game_state = GameState(board)
n = 1000
results = game_state.multiple_simulations(n)
expected_val = game_state.expected_value(n, results[0], results[1], results[2])
print(f"Expected value: {game_state.hint(expected_val)}")
