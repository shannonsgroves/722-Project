from __future__ import print_function
from time import process_time
from pyhop import *

import satellite_operators
print('')
print_operators()

import satellite_methods
print('')
print_methods()

file1 = open('satellite_problem').read()

objects = file1.split(":init")[0]
objects = objects.replace(" - ", " ")
objects = objects.replace("(", "")
objects = objects.replace(")", "")
objects = objects.replace("\t", "")
objects = objects.split(":objects")[1].split("\n")

text = file1.split(":init")[1]
initial = text.split(":goal")[0]
initial = initial.replace("(", "")
initial = initial.replace(")", "")
initial = initial.replace("\t", "")
initial = initial.replace("= ", "")
initial = initial.split("\n")

state = State('state')
state.on_board = {} #doesn't change after init
state.supports = {}#doesn't change after init
state.pointing = {}
state.power_avail = {}
state.power_on = {} #starts off false for all
state.calibrated = {} #starts off false for all
state.have_image = {} #starts off empty
state.calibration_target = {}
state.data_capacity = {}
state.data = {}
state.slew_time = {}
state.data_stored = 0.00
state.fuel = {}
state.fuel_used = 0.00
state.plan_length = 0
state.number_nodes = 0

for line in objects:
    words = line.split(" ")
    if len(words) == 2 and words[1] == 'instrument':
        state.power_on[words[0]] = False

for line in initial:
    first_word = line.split(" ")[0]
    if first_word == "on_board":
        instrument = line.split(" ")[1]
        satellite = line.split(" ")[2]
        if satellite in state.on_board.keys():
            state.on_board[satellite] =  state.on_board[satellite]+[instrument]
        else:
            state.on_board[satellite] = [instrument]
        
    elif first_word == "supports":
        instrument = line.split(" ")[1]
        mode = line.split(" ")[2]
        if instrument in state.supports.keys():
            state.supports[instrument] =  state.supports[instrument]+[mode]
        else:
            state.supports[instrument] = [mode]
            
    elif first_word == "pointing":
        satellite = line.split(" ")[1]
        direction = line.split(" ")[2]
        state.pointing[satellite] = direction
        
    elif first_word == "power_avail":
        satellite = line.split(" ")[1]
        state.power_avail[satellite] = True

    elif first_word == "calibration_target":
        satellite = line.split(" ")[1]
        direction = line.split(" ")[2]
        state.calibration_target[satellite] = direction
        
    elif first_word == "data_capacity":
        satellite = line.split(" ")[1]
        value = line.split(" ")[2]
        state.data_capacity[satellite] = float(value)

    elif first_word == "data":
        direction = line.split(" ")[1]
        mode = line.split(" ")[2]
        value = line.split(" ")[3]
        state.data[(direction, mode)] = float(value)

    elif first_word == "slew_time":
        direction1 = line.split(" ")[1]
        direction2 = line.split(" ")[2]
        value = line.split(" ")[3]
        state.slew_time[(direction1,direction2)] = float(value)

    elif first_word == "fuel":
         satellite = line.split(" ")[1]
         value = line.split(" ")[2]
         state.fuel[satellite] = float(value)



goal_text = text.split(":goal")[1].split(":metric")[0]
goal_text = goal_text.replace("(", "")
goal_text = goal_text.replace(")", "")
goal_text = goal_text.replace("\t", "")
goal_text = goal_text.split("\n")

goal = Goal('goal')
goal.pointing = {}
goal.have_image = {}

for line in goal_text:
    words = line.split(" ")
    if len(words) == 3:
        command = words[0]
        if command == "pointing":
            satellite = words[1]
            direction = words[2]
            goal.pointing[satellite] =direction
        elif command == "have_image":
            direction = words[1]
            mode = words[2]
            goal.have_image[direction] = mode

print_goal(goal)


t1_start = process_time() 
   
pyhop(state, [('complete_goals', goal)], verbose =1)

t1_stop = process_time()

print("Elapsed time {} seconds".format(round(t1_stop-t1_start, 2)))



            
        
    

