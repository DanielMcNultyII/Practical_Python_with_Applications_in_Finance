'''
Daniel McNulty II
Last Modified: 7/2/2020

The Monty Hall Problem

This code is a duplicate of "Monty Hall Main.py", except that it now allows for user input total number of simulations
and number of processes to use.
'''


# Import the MontyHallGame class from the game module in the Monty_Hall_Problem_Simulation package
from Monty_Hall_Problem_Simulation.game import MontyHallGame
# Import the AlwaysSwitchPlayer and NeverSwitchPlayer classes from the player module in the
# Monty_Hall_Problem_Simulation package
from Monty_Hall_Problem_Simulation.player import AlwaysSwitchPlayer, NeverSwitchPlayer
# Import the Timer class from the timer module
from timer import Timer
# Import the logging module
import logging
# Import the multiprocessing module
import multiprocessing


'''
monty_hall_sim Function:
Takes in the number of trials to perform and the name of the player type to perform them on. Returns a generator with
the results of all the trials.
'''


def monty_hall_sim(num_trial, player_type='AlwaysSwitchPlayer'):
    # If the user inputs 'NeverSwitchPlayer' for the player_type, then set the variable player equal to a
    # NeverSwitchPlayer object.
    if player_type == 'NeverSwitchPlayer':
        player = NeverSwitchPlayer('Never Switch Player')
    # If the user does not input 'NeverSwitchPlayer' for the player_type, then set the variable player equal to a
    # AlwaysSwitchPlayer object.
    else:
        player = AlwaysSwitchPlayer('Always Switch Player')

    # Use a generator expression to return a generator with num_trial amount of simulation results from the
    # MontyHallGame class play_game function with the above created player variable as its input.
    return [MontyHallGame().play_game(player) for trial in range(num_trial)]


'''
do_work Function:
Takes in 2 queues, in_queue and out_queue. in_queue should contain tuples with (Function_Name, (Function_Args,)), since
the do_work function takes the function associated with the input_queue tuple Function_Name and passes the *args tuple
(Function_Args,) into it. Then it puts the result of the output from Function_Name(*(Function_Args,)) into the out_queue
using the result and the queue put function within map.
'''


def do_work(in_queue, out_queue):
        # Unpack the tuple returned by in_queue.get() and store the contents in f and args.
        f, args = in_queue.get()
        # Call the function referred to by f with input parameter being the unpacked args tuple from above. Store
        # the result in variable ret
        ret = f(*args)
        # Use store the result ret in the output queue out_queue
        out_queue.put(ret)


'''
Main Program:
This code is a duplicate of "Monty Hall Main.py", except that it now allows for user input total number of simulations
and number of processes to use.
'''


