from game.game_state import GameState
from game.item import Item
import game.character_class

from game.position import Position

def getDist(a: Position, b: Position):
    dx = abs(a.x - b.x)
    dy = abs(a.y - b.y)
    return max(dx, dy)