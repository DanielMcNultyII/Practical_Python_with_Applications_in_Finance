'''
Daniel McNulty II

This file contains the classes derived from the Loan base class
    - FixedRateLoan
    - VariableRateLoan
    - AutoLoan
'''


# Import the Loan base class from the loan_base module
from Loan.loan_base import Loan
# Import the Car class from the car module within the Assets package. This is used by AutoLoan.
from Loan.Assets.car import Car
# Import the logging module
import logging


# VARIABLE AND FIXED RATE LOAN DERIVED CLASSES =========================================================================
# Declare the FixedRateLoan class and derive it from the Loan class
class FixedRateLoan(Loan):
    # Function to generate and return the string value of the FixedRateLoan object
    def __str__(self):
        # Returns string of the FixedRateLoan's attributes. This is accomplished by placing the attributes of the
        # FixedRateLoan into a tuple of tuples with the attribute name and attribute's corresponding value, and casting
        # this tuple of tuples to a string.
        return 'FixedRateLoan | Face: {face} | Rate: {rate} | Term: {term} | ' \
               'Assets: {asset}'.format(face=self._face,
                                       rate=Loan.annual_rate(self._rate),
                                       term=self._term,
                                       asset=self._asset)

    # Function to generate and return the string value of the FixedRateLoan object
    def __repr__(self):
        # Returns string of the FixedRateLoan's attributes. This is accomplished by placing the attributes of the
        # FixedRateLoan into a tuple of tuples with the attribute name and attribute's corresponding value, and casting
        # this tuple of tuples to a string.
        return 'FixedRateLoan | Face: {face} | Rate: {rate} | Term: {term} | ' \
               'Assets: {asset}'.format(face=self._face,
                                       rate=Loan.annual_rate(self._rate),
                                       term=self._term,
                                       asset=self._asset)

    # Overrides the base class rate() function
    # For a Fixed Rate Loan, just return the rate
    def rate(self, t=0.0):
        return self._rate


# Declare the VariableRateLoan class and derive it from the Loan class
class VariableRateLoan(Loan):
    # Override the base class __init__() function because we want a rateDict input that the
    # base class doesn't know about.
    #   Uses the base class within the derived class __init__ to set the input face and term
    #   Set the rate parameter to None because we do not need the rate parameter for
    #   VariableRateLoan, we use the rateDict
    #
    # We want a dictionary of rates for each period (Real life is more complicated)
    #   ie. rateDict = {0:.025, 15:.045, ...}
    #           Assumes that the last value in the dict is the rate for the rest of later
    #           periods
    #           Only value that is ESSENTIAL is the rate at period 0
    def __init__(self, loan_num=None, face=None, rate_dict=None, term=None, asset=None):
        # Check if the input for the rate_dict variable is of the type dict. If it is, then initialize the
        # VariableRateLoan object with the input parameters
        if isinstance(rate_dict, dict):
            super(VariableRateLoan, self).__init__(loan_num, face, None, term, asset)
            self._rate_dict = rate_dict
        # If the input for the rate_dict variable is not of the type dict, then log an error and raise a TypeError with
        # an error message that says the VariableRateLoan rate_dict variable must be a dict.
        else:
            logging.error('Input for the VariableRateLoan rate_dict variable must be dict. Your input for rate dict'
                          '({input}) is of type {type}, not a dict'.format(input=rate_dict, type=type(rate_dict)))
            raise TypeError('Input for the VariableRateLoan rate_dict variable must be dict. Your input for rate dict'
                            '({input}) is of type {type}, not a dict'.format(input=rate_dict, type=type(rate_dict)))

    # Function to generate and return the string value of the VariableRateLoan object
    def __str__(self):
        # Returns string of the VariableRateLoan's attributes. This is accomplished by placing the attributes of the
        # VariableRateLoan into a tuple of tuples with the attribute name and attribute's corresponding value, and
        # casting this tuple of tuples to a string.
        return 'Variable Rate Loan: {face}, {rate_dict}, {term}, {asset}'.format(face=('Face', self._face),
                                                                                 rate_dict=('Rate', self._rate_dict),
                                                                                 term=('Term', self._term),
                                                                                 asset=('Assets', self._asset))

    # Function to generate and return the string value of the VariableRateLoan object
    def __repr__(self):
        # Returns string of the VariableRateLoan's attributes. This is accomplished by placing the attributes of the
        # VariableRateLoan into a tuple of tuples with the attribute name and attribute's corresponding value, and
        # casting this tuple of tuples to a string.
        return 'Variable Rate Loan: {face}, {rate_dict}, {term}, {asset}'.format(face=('Face', self._face),
                                                                                 rate_dict=('Rate', self._rate_dict),
                                                                                 term=('Term', self._term),
                                                                                 asset=('Assets', self._asset))

    # Overrides the base class rate() function
    def rate(self, t):
        # Get a list of the keyword startPeriods and store it in variable start_times
        start_times = sorted(list(self._rate_dict))
        # Check if the input period is an int or float.
        if isinstance(t, int):
            # Initially check if the input period is negative. If it is, log an error and raise a ValueError with an
            # error message that states the input period for rate(t) must be a positive int.
            if t < 0.0:
                logging.error('The input period for rate(t) must be a positive int. Your input t = {input} is below'
                              '0'.format(input=t, type=type(t)))
                raise ValueError('The input period for rate(t) must be a positive int. Your input t = {input} is below'
                                 '0'.format(input=t, type=type(t)))
            # Otherwise, check if the input period is greater than or equal to the last startPeriod in start_times.
            # If it is, then return the value associated with that startPeriod in rate_dict.
            elif t >= start_times[-1]:
                return self._rate_dict[start_times[-1]]
            # If the above criteria has not been reached, initialize a for loop that goes through the range of indices
            # of the above-created start_times.
            else:
                for n in range(0, len(start_times)):
                    # Otherwise, check if the input period is between the startPeriods in start_times that are
                    # referred to by start_times[n] and start_times[n + 1]. If it is, then return the value within
                    # the VariableRateLoan rate_dict that corresponds to startPeriod start_times[n].
                    if start_times[n] <= t < start_times[n + 1]:
                        return self._rate_dict[start_times[n]]
                    # If none of the above criteria has been met, then continue to the next iteration of the for
                    # loop.
                    else:
                        continue
        # If the input period is not an int, log an error and raise a TypeError that tells users the input period for
        # rate(t) must be a positive int.
        else:
            logging.error('The input period for rate(t) must be a positive int. Your input for t = {input} is of type'
                          '{type}, not int.'.format(input=t, type=type(t)))
            raise TypeError('The input period for rate(t) must be a positive int. Your input for t = {input} is of type'
                            '{type}, not int.'.format(input=t, type=type(t)))


