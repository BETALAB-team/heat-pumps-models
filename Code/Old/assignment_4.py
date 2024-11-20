# -*- coding: utf-8 -*-
"""
Created on Wed Aug 28 16:11:12 2024

@author: Nicola, Mattia
"""

# ASSIGNMENT 4:
#%% Packages:
import json
import copy
import random
import pickle
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import pandas as pd
from collections import Counter
from Pokemon_class_v3 import PokemonCharacter
from Trainer_class_v3 import PokemonTrainer
from FiniteStateMachine import FiniteStateMachine, State

#%% Plot theme:
# Apply default theme:
sns.set_theme(rc={'figure.figsize':(19,9.5)})
#%% Class:

class Story_phase(State):
    previous = None
    counter = 0
    options = ['Explore', 'Exit']
    
    def run(self, pkmn_trainer):
        print(f'\n ---------------- \n You are in {self.name} \n')
        
    def update(self, choices):
        # Function passed to update method of FSM class. It is called only if len(possible_transitions) > 1
        for i, opt in enumerate(Story_phase.options):
            print(i,':', opt)
        control = True
        while control:
            choice = int(input('Where do you want to go? '))
            if choice == 0:
                next_state = Explore
                control = False
            elif choice == 1:
                next_state = Exit
                control = False
            else:
                print('choose a valid alternative')
        return next_state

    def __str__(self):
        return self.name

    def __repr__(self):
        return str(self)    

class Pokemon_center_phase(State):
    previous = None
    # options = ['Go to Main Story']
    
    def run(self, pkmn_trainer):
        # pkmn_trainer: PokemonTrainer obj
        # Hp restored:
        print(f'\n ---------------- \n You are in {self.name} \n')
        for pkmn in pkmn_trainer.Pokemon_list:
            pkmn.current_HP = pkmn.baseStats['hp']
        print('Your Pokemon are now healed!')
        # PP restored:
        for pkmn in pkmn_trainer.Pokemon_list:
            for mov in pkmn.moves:
                mov.pp = mov.move_database[f'{mov.name}']['pp']
        return pkmn_trainer
    
    def __str__(self):
        return self.name

    def __repr__(self):
        return str(self)

class Exit_phase(State):
    previous = None
    
    def run(self, pkmn_trainer):
        print('Goodbye')
        return pkmn_trainer
    
    def update(self, choices):
        return
    
    def __str__(self):
        return self.name

    def __repr__(self):
        return str(self)
    
class Explore_phase(State):
    previous = None
    
    def run(self, pkmn_trainer):
        # pkmn_trainer: PokemonTrainer obj
        print(f'\n ---------------- \n You are in {self.name} \n')
        return pkmn_trainer
    
    def update(self, choices):
        probability = 1
        success = random.random() < probability
        if success:
            next_state = Battle
            print('You find a wild Pokemon!')
        else:
            next_state = Story_state
            print('All seems quiet...')
        return next_state
    
    def __str__(self):
        return self.name

    def __repr__(self):
        return str(self)

