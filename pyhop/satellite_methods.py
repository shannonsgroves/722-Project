
import pyhop


def is_image_done(direction, mode, state, goal):
    if direction not in state.have_image.keys():
        return False
    if mode != state.have_image[direction]:
        return False
    return True


def status_image(direction, mode, state, goal):
    if is_image_done(direction, mode,  state, goal):
        return 'done', '', ''

    #check if a satellite pointing in the right direction
    satellites_in_direction = [satellite for satellite in state.on_board.keys() if state.pointing[satellite] == direction]

    for satellite in satellites_in_direction:
        instrument = [instrument for instrument in state.on_board[satellite] if mode in state.supports[instrument]]
        if instrument !=[]:
            state.calibration_target[instrument[0]] = direction
            return 'satellite and instrument', instrument[0], satellite
            #got satellite and instrument

    #No satelites are pointing in the direction or no instrument is on board the satellite with the right mode, just find the satellite with an instrument that has the right mode 
    instruments= [instrument for instrument in state.supports.keys() if mode in state.supports[instrument]]


    for instrument in instruments:
        satellite_with_instrument  = [satellite for satellite in state.on_board.keys() if instrument in state.on_board[satellite]] #gets the one satellite that the instrument is on
        state.calibration_target[instrument] = direction
        return 'turn satellite', instrument, satellite_with_instrument[0]



def is_satellite_done(satellite, state, goal):
    if goal.pointing[satellite] != state.pointing[satellite]:
        return False
    return True


def complete_goals(state, goal):
    state.number_nodes+=1

    for direction in goal.have_image.keys():
        mode = goal.have_image[direction]
        status, instrument, satellite  = status_image(direction, mode, state, goal)
        
        if status == 'satellite and instrument':
             return [('get_image', instrument, satellite, direction, mode), ('complete_goals', goal)]

        elif status == 'turn satellite':
            prev_direction = state.pointing[satellite]
            new_direction = direction
            return [('turn_to', satellite, new_direction, prev_direction), ('get_image', instrument, satellite, direction, mode), ('complete_goals', goal)]
             
    for satellite in goal.pointing.keys():
        status = is_satellite_done(satellite, state, goal)
        if not status:
            prev_direction = state.pointing[satellite]
            new_direction = goal.pointing[satellite]
            return [('turn_to', satellite, new_direction, prev_direction), ('complete_goals', goal)]

    print("Plan length is {}".format(state.plan_length))
    print("Number nodes is {}".format(state.number_nodes))   
    return []
              

pyhop.declare_methods('complete_goals', complete_goals)

def get_image(state, instrument, satellite, direction, mode):
     state.number_nodes+=1
     return [('switch_on', instrument, satellite), ('calibrate', satellite, instrument, direction), ('take_image', satellite, direction, instrument, mode), ('switch_off', instrument, satellite)]

pyhop.declare_methods('get_image', get_image)

    