def main():
    # Let users know the following output is for Exercise Monty_Hall_Main_Codes.1
    print('\nThe Monty Hall Problem\n')

    # Get the Logger from the logging package using getLogger() and use setLevel to set logging.ERROR to the lowest
    # level of logging that will work. This was to keep the WARN log from timer off the screen when timing in part E,
    # since we know that that part takes a significant amount of time.
    logging.getLogger().setLevel(logging.ERROR)

    # Initialize variables total_sims, num_processes, and process_sims as floats. These variables will be used later to
    # hold the total amount of simulations, the total number of processes to use, and the number of simulations to
    # allocate to each process respectively.
    total_sims = 0.1
    num_processes = 0.1
    process_sims = 0.1

    # SETTING THE TOTAL SIMULATIONS AND NUMBER OF PROCESSES TO RUN =====================================================
    # Set the total amount of simulations, total_sims, and the total number of processes, num_processes, to whatever the
    # user inputs. Then set the amount of simulations to be allotted to each process, process_sims, to the quotient of
    # total_sims/num_processes. While loop used to ensure all variables are integers by the end of the input process.
    while isinstance(total_sims, float) and isinstance(num_processes, float) and isinstance(process_sims, float):
        total_sims = float(input("Please input the total number of simulations to perform overall as an integer: "))
        num_processes = float(input("Please input the number of number of processes to use as an integer: "))
        process_sims = total_sims/num_processes

        # Check if total_sims is an integer. If it isn't, let the user know.
        if total_sims.is_integer() is False:
            print("\nInput is not acceptable. The total number of simulations must be an integer. Please try again.\n")
        # Check if num_processes is an integer. If it isn't, let the user know.
        elif num_processes.is_integer() is False:
            print("\nInput is not acceptable. The number of processes to use must be an integer. Please try again.\n")
        # Check if process_sims is an integer. If it isn't, let the user know that their total_sims isn't divisible by
        # their num_processes.
        elif process_sims.is_integer() is False:
            print("\nInput is not acceptable. The total number of simulations must be divisible by the number of "
                  "processes to use. Please try again.\n")
        # If everything is an integer, cast them as such, let the user know the value of process_sims, and exit the
        # while loop.
        else:
            total_sims = int(total_sims)
            num_processes = int(num_processes)
            process_sims = int(process_sims)
            print('Number of Simulations Allocated to each Process: {ps}'.format(ps=process_sims))

    # NEVER SWITCH PLAYER SIMULATIONS ==================================================================================
    print('\n========================================================================================================'
          '\nNever Switch Doors Strategy Simulation:')
    # Initialize an input queue, never_switch_input_queue, and output queue, never_switch_output_queue, using
    # multiprocessing.Queue()
    never_switch_input_queue = multiprocessing.Queue()
    never_switch_output_queue = multiprocessing.Queue()

    # Put num_processes amount of tuples with (monty_hall_sim, (process_sims, 'NeverSwitchPlayer)) into the input
    # queue always_switch_input_queue
    for i in range(num_processes):
        never_switch_input_queue.put((monty_hall_sim, (process_sims, 'NeverSwitchPlayer')))

    # Create a generator of num_processes processes, with target function do_work and args
    # (never_switch_input_queue, never_switch_output_queue)
    never_procs = (multiprocessing.Process(target=do_work, args=(never_switch_input_queue, never_switch_output_queue))
                   for i in range(num_processes))

    # Use a with statement to start a timer called 'Never Switch Timer'
    with Timer(timer_name='Never Switch Timer'):
        # Use a for loop to start all the above made processes using start()
        for proc in never_procs:
            proc.start()

        # Initialize an empty list and store it in variable never_switch_res
        never_switch_res = []
        # Initialize a while loop that will continuously iterate until the never_switch_res list is equal in size to
        # the total_sims
        while len(never_switch_res) != total_sims:
            # Get the next list in the queue never_switch_output_queue using get() and add it to the list
            # never_switch_res using extend.
            never_switch_res.extend(never_switch_output_queue.get())

        # Count the number of times True appears in the never_switch_res list and cast the result to a float. Then
        # divide that by the length of the never_switch_res list cast to a float in order to calculate the percentage of
        # times always switching doors resulted in the player winning the game. This percentage should be the
        # approximate probability of winning when not switching doors. Store this result in the variable
        # never_switch_success.
        never_switch_success = float(never_switch_res.count(True))/float(len(never_switch_res))

    # Print the length of never_switch_res to confirm that it has the proper number of simulations in it and the print
    # the success average of not switching doors, never_switch_success, found above.
    print('\tLength of Never Switch Result List: {alw_sw_len}'.format(alw_sw_len=len(never_switch_res)))
    print('\tThe success average of not switching doors was: {alw_sw_prob}'.format(alw_sw_prob=never_switch_success))

    # ALWAYS SWITCH PLAYER SIMULATIONS =================================================================================
    print('\n========================================================================================================'
          '\nAlways Switch Doors Strategy Simulation:')
    # Initialize an input queue, always_switch_input_queue, and output queue, always_switch_output_queue, using
    # multiprocessing.Queue()
    always_switch_input_queue = multiprocessing.Queue()
    always_switch_output_queue = multiprocessing.Queue()

    # Put num_processes amount of tuples with (monty_hall_sim, (process_sims, 'AlwaysSwitchPlayer)) into the input
    # queue always_switch_input_queue
    for i in range(num_processes):
        always_switch_input_queue.put((monty_hall_sim, (process_sims, 'AlwaysSwitchPlayer')))

    # Create a generator of num_processes processes, with target function do_work and args
    # (always_switch_input_queue, always_switch_output_queue)
    procs = (multiprocessing.Process(target=do_work, args=(always_switch_input_queue, always_switch_output_queue))
             for i in range(num_processes))

    # Use a with statement to start a timer called 'Always Switch Timer'
    with Timer(timer_name='Always Switch Timer'):
        # Use a for loop to start all the above made processes using start()
        for proc in procs:
            proc.start()

        # Initialize an empty list and store it in variable always_switch_res
        always_switch_res = []
        # Initialize a while loop that will continuously iterate until the always_switch_res list is equal in size to
        # the total_sims
        while len(always_switch_res) != total_sims:
            # Get the next list in the queue always_switch_output_queue using get() and ADD it to the list
            # always_switch_res using extend.
            always_switch_res.extend(always_switch_output_queue.get())

        # Count the number of times True appears in the always_switch_res list and cast the result to a float. Then
        # divide that by the length of the always_switch_res list cast to a float in order to calculate the percentage
        # of times always switching doors resulted in the player winning the game. This percentage should be the
        # approximate probability of winning when switching doors. Store this result in the variable
        # always_switch_success.
        always_switch_success = float(always_switch_res.count(True))/float(len(always_switch_res))

    # Print the length of always_switch_res to confirm that it has the proper number of simulations in it and the print
    # the success average of switching doors, always_switch_success, found above.
    print('\tLength of Always Switch Result List: {alw_sw_len}'.format(alw_sw_len=len(always_switch_res)))
    print('\tThe success average of switching doors was: {alw_sw_prob}'.format(alw_sw_prob=always_switch_success))


########################################################################################################################
if __name__ == '__main__':
    main()
