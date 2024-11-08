# -*- coding: utf-8 -*-
"""
Created on Thu May  9 10:30:04 2024

@author: User
"""

# ASSIGNMENT 3:

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
from Pokemon_class_v2 import PokemonCharacter
from Trainer_class_v2 import PokemonTrainer
from FiniteStateMachine import FiniteStateMachine, State

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
        print(f'Wild {wild_pkmn.name} appeared! \n')
        # Active Pokemon:
        active_pkmn = pkmn_trainer.Pokemon_list[0]
        print(f'Go, {active_pkmn.name}! \n I choose you! \n')
        # 1S: Save wild pokemon ecountered:
        pkmn_trainer.encountered_wild_pokemons.append(wild_pkmn.name)
        
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
                battle_on = False
                Battle_phase.battle_result = 1
                return
            
            # Attack:
            turn = True
            while turn:
                    # active pokemon attacks:
                    active_move = active_pkmn.moves[random.randint(0, len(active_pkmn.moves)-1)]
                    print(f'{active_pkmn.name} uses {active_move.name}')
                    active_pkmn, wild_pkmn = active_pkmn.useMove(active_move, wild_pkmn, type_effectiveness_dict)
                    
                    # wild pokemon attacks:
                    wild_move = wild_pkmn.moves[random.randint(0, len(wild_pkmn.moves)-1)]
                    print(f'{wild_pkmn.name} uses {wild_move.name}')
                    wild_pkmn, active_pkmn = wild_pkmn.useMove(wild_move, active_pkmn, type_effectiveness_dict)
                    
                    n_turn += 1
                    turn = False
        return pkmn_trainer
    
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

def random_battle_mode(starter_pkmn, moves, Machine):
    # starter_pkmn: str obj with name of the pokemon
    # moves: list of str obj with name of moves. Ex: ['tackle', 'razor leaf']
    # Machine: FSM obj
    statistics_results = []
    for game in range(50):
        # Choose character name:
        character_name = 'Nicola'
        # Creation of pokemon trainer:
        trainer = PokemonTrainer(character_name)
        # Bulbasaur as starter pokemon:
        trainer.Pokemon_list.append(PokemonCharacter(starter_pkmn))
        trainer.Pokemon_list[0].addMoves(moves)
        # Random automatic battle mode:
        exit = False
        max_Battles = 150
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
                      'percentage_residual_hp': trainer.percentage_residual_hp,}
        statistics_results.append(statistics)

    # Save in a pickle file:
    pickle_out = open(f"statistics_results_{starter_pkmn}.pickle","wb")
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
# 1: Bulbasaur starter:
statistics_results_bulbasaur = random_battle_mode('bulbasaur', ['tackle', 'razor leaf'], Machine)
# 1: Charmander starter:
statistics_results_charmander = random_battle_mode('charmander', ['tackle', 'ember'], Machine)
# 1: Squirtle starter:
statistics_results_squirtle = random_battle_mode('squirtle', ['tackle', 'water gun'], Machine)
# 1: Pikachu starter:
statistics_results_pikachu = random_battle_mode('pikachu', ['tackle', 'thunder shock'], Machine)

#%% variables:
# 1: cumulated number of vistories, averaged across games:
bulbasaur_cum_vic_mean = cumulated_victory_mean(statistics_results_bulbasaur)
charmander_cum_vic_mean = cumulated_victory_mean(statistics_results_charmander)
squirtle_cum_vic_mean = cumulated_victory_mean(statistics_results_squirtle)
pikachu_cum_vic_mean = cumulated_victory_mean(statistics_results_pikachu)

# 2: Number of turns in each battle:
bulbasaur_turns_boxplot = turns_boxplot(statistics_results_bulbasaur)
charmander_turns_boxplot = turns_boxplot(statistics_results_charmander)
squirtle_turns_boxplot = turns_boxplot(statistics_results_squirtle)
pikachu_turns_boxplot = turns_boxplot(statistics_results_pikachu)

# 3: Residual HP:
bulbasaur_residual_hp_boxplot = residual_hp_boxplot(statistics_results_bulbasaur)
charmander_residual_hp_boxplot = residual_hp_boxplot(statistics_results_charmander)
squirtle_residual_hp_boxplot = residual_hp_boxplot(statistics_results_squirtle)
pikachu_residual_hp_boxplot = residual_hp_boxplot(statistics_results_pikachu)