# AUTOMOBILE DERIVED LOAN CLASS ========================================================================================
# Declare the AutoLoan class and derive it from the Loan class
class AutoLoan(FixedRateLoan):
    # Standard initialization function
    def __init__(self, loan_num=None, face=None, annual_rate=None, term=None, car=None):
        # Check if the input for the car variable is of the Car class. Checking if its part of the Car class allows for
        # the input to be of either the Car class or one of Car's derived classes (ie. Civic, Lexus, Lamborghini).
        if isinstance(car, Car):
            # Use super() in order to avoid duplicating the functionality of the base class __init__ function to set the
            # face, rate, and term of the AutoLoan
            super(AutoLoan, self).__init__(loan_num, face, annual_rate, term, car)
            # Store the user input Car asset that the Loan is based on within the variable car. If the user does not
            # input a Car object, or an object of one of its derived classes, then set the car object level protected
            # variable to a default Car object of $30,000 and the default depreciation rate of the Car class.
            self._car = car
        # If the input for car is not of the Car class, then raise a TypeError with an error message stating that the
        # input for the AutoLoan's car variable must be of the Car class or any of its derived classes.
        else:
            logging.error('Input for the AutoLoan car variable must be of the Car class or any of its derived classes.'
                          'Your input for car ({input}) is of type {type}, not the Car class or any of its derived '
                          'classes'.format(input=car, type=type(car)))
            raise TypeError('Input for the AutoLoan car variable must be of the Car class or any of its derived '
                            'classes. Your input for car ({input}) is of type {type}, not the Car class or any of its '
                            'derived classes'.format(input=car, type=type(car)))

    # Function to generate and return the string value of the AutoLoan object
    def __str__(self):
        # Returns string of the AutoLoan's attributes. This is accomplished by placing the attributes of the AutoLoan
        # into a tuple of tuples with the attribute name and attribute's corresponding value, and casting this tuple of
        # tuples to a string.
        return 'Auto Loan | Face: {face} | Rate: {rate} | Term: {term} | ' \
               'Assets: {asset}'.format(face=self._face,
                                       rate=Loan.annual_rate(self._rate),
                                       term=self._term,
                                       asset=self._asset)

    # Function to generate and return the string value of the AutoLoan object
    def __repr__(self):
        # Returns string of the AutoLoan's attributes. This is accomplished by placing the attributes of the AutoLoan
        # into a tuple of tuples with the attribute name and attribute's corresponding value, and casting this tuple of
        # tuples to a string.
        return 'Auto Loan | Face: {face} | Rate: {rate} | Term: {term} | ' \
               'Assets: {asset}'.format(face=self._face,
                                       rate=Loan.annual_rate(self._rate),
                                       term=self._term,
                                       asset=self._asset)
