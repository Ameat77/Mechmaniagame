from abc import abstractmethod
from random import Random, random
from game.game_state import GameState
from game.item import Item
from strategy.functions import getDist
import game.character_class

from game.position import Position
from strategy.strategy import Strategy


class DumbKnightStrategy(Strategy):
    """Before the game starts, pick a class for your bot to start with.

    :returns: A game.CharacterClass Enum.
    """
    def strategy_initialize(self, my_player_index: int):
        return game.character_class.CharacterClass.KNIGHT

    """Each turn, decide if you should use the item you're holding. Do not try to use the
    legendary Item.None!

    :param gameState:     A provided GameState object, contains every piece of info on the game board.
    :param myPlayerIndex: You may find out which player on the board you are.

    :returns: If you want to use your item
    """
    def use_action_decision(self, game_state: GameState, my_player_index: int) -> bool:
        return False

    """Each turn, pick a position on the board that you want to move towards. Be careful not to
    fall out of the board!

    :param gameState:     A provided GameState object, contains every piece of info on the game board.
    :param myPlayerIndex: You may find out which player on the board you are.

    :returns: A game.Position object.
    """

    def move_action_decision(self, game_state: GameState, my_player_index: int) -> Position:
        player = game_state.player_state_list[my_player_index]
        pos = player.position
        if pos.x == 4 and pos.y == 4 and player.health == 9:
            return Position(4, 4)
        if pos.x == 4 and pos.y == 4:
            return Position(0, 0)
        else:
            return Position(pos.x + 1, pos.y + 1)

    """Each turn, pick a player you would like to attack. Feel free to be a pacifist and attack no
    one but yourself.

    :param gameState:     A provided GameState object, contains every piece of info on the game board.
    :param myPlayerIndex: You may find out which player on the board you are.

    :returns: Your target's player index.
    """

    def attack_action_decision(self, game_state: GameState, my_player_index: int) -> int:
        my_player = game_state.player_state_list[my_player_index]
        attackable_players = []
        for i, player in enumerate(game_state.player_state_list):
            if i == my_player_index:
                continue
            if getDist(my_player.position, player.position) <= my_player.stat_set.range:
                attackable_players.append(i) 
        if len(attackable_players) == 0:
            if my_player_index != 1:
                return 1
            else:
                return 0
        else:
            return attackable_players[Random().randint(0, len(attackable_players) - 1)]
        # return Random().randint(0, 3)
        

    """Each turn, pick an item you want to buy. Return Item.None if you don't think you can
    afford anything.

    :param gameState:     A provided GameState object, contains every piece of info on the game board.
    :param myPlayerIndex: You may find out which player on the board you are.

    :returns: A game.Item object.
    """

    def buy_action_decision(self, game_state: GameState, my_player_index: int) -> Item:
        return Item.NONE