# 4: Number of victories vs every enemy pokemon:
bulbasaur_percentage_win = percentage_victories(pokemons_dict, statistics_results_bulbasaur)
charmander_percentage_win = percentage_victories(pokemons_dict, statistics_results_charmander)
squirtle_percentage_win = percentage_victories(pokemons_dict, statistics_results_squirtle)
pikachu_percentage_win = percentage_victories(pokemons_dict, statistics_results_pikachu)

# 5: Mean adn std HP at the end of the battles:
bulbasaur_mean_std_hp = mean_std_residual_hp(pokemons_dict, statistics_results_bulbasaur)
charmander_mean_std_hp = mean_std_residual_hp(pokemons_dict, statistics_results_charmander)
squirtle_mean_std_hp = mean_std_residual_hp(pokemons_dict, statistics_results_squirtle)
pikachu_mean_std_hp = mean_std_residual_hp(pokemons_dict, statistics_results_pikachu)

# 6: Highlight novice and skilled user pokemons:
bulbasaur_novice, bulbasaur_skilled = novice_skilled_pokemons(pokemons_dict, statistics_results_bulbasaur, bulbasaur_percentage_win, bulbasaur_mean_std_hp)
charmander_novice, charmander_skilled = novice_skilled_pokemons(pokemons_dict, statistics_results_charmander, charmander_percentage_win, charmander_mean_std_hp)
squirtle_novice, squirtle_skilled = novice_skilled_pokemons(pokemons_dict, statistics_results_squirtle, squirtle_percentage_win, squirtle_mean_std_hp)
pikachu_novice, pikachu_skilled = novice_skilled_pokemons(pokemons_dict, statistics_results_pikachu, pikachu_percentage_win, pikachu_mean_std_hp)
# %% Plot results:
# Apply default theme:
sns.set_theme(rc={'figure.figsize':(19,9.5)})

plt.figure(figsize = (19,9.5))
plt.plot(range(len(statistics_results_squirtle[0]['total_n_turns'])), squirtle_cum_vic_mean, label = 'squirtle')
plt.plot(range(len(statistics_results_charmander[0]['total_n_turns'])), charmander_cum_vic_mean, label = 'charmander')
plt.plot(range(len(statistics_results_bulbasaur[0]['total_n_turns'])), bulbasaur_cum_vic_mean, label = 'bulbasaur')
plt.plot(range(len(statistics_results_pikachu[0]['total_n_turns'])), pikachu_cum_vic_mean, label = 'pikachu')
plt.legend()
plt.title('N of victories vs N of battles')
plt.xlabel('N battles')
plt.ylabel('Mean cumulated number of victories')

plt.tight_layout()
plt.savefig('cumulative_victories.jpg')
plt.close()

#%% Boxplots n turns:
fig1, axs1 = plt.subplots(2, 2, figsize = (19,9.5))
fig1.suptitle("N turns boxplots")

axs1[0,0].boxplot(bulbasaur_turns_boxplot, notch = True)
axs1[0,0].set_title('Bulbasaur')
axs1[0,0].set_xlabel('N battles')
axs1[0,0].set_ylabel('N of turns')

axs1[0,1].boxplot(charmander_turns_boxplot, notch = True)
axs1[0,1].set_title('Charmander')
axs1[0,1].set_xlabel('N battles')
axs1[0,1].set_ylabel('N of turns')

axs1[1,0].boxplot(squirtle_turns_boxplot, notch = True)
axs1[1,0].set_title('Squirtle')
axs1[1,0].set_xlabel('N battles')
axs1[1,0].set_ylabel('N of turns')

axs1[1,1].boxplot(pikachu_turns_boxplot, notch = True)
axs1[1,1].set_title('Pikachu')
axs1[1,1].set_xlabel('N battles')
axs1[1,1].set_ylabel('N of turns')

fig1.tight_layout()
fig1.savefig('turns_boxplot.jpg') #put .svg
# plt.close()

