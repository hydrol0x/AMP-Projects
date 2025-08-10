from Camel import Camel, Color
from SpectatorTile import SpectatorTile
from BettingCards import BettingCards
from Pyramid import Pyramid
from enum import Enum, auto
from Player import Player
# from Simulation import GameState
# from rich.console import Console

class Bet():
    def __init__(self):
        self.card: tuple[Color, int] | None = None
        self.color: Color | None = None

class BetFinish():
    def __init__(self):
        self.color: Color | None = None
        self.bet_type: bool = True # Bet on winner (True), bet on loser (False)

class PlaceCard():
    def __init__(self):
        self.position: int | None = None
        self.side: bool | None = None # Place +1 side up (True) -1 side up (False)

class MoveType(Enum):
    ROLL = auto()
    BET = Bet()
    PLACE_CARD = PlaceCard()
    BET_FINISH = BetFinish()
    # AI_HINT = auto()

class Board:
    def __init__(self):
        self.pyramid: Pyramid = Pyramid()
        self.cards: BettingCards = BettingCards()
        self.camels: list[Camel] = list()
        self.spectators: list[SpectatorTile] = list()
        self.is_game_over: bool = False
        self.current_player: int = 0
        self.num_players: int = 0
        self.players: list[Player] = []
        self.colors: list[Color] = [Color.RED, Color.YELLOW, Color.GREEN, Color.BLUE, Color.PURPLE]
        self.color_dictionary: dict[str, str] = {'R': '🔴', 'Y': '🟡', 'P': '🟣', 'G': '🟢', 'B': '🔵'}
        self.finish_cards_winner: list[tuple[Color, Player]] = list()
        self.finish_cards_loser: list[tuple[Color, Player]] = list()
        self.scores: dict[str, int ]= {}
        self.reset_board()

    def stack_to_str(self, camel: Camel, stack: str = "") -> str:
        stack = str(camel.color) + stack
        if camel.stacked_on_me:
           return self.stack_to_str(camel.stacked_on_me, stack)
        temp_stack = stack
        stack = ''
        for i in temp_stack:
            stack += self.color_dictionary[i]
        return stack

    def visualize_bets(self):
        bets: list[tuple[str, dict[Color, list[int]]]] = []
        for player in self.players:
            bets.append((f"Player {player.get_name()}", player.get_current_bets()))
        return bets

    def stacked_below(self, above_camel: Camel) -> Camel | None:
        for camel in self.camels:
            if camel.stacked_on_me == above_camel:
                return camel

    def visualize_board(self):
        visual_track = [f".{i}." for i in range(1, 17)]
        for camel in self.camels:
            if not self.stacked_below(camel):
                pos = camel.get_position()
                if 0 <= pos < len(visual_track):  # Added a bound check in case we get index out of bounds
                    visual_track[pos] = self.stack_to_str(camel)
        for spec_tile in self.spectators:
            spec_val = spec_tile.tile_value()
            show = None
            if spec_val:
                show = "+1"
            else:
                show = "-1"
            if spec_tile.tile_position() is not None:
                visual_track[spec_tile.tile_position()] = show
        return visual_track

    def visualize_board_1(self):
        visual_track = [f"{i} " for i in range(1, 17)]
        for camel in self.camels:
            if not self.stacked_below(camel):
                visual_track[camel.get_position()] += self.stack_to_str(camel)

        for spec_tile in self.spectators:
            spec_val = spec_tile.tile_value()
            show = None
            if spec_val:
                show = "+1"
            else:
                show = "-1"
            if spec_tile.tile_position() != None:
                visual_track[spec_tile.tile_position()] = show
        return visual_track

    def visualize_board_1(self):
        visual_track = []

        for pos in range(1, 17):
            position_str = f" {pos:2d}: "
            camel_stack = ""
            spectator_info = ""

            for camel in self.camels:
                if camel.get_position() == pos and not self.stacked_below(camel):
                    camel_stack = self.stack_to_str(camel)
                    camel_stack = camel_stack[::-1]
                    break

            for spec_tile in self.spectators:
                if spec_tile.tile_position() == pos:
                    spec_val = spec_tile.tile_value()
                    spectator_info = " [+1]" if spec_val else " [-1]"
                    break

            if camel_stack:
                line = f"{position_str}{camel_stack}{spectator_info}"
            elif spectator_info:
                line = f"{position_str}---{spectator_info}"
            else:
                line = f"{position_str}---"

            visual_track.append(line)

        return visual_track

    def get_current_player(self) -> Player:
        return self.players[self.current_player]

    def add_players(self):
        to_add = True
        while to_add:
            print("\n1. Add Players\n2. Start Game\n")
            try:
                action = int(input("Pick an action\n"))
            except ValueError:
                print("Please pick a valid option by typing it's number from the list above")
                continue
            match action:
                case 1:
                    player_name = input("Player Name: ")
                    self.players.append(Player(player_name))
                    self.num_players+=1
                case 2:
                    if not self.num_players < 2:
                        to_add = False
                    else:
                        print("Not enough players. Please add more.\n")
                case _:
                    print("Invalid option!")
                    continue

    def initialize_camels(self):
        while tup := self.pyramid.roll_dice():
            color, number = tup
            current_camel = Camel(color)
            self.handle_occupied_tile(current_camel, number)
            current_camel.move_camel(number)
            self.camels.append(current_camel)
        self.pyramid.reset_dice()

    def _test_init_players(self):
        self.players.append(Player("test1"))
        self.players.append(Player("test2"))
        self.num_players = len(self.players)

    def _test_initialize_stack(self):
        for i, color in enumerate(self.colors):
            camel = Camel(color)
            if len(self.camels) > 0:
                camel.stacked_on_me = self.camels[i-1]
            self.camels.append(camel)

    def advance_player(self):
        self.current_player = (self.current_player + 1) % self.num_players

    def prompt_player(self) -> MoveType:
        while True:
            print("\n1. Roll dice\n2. Place a bet\n3. Place your spectator card\n4. Bet on winner/loser\n5. Get advice on the best move to make")
            try:
                move_selected: int = int(input("\nPick an action\n"))
            except ValueError:
                print("Please pick a valid option by typing it's number from the list above")
                continue
            match move_selected:
                case 1: # player chose to roll the dice
                    return MoveType.ROLL
                case 2: # player chose to make a bet
                    move = MoveType.BET
                    color_ask = True
                    while color_ask:
                        color_index = int(input("What color camel would you like to bet on?\n1. Red\n2. Yellow\n3. Green\n4. Blue\n5. Purple\n")) # prompt the user for a color
                        user_color = self.colors[color_index-1]
                        move.value.card = self.cards.remove(user_color)
                        if move.value.card is not None: # if remove returns None, that means that the user cannot take any more of that color card
                            color_ask = False
                        else:
                            print("There are no more betting cards of that color. Pick again.\n")
                    return move
                case 3: # player chose to place a spectator tile
                    move = MoveType.PLACE_CARD
                    user_position = None
                    user_side = None
                    free_space_list = self.free_spaces()
                    print_string = ', '.join(map(str, free_space_list))
                    # print(free_space_list)

                    player = self.get_current_player()
                    if not player.spectator_card_played: # if the player has not played their spectator tile yet
                        # We need to check if the tile that they are putting the tile on is valid, because two spectactor tiles can't be adjacent to one another
                        user_position = int(input(f'On what space would you like to place your spectator tile?\nThe spaces {print_string} are availible.\n')) # prompt the user for a position

                        while user_position not in free_space_list:
                            user_position = int(input('That is not a valid space for a spectator tile. Please pick again.\n'))
                        user_side = bool(int(input('What side of the tile would you like to use?\n1. -1\n2. +1\n'))-1) # true is +1 false is -1
                    else: # if the player has played their spectator tile already, they can move it or flip it
                        choice = int(input("Would you like to move or flip your spectator tile?\n1. Move Tile\n2. Flip Tile\n"))
                        if choice == 1:
                            user_position = int(input('On what space would you like to move your spectator tile to?\nThe spaces {print_string} are availible.\n')) # prompt the user for a position
                            while user_position not in free_space_list:
                                user_position = int(input('That is not a valid space for a spectator tile. Please pick again.\n'))
                        elif choice == 2:
                            print(f"Flipped card to {"-1" if player.spectator_card_value else "+1"}")
                            user_side = not player.spectator_card_value
                    move.PLACE_CARD.value.position = user_position
                    move.PLACE_CARD.value.side = user_side
                    return move
                case 4: # player chose to place down a finish card (bet on overall winer or loser)
                    move = MoveType.BET_FINISH
                    bet_type = bool(int(input("Would you like to bet on an overall winner or loser?\n1. Overall Loser\n2. Overall Winner\n"))-1)
                    move.BET_FINISH.value.bet_type = bet_type
                    availible_cards = self.get_current_player().get_availible_finish_cards()
                    print(availible_cards)
                    color_index = int(input("What finish card would you like to put down?\n1. Red\n2. Yellow\n3. Green\n4. Blue\n5. Purple\n")) # prompt the user for a color
                    user_color = self.colors[color_index-1]
                    while user_color not in availible_cards:
                        color_index = int(input("You do not hold a finish card of that color. Try Again.\nWhat finish card would you like to put down?\n1. Red\n2. Yellow\n3. Green\n4. Blue\n5. Purple\n")) # prompt the user for a color
                        user_color = self.colors[color_index-1]
                    move.BET_FINISH.value.color = user_color
                    return move
                case 5: # player wants help from the AI
                    return None
                    return MoveType.AI_HINT
                case _:
                    print("Please pick a valid option by typing it's number from the list above")
                    print(f"{move_selected} is not a valid option in list!")
                    continue

    def free_spaces(self): # returns free spaces that a spectator tile can be placed in
        availible = list(range(2,17))
        for camel in self.camels:
            if camel.get_position() in availible:
                availible.remove(camel.get_position())
        for spec_tile in self.spectators:
            pos = spec_tile.tile_position()
            if pos in availible:
                availible.remove(pos)
            if pos-1 in availible: # spectator tiles cannot be placed next to one another
                availible.remove(pos-1)
            if pos+1 in availible:
                availible.remove(pos+1)
        return availible


    def handle_occupied_tile(self, camel: Camel, number: int):
        for other_camel in self.camels:
            if other_camel is not camel and other_camel.position == camel.position + number and other_camel.stacked_on_me is None:
                other_camel.stacked_on_me = camel
                break

    def handle_roll_dice(self, color: Color, number: int):
        camel = self.get_camel(color)
        assert camel is not None, "Camel should never be none because get_camel never returns None"

        # we have to check if there were any camels below before the move and update them
        if below:=self.stacked_below(camel):
            below.set_stacked_on_me(None)

        # We check if there is a camel already on that tile. In that case, the new camel stacks on top of it
        self.handle_occupied_tile(camel, number)
        # for other_camel in self.camels:
        #     if other_camel is not camel and other_camel.position == camel.position + number and other_camel.stacked_on_me is None:
        #         # print(f"setting {other_camel} stack on {camel} because we landed back on it")
        #         # print(f"other camel is {other_camel}, other_camel.stacked_on_me = {other_camel.stacked_on_me}")
        #         # print(f"present camel is {camel}, camel.stacked_on_me = {camel.stacked_on_me}")
        #         # other_camel.set_stacked_on_me(camel)
        #         other_camel.stacked_on_me = camel
        #         break

        print(f"moving {camel} by {number}")
        camel.move_camel(number)

        # Add game over check
        if camel.get_position() >= 16:
            self.is_game_over = True

        for spec_tile in self.spectators:
            if camel.get_position() == spec_tile.tile_position():
                if spec_tile.tile_value():
                    camel.move_camel(1) # moves camel up one space forward if it lands on a +1 spectator tile
                    # TODO: put camel on top of other camels if they are on the square ahead
                else:
                    camel.move_camel(-1) # moves camel up one space backward if it lands on a -1 spectator tile
                    # TODO: put camel below other camels if they are on the square before

    def play_turn(self):
        # Get move
        # print(*self.visualize_board(), sep="")
        move = self.prompt_player()

        if move == MoveType.ROLL:
            self.get_current_player().add_money(1)
            if tup := self.pyramid.roll_dice():
                color, number = tup
                self.handle_roll_dice(color, number)
            else:
                self.pyramid.reset_dice()
        elif move == MoveType.BET:
            card = move.value.card
            assert card is not None, "Unreachable. Card should never be none after being chosen by user"
            color = card[0]
            bet_card_value = card[1]
            self.get_current_player().current_bets[color].append(bet_card_value)
        # else:
        #     self.get_current_player().current_bets.append(move.BET.value.card)
            # self.get_current_player().current_bets.append(move.value.card)
        elif move == MoveType.PLACE_CARD:
            if not self.get_current_player().spectator_card_played: # if card hasn't been placed yet
                self.spectators.append(SpectatorTile(move.PLACE_CARD.value.position, move.PLACE_CARD.value.side))
                self.get_current_player().spectator_card_played = True
                pos = move.PLACE_CARD.value.position
                side = move.PLACE_CARD.value.side
                assert pos is not None, "Should never be None"
                assert side is not None, "Should never be None"
                self.get_current_player().add_spectator_card(pos, side)
            else: # if card has already been played
                cur = self.get_current_player()
                cur_pos = cur.get_spectator_card_position()
                if move.PLACE_CARD.value.position: # if user changing position of spec tile
                    value = cur.get_spectator_card_value()
                    assert value is not None, "Should never be None"
                    cur.add_spectator_card(move.PLACE_CARD.value.position, value)
                    for spec_tile in self.spectators:
                        if spec_tile.tile_position() == cur_pos:
                            spec_tile.set_position(move.PLACE_CARD.value.position)
                else: # if user flipping spec tile
                    for spec_tile in self.spectators:
                        if spec_tile.tile_position() == cur_pos:
                            spec_tile.flip_tile()
                    pos = cur.get_spectator_card_position()
                    side = move.PLACE_CARD.value.side
                    assert pos is not None, "Should never be None"
                    assert side is not None, "Should never be None"
                    cur.add_spectator_card(pos, side)
        elif move == MoveType.BET_FINISH:
            cur = self.get_current_player()
            if move.BET_FINISH.value.bet_type: # if the player chose to bet on an overall winner
                winning_color = move.BET_FINISH.value.color
                assert winning_color is not None, "Should never be None"
                cur.set_overall_winner(winning_color)
                self.finish_cards_winner.append((winning_color, cur))
            else: # if the player chose to bet on an overall loser
                loser = move.BET_FINISH.value.color
                assert loser is not None, "Should never be None"
                cur.set_overall_loser(loser)
                self.finish_cards_loser.append((loser, cur))
        # else:
        #     game_state = GameState(board)
        #     results = game_state.multiple_simulations(n)
        #     expected_val = game_state.expected_value(n, results[0], results[1], results[2])
        #     print(f"Expected value: {game_state.hint(expected_val)}")
        print(*self.visualize_board_1(), sep=" | ")
        print(f"Bets {self.visualize_bets()}")

        self.advance_player()

    # def move_camels_on_top(self, camel, move_amount):
    #     if camel.stacked_on_me == None:
    #         return 0
    #     else:
    #         new_camel = camel.stacked_on_me
    #         new_camel.position += move_amount
    #         # need to update self.track
    #         self.move_camels_on_top(new_camel, move_amount)

    def get_camel(self, camel_color: Color): # returns the camel pbject for the color passed through
        for object in self.camels:
            if getattr(object, 'color') == camel_color:
                return object


    def is_leg_over(self):
        return len(self.pyramid.dice) == 0

    def reset_board(self):
        self.cards.reset_cards()
        self.spectators = list() # reset spectator tiles
        for player in self.players:
            player.spectator_card_played = False
            player.spectator_card_position = None
            player.spectator_card_value = None
            player.current_bets = {} 

    def get_top_of_stack(self, camel: Camel) -> Camel:
        """ Traverses camel stack to get to the top"""
        if camel.stacked_on_me is None:
            return camel
        return self.get_top_of_stack(camel.stacked_on_me)

    def get_winners(self) -> tuple[Camel, Camel]:
        """
        Get first and second place camels
        """
        
        tops: list[Camel] = []
        for camel in self.camels:
            if camel not in tops:
                tops.append(self.get_top_of_stack(camel))
        tops.sort(key=lambda camel: camel.position, reverse=True)
        first = tops[0]
        if second:=self.stacked_below(first):
            return (first,second)
        else:
            return (first, tops[1]) # the second place camel, if not stacked below first, is the one at the next greatest position
