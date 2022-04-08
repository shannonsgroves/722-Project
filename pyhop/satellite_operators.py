import pyhop

#state.on_board={satellite:list of instruments, sat2:list ...}
#state.supports = {instrument:list of modes, ...}
#state.pointing = {sat:direction...}
#state. power_avail = {sat:True or false}
#state.power_on = {instrument:True or False...}
#state.calibrated = {instrument:True..}
#state.have_image = {direction:mode, ...}
#state.calibration_target= {instrument:direction...}
#state.data_cpacity = {sat:number...}
#state.data = {(direction, mode) : number ...}
#state.slew_time = {(a,b):number ...}
#state.data_stored = number
#state.fuel{sat:number...}
# sate.fuel_used = number


def turn_to(state, sat, new_dir, prev_dir):
    if state.pointing[sat] == prev_dir and new_dir != prev_dir and state.fuel[sat] >= state.slew_time[(new_dir, prev_dir)]:
        state.pointing[sat] = new_dir
        state.fuel[sat] -= state.slew_time[(new_dir, prev_dir)]
        state.fuel_used += state.slew_time[(new_dir, prev_dir)]
        state.plan_length+= 1
        state.number_nodes+=1
        return state
    else:
        return False

def switch_on(state, instrument, satellite):
    if instrument in state.on_board[satellite] and state.power_avail[satellite] == True:
        state.power_on[instrument] = True
        state.calibrated[instrument] = False
        state.power_avail[satellite] = False
        state.plan_length+= 1
        state.number_nodes+=1
        return state
    else: return False

def switch_off(state, instrument, satellite):
    if instrument in state.on_board[satellite] and state.power_on[instrument] == True:
        state.power_on[instrument] = False
        state.power_avail[satellite] = True
        state.plan_length+= 1
        state.number_nodes+=1
        return state
    else: return False
 

def calibrate(state, satellite, instrument, direction):
    if instrument in state.on_board[satellite] and state.calibration_target[instrument] == direction and state.pointing[satellite] == direction and state.power_on[instrument] == True:
        state.calibrated[instrument] = True
        state.plan_length+= 1
        state.number_nodes+=1
        return state
    else: return False

def take_image(state, satellite, direction, instrument, mode):
    if state.calibrated[instrument] == True and instrument in state.on_board[satellite] and mode in state.supports[instrument] and state.power_on[instrument] == True and state.pointing[satellite] == direction and state.power_on[instrument] == True and state.data_capacity[satellite] >= state.data[(direction, mode)]:
        state.data_capacity[satellite] -= state.data[(direction, mode)]
        state.have_image[direction] = mode
        state.data_stored += state.data[(direction, mode)]
        state.plan_length+= 1
        state.number_nodes+=1
        return state
    else:return False


pyhop.declare_operators(turn_to, switch_on, switch_off, calibrate, take_image)