class Battle_phase(State):
    previous = None
    options = ['Go to Story', 'Battle']
    battle_result = 2
    
    
    def run(self, pkmn_trainer):
        # pkmn_trainer: PokemonTrainer obj
        print(f'\n ---------------- \n You are in {self.name} \n')
        
        # Wild Pokemon selection:
        wild_pkmn = copy.deepcopy(list(pokemons_database.values())[random.randint(0, len(pokemons_database)-1)])
        # set random level to wild pokemon:
        random_level = random.randint(1,20)
        wild_pkmn.level = random_level
        # Set new stats according to level:
        wild_pkmn.set_Act_HP()
        wild_pkmn.set_Act_Stat()
        print(f'Wild {wild_pkmn.name} appeared! \n')
        # Active Pokemon:
        active_pkmn = pkmn_trainer.Pokemon_list[0]
        print(f'Go, {active_pkmn.name}! \n I choose you! \n')
        # 1S: Save wild pokemon ecountered and levels:
        pkmn_trainer.encountered_wild_pokemons.append(wild_pkmn.name)
        pkmn_trainer.wild_pkmn_level.append(wild_pkmn.level)
        pkmn_trainer.player_pkmn_level.append(active_pkmn.level)
        # Statistics of battle for ass. 4:
        battle_current_player_pkmn_HP = []
        battle_selected_attacks = []
        battle_damage_done = []
        # initialize player pkmn HP statistic with max HP:
        battle_current_player_pkmn_HP.append(active_pkmn.current_HP)
        
        # Battle begins:
        battle_on = True
        n_turn = 0
        while battle_on:
            # Possible battle endings:
            print(f'\n Your {active_pkmn.name} has {active_pkmn.current_HP} HP')
            print(f' Wild {wild_pkmn.name} has {wild_pkmn.current_HP} HP \n')
            # 1 all pokemons are defeated
            if active_pkmn.current_HP <= 0:
                for pkmn in pkmn_trainer.Pokemon_list:
                    if pkmn.current_HP >= 0:
                        active_pkmn = pkmn
                    else:
                        print('All Pokemons are defeated.')
                        # 2S: save win battle result:
                        pkmn_trainer.victories_losses.append(0)
                        pkmn_trainer.percentage_residual_hp.append(0)
                        pkmn_trainer.total_n_turns.append(n_turn)
                        pkmn_trainer.current_player_pkmn_HP.append(battle_current_player_pkmn_HP)
                        pkmn_trainer.selcted_attacks.append(battle_selected_attacks)
                        pkmn_trainer.damage_done.append(battle_damage_done)
                        battle_on = False
                        Battle_phase.battle_result = 1
                        return
            
            # 2 Opponent is defeated:
            if wild_pkmn.current_HP <= 0:
                print(f'Wild {wild_pkmn.name} is defeated')
                # 2S: save loose battle result:
                pkmn_trainer.victories_losses.append(1)
                pkmn_trainer.percentage_residual_hp.append(active_pkmn.current_HP/active_pkmn.baseStats['hp'])
                pkmn_trainer.total_n_turns.append(n_turn)
                pkmn_trainer.current_player_pkmn_HP.append(battle_current_player_pkmn_HP)
                pkmn_trainer.selcted_attacks.append(battle_selected_attacks)
                pkmn_trainer.damage_done.append(battle_damage_done)
                battle_on = False
                Battle_phase.battle_result = 1
                return
            
            # Attack:
            turn = True
            while turn:
                    # active pokemon attacks:
                    active_move = active_pkmn.moves[random.randint(0, len(active_pkmn.moves)-1)]
                    print(f'{active_pkmn.name} uses {active_move.name}')
                    active_pkmn, wild_pkmn, damage1 = active_pkmn.useMove(active_move, wild_pkmn, type_effectiveness_dict)
                    
                    # wild pokemon attacks:
                    wild_move = wild_pkmn.moves[random.randint(0, len(wild_pkmn.moves)-1)]
                    print(f'{wild_pkmn.name} uses {wild_move.name}')
                    wild_pkmn, active_pkmn, damage2 = wild_pkmn.useMove(wild_move, active_pkmn, type_effectiveness_dict)
                    # Save statistics:
                    if active_pkmn.current_HP < 0.0:
                        battle_current_player_pkmn_HP.append(0)
                    else:
                        battle_current_player_pkmn_HP.append(active_pkmn.current_HP)
                    battle_selected_attacks.append(active_move)
                    battle_damage_done.append(damage1)
                    
                    n_turn += 1
                    turn = False
        # pkmn_trainer.current_player_pkmn_HP.append(battle_current_player_pkmn_HP)
        # pkmn_trainer.selcted_attacks.append(battle_selected_attacks)
        # pkmn_trainer.damage_done.append(battle_damage_done)
    
    def update(self, choices):
        if Battle_phase.battle_result == 0:
            next_step = Story_state
            print('Return to Story')
        elif Battle_phase.battle_result == 1:
            next_step = Pokemon_center
            print('Go to Pokemon Center')
        return next_step
    
    def __str__(self):
        return self.name

    def __repr__(self):
        return str(self)

#%% Modules:
def FSM_initialization(Story_state, Exit, Explore, Battle, Pokemon_center):
    Machine = FiniteStateMachine()

    # Adding FSM states:
    Machine.add_state(Story_state)
    # Machine.add_state(Exit)
    Machine.add_state(Explore)
    Machine.add_state(Battle)
    Machine.add_state(Pokemon_center)

    # Adding FSM transitions:
    Machine.add_transition(Pokemon_center, Story_state)
    Machine.add_transition(Story_state, Explore)
    Machine.add_transition(Explore, Story_state)
    # Machine.add_transition(Story_state, Exit)
    Machine.add_transition(Explore, Battle)
    Machine.add_transition(Battle, Story_state)
    Machine.add_transition(Battle, Pokemon_center)
    # FSM inizialization:
    Machine.set_start_state(Story_state)
    # Machine.add_final_state(Exit)
    Machine.initialize()

    # Machine.draw()
    return Machine

def random_battle_mode(Machine, starter_pkmn = 'random'):
    # starter_pkmn: str obj with name of the pokemon
    # moves: list of str obj with name of moves. Ex: ['tackle', 'razor leaf']
    # Machine: FSM obj
    statistics_results = []
    for game in range(1000):  #put 500
        # Choose character name:
        character_name = 'Nicola'
        # Creation of pokemon trainer:
        trainer = PokemonTrainer(character_name)
        # Creation of starter dict and selection of a random pokemon:
        starter_selection_dict = {'bulbasaur' : ['tackle', 'razor leaf'], 'charmander' : ['tackle', 'ember'], 'squirtle' : ['tackle', 'water gun'], 'pikachu' : ['tackle', 'thunder shock']}
        # Randomly selected pokemon as starter pokemon (if random_starter = True):
        if starter_pkmn == 'random':
            random_pokemon = random.choice(list(starter_selection_dict.keys()))
        else:
            random_pokemon = starter_pkmn
        trainer.Pokemon_list.append(PokemonCharacter(random_pokemon))
        trainer.Pokemon_list[0].addMoves(starter_selection_dict[random_pokemon])
        # Set random level between 1 - 20 and assign to pokemon level:
        random_level = random.randint(1,20)
        trainer.Pokemon_list[0].level = random_level
        # Set stats according to level:
        trainer.Pokemon_list[0].set_Act_HP()
        trainer.Pokemon_list[0].set_Act_Stat()
        # Random automatic battle mode:
        exit = False
        max_Battles = 200
        n_battle = 0
        while not exit:
            if n_battle < max_Battles:
                Machine.eval_current(trainer)
                
                target = None
                if Machine.state not in Machine.final_states:
                    target = Machine.update()
                    State.previous = Machine.state
                    
                    Machine.do_transition(target)
                    n_battle += 0.25
            
                if not target:
                    print("EXIT FROM FSM")
                    exit = True
            else:
                exit = True
        print('Maximum N battles reached')
        
        # Saving statistics:
        cum_victories = trainer.victories_losses.count(1)
        # Creating dictonaries:
        statistics = {'encountered_wild_pokemons': trainer.encountered_wild_pokemons, 
                      'victories_losses': trainer.victories_losses,
                      'cum_victories': cum_victories,
                      'total_n_turns': trainer.total_n_turns,
                      'percentage_residual_hp': trainer.percentage_residual_hp,
                      'current_player_pkmn_HP' : trainer.current_player_pkmn_HP,
                      'selected_attacks' : trainer.selcted_attacks,
                      'damage_done' : trainer.damage_done,
                      'wild_pkmn_level' : trainer.wild_pkmn_level,
                      'player_pkmn_level' : trainer.player_pkmn_level,
                      'starter_pkmn' : trainer.Pokemon_list[0].name}
        statistics_results.append(statistics)

    # Save in a pickle file:
    pickle_out = open(f"statistics_results_{random_pokemon}.pickle","wb")
    pickle.dump(statistics_results, pickle_out)
    pickle_out.close()
    return statistics_results

