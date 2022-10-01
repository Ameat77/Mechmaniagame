from abc import abstractmethod
from random import Random, random
from game.game_state import GameState
from game.player_state import PlayerState
from game.item import Item
from strategy.functions import getDist
from strategy.functions import canBeAttacked
from strategy.functions import killable
from strategy.functions import *
import game.character_class

import logging

from game.position import Position
from strategy.strategy import Strategy


class KillerWizardStrategyBL(Strategy):
    """Before the game starts, pick a class for your bot to start with.

    :returns: A game.CharacterClass Enum.
    """
    def strategy_initialize(self, my_player_index: int):
        return game.character_class.CharacterClass.WIZARD

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

        #go back to spawn if we can afford a rally banner
        if player.gold >= 8 and player.item == Item.NONE:
            return Position(0, 9)

        # for i, p in enumerate(game_state.player_state_list):
        #     logging.info(getRing(p))
        closest = 5
        closest_player = player
        distances = []
        for i, p in enumerate(game_state.player_state_list):
            if i == my_player_index:
                continue
            ring = getRing(p)
            # logging.info(ring)
            if ring < closest:
                closest = ring
                closest_player = p
            distances.append(ring)
        # logging.info("closest: " + str(closest))
        # logging.info("closest y: " + str(closest_player.position.y))
        
        if pos.x < 3 and pos.y > 6:
            if pos.x <= (9 - pos.y):
                return Position(pos.x + 2, pos.y - 1)
            else:
                return Position(pos.x + 1, pos.y - 2)

        # #someone on hill or one ring outside -> go outside of the hill
        if closest <= 1:
            return Position(3, 6)
        
        # #someone outside of 2 rings -> far center
        # #needs some more work
        if closest >= 3:
            return Position(4, 4)
        
        # # someone on second ring northern -> near center
        # logging.info("closest y: " + str(closest_player.position.y))
        if closest == 2 and closest_player.position.y == 2:
            return Position(4, 5)
        
        #otherwise retreat a little
        return Position(3, 6)

        # attacking_players = canBeAttacked(game_state, my_player_index)
        # for index in attacking_players:
        #     attacker = game_state.player_state_list[index]
        #     if attacker.stat_set.damage >= player.health:
        #         return Position(9, 9)

        

    """Each turn, pick a player you would like to attack. Feel free to be a pacifist and attack no
    one but yourself.

    :param gameState:     A provided GameState object, contains every piece of info on the game board.
    :param myPlayerIndex: You may find out which player on the board you are.

    :returns: Your target's player index.
    """

    def attack_action_decision(self, game_state: GameState, my_player_index: int) -> int:
        my_player = game_state.player_state_list[my_player_index]
        # attackable_players = []
        # for i, player in enumerate(game_state.player_state_list):
        #     if i == my_player_index:
        #         continue
        #     if getDist(my_player.position, player.position) <= my_player.stat_set.range:
        #         attackable_players.append(i) 
        # if len(attackable_players) == 0:
        #     return my_player_index
        # else:
        #     return attackable_players[Random().randint(0, len(attackable_players) - 1)]
        return killable(game_state.player_state_list, my_player_index)
        

    """Each turn, pick an item you want to buy. Return Item.None if you don't think you can
    afford anything.

    :param gameState:     A provided GameState object, contains every piece of info on the game board.
    :param myPlayerIndex: You may find out which player on the board you are.

    :returns: A game.Item object.
    """

    def buy_action_decision(self, game_state: GameState, my_player_index: int) -> Item:
        player = game_state.player_state_list[my_player_index]
        if player.gold < 8:
            return Item.NONE
        else:
            return Item.RALLY_BANNER

class KillerWizardStrategyTL(Strategy):
    """Before the game starts, pick a class for your bot to start with.

    :returns: A game.CharacterClass Enum.
    """
    def strategy_initialize(self, my_player_index: int):
        return game.character_class.CharacterClass.WIZARD

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

        #go back to spawn if we can afford a rally banner
        if player.gold >= 8 and player.item == Item.NONE:
            return Position(9, 0)

        # for i, p in enumerate(game_state.player_state_list):
        #     logging.info(getRing(p))
        closest = 5
        closest_player = player
        distances = []
        for i, p in enumerate(game_state.player_state_list):
            if i == my_player_index:
                continue
            ring = getRing(p)
            # logging.info(ring)
            if ring < closest:
                closest = ring
                closest_player = p
            distances.append(ring)
        # logging.info("closest: " + str(closest))
        # logging.info("closest y: " + str(closest_player.position.y))
        
        if pos.x > 6 and pos.y < 3:
            if (9 - pos.x) <= pos.y:
                return Position(pos.x - 2, pos.y + 1)
            else:
                return Position(pos.x - 1, pos.y + 2)

        # #someone on hill or one ring outside -> go outside of the hill
        if closest <= 1:
            return Position(6, 3)
        
        # #someone outside of 2 rings -> far center
        # #needs some more work
        if closest >= 3:
            return Position(4, 4)
        
        # # someone on second ring northern -> near center
        # logging.info("closest y: " + str(closest_player.position.y))
        if closest == 2 and closest_player.position.y == 2:
            return Position(5, 4)
        
        #otherwise retreat a little
        return Position(6, 3)

        # attacking_players = canBeAttacked(game_state, my_player_index)
        # for index in attacking_players:
        #     attacker = game_state.player_state_list[index]
        #     if attacker.stat_set.damage >= player.health:
        #         return Position(9, 9)

        

    """Each turn, pick a player you would like to attack. Feel free to be a pacifist and attack no
    one but yourself.

    :param gameState:     A provided GameState object, contains every piece of info on the game board.
    :param myPlayerIndex: You may find out which player on the board you are.

    :returns: Your target's player index.
    """

    def attack_action_decision(self, game_state: GameState, my_player_index: int) -> int:
        my_player = game_state.player_state_list[my_player_index]
        # attackable_players = []
        # for i, player in enumerate(game_state.player_state_list):
        #     if i == my_player_index:
        #         continue
        #     if getDist(my_player.position, player.position) <= my_player.stat_set.range:
        #         attackable_players.append(i) 
        # if len(attackable_players) == 0:
        #     return my_player_index
        # else:
        #     return attackable_players[Random().randint(0, len(attackable_players) - 1)]
        return killable(game_state.player_state_list, my_player_index)
        

    """Each turn, pick an item you want to buy. Return Item.None if you don't think you can
    afford anything.

    :param gameState:     A provided GameState object, contains every piece of info on the game board.
    :param myPlayerIndex: You may find out which player on the board you are.

    :returns: A game.Item object.
    """

    def buy_action_decision(self, game_state: GameState, my_player_index: int) -> Item:
        player = game_state.player_state_list[my_player_index]
        if player.gold < 8:
            return Item.NONE
        else:
            return Item.RALLY_BANNER
