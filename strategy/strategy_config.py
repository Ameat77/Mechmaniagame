from strategy.dumb_knight import DumbKnightStrategy
from strategy.random_movement import RandomStrategy
from strategy.strategy import Strategy
from strategy.dumb_wizard import DumbWizardStrategyBR
from strategy.killer_wizard import *

"""Return the strategy that your bot should use.

:param playerIndex: A player index that can be used if necessary.

:returns: A Strategy object.
"""
def get_strategy(player_index: int) -> Strategy:  
  
  if player_index == 0:
    return DumbKnightStrategy()
  elif player_index == 1:
    return KillerWizardStrategyTL()
  elif player_index == 2:
    return DumbWizardStrategyBR()
  elif player_index == 3:
    return KillerWizardStrategyBL()
  else:
    return RandomStrategy()
  
