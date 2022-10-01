from game.game_state import GameState
from game.item import Item
import game.character_class
from game.player_state import PlayerState
from typing import List

from game.position import Position

def getDist(a: Position, b: Position):
    dx = abs(a.x - b.x)
    dy = abs(a.y - b.y)
    return max(dx, dy)
def canBeAttacked(game_state: GameState, my_player_index: int) -> List[int]:
    players = game_state.player_state_list
    attacking_players = []
    for i, p in enumerate(players):
        if i == my_player_index:
            continue
        if p.stat_set.range >= getDist(p.position, players[my_player_index].position):
            attacking_players.append(i)
    return attacking_players
def canAttack(player_state_list: List[PlayerState], my_player_index: int) -> List[int]:
    this_player = player_state_list[my_player_index]
    victims = []
    for i, player in enumerate(player_state_list):
        if i == my_player_index:
            continue
        if getDist(player.position, this_player.position) <= this_player.stat_set.range:
            victims.append(i)
    return victims
def killable(player_state_list: List[PlayerState], my_player_index: int) -> int:
    this_player = player_state_list[my_player_index]
    victims = canAttack(player_state_list, my_player_index)
    for index in victims:
        victim = player_state_list[index]
        if victim.health <= this_player.stat_set.damage:
            return index
    #if no one is killable, get the first player I can attack
    if len(victims) != 0:
        return victims[0]
    else:
        return my_player_index
def getRing(player: PlayerState) -> int:
    pos = player.position
    dx = 0
    dy = 0
    if pos.x >= 5:
        dx = abs(pos.x - 5)
    else:
        dx = abs(pos.x - 4)
    if pos.y >= 5:
        dy = abs(pos.y - 5)
    else:
        dy = abs(pos.y - 4)
    return max(dx, dy)