'''
Daniel McNulty II
Last Modified: 07/15/2018
This module contains the Timer class
'''


# Import the time module so that the function time() can be used
import time
# Import the logging module
import logging
# Import partial from the functools module
from functools import partial


'''
Timer class
This class generalizes and encapsulates the use of time.time() before and after code blocks into a class. It contains a 
start_time and end_time protected variables, which are set using the start() and end() functions respectively. The end()
function also stores the difference between the start_time and end_time within its own variable, last_timer_result, and
prints it on screen.
'''


# Declare and implement the class Timer derived from object
class Timer(object):
    # Class level threshold variable, which defaults to 60 seconds (1 minute)
    _warn_threshold = 60

    # Standard initialization function
    def __init__(self, fcn=None, timer_name='Timer'):
        # Initialize object-level variables for the start time and the last_timer_result of the Timer to None.
        self._start_time = None
        self._last_timer_result = None
        # Initialize object-level variable for display to 'seconds' by default. This variable will be used to determine
        # which units are displayed by the Timer when its various functions and properties are called. It should be set
        # to 'seconds' to display values in seconds, 'minutes' to display values in minutes, and 'hours' to display
        # values in hours.
        self._display = 'seconds'
        # Initialize a function object-level protected variable _fcn to hold the function input fcn
        self._fcn = fcn
        # Initialize an object-level name variable to hold the input timer_name.
        self._timer_name = timer_name

    # Define __call__ to be used for the Timer decorator
    def __call__(self, *args):
        # Start the timer
        self.start()
        # Perform the function stored in self._fcn with input (*args, **kwargs). The use of *args and **kwargs
        # allows this to work with any function.
        fcn_res = self._fcn(*args)
        # End the timer. This will make an INFO log stating the time elapsed in seconds.
        self.end()
        # Print the time elapsed message specified in the example in the Exercise 5.2.1 prompt. This is useful for
        # cases where the lowest level of logging that is allowed on screen is greater than INFO.
        print('\n\t{func} {time} seconds'.format(func=self._fcn, time=self.last_timer_result))
        # Return the result of the self._fcn call
        return fcn_res

    # Define __get__, which is needed when Timer is used to decorate class functions
    def __get__(self, obj, objtype):
        # Return __call__ with the class object itself as an input argument
        return partial(self.__call__, obj)

    # Define what happens when you call the with statement with Timer, allowing the Timer class to work as a context
    # manager
    def __enter__(self):
        # Call the Timer class' start() function to start the Timer object
        self.start()
        # Return the timer object itself, which can then be used with an 'as timerName' statement to store the created
        # timer in the with statement within the variable timerName.
        return self

    # Define what happens when you finish the with statement with Timer.
    def __exit__(self, typ, value, traceback):
        # Call the Timer class' end() function to stop the timer and print the time elapsed from the with statement
        # being declared to the with statement ending.
        self.end()

    # Getter function for the threshold variable of the Timer object, which holds the threshold of the Timer class.
    def threshold_getter(self):
        # Check if the Time class object's display variable is equal to 'seconds'. If it is, return the Timer's
        # threshold in seconds.
        if self._display == 'seconds':
            return Timer._warn_threshold
        # Check if the Time class object's display variable is equal to 'minutes'. If it is, return the Timer's
        # threshold in minutes.
        elif self._display == 'minutes':
            return Timer._warn_threshold/60.0
        # Check if the Time class object's display variable is equal to 'hours'. If it is, return the Timer's
        # threshold in hours.
        elif self._display == 'hours':
            return Timer._warn_threshold/3600.0
        # If the display variable is somehow anything other than 'seconds', 'minutes', or 'hours', log an error and then
        # raise a ValueError with an error message stating that the input parameter for display could only be 'seconds',
        # 'minutes', or 'hours'.
        else:
            logging.error('{timer_name} display setting {units} is not a valid display unit. Input parameter for '
                          'display can only be seconds, minutes, or hours'.format(timer_name=self._timer_name,
                                                                                  units=self.display))
            raise ValueError('Input parameter for display can only be seconds, minutes, or hours')

    # classmethod threshold class-level variable setter function
    @classmethod
    def threshold_setter(cls, ithreshold):
        cls._warn_threshold = float(ithreshold) if isinstance(ithreshold, (float, int)) else 60

    # Getter property for the start_time variable of the Timer object, which holds the start time of the Timer object.
    @property
    def start_time(self):
        # Check if the Time class object's display variable is equal to 'seconds'. If it is, return the Timer's
        # start_time in seconds.
        if self._display == 'seconds':
            return self._start_time
        # Check if the Time class object's display variable is equal to 'minutes'. If it is, return the Timer's
        # start_time in minutes.
        elif self._display == 'minutes':
            return self._start_time/60.0
        # Check if the Time class object's display variable is equal to 'hours'. If it is, return the Timer's
        # start_time in hours.
        elif self._display == 'hours':
            return self._start_time/3600.0
        # If the display variable is somehow anything other than 'seconds', 'minutes', or 'hours', log an error and
        # raise a ValueError with an error message stating that the input parameter for display could only be 'seconds',
        # 'minutes', or 'hours'.
        else:
            logging.error('{timer_name} display setting {units} is not a valid display unit. Input parameter for '
                          'display can only be seconds, minutes, or hours'.format(timer_name=self._timer_name,
                                                                                  units=self.display))
            raise ValueError('Input parameter for display can only be seconds, minutes, or hours')

    # Getter property for the start_time variable of the Timer object, which holds the start time of the Timer object.
    @property
    def last_timer_result(self):
        # Check if the Time class object's display variable is equal to 'seconds'. If it is, return the Timer's
        # last_timer_result in seconds.
        if self._display == 'seconds':
            return self._last_timer_result
        # Check if the Time class object's display variable is equal to 'minutes'. If it is, return the Timer's
        # last_timer_result in minutes.
        elif self._display == 'minutes':
            return self._last_timer_result/60.0
        # Check if the Time class object's display variable is equal to 'hours'. If it is, return the Timer's
        # last_timer_result in hours.
        elif self._display == 'hours':
            return self._last_timer_result/3600.0
        # If the display variable is somehow anything other than 'seconds', 'minutes', or 'hours', log an error and
        # raise a ValueError with an error message stating that the input parameter for display could only be 'seconds',
        # 'minutes', or 'hours'.
        else:
            logging.error('{timer_name} display setting {units} is not a valid display unit. Input parameter for '
                          'display can only be seconds, minutes, or hours'.format(timer_name=self._timer_name,
                                                                                  units=self.display))
            raise ValueError('Input parameter for display can only be seconds, minutes, or hours')

    # Getter property for the display variable of the Timer object, which holds the display setting of Timer object
    @property
    def display(self):
        return self._display

    # Setter property for the display variable of the Timer object, which holds the display setting of Timer object
    @display.setter
    def display(self, units):
        # Check if the input value units is either 'seconds', 'minutes', and 'hours'. If it is, then set variable
        # display to that string.
        if units == 'seconds' or units == 'minutes' or units == 'hours':
            self._display = units
        # If the display variable is somehow anything other than 'seconds', 'minutes', or 'hours', log an error and then
        # raise a ValueError with an error message stating that the input parameter for display could only be 'seconds',
        # 'minutes', or 'hours'.
        else:
            logging.error('{timer_name} display setting {units} is not a valid display unit. Input parameter for '
                          'display can only be seconds, minutes, or hours'.format(timer_name=self._timer_name,
                                                                                  units=self.display))
            raise ValueError('Input parameter for display can only be seconds, minutes, or hours')

    # start() function
    #   Sets the start_time variable within the Timer object to the current time indicated by the time() function within
    #   the time module so long as variable start_time is set to None. Otherwise, start() raises an Exception
    #   stating that the Timer has already started and do nothing to the start_time variable.
    def start(self):
        # Check if the value of the variable start_time is None. If it is, then set start_time to the current time
        # indicated by time.time()
        if self._start_time is None:
            self._start_time = time.time()
        # If start_time is not None, log an error and then raise an Exception with an error message stating that the
        # Timer has already started and do nothing to the start_time variable.
        else:
            logging.error('The Timer has already started')
            raise Exception('The Timer has already started')

    # end() function
    #   Sets the end_time variable within the Timer object to the current time indicated by the time() function within
    #   the time module. Then, it calculates the time between the start() and end() function calls and stores it in the
    #   variable last_timer_result. Finally, it prints the calculated time between the start() and end() function calls.
    def end(self):
        # Check if the value of the variable start_time is not None. If it is not, then calculate the time elapsed
        # between calling start() and end() by subtracting start_time from the current time indicated by time.time(),
        # and assign the result to variable last_timer_result.
        if self._start_time is not None:
            self._last_timer_result = time.time() - self._start_time
            # Check if the time taken is less than or equal to the Timer class' threshold. If it is, INFO-level log
            # statements will be used to display the time elapsed.
            if self._last_timer_result <= Timer._warn_threshold:
                # Use a info level logging statement to display the time elapsed, with the format function used to
                # insert the timer_name, time elapsed/last_timer_result, and units/display on screen.
                logging.info('{timer_name} Time Elapsed (in {units}): {timer_result}'.format(timer_name=self._timer_name,
                                                                                             timer_result=self.last_timer_result,
                                                                                             units=self.display))
                # Print the time elapsed on screen, with the format function used to insert the timer_name,
                # time elapsed/last_timer_result, and units/display into the printed string.
                print('\t{timer_name} Time Elapsed: {timer_result} {units}'.format(timer_name=self._timer_name,
                                                                                   timer_result=self.last_timer_result,
                                                                                   units=self.display))
                self._start_time = None
                # Check if the Time class object's display variable is equal to 'minutes'. If it is, use an info level
                # logging statement to display the time elapsed in minutes.

            # Otherwise, if the time taken is greater than the Timer class threshold value, warn-level log statements
            # will be used to display the time elapsed rather than info-level log statements.
            else:
                # Use a warn level logging statement to display the time elapsed and warn the user that the time taken
                # was over the threshold time elapsed, with the format function used to insert the timer_name,
                # time elapsed/last_timer_result, threshold value/threshold, and units/display on screen.
                logging.warning('{timer_name} Time elapsed {timer_result} {units} is over the threshold time elapsed of'
                                ' {threshold_value} {units}'.format(timer_name=self._timer_name,
                                                                    timer_result=self.last_timer_result,
                                                                    threshold_value=self.threshold_getter(),
                                                                    units=self.display))
                # Print the time elapsed on screen, with the format function used to insert the timer_name,
                # time elapsed/last_timer_result, and units/display into the printed string.
                print('\t{timer_name} Time Elapsed: {timer_result} {units}'.format(timer_name=self._timer_name,
                                                                                   timer_result=self.last_timer_result,
                                                                                   units=self.display))
                # Set the Timer start_time object variable to None to indicate that the Timer object is no longer
                # ongoing and start() can once again be called to perform a new Timer operation.
                self._start_time = None

        # If the Timer object variable start_time is equal to None, log an error and then raise an Exception with an
        # error message on screen stating that the timer has not been started and to use the start() function to start
        # it.
        else:
            logging.error('The Timer has not been started (Use start() to start the timer)')
            raise Exception('The Timer has not been started (Use start() to start the timer)')

    # Getter property for the last_timer_result variable of the Timer object, which holds the last result calculated in
    # the timer.
    def last_result(self):
        # Check if the value assigned to the Timer object variable last_timer_result is not None. If it is not, return
        # the value of last_timer_result in accordance with the desired display units as indicated by Timer object
        # variable display.
        if self._last_timer_result is not None:
            # Check if the Time class object's display variable is equal to 'seconds'. If it is, return the value
            # assigned to the last_timer_result variable in seconds.
            if self._display == 'seconds':
                return self._last_timer_result
            # Check if the Time class object's display variable is equal to 'minutes'. If it is, return the value
            # assigned to the last_timer_result variable in minutes.
            elif self._display == 'minutes':
                return self._last_timer_result/60.0
            # Check if the Time class object's display variable is equal to 'hours'. If it is, return the value assigned
            # to the last_timer_result variable in hours.
            elif self._display == 'hours':
                return self._last_timer_result/3600.0
            # If the display variable is somehow anything other than 'seconds', 'minutes', or 'hours', log an error and
            # raise a ValueError with an error message stating that the input parameter for display could only be
            # 'seconds', 'minutes', or 'hours'.
            else:
                logging.error('{timer_name} display setting {units} is not a valid display unit. Input parameter for '
                              'display can only be seconds, minutes, or hours'.format(timer_name=self._timer_name,
                                                                                      units=self.display))
        # Otherwise, if the value assigned to Timer object variable last_timer_result is None, log an error and raise an
        # Exception with an error message stating that no Timer result has been calculated yet and return nothing.
        else:
            logging.error('No timer result has been calculated yet')
            raise Exception('No Timer result has been calculated yet')
