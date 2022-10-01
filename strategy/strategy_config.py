from strategy.dumb_knight import DumbKnightStrategy
from strategy.random_movement import RandomStrategy
from strategy.strategy import Strategy
# from strategy.dumb_wizard import DumbWizardStrategyBR

"""Return the strategy that your bot should use.

:param playerIndex: A player index that can be used if necessary.

:returns: A Strategy object.
"""
def get_strategy(player_index: int) -> Strategy:  
  
  if player_index == 0:
    return DumbKnightStrategy()
  else:
    return RandomStrategy()
  # elif player_index == 2:
  #   return RandomStrategy()
  # return DumbWizardStrategyBR()