#%% Boxplots residual hp:
fig1, axs1 = plt.subplots(2, 2, figsize = (19,9.5))
fig1.suptitle("Residual HP boxplots")

axs1[0,0].boxplot(bulbasaur_residual_hp_boxplot, notch = True)
axs1[0,0].set_title('Bulbasaur')
axs1[0,0].set_xlabel('N battles')
axs1[0,0].set_ylabel('Residual HP')

axs1[0,1].boxplot(charmander_residual_hp_boxplot, notch = True)
axs1[0,1].set_title('Charmander')
axs1[0,1].set_xlabel('N battles')
axs1[0,1].set_ylabel('Residual HP')

axs1[1,0].boxplot(squirtle_residual_hp_boxplot, notch = True)
axs1[1,0].set_title('Squirtle')
axs1[1,0].set_xlabel('N battles')
axs1[1,0].set_ylabel('Residual HP')

axs1[1,1].boxplot(pikachu_residual_hp_boxplot, notch = True)
axs1[1,1].set_title('Pikachu')
axs1[1,1].set_xlabel('N battles')
axs1[1,1].set_ylabel('Residual HP')

fig1.tight_layout()
fig1.savefig('residual_hp_boxplot.jpg') #put .svg
# plt.close()

#%% Barcharts percentage victories:
# Bulbasaur:
bulbasaur_df = pd.DataFrame({'pokemons' : bulbasaur_percentage_win.keys(),
                            'novice' : bulbasaur_novice.values(), 
                            'skilled' : bulbasaur_skilled.values()})

ax1 = sns.barplot(x=bulbasaur_percentage_win.keys(), y=bulbasaur_percentage_win.values(), dodge=False, data=bulbasaur_percentage_win, label = 'Victories %')
ax1.set_xticklabels(labels=bulbasaur_percentage_win.keys(), rotation=90)
for (novice, skilled, ticklbl) in zip(bulbasaur_df['novice'], bulbasaur_df['skilled'], ax1.xaxis.get_ticklabels()):
    if novice == 1:
        ticklbl.set_color('red')
    elif skilled == 1:
        ticklbl.set_color('blue')
    else:
        ticklbl.set_color('grey')
sns.barplot(x=bulbasaur_mean_std_hp.keys(), y=[A['std'] for A in bulbasaur_mean_std_hp.values()], dodge=False, data=bulbasaur_mean_std_hp, label = 'Std deviation residual HP')
sns.barplot(x=bulbasaur_mean_std_hp.keys(), y=[A['mean'] for A in bulbasaur_mean_std_hp.values()], dodge=False, data=bulbasaur_mean_std_hp, alpha = 0.5, label = 'Mean residual HP')
handles, labels = ax1.get_legend_handles_labels()
# manually define a new patch 
patch = mpatches.Patch(color='red', label='novice pokemons')
patch_2 = mpatches.Patch(color='blue', label='skilled pokemons')
# handles is a list, so append manual patch
handles.append(patch)
handles.append(patch_2) 
plt.legend(handles=handles)
plt.title('Bulbasaur')
plt.tight_layout()
plt.savefig('victories_percentage_bulbasaur.jpg')
plt.close()

# Charmander:
charmander_df = pd.DataFrame({'pokemons' : charmander_percentage_win.keys(),
                            'novice' : charmander_novice.values(), 
                            'skilled' : charmander_skilled.values()})

ax1 = sns.barplot(x=charmander_percentage_win.keys(), y=charmander_percentage_win.values(), dodge=False, data=charmander_percentage_win, label = 'Victories %')
ax1.set_xticklabels(labels=charmander_df['pokemons'], rotation=90)
for (novice, skilled, ticklbl) in zip(charmander_df['novice'], charmander_df['skilled'], ax1.xaxis.get_ticklabels()):
    if novice == 1:
        ticklbl.set_color('red')
    elif skilled == 1:
        ticklbl.set_color('blue')
    else:
        ticklbl.set_color('grey')
