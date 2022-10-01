from strategy.dumb_knight_strategy import DumbKnightStrategy
from strategy.starter_strategy import StarterStrategy
from strategy.strategy import Strategy
from strategy.smart_knight_strategy import SmartKnightStrategy
from strategy.dumb_wizard import DumbWizardStrategyBR
from strategy.killer_wizard import KillerWizardStrategyBL

"""Return the strategy that your bot should use.

:param playerIndex: A player index that can be used if necessary.

:returns: A Strategy object.
"""
def get_strategy(player_index: int):  
    return SmartKnightStrategy()