def cumulated_victory_mean(statistics_results):
    # statistics_results: output of previous module
    cum_vic_mean = []
    for battle in range(1, len(statistics_results[0]['total_n_turns'])+1):
        control = np.zeros([len(statistics_results), battle])
        control_count_vector = []
        for game in range(1,len(statistics_results)):
            control[game,:] = statistics_results[game]['victories_losses'][:battle]
            unique, counts = np.unique(control[game,:], return_counts=True)
            control_count = dict(zip(unique, counts))
            if 1 in control_count.keys():
                control_count_vector.append(control_count[1])
        cum_vic_mean.append(np.mean(control_count_vector))
    return cum_vic_mean

def turns_boxplot(statistics_results):
    turns_boxplot = np.zeros([len(statistics_results), len(statistics_results[0]['total_n_turns'])])
    for game in range(len(statistics_results)):
        turns_boxplot[game] = statistics_results[game]['total_n_turns']
    return turns_boxplot

def residual_hp_boxplot(statistics_results):
    resdiual_boxplot = np.zeros([len(statistics_results), len(statistics_results[0]['total_n_turns'])])
    for game in range(len(statistics_results)):
        resdiual_boxplot[game] = [ round(elem, 3) for elem in statistics_results[game]['percentage_residual_hp'] ]
    return resdiual_boxplot

def percentage_victories(pokemons_dict, statistics_results):
    # statistics_results: output of previous module
    # pokemons_dict: dict obj with pokemons database
    bulbasaur_enemy_pkmn = dict(zip(list(pokemons_dict.keys()), np.zeros(len(pokemons_dict.keys()))))
    bulbasaur_enemy_pkmn_win = dict(zip(list(pokemons_dict.keys()), np.zeros(len(pokemons_dict.keys()))))
    for pkmn in bulbasaur_enemy_pkmn.keys():
        for game in range(len(statistics_results)):
            if pkmn in statistics_results[game]['encountered_wild_pokemons']:
                bulbasaur_enemy_pkmn[pkmn] += 1 
                index_pkmn = statistics_results[game]['encountered_wild_pokemons'].index(pkmn)
                if statistics_results[game]['victories_losses'][index_pkmn] == 1:
                    bulbasaur_enemy_pkmn_win[pkmn] += 1
    bulbasaur_percentage_win = dict(zip(list(pokemons_dict.keys()), np.zeros(len(pokemons_dict.keys()))))
    for pkmn in bulbasaur_enemy_pkmn.keys():
        bulbasaur_percentage_win[pkmn] = (bulbasaur_enemy_pkmn_win[pkmn] / bulbasaur_enemy_pkmn[pkmn]) * 100
    return bulbasaur_percentage_win

def mean_std_residual_hp(pokemons_dict, statistics_results):
    bulbasaur_left_hp = dict(zip(list(pokemons_dict.keys()), [ [] for _ in range(len(pokemons_dict.keys())) ]))
    for pkmn in bulbasaur_left_hp.keys():
        for game in range(len(statistics_results)):
            if pkmn in statistics_results[game]['encountered_wild_pokemons']:
                index_pkmn = statistics_results[game]['encountered_wild_pokemons'].index(pkmn)
                bulbasaur_left_hp[pkmn].append((statistics_results[game]['percentage_residual_hp'][index_pkmn])*100)
    bulbasaur_mean_std_hp = dict(zip(list(pokemons_dict.keys()), [{} for _ in range(len(pokemons_dict.keys()))]))
    for pkmn in bulbasaur_left_hp.keys():
        bulbasaur_mean_std_hp[pkmn]['std'] = np.std(np.array(bulbasaur_left_hp[pkmn]))
        bulbasaur_mean_std_hp[pkmn]['mean'] = np.mean(np.array(bulbasaur_left_hp[pkmn]))
    return bulbasaur_mean_std_hp

