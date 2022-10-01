from strategy.dumb_knight import DumbKnightStrategy
from strategy.random_movement import RandomStrategy
from strategy.smart_knight_strategy import SmartKnightStrategy
from strategy.strategy import Strategy
from strategy.dumb_wizard import DumbWizardStrategyBR
from strategy.killer_wizard import *
from strategy.smart_knight_strategy import SmartKnightStrategy

"""Return the strategy that your bot should use.

:param playerIndex: A player index that can be used if necessary.

:returns: A Strategy object.
"""
def get_strategy(player_index: int) -> Strategy:  
    return SmartKnightStrategy()
  