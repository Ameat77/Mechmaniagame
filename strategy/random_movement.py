from random import Random, random
from game.game_state import GameState
from strategy.functions import getDist
import game.character_class

from game.item import Item

from game.position import Position
from strategy.strategy import Strategy

class RandomStrategy(Strategy):
    def strategy_initialize(self, my_player_index: int):
        return game.character_class.CharacterClass.WIZARD

    def move_action_decision(self, game_state: GameState, my_player_index: int) -> Position:
        player = game_state.player_state_list[my_player_index]
        dx = Random().randint(0, player.stat_set.speed)
        dy = player.stat_set.speed - dx
        if random() < 0.5 and player.position.x - dx >= 0:
            dx = -dx
        if random() < 0.5 and player.position.y - dy >= 0:
            dy = -dy
        if player.position.x + dx > 9:
            dx = -dx
        if player.position.y + dy > 9:
            dy = -dy
        return Position(player.position.x + dx, player.position.y + dy)

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

    def buy_action_decision(self, game_state: GameState, my_player_index: int) -> Item:
        return Item.NONE

    def use_action_decision(self, game_state: GameState, my_player_index: int) -> bool:
        return False