def novice_skilled_pokemons(pokemons_dict, statistics_results, bulbasaur_percentage_win, bulbasaur_mean_std_hp):
    # Find novice user pokemons:
    bulbasaur_novice = dict(zip(list(pokemons_dict.keys()), np.zeros(len(pokemons_dict.keys()))))
    for pkmn in bulbasaur_novice.keys():
        if bulbasaur_percentage_win[pkmn] >= 70 and bulbasaur_percentage_win[pkmn] <= 100:
            if bulbasaur_mean_std_hp[pkmn]['mean'] >= 70:
                bulbasaur_novice[pkmn] = 1 

    # Find mean number of turns for every encountered pokemon:
    bulbasaur_mean_turns = dict(zip(list(pokemons_dict.keys()), [ [] for _ in range(len(pokemons_dict.keys())) ]))
    for pkmn in bulbasaur_mean_turns.keys():
        for game in range(len(statistics_results)):
            if pkmn in statistics_results[game]['encountered_wild_pokemons']:
                index_pkmn = statistics_results[game]['encountered_wild_pokemons'].index(pkmn)
                bulbasaur_mean_turns[pkmn].append(statistics_results[game]['total_n_turns'][index_pkmn])
    bulbasaur_mean_turns_single = dict(zip(list(pokemons_dict.keys()), np.zeros(len(pokemons_dict.keys()))))
    for pkmn in bulbasaur_mean_turns_single.keys():
        bulbasaur_mean_turns_single[pkmn] = np.mean(np.array(bulbasaur_mean_turns[pkmn]))

    # Determine list with all turns distribution
    turns_distribution_list = []
    for k, v in bulbasaur_mean_turns.items():
        turns_distribution_list.extend(v)

    # Find skilled user pokemons:
    bulbasaur_skilled = dict(zip(list(pokemons_dict.keys()), np.zeros(len(pokemons_dict.keys()))))
    for pkmn in bulbasaur_skilled.keys():
        if bulbasaur_percentage_win[pkmn] >= 50 and bulbasaur_percentage_win[pkmn] <= 70:
            if bulbasaur_mean_turns_single[pkmn] >= np.median(turns_distribution_list):
                bulbasaur_skilled[pkmn] = 1
    
    return bulbasaur_novice, bulbasaur_skilled

def perc_atk(statistics_results_bulbasaur):
    # Df for % of times each atk is used and % of total damage

    # List with moves name (for index):
    starter_selection_dict = {'bulbasaur' : ['tackle', 'razor leaf'], 'charmander' : ['tackle', 'ember'], 'squirtle' : ['tackle', 'water gun'], 'pikachu' : ['tackle', 'thunder shock']}
    moves_list = starter_selection_dict[statistics_results_bulbasaur[0]['starter_pkmn']]

    perc_atk_used_total = pd.DataFrame(0.0, index = moves_list, columns = np.arange(len(statistics_results_bulbasaur)))
    perc_atk_damage_total = pd.DataFrame(0.0, index = moves_list, columns = np.arange(len(statistics_results_bulbasaur)))

    for game in range(len(statistics_results_bulbasaur)):
        # crate df with atk name as index and battles as columns
        battle_atks_used_df = pd.DataFrame(0.0, index = moves_list, columns = np.arange(len(statistics_results_bulbasaur[0]['total_n_turns'])))
        perc_atk_used_df = pd.DataFrame(0.0, index = moves_list, columns = np.arange(len(statistics_results_bulbasaur[0]['total_n_turns'])))
        battle_atks_damage_df = pd.DataFrame(0.0, index = moves_list, columns = np.arange(len(statistics_results_bulbasaur[0]['total_n_turns'])))
        perc_atk_damage_df = pd.DataFrame(0.0, index = moves_list, columns = np.arange(len(statistics_results_bulbasaur[0]['total_n_turns'])))
        
        # fill df with atks used in every battle:
        for battle in range(len(battle_turn_df.columns)):
            # Count n times each atk is used:
            selected_atks = statistics_results_bulbasaur[game]['selected_attacks'][battle]
            selected_atks = [x.name for x in selected_atks]
            selected_atks_n_times = {i : selected_atks.count(i) for i in selected_atks}
            # Save into df:
            for key in selected_atks_n_times.keys():
                battle_atks_used_df.loc[key, battle] = selected_atks_n_times[key]
            for index_move in range(len(selected_atks)):
                damage_done_atk = statistics_results_bulbasaur[game]['damage_done'][battle][index_move]
                battle_atks_damage_df.loc[selected_atks[index_move], battle] += damage_done_atk
            
            for move in moves_list:
                perc_atk_used_df.loc[move, battle] = battle_atks_used_df.loc[move, battle] / battle_atks_used_df[battle].sum()
                if battle_atks_damage_df[battle].sum() != 0.0:
                    perc_atk_damage_df.loc[move, battle] = battle_atks_damage_df.loc[move, battle] / battle_atks_damage_df[battle].sum()
                else:
                    perc_atk_damage_df.loc[move, battle] = 0.0
            
        for move in moves_list:
            perc_atk_used_total.loc[move, game] = perc_atk_used_df.mean(axis = 1)[move]
            perc_atk_damage_total.loc[move, game] = perc_atk_damage_df.mean(axis = 1)[move]

    perc_atk_used_global = perc_atk_used_total.mean(axis = 1)
    perc_atk_damage_global = perc_atk_damage_total.mean(axis = 1)
    
    # Set df for output
    list_of_series = [perc_atk_used_global, perc_atk_damage_global]
    perc_atk_df = pd.DataFrame(list_of_series).transpose()
    perc_atk_df = perc_atk_df.rename(columns = {0 : 'perc_atk_used', 1 : 'perc_atk_damage'})
    
    return perc_atk_df

def avg_damage_by_level(statistics_results_bulbasaur):
    bulbasaur_avg_damage_level_dict = {}
    for game in range(len(statistics_results_bulbasaur)):
        avg_damage_game = []
        for battle in range(len(battle_turn_df.columns)):
            statistics_results_bulbasaur[game]['damage_done'][battle] = [float(i) for i in statistics_results_bulbasaur[game]['damage_done'][battle]]
            avg_damage = np.array(statistics_results_bulbasaur[game]['damage_done'][battle]).mean()
            avg_damage_game.append(avg_damage)
        if statistics_results_bulbasaur[game]['player_pkmn_level'][0] not in bulbasaur_avg_damage_level_dict.keys():
            bulbasaur_avg_damage_level_dict[statistics_results_bulbasaur[game]['player_pkmn_level'][0]] = []
            bulbasaur_avg_damage_level_dict[statistics_results_bulbasaur[game]['player_pkmn_level'][0]].append(np.array(avg_damage_game).mean())
        else:
            bulbasaur_avg_damage_level_dict[statistics_results_bulbasaur[game]['player_pkmn_level'][0]].append(np.array(avg_damage_game).mean())

    bulbasaur_avg_damage_level_dict_global = {}
    for level in bulbasaur_avg_damage_level_dict.keys():
        bulbasaur_avg_damage_level_dict_global[level] = np.array(bulbasaur_avg_damage_level_dict[level]).mean()
    
    return bulbasaur_avg_damage_level_dict_global

def perc_win_vs_level_type(statistics_results_bulbasaur, pkmn_type_database_df, pokemons_dict):
    type_level_perc_win_df = pd.DataFrame(0.0, index = np.arange(1,21), columns = pkmn_type_database_df.index)
    type_level_perc_total_df = pd.DataFrame(0.0, index = np.arange(1,21), columns = pkmn_type_database_df.index)
    for game in range(len(statistics_results_bulbasaur)):
        for battle in range(len(battle_turn_df.columns)):
            # Save battle in total df:
            player_pkmn_level = statistics_results_bulbasaur[game]['player_pkmn_level'][0]
            enemy_pkmn_type = pokemons_dict[statistics_results_bulbasaur[game]['encountered_wild_pokemons'][battle]]['types'][0]
            type_level_perc_total_df.loc[player_pkmn_level, enemy_pkmn_type] += 1 
            if statistics_results_bulbasaur[game]['victories_losses'][battle] == 1:
                type_level_perc_win_df.loc[player_pkmn_level, enemy_pkmn_type] += 1 

    # Caluclate % df:
    type_level_perc_win_df_global = type_level_perc_win_df / type_level_perc_total_df
    # remove flying type (no pkmn in 1° gen has flying as primary type):
    type_level_perc_win_df_global = type_level_perc_win_df_global.dropna(axis = 1)
    
    return type_level_perc_win_df_global


#%% FSM states:
Story_state = Story_phase('Story')
Exit = Exit_phase('Exit')
Explore = Explore_phase('Explore')
Battle = Battle_phase('Battle')
Pokemon_center = Pokemon_center_phase('Pokemon Center')

#%% Create FSM for managing the story:
Machine = FSM_initialization(Story_state, Exit, Explore, Battle, Pokemon_center)

#%% Main:
#%% Load json files:
# Pokemon dict:
pokemons_dict = dict()
with open('pokemons.json', 'r') as file: # open the file containing the data
    for line in file:
        p = json.loads(line) # convert each json line into a dictionary
        pokemons_dict[p['name']] = p

# Moves dict:
moves_dict_complete = dict()
with open('moves.json', 'r', encoding = 'utf8') as file:
    for line in file:
        p = json.loads(line)
        moves_dict_complete[p['name']] = p

# Exclude moves with null power:
moves_dict = copy.deepcopy(moves_dict_complete)
for key in moves_dict_complete:
    if moves_dict_complete[key]['power'] == None:
        del moves_dict[key]

# Type effectiveness dict:
attack_type = ["normal", "fire", "water", "electric", "grass", "ice", "fighting", "poison", "ground", "flying", "psychic", 'bug', 'rock', 'ghost', 'dragon']
type_effectiveness_dict = {}
for pkmn_type in attack_type:
    type_effectiveness_dict[pkmn_type] = {}

with open('type_effectiveness.json', 'r', encoding = 'utf8') as file:
    for line in file:
        p = json.loads(line)
        type_effectiveness_dict[p['attack']][p['defend']] = p['effectiveness']

#%% Database in DataFrame structures:
# Pokemon DataFrame:
pokemons_df = pd.DataFrame(pokemons_dict).transpose()

# Moves DataFrame:
moves_df = pd.DataFrame(moves_dict).transpose()

# Type effectiveness DataFrame:
type_effectiveness_df = pd.DataFrame(type_effectiveness_dict).transpose()

#%% Generate Pokemon database:
pokemons_database = {}
for key in pokemons_dict:
    pokemons_database[key] = PokemonCharacter(key)

#%% Assign random moves to pokemons:
for key_p in pokemons_database:
    pkmn = pokemons_database[key_p]
    possible_moves = []
    for key_m in moves_dict:
        if moves_dict[key_m]['type'] in pkmn.types:
            possible_moves.append(key_m)
        if moves_dict[key_m]['type'] == 'normal':
            possible_moves.append(key_m)
    pkmn.addMoves(random.sample(possible_moves, k=random.randint(2,4)))

#%% Iterative Game mode:
statistics_results_random = random_battle_mode(Machine)

#%% Iterative Game mode (starter selection):
statistics_results_bulbasaur = random_battle_mode(Machine, starter_pkmn = 'bulbasaur')
statistics_results_charmander = random_battle_mode(Machine, starter_pkmn = 'charmander')
statistics_results_squirtle = random_battle_mode(Machine, starter_pkmn = 'squirtle')
statistics_results_pikachu = random_battle_mode(Machine, starter_pkmn = 'pikachu')
#%% Data analysis:
#%% Avg reduction of % player HP along battle turns

# Create Pandas DataFrame with data:
# find max n° of turns:
number_of_turns = []
for game in statistics_results_random:
    for battle_turn in game['total_n_turns']:
        number_of_turns.append(battle_turn)
max_turn_number = np.max(number_of_turns) + 1

# create dict with df for every single game:
perc_reduction_dict = {}
for game in range(len(statistics_results_random)):
    # create df with n° turn on rows and n° battle on columns:
    # max_turn_number = n° rows
    battle_turn_df = pd.DataFrame(0.0, index = np.arange(max_turn_number), columns = np.arange(len(statistics_results_random[0]['total_n_turns'])))
    
    # fill df with HP values of player pkmn in every battle:
    for battle in range(len(battle_turn_df.columns)):
        battle_turn_df.loc[0 : len(statistics_results_random[game]['current_player_pkmn_HP'][battle]) - 1, battle] = [float(i) for i in statistics_results_random[game]['current_player_pkmn_HP'][battle]]
    
    # New df with % reduction of players' pkmn HP:
    perc_reduction_df = pd.DataFrame(0.0, index = np.arange(max_turn_number), columns = np.arange(len(statistics_results_random[0]['total_n_turns'])))
    for turn in range(len(battle_turn_df.index.values) - 1):
        perc_reduction_df.loc[turn] = abs((battle_turn_df.loc[turn+1] - battle_turn_df.loc[turn]) / battle_turn_df.loc[0])
    
    perc_reduction_dict[game] = perc_reduction_df

# Create a dict with avg values of HP reduction per turn per game:
avg_HP_reduction_per_game_dict_mean = {}
avg_HP_reduction_per_game_dict_std = {}
for game in range(len(statistics_results_random)):
    avg_HP_reduction_per_game_dict_mean[game] = perc_reduction_dict[game].mean(axis = 1)
    avg_HP_reduction_per_game_dict_std[game] = perc_reduction_dict[game].std(axis = 1)
avg_HP_reduction_per_game_df_mean = pd.DataFrame(avg_HP_reduction_per_game_dict_mean)
avg_HP_reduction_per_game_df_std = pd.DataFrame(avg_HP_reduction_per_game_dict_std)

# Create a df with avg values of HP reduction per turn (avg and std between all battle turns and all games):
avg_HP_reduction_per_turn_mean = avg_HP_reduction_per_game_df_mean.mean(axis = 1)
avg_HP_reduction_per_turn_std = avg_HP_reduction_per_game_df_std.std(axis = 1)

# Create df for plotting:
avg_HP_reduction_df_plot = pd.DataFrame(avg_HP_reduction_per_turn_mean, columns = ['mean'])
avg_HP_reduction_df_plot['mean_plus_std'] = avg_HP_reduction_per_turn_mean + avg_HP_reduction_per_turn_std
avg_HP_reduction_df_plot['mean_minus_std'] = avg_HP_reduction_per_turn_mean - avg_HP_reduction_per_turn_std
avg_HP_reduction_df_plot[avg_HP_reduction_df_plot['mean_minus_std'] < 0] = 0

# Plot
fig1 = plt.figure(2, figsize = (19,9.5))

limit_range = len(avg_HP_reduction_df_plot) + 1

plt.plot(np.arange(1, limit_range), avg_HP_reduction_df_plot['mean'], label = 'mean', marker = 'o', figure = fig1)
plt.plot(np.arange(1, limit_range), avg_HP_reduction_df_plot['mean_plus_std'], label = 'mean + std', marker = 'o', figure = fig1)
plt.plot(np.arange(1, limit_range), avg_HP_reduction_df_plot['mean_minus_std'], label = 'mean - std', marker = 'o', figure = fig1)
plt.grid(True)
plt.title('Avg HP reduction along battle', figure = fig1)
plt.xlabel('N turns', figure = fig1)
plt.ylabel('% HP reduction', figure = fig1)
plt.legend()
plt.xticks(range(1,16))

fig1.tight_layout()
fig1.savefig('percentage_HP_reduction.jpg') 

#%% Pie plot
# Creation of df for plotting
perc_atk_bulbasaur = perc_atk(statistics_results_bulbasaur)
perc_atk_charmander = perc_atk(statistics_results_charmander)
perc_atk_squirtle = perc_atk(statistics_results_squirtle)
perc_atk_pikachu = perc_atk(statistics_results_pikachu)

#%% plot
fig2, axs2 = plt.subplots(2,4, figsize = (19,9.5))

# Bulbasaur
axs2[0,0].pie(perc_atk_bulbasaur['perc_atk_used'], autopct='%1.1f%%', pctdistance=1.15, labeldistance=.4, labels = perc_atk_bulbasaur.index)
axs2[0,0].set_title('Bulbasaur % atk used')
axs2[0,1].pie(perc_atk_bulbasaur['perc_atk_damage'], autopct='%1.1f%%', pctdistance=1.15, labeldistance=.4, labels = perc_atk_bulbasaur.index)
axs2[0,1].set_title('Bulbasaur % atk damage')

# Cahrmander
axs2[0,2].pie(perc_atk_charmander['perc_atk_used'], autopct='%1.1f%%', pctdistance=1.15, labeldistance=.4, labels = perc_atk_charmander.index)
axs2[0,2].set_title('Cahrmander % atk used')
axs2[0,3].pie(perc_atk_charmander['perc_atk_damage'], autopct='%1.1f%%', pctdistance=1.15, labeldistance=.4, labels = perc_atk_charmander.index)
axs2[0,3].set_title('Cahrmander % atk damage')

# Squirtle
axs2[1,0].pie(perc_atk_squirtle['perc_atk_used'], autopct='%1.1f%%', pctdistance=1.15, labeldistance=.4, labels = perc_atk_squirtle.index)
axs2[1,0].set_title('Squirtle % atk used')
axs2[1,1].pie(perc_atk_squirtle['perc_atk_damage'], autopct='%1.1f%%', pctdistance=1.15, labeldistance=.4, labels = perc_atk_squirtle.index)
axs2[1,1].set_title('Squirtle % atk damage')

# Pikachu
axs2[1,2].pie(perc_atk_pikachu['perc_atk_used'], autopct='%1.1f%%', pctdistance=1.15, labeldistance=.4, labels = perc_atk_pikachu.index)
axs2[1,2].set_title('Pikachu % atk used')
axs2[1,3].pie(perc_atk_pikachu['perc_atk_damage'], autopct='%1.1f%%', pctdistance=1.15, labeldistance=.4, labels = perc_atk_pikachu.index)
axs2[1,3].set_title('Pikachu % atk damage')

fig2.tight_layout()
fig2.savefig('percentage_atk.jpg') 
#%%
# Distribution of pkmn types in database and in encountered:
# Pokemon dict:
pokemons_dict = dict()
with open('pokemons.json', 'r') as file: # open the file containing the data
    for line in file:
        p = json.loads(line) # convert each json line into a dictionary
        pokemons_dict[p['name']] = p
        
# Pokemon df of pokemon database:
pkmn_type_list = []
for pkmn in pokemons_dict.keys():
    types = pokemons_dict[pkmn]['types']
    for element in types:
        pkmn_type_list.append(element)

# Dict for counting pokemon types in pokemon database:
pkmn_type_database_dict = {i : pkmn_type_list.count(i) for i in pkmn_type_list}
pkmn_type_database_df = pd.Series(pkmn_type_database_dict)

# Pokemon df of simulated games:
pkmn_type_list_battle = []
for game in range(len(statistics_results_bulbasaur)):
    for battle in range(len(battle_turn_df.columns)):
        battle_pkmn = statistics_results_bulbasaur[game]['encountered_wild_pokemons'][battle]
        battle_pkmn_types = pokemons_dict[battle_pkmn]['types']
        for element in battle_pkmn_types:
            pkmn_type_list_battle.append(element)

# Dict for counting pokemon types in pokemon battles:
# Counter method for better performance (faster):
pkmn_type_battles_dict = Counter(pkmn_type_list_battle)
pkmn_type_battles_df = pd.Series(pkmn_type_battles_dict)
# Reorder index (same as previous df):
pkmn_type_battles_df = pkmn_type_battles_df.reindex(index = pkmn_type_database_df.index)


# Plot
fig3, axs3 = plt.subplots(1,2, figsize = (19,9.5))

axs3[0].pie(pkmn_type_database_df, autopct='%1.2f%%', pctdistance=1.10, labeldistance=.75, labels = pkmn_type_database_df.index)
axs3[0].set_title('% Pkmn types distribution in database')
axs3[1].pie(pkmn_type_battles_df, autopct='%1.2f%%', pctdistance=1.10, labeldistance=.75, labels = pkmn_type_battles_df.index)
axs3[1].set_title('% Pkmn types distribution in simulated games (Bulbasaur)')

fig3.tight_layout()
fig3.savefig('type_distribution.jpg') 

#%% Bar charts:
# Avg damage done by player's pkmn grouped by pkmn level:
avg_damage_level_bulbasaur = avg_damage_by_level(statistics_results_bulbasaur)
avg_damage_level_charmander = avg_damage_by_level(statistics_results_charmander)
avg_damage_level_squirtle = avg_damage_by_level(statistics_results_squirtle)
avg_damage_level_pikachu = avg_damage_by_level(statistics_results_pikachu)

# Plot:
fig4, axs4 = plt.subplots(2,2, figsize = (19,9.5))

axs4[0,0].bar(avg_damage_level_bulbasaur.keys(), avg_damage_level_bulbasaur.values())
axs4[0,0].set_xlabel('Pokemon level')
axs4[0,0].set_ylabel('Avg damage')
axs4[0,0].set_ylim([0, 16])
axs4[0,0].set_title('Bulbasaur')

axs4[0,1].bar(avg_damage_level_charmander.keys(), avg_damage_level_charmander.values())
axs4[0,1].set_xlabel('Pokemon level')
axs4[0,1].set_ylabel('Avg damage')
axs4[0,1].set_ylim([0, 16])
axs4[0,1].set_title('Charmander')

axs4[1,0].bar(avg_damage_level_squirtle.keys(), avg_damage_level_squirtle.values())
axs4[1,0].set_xlabel('Pokemon level')
axs4[1,0].set_ylabel('Avg damage')
axs4[1,0].set_ylim([0, 16])
axs4[1,0].set_title('Squirtle')

axs4[1,1].bar(avg_damage_level_pikachu.keys(), avg_damage_level_pikachu.values())
axs4[1,1].set_xlabel('Pokemon level')
axs4[1,1].set_ylabel('Avg damage')
axs4[1,1].set_ylim([0, 16])
axs4[1,1].set_title('Pikachu')

fig4.tight_layout()
fig4.savefig('avg-damage_by_level.jpg') 

#%% Image charts:
# df for total victories and total battles per enermy level and enemy type:
perc_win_level_type_bulbasaur = perc_win_vs_level_type(statistics_results_bulbasaur, pkmn_type_database_df, pokemons_dict)
perc_win_level_type_charmander = perc_win_vs_level_type(statistics_results_charmander, pkmn_type_database_df, pokemons_dict)
perc_win_level_type_squirtle = perc_win_vs_level_type(statistics_results_squirtle, pkmn_type_database_df, pokemons_dict)
perc_win_level_type_pikachu = perc_win_vs_level_type(statistics_results_pikachu, pkmn_type_database_df, pokemons_dict)

#%%
# put correct indexes:
indexes_array = np.arange(1, 21)
indexes_array = indexes_array[::-1]
perc_win_level_type_bulbasaur = perc_win_level_type_bulbasaur.set_index(indexes_array)
perc_win_level_type_charmander = perc_win_level_type_charmander.set_index(indexes_array)
perc_win_level_type_squirtle = perc_win_level_type_squirtle.set_index(indexes_array)
perc_win_level_type_pikachu = perc_win_level_type_pikachu.set_index(indexes_array)

perc_win_level_type_bulbasaur = perc_win_level_type_bulbasaur.iloc[::-1]
perc_win_level_type_charmander = perc_win_level_type_charmander.iloc[::-1]
perc_win_level_type_squirtle = perc_win_level_type_squirtle.iloc[::-1]
perc_win_level_type_pikachu = perc_win_level_type_pikachu.iloc[::-1]
#%% Plot:
fig5, axs5 = plt.subplots(2,2, figsize = (19,9.5))

heatmap = axs5[0,0].pcolor(perc_win_level_type_bulbasaur, )
axs5[0,0].set_xticks(np.arange(0.5, 14.5, 1), [str(i) for i in perc_win_level_type_bulbasaur.columns.values])
plt.setp(axs5[0,0].get_xticklabels(), rotation=45, ha="right",rotation_mode="anchor")
axs5[0,0].set_ylabel('Level')
axs5[0,0].set_ylim([0,20])
cbar = plt.colorbar(heatmap)
cbar.set_label('% of win')
axs5[0,0].set_title('Bulbasaur')

heatmap = axs5[0,1].pcolor(perc_win_level_type_charmander)
axs5[0,1].set_xticks(np.arange(0.5, 14.5, 1), [str(i) for i in perc_win_level_type_charmander.columns.values])
plt.setp(axs5[0,1].get_xticklabels(), rotation=45, ha="right",rotation_mode="anchor")
axs5[0,1].set_ylabel('Level')
axs5[0,1].set_ylim([0,20])
cbar = plt.colorbar(heatmap)
cbar.set_label('% of win')
axs5[0,1].set_title('Charmander')

heatmap = axs5[1,0].pcolor(perc_win_level_type_squirtle)
axs5[1,0].set_xticks(np.arange(0.5, 14.5, 1), [str(i) for i in perc_win_level_type_squirtle.columns.values])
plt.setp(axs5[1,0].get_xticklabels(), rotation=45, ha="right",rotation_mode="anchor")
axs5[1,0].set_ylabel('Level')
axs5[1,0].set_ylim([0,20])
cbar = plt.colorbar(heatmap)
cbar.set_label('% of win')
axs5[1,0].set_title('Squirtle')

heatmap = axs5[1,1].pcolor(perc_win_level_type_pikachu)
axs5[1,1].set_xticks(np.arange(0.5, 14.5, 1), [str(i) for i in perc_win_level_type_pikachu.columns.values])
plt.setp(axs5[1,1].get_xticklabels(), rotation=45, ha="right",rotation_mode="anchor")
axs5[1,1].set_ylabel('Level')
axs5[1,1].set_ylim([0,20])
cbar = plt.colorbar(heatmap)
cbar.set_label('% of win')
axs5[1,1].set_title('Pikachu')

fig5.tight_layout()
fig5.savefig('heatmap_perc_win.jpg') 

