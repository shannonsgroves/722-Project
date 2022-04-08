from __future__ import print_function
from time import process_time
from pyhop import *

import blocks_world_operators
print('')
print_operators()

import blocks_world_methods
print('')
print_methods()

file1 = open('block_problem', 'r')
Lines = file1.readlines()
total_blocks = (int)((Lines[0].split())[0])

state = State('state')
state.pos={}
state.clear= {x:True for x in range(1,total_blocks)}
state.holding=False
state.plan_length = 0
state.number_nodes = 0

block_on = Lines[1].split()

count=1
for block in block_on:
    if(block == '0'):
        state.pos.update({int(count):'table'})
    else:
        state.pos.update({int(count):int(block)})
        state.clear.update({int(block): False})
    count+=1

print_state(state)

goal = Goal('goal')
goal.pos={}
goal.clear= {x:True for x in range(1,total_blocks)}
goal.holding=False

block_on = Lines[3].split()

count=1
for block in block_on:
    if(block == '0'):
        goal.pos.update({int(count):'table'})
    else:
        goal.pos.update({int(count):int(block)})
        goal.clear.update({int(block): False})
    count+=1


print_goal(goal)

t1_start = process_time() 

pyhop(state,[('move_blocks', goal)], verbose=1)

t1_stop = process_time()

print("Elapsed time {} seconds".format(round(t1_stop-t1_start, 2)))