# 
    def calculate_score(self) -> dict[str, int]:
        first, second = self.get_winners()
        print(f"winning camel is {first}")
        print(f"second place camel is {second}")

        if self.is_game_over:
            print("the game is over")
            self.overall_betting_scoring(first.color, self.finish_cards_winner)
            self.overall_betting_scoring(first.color, self.finish_cards_loser)
        # only runs once a leg has finished
        if self.is_leg_over():
            # print(self.visualize_board_1())
            print("\nOne leg completed\n")

            for player in self.players:
                bet_list = player.get_current_bets()
                for color, bet_amounts in bet_list.items():
                    # if the winning camel color is the same as the color of the betting card, add the bet amount
                    if color == first.color:
                        player.add_money(sum(bet_amounts)) # Add up all the maximum bets
                    elif color == second.color:
                        player.add_money(len(bet_amounts)) # Adds dollar for each bet the player had on camel
                    else:
                        player.add_money(-len(bet_amounts))
                self.scores[player.get_name()] = player.get_money()
        print(self.scores)
        return self.scores

    def overall_betting_scoring(self, winner_color, finish_card_list) -> None:
        scores = [2, 3, 5, 8]
        for card_color, player in finish_card_list:
            if card_color == winner_color: # if the player has put down a matching card for the winning camel
                if scores:
                    player.add_money(scores.pop())
                else:
                    player.add_money(1)
            else:
                player.add_money(-1)

    # gets the winner of the game (whoever has the most money)
    def get_winner(self):
        scores = self.calculate_score()
        print(f"scores are {scores}")
        max_key = max(scores, key=lambda camel: scores[camel])
        print("The winner is " + str(max_key) + " with a total of " + str(scores[max_key]) + " coins")
        return max_key


