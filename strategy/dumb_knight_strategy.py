from random import Random
from game.game_state import GameState
import game.character_class
from abc import abstractmethod

from game.item import Item

from game.position import Position
from strategy.strategy import Strategy


class DumbKnightStrategy(object):
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
        if (self.item == Item.NONE):
            return False
        return True

    """Each turn, pick a position on the board that you want to move towards. Be careful not to
    fall out of the board!

    :param gameState:     A provided GameState object, contains every piece of info on the game board.
    :param myPlayerIndex: You may find out which player on the board you are.

    :returns: A game.Position object.
    """

    def possible_moves(x, y, speed):
        moves = []
        for i in range(-speed, speed+1):
            for j in range(-speed, speed+1):
                new_pos = (x + i, y + j)
                if new_pos[0] > -1 and new_pos[0] < 10 and new_pos[1] > -1 and new_pos[1] < 10:
                    moves.append(new_pos)
        return moves
                    

    def most_central(moves):
        center = (4.5, 4.5)
        best_move = (-1, -1)
        lowest = 1000
        for i in range(len(moves)):
            d = (abs(center[0] - moves[0]), abs(center[1] - moves[1]))
            if d < lowest:
                lowest = d
                best_move = moves[i]
        return best_move



    @abstractmethod
    def move_action_decision(self, game_state: GameState, my_player_index: int) -> Position:
        KNIGHT = (9, 6, 2, 1) #Health, Damage, Speed, Range
        position = (game_state.player_state_list[my_player_index].position.x, game_state.player_state_list[my_player_index].position.y)
        moves = DumbKnightStrategy.possible_moves(position[0], position[1], KNIGHT[2])
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
        KNIGHT = (9, 6, 2, 1) #Health, Damage, Speed, Range
        #WIZARD = (6, 4, 3, 2)
        #ARCHER = (3, 2, 4, 3)
        player_list = game_state.player_state_list
        my_position = (player_list[my_player_index].position.x, player_list[my_player_index].position.y)
        in_range = [] #Players who are in range to hit
        can_kill = [] #Players who are in range and I can kill
        for i in range(len(player_list)):
            their_position = (player_list[i].position.x, player_list[i].position.y)
            d = max(abs(their_position[0] - my_player_index[0]), abs(their_position[1] - my_player_index[1]))
            if d <= KNIGHT[3] and i != my_player_index:
                in_range.append(i)
                health = player_list[i].health
                if health <= KNIGHT[1]:
                    can_kill.append(i)
        if len(can_kill) >= 1:
            return can_kill[0]
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
        gold = player_list[my_player_index]
        pass


   
