from random import Random
from turtle import position
from game.game_state import GameState
import game.character_class
from abc import abstractmethod

from game.item import Item

from game.position import Position
import player
from strategy.strategy import Strategy
from game.character_class import CharacterClass


class SmartKnightStrategy(Strategy):
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
        position = (player_list[my_player_index].position.x, player_list[my_player_index].position.y)
        center = [(4, 4), (4, 5), (5, 4), (5, 5)]
        if (player_list[my_player_index].item == Item.NONE):
            return False
        if (player_list[my_player_index].item == Item.SHIELD and position in center):
            return True
        if (player_list[my_player_index].item == Item.STRENGTH_POTION and position in center):
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
        center = [(4, 4), (4, 5), (5, 4), (5, 5)]
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
        if item_stats == "Item.HUNTER_SCOPE":
            rangee += 1
        position = (game_state.player_state_list[my_player_index].position.x, game_state.player_state_list[my_player_index].position.y)
        if position == starting_point and player_list[my_player_index].gold >= 5 and player_list[my_player_index].item == Item.NONE:
            return Position(starting_point[0], starting_point[1])
        moves = SmartKnightStrategy.possible_moves(position[0], position[1], speed)
        moves.add(starting_point)
      #  if health < 5:
       #     return Position(starting_point[0], starting_point[1])
        prediction_dic = {}
        predictions = []
        danger_area = {}
        for i in range(4):
            if i != my_player_index:
                their_position = (game_state.player_state_list[i].position.x, game_state.player_state_list[i].position.y)
                if their_position in center:
                    prediction_dic[i] = their_position
                else:
                    their_speed = player_list[i].stat_set.speed
                    their_range = player_list[i].stat_set.range
                    their_damage = player_list[i].stat_set.damage
                    item_stats = str(player_list[i].item)
                    if item_stats == "Item.ANEMOI_WINGS":
                        their_speed += 1
                    if item_stats == "Item.RALLEY_BANNER":
                        their_damage += 2
                    if item_stats == "Item.HUNTER_SCOPE":
                        their_range += 1
                    their_moves = SmartKnightStrategy.possible_moves(their_position[0], their_position[1], their_speed)
                    their_best_move = SmartKnightStrategy.most_central(their_moves)
                    prediction_dic[i] = their_best_move
                    predictions.append(their_best_move)
                    for i in range(-their_range, their_range + 1):
                        for j in range(-their_range, their_range + 1):
                            hit_zone = (their_best_move[0] + i, their_best_move[1] + j)
                            if hit_zone[0] >= 0 and hit_zone[0] < 10 and hit_zone[1] >= 0 and hit_zone[1] < 10:
                                if hit_zone in danger_area:
                                    danger_area[hit_zone] += 1
                                else:
                                    danger_area[hit_zone] = 1
        score_dic = {}
        for move in moves:
            score = 0
            weight_danger = -20
            weight_hits = 5
            weight_dist_center = 8
            weight_kill = 2
            weight_in_center = 30
            can_hit = 0
            can_kill = 0
            if move in danger_area:
                score += weight_danger * danger_area[move]
            else:
                weight_in_center = 40
            for i in range(-rangee, rangee + 1):
                    for j in range(-rangee, rangee + 1):
                        hit_zone = (move[0] + i, move[1] + j)
                        if hit_zone[0] >= 0 and hit_zone[0] < 10 and hit_zone[1] >= 0 and hit_zone[1] < 10:
                            if hit_zone in predictions:
                                can_hit += 1
                                if my_player_index != 0 and prediction_dic[0] == move and damage > player_list[0].health:
                                    can_kill += 1
                                if my_player_index != 1 and prediction_dic[1] == move and damage > player_list[1].health:
                                    can_kill += 1
                                if my_player_index != 2 and prediction_dic[2] == move and damage > player_list[2].health:
                                    can_kill += 1
                                if my_player_index != 3 and prediction_dic[3] == move and damage > player_list[3].health:
                                    can_kill += 1
            if move in center:
                score += weight_in_center
            score += can_kill * weight_kill
            score += can_hit * weight_hits

            dist1 = abs(move[0] - 4) + abs(move[1] - 4)
            dist2 = abs(move[0] - 4) + abs(move[1] - 5)
            dist3 = abs(move[0] - 5) + abs(move[1] - 4)
            dist4 = abs(move[0] - 5) + abs(move[1] - 5)
            dist = min(dist1, dist2, dist3, dist4)
            score += (10-dist) * weight_dist_center
            score_dic[move] = score # Last line of for-loop
        
        
        
        high_score = -10000 #Whichever move has the highest score will be selected
        the_move = (-1, -1)
        for key in score_dic:
            if score_dic[key] > high_score:
                high_score = score_dic[key]
                the_move = key
        return Position(the_move[0], the_move[1])

                                    



                        
                
                        




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
        if item_stats == "Item.HUNTER_SCOPE":
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
        most_points = -1
        to_kill = -1
        if len(can_kill) >= 1:
            for index in can_kill:
                if player_list[index].score > most_points:
                    most_points = player_list[index].score
                    to_kill = index
            return to_kill
        if len(in_range) >= 1:
            for index in in_range:
                if player_list[index].score > most_points:
                    most_points = player_list[index].score
                    to_kill = index
            return to_kill
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
            return Item.HUNTER_SCOPE
        elif gold >= 5 and player_list[my_player_index].item == Item.NONE:
            return Item.STRENGTH_POTION
        return Item.NONE


   