sns.barplot(x=charmander_mean_std_hp.keys(), y=[A['std'] for A in charmander_mean_std_hp.values()], dodge=False, data=charmander_mean_std_hp, label = 'Std deviation residual HP')
sns.barplot(x=charmander_mean_std_hp.keys(), y=[A['mean'] for A in charmander_mean_std_hp.values()], dodge=False, data=charmander_mean_std_hp, alpha = 0.5, label = 'Mean residual HP')
handles, labels = ax1.get_legend_handles_labels()
# manually define a new patch 
patch = mpatches.Patch(color='red', label='novice pokemons')
patch_2 = mpatches.Patch(color='blue', label='skilled pokemons')
# handles is a list, so append manual patch
handles.append(patch)
handles.append(patch_2) 
plt.legend(handles=handles)
plt.title('Cahrmander')
plt.tight_layout()
plt.savefig('victories_percentage_charmander.jpg')
plt.close()

# Squirtle:
squirtle_df = pd.DataFrame({'pokemons' : squirtle_percentage_win.keys(),
                            'novice' : squirtle_novice.values(), 
                            'skilled' : squirtle_skilled.values()})

ax1 = sns.barplot(x=squirtle_percentage_win.keys(), y=squirtle_percentage_win.values(), dodge=False, data=squirtle_percentage_win, label = 'Victories %')
ax1.set_xticklabels(labels=squirtle_df['pokemons'], rotation=90)
for (novice, skilled, ticklbl) in zip(squirtle_df['novice'], squirtle_df['skilled'], ax1.xaxis.get_ticklabels()):
    if novice == 1:
        ticklbl.set_color('red')
    elif skilled == 1:
        ticklbl.set_color('blue')
    else:
        ticklbl.set_color('grey')
sns.barplot(x=squirtle_mean_std_hp.keys(), y=[A['std'] for A in squirtle_mean_std_hp.values()], dodge=False, data=squirtle_mean_std_hp, label = 'Std deviation residual HP')
sns.barplot(x=squirtle_mean_std_hp.keys(), y=[A['mean'] for A in squirtle_mean_std_hp.values()], dodge=False, data=squirtle_mean_std_hp, alpha = 0.5, label = 'Mean residual HP')
handles, labels = ax1.get_legend_handles_labels()
# manually define a new patch 
patch = mpatches.Patch(color='red', label='novice pokemons')
patch_2 = mpatches.Patch(color='blue', label='skilled pokemons')
# handles is a list, so append manual patch
handles.append(patch)
handles.append(patch_2) 
plt.legend(handles=handles)
plt.title('Squirtle')
plt.tight_layout()
plt.savefig('victories_percentage_squirtle.jpg')
plt.close()

# Pikachu:
pikachu_df = pd.DataFrame({'pokemons' : pikachu_percentage_win.keys(),
                            'novice' : pikachu_novice.values(), 
                            'skilled' : pikachu_skilled.values()})

ax1 = sns.barplot(x=pikachu_percentage_win.keys(), y=pikachu_percentage_win.values(), dodge=False, data=pikachu_percentage_win, label = 'Victories %')
ax1.set_xticklabels(labels=pikachu_df['pokemons'], rotation=90)
for (novice, skilled, ticklbl) in zip(pikachu_df['novice'], pikachu_df['skilled'], ax1.xaxis.get_ticklabels()):
    if novice == 1:
        ticklbl.set_color('red')
    elif skilled == 1:
        ticklbl.set_color('blue')
    else:
        ticklbl.set_color('grey')
sns.barplot(x=pikachu_mean_std_hp.keys(), y=[A['std'] for A in pikachu_mean_std_hp.values()], dodge=False, data=pikachu_mean_std_hp, label = 'Std deviation residual HP')
sns.barplot(x=pikachu_mean_std_hp.keys(), y=[A['mean'] for A in pikachu_mean_std_hp.values()], dodge=False, data=pikachu_mean_std_hp, alpha = 0.5, label = 'Mean residual HP')
handles, labels = ax1.get_legend_handles_labels()
# manually define a new patch 
patch = mpatches.Patch(color='red', label='novice pokemons')
patch_2 = mpatches.Patch(color='blue', label='skilled pokemons')
# handles is a list, so append manual patch
handles.append(patch)
handles.append(patch_2) 
plt.legend(handles=handles)
plt.title('Pikachu')
plt.tight_layout()
plt.savefig('victories_percentage_pikachu.jpg')
plt.close()
