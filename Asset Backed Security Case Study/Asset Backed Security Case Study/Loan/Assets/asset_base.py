'''
Daniel McNulty II

This file contains the Assets base class
'''


# Import the logging module
import logging


# Declare the Assets class
class Asset(object):
    # Initialize and assign class-level variables for the Assets class objects' initial value and yearly depreciation
    # rate, to be used if users input values other than floats and ints into the asset object initialization function.
    _def_init_value = 100000
    _def_depr_rate = 0.1

    # Standard initialization function
    def __init__(self, init_val=None, depr_rate=None):
        # Initialize and set the object level protected variables for initial value and depreciation rate to the user
        # input initial value and depreciation rate. Cast each input parameter to a float in order to avoid any
        # complications or truncation that could occur when doing arithmetic with floats and ints in Python in later
        # Assets class functions. If what the user input for any of the values is not a float or an int, set that value
        # to the default value for that attribute as defined by the default value variables above. Use the
        # monthly_depreciation_rate static method in order to convert input annual rates to monthly rates.
        self._init_val = float(init_val) if isinstance(init_val, (float, int)) else float(Asset._def_init_value)
        self._depr_rate = Asset.monthly_depreciation_rate(float(depr_rate)) if isinstance(depr_rate, (float, int)) \
            else Asset.monthly_depreciation_rate(float(Asset._def_depr_rate))

    # Function to generate and return the string value of the Assets object
    def __str__(self):
        # Returns string of the Assets's attributes. This is accomplished by placing the attributes of the Assets into a
        # tuple of tuples with the attribute name ('Initial Value' and 'Depreciation Rate') and attribute's
        # corresponding value, and casting this tuple of tuples to a string.
        return 'Assets | Initial Value: {init_val} | ' \
               'Depreciation Rate: {depr_rate}'.format(init_val=self._init_val, depr_rate=self._depr_rate)

    # Function to generate and return the string value of the Assets object
    def __repr__(self):
        # Returns string of the Assets's attributes. This is accomplished by placing the attributes of the Assets into a
        # tuple of tuples with the attribute name ('Initial Value' and 'Depreciation Rate') and attribute's
        # corresponding value, and casting this tuple of tuples to a string.
        return 'Assets | Initial Value: {init_val} | ' \
               'Depreciation Rate: {depr_rate}'.format(init_val=self._init_val, depr_rate=self._depr_rate)

    # Getter property for the initial value of the Assets class object
    @property
    def init_val(self):
        return self._init_val

    # Setter property for the initial value of the Assets class object
    @init_val.setter
    def init_val(self, ival):
        # Check if input ival is of type int or float. If it is, then set the Assets object's init_val variable to ival.
        if isinstance(ival, (int, float)):
            self._init_val = ival
        # If input ival is not of type int or float, then log an error and raise a TypeError with an error message
        # stating that the input for the init_val setter must be of type float or int.
        else:
            logging.error('The initial value (init_val) setter input must be a float or an int. Your input {input} is'
                          'of type {type}, not a float or an int.'.format(input=ival, type=type(ival)))
            raise TypeError('The initial value (init_val) setter input must be a float or an int. Your input {input} is'
                            'of type {type}, not a float or an int.'.format(input=ival, type=type(ival)))

    # Getter property for the depreciation rate of the Assets class object
    @property
    def depr_rate(self):
        return self._depr_rate

    # Setter property for the depreciation rate of the Assets class object
    @depr_rate.setter
    def depr_rate(self, i_depr_rate):
        # Check if input i_depr_rate is of type int or float. If it is, then set the Assets object's depr_rate variable
        # to i_depr_rate.
        if isinstance(i_depr_rate, (int, float)):
            self._depr_rate = i_depr_rate
        # If input i_depr_rate is not of type int or float, then log an error and raise a TypeError with an error
        # message stating that the input for the depr_rate setter must be of type float or int.
        else:
            logging.error('The depreciation rate (depr_rate) setter input must be a float or an int. Your input '
                          '{input} is of type {type}, not a float or an int.'.format(input=i_depr_rate,
                                                                                     type=type(i_depr_rate)))
            raise TypeError('The depreciation rate (depr_rate) setter input must be a float or an int. Your input '
                            '{input} is of type {type}, not a float or an int.'.format(input=i_depr_rate,
                                                                                       type=type(i_depr_rate)))

    # static-level method to return a yearly depreciation rate from a passed-in monthly depreciation rate. Triggers a
    # not-implemented error, ensuring no one can directly instantiate an Assets object, making it an abstract class
    @staticmethod
    def annual_depreciation_rate(monthly_depreciation_rate):
        # Raise a NotImplementedError() when called. Makes the Assets class abstract.
        raise NotImplementedError()

    # static-level method to return a monthly depreciation rate from a passed-in yearly depreciation rate
    @staticmethod
    def monthly_depreciation_rate(annual_depreciation_rate):
        # Check if the input argument annual_depreciation_rate is an int or a float. If it is, calculate and return the
        # monthly depreciation rate from the input annual depreciation rate by dividing the annual depreciation rate by
        # 12. The annual_depreciation_rate is cast to a float before performing calculations in order to avoid
        # truncation or other complications from the use of floats and ints together in mathematics in Python.
        if isinstance(annual_depreciation_rate, (int, float)):
            return float(annual_depreciation_rate) / 12
        # Else, if the input argument annual_depreciation_rate is not an int or a float, log an error and raise a
        # TypeError with an error message telling users that the input into monthly_depreciation_rate() must be a float
        # or an int.
        else:
            logging.error('annual_depreciation_rate input into monthly_depreciation_rate(annual_depreciation_rate) '
                          'must be an int or a float. Your input {input} is of type {type}, not an int or a '
                          'float'.format(input=annual_depreciation_rate, type=type(annual_depreciation_rate)))
            raise TypeError('annual_depreciation_rate input into monthly_depreciation_rate(annual_depreciation_rate) '
                            'must be an int or a float. Your input {input} is of type {type}, not an int or a '
                            'float'.format(input=annual_depreciation_rate, type=type(annual_depreciation_rate)))

    # Function to return the current value of the Assets object for an passed-in period.
    def current_value(self, t):
        # Check if the input argument period t is a float or an int. If it is, then calculate the value of the asset at
        # the input period by multiplying the initial value of the asset by the total depreciation, as calculated using
        # (1 - monthly_depreciation_rate)**period. period is cast to a float before being used within calculations in
        # order to avoid truncation or other complications from the use of floats and ints together in mathematics in
        # Python.
        if isinstance(t, (int, float)):
            return self._init_val * ((1 - self._depr_rate)**float(t))
        else:
            # Else, if the period input t is not an int or a float, log an error and raise a TypeError with an error
            # message telling users that the input into current_value(t) must be a float or an int.
            logging.error('Input period t into current_value(t) must be of type int or float. Your input t = {input} '
                          'is of type {type}, not int or float.'.format(input=t, type=type(t)))
            raise TypeError('Input period t into current_value(t) must be of type int or float. Your input t = {input} '
                            'is of type {type}, not int or float.'.format(input=t, type=type(t)))