if __name__ == "__main__":
    game = Board()
    # console = Console()
    game.add_players()
    game.initialize_camels()
    # game._test_init_players()
    # print(f"initial board pos")
    # print(*game.visualize_board(), sep=" | ")
    # print(f"init camels")
    # print(game.camels)
    # print(f"initial board pos")
    print(*game.visualize_board_1(), sep="\n")
    # print(f"init camels")
    # print(game.camels)
    # game._test_initialize_stack()
    # print(f"Camels are {game.camels}")
    # # print(f"the first camel is {game.camels[0]}")
    # # print(game.stack_to_str(game.camels[-1]))
    # print(*game.visualize_board(), sep='')
    # game.play_turn()

    # game.stack_to_str(game.camels[0])
    # print(game.visualize_board())
    # print(f"=== init positions ===")
    # for camel in game.camels:
    #     print(f"{camel}", end=" | ")
    # print(f"\n\n moving the third camel green camel 2 spots")
    # game.handle_roll_dice(Color.GREEN, 2)
    # for camel in game.camels:
    #     print(f"{camel}", end=" | ")
    # print("\n" + str(game.visualize_board()))
    # print(f"\n\n moving the BLUE camel 2 spots")
    # game.handle_roll_dice(Color.BLUE, 2)
    # for camel in game.camels:
    #     print(f"{camel}", end=" | ")
    # print(game.visualize_board())
    # # print(f"=== new positions ===")
    # print("players")
    # print([player.get_money() for player in game.players])
    print(game.visualize_board_1())
    while not game.is_game_over:
        game.play_turn()
        for player in game.players:
            print(f"{player}'s score is {player.get_money()}")
        if game.is_leg_over():
            game.calculate_score()
            game.reset_board()
    print(game.get_winner())
