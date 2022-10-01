from random import Random
from game.game_state import GameState
import game.character_class
from abc import abstractmethod

from game.item import Item

from game.position import Position
import player
from strategy.strategy import Strategy
from game.character_class import CharacterClass


class DumbKnightStrategy(Strategy):
    """Before the game starts, pick a class for your bot to start with.

    :returns: A game.CharacterClass Enum.
    """
    @abstractmethod
    def strategy_initialize(self, my_player_index: int):
        return game.character_class.CharacterClass.KNIGHT

    """Each turn, decide if you should use the item you're holding. Do not try to use the
    legendary Item.None!

    :param gameState:     A provided GameState object, contains every piece of info on the game board.
    :param myPlayerIndex: You may find out which player on the board you are.

    :returns: If you want to use your item
    """
    @abstractmethod
    def use_action_decision(self, game_state: GameState, my_player_index: int) -> bool:
        player_list = game_state.player_state_list
        if (player_list[my_player_index].item == Item.NONE):
            return False
        return True

    """Each turn, pick a position on the board that you want to move towards. Be careful not to
    fall out of the board!

    :param gameState:     A provided GameState object, contains every piece of info on the game board.
    :param myPlayerIndex: You may find out which player on the board you are.

    :returns: A game.Position object.
    """

    def possible_moves(x, y, speed):
        moves = set()
        pairs = []
        for i in range(speed + 1):
            pairs.append((i, speed - i))
        for i in range(len(pairs)):
            new_pos = (x + pairs[i][0], y + pairs[i][1])
            if new_pos[0] >= 0 and new_pos[0] < 10 and new_pos[1] >= 0 and new_pos[1] < 10:
                moves.add(new_pos)
            new_pos = (x - pairs[i][0], y - pairs[i][1])
            if new_pos[0] >= 0 and new_pos[0] < 10 and new_pos[1] >= 0 and new_pos[1] < 10:
                moves.add(new_pos)
            new_pos = (x - pairs[i][0], y + pairs[i][1])
            if new_pos[0] >= 0 and new_pos[0] < 10 and new_pos[1] >= 0 and new_pos[1] < 10:
                moves.add(new_pos)
            new_pos = (x + pairs[i][0], y - pairs[i][1])
            if new_pos[0] >= 0 and new_pos[0] < 10 and new_pos[1] >= 0 and new_pos[1] < 10:
                moves.add(new_pos)
        return moves
                    

    def most_central(moves):
        center = (4.5, 4.5)
        best_move = (-1, -1)
        lowest = 1000
        for move in moves:
            dd = (abs(center[0] - float(move[0])), abs(center[1] - float(move[1])))
            d = pow(dd[0], 2) + pow(dd[1], 2)
            if d < lowest:
                lowest = d
                best_move = move
        return best_move



    @abstractmethod
    def move_action_decision(self, game_state: GameState, my_player_index: int) -> Position:
        starting_point = (-1, -1)
        if my_player_index == 0:
            starting_point = (0, 0)
        if my_player_index == 1:
            starting_point = (9, 0)
        if my_player_index == 2:
            starting_point = (9, 9)
        if my_player_index == 3:
            starting_point = (0, 9)
        player_list = game_state.player_state_list
        current_stats = player_list[my_player_index].stat_set
        health, damage, speed, rangee = player_list[my_player_index].health, current_stats.damage, current_stats.speed, current_stats.range
        item_stats = str(player_list[my_player_index].item)
        if item_stats == "Item.ANEMOI_WINGS":
            speed += 1
        if item_stats == "Item.RALLEY_BANNER":
            damage += 2
        if item_stats == "Item.HUNTING_SCOPE":
            rangee += 1
        position = (game_state.player_state_list[my_player_index].position.x, game_state.player_state_list[my_player_index].position.y)
        if position == starting_point and player_list[my_player_index].gold > 8 and player_list[my_player_index].item == Item.NONE:
            return Position(starting_point[0], starting_point[1])
        moves = DumbKnightStrategy.possible_moves(position[0], position[1], speed)
        best_move = DumbKnightStrategy.most_central(moves)
        return Position(best_move[0], best_move[1])


    """Each turn, pick a player you would like to attack. Feel free to be a pacifist and attack no
    one but yourself.

    :param gameState:     A provided GameState object, contains every piece of info on the game board.
    :param myPlayerIndex: You may find out which player on the board you are.

    :returns: Your target's player index.
    """
    @abstractmethod
    def attack_action_decision(self, game_state: GameState, my_player_index: int) -> int:
        player_list = game_state.player_state_list
        current_stats = player_list[my_player_index].stat_set
        health, damage, speed, rangee = player_list[my_player_index].health, current_stats.damage, current_stats.speed, current_stats.range
        item_stats = str(player_list[my_player_index].item)
        if item_stats == "Item.ANEMOI_WINGS":
            speed += 1
        if item_stats == "Item.RALLEY_BANNER":
            damage += 2
        if item_stats == "Item.HUNTING_SCOPE":
            rangee += 1
        my_position = (player_list[my_player_index].position.x, player_list[my_player_index].position.y)
        in_range = [] #Players who are in range to hit
        can_kill = [] #Players who are in range and I can kill
        for i in range(len(player_list)):
            their_position = (player_list[i].position.x, player_list[i].position.y)
            d = max(abs(their_position[0] - my_position[0]), abs(their_position[1] - my_position[1]))
            if d <= rangee and i != my_player_index:
                in_range.append(i)
                health = player_list[i].health
                if health <= damage:
                    can_kill.append(i)
        if len(can_kill) >= 1:
            return can_kill[0]
        if len(in_range) >= 1:
            return in_range[0]
        return None



    """Each turn, pick an item you want to buy. Return Item.None if you don't think you can
    afford anything.

    :param gameState:     A provided GameState object, contains every piece of info on the game board.
    :param myPlayerIndex: You may find out which player on the board you are.

    :returns: A game.Item object.
    """
    @abstractmethod
    def buy_action_decision(self, game_state: GameState, my_player_index: int) -> Item:
        player_list = game_state.player_state_list
        gold = player_list[my_player_index].gold
        if gold >= 8 and player_list[my_player_index].item == Item.NONE:
            return Item.ANEMOI_WINGS
        return Item.NONE


   
