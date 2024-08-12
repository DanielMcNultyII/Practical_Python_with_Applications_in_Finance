'''
Daniel McNulty II

This file contains the Car asset classes
    - Car
        - Civic
        - Lexus
        - Lamborghini
'''


# Import the Assets class from the asset_base module
from Loan.Assets.asset_base import Asset
# Import logging
import logging


# Declare the Car class derived from the Assets class
class Car(Asset):
    # Standard initialization function
    # Default depreciation rate for the Car class is set to 0.1 by making the depr_rate a keyword argument with a
    # default setting of 0.1.
    def __init__(self, init_val, depr_rate=0.1):
        # Call super in order to avoid duplicating duplicating the functionality within this __init__ that is already
        # contained within the base Assets class __init__
        super(Car, self).__init__(init_val, depr_rate)

    # Function to generate and return the string value of the Car object
    def __str__(self):
        # Returns string of the Car's attributes. This is accomplished by placing the attributes of the Car into a
        # tuple of tuples with the attribute name ('Initial Value' and 'Depreciation Rate') and attribute's
        # corresponding value, and casting this tuple of tuples to a string.
        return 'Car | Initial Value: {init_val} | ' \
               'Depreciation Rate: {depr_rate}'.format(init_val=self._init_val, depr_rate=self._depr_rate)

    # Function to generate and return the string value of the Car object
    def __repr__(self):
        # Returns string of the Car's attributes. This is accomplished by placing the attributes of the Car into a
        # tuple of tuples with the attribute name ('Initial Value' and 'Depreciation Rate') and attribute's
        # corresponding value, and casting this tuple of tuples to a string.
        return 'Car | Initial Value: {init_val} | ' \
               'Depreciation Rate: {depr_rate}'.format(init_val=self._init_val, depr_rate=self._depr_rate)

    # static-level method to return a yearly depreciation rate from a passed-in monthly depreciation rate
    @staticmethod
    def annual_depreciation_rate(monthly_depreciation_rate):
        # Check if the input argument monthly_depreciation_rate is an int or a float. If it is, calculate and return the
        # annual depreciation rate from the input monthly depreciation rate by multiplying the monthly depreciation rate
        # by 12. The monthly_depreciation_rate is cast to a float before performing calculations in order to avoid
        # truncation or other complications from the use of floats and ints together in mathematics in Python.
        if isinstance(monthly_depreciation_rate, (int, float)):
            return float(monthly_depreciation_rate) * 12
        # Else, if the input argument monthly_depreciation_rate is not an int or a float, log an error and raise a
        # TypeError with an error message telling users that the input into annual_depreciation_rate() must be a float
        # or an int.
        else:
            logging.error('monthly_depreciation_rate input into annual_depreciation_rate(monthly_depreciation_rate) '
                          'must be an int or a float. Your input {input} is of type {type}, not a float or an '
                          'int.'.format(input=monthly_depreciation_rate, type=type(monthly_depreciation_rate)))
            raise TypeError('monthly_depreciation_rate input into annual_depreciation_rate(monthly_depreciation_rate) '
                            'must be an int or a float. Your input {input} is of type {type}, not a float or an '
                            'int.'.format(input=monthly_depreciation_rate, type=type(monthly_depreciation_rate)))


# Declare the Civic class derived from the Car class
class Civic(Car):
    # Standard initialization function
    # Default depreciation rate for the Civic class is set to 0.3 by making the depr_rate a keyword argument with a
    # default setting of 0.3.
    def __init__(self, init_val, depr_rate=0.3):
        # Call super in order to avoid duplicating duplicating the functionality within this __init__ that is already
        # contained within the base Assets class __init__
        super(Civic, self).__init__(init_val, depr_rate)

    # Function to generate and return the string value of the Civic object
    def __str__(self):
        # Returns string of the Civic's attributes. This is accomplished by placing the attributes of the Civic into a
        # tuple of tuples with the attribute name ('Initial Value' and 'Depreciation Rate') and attribute's
        # corresponding value, and casting this tuple of tuples to a string.
        return 'Civic | Initial Value: {init_val} | ' \
               'Depreciation Rate: {depr_rate}'.format(init_val=self._init_val, depr_rate=self._depr_rate)

    # Function to generate and return the string value of the Civic object
    def __repr__(self):
        # Returns string of the Civic's attributes. This is accomplished by placing the attributes of the Civic into a
        # tuple of tuples with the attribute name ('Initial Value' and 'Depreciation Rate') and attribute's
        # corresponding value, and casting this tuple of tuples to a string.
        return 'Civic | Initial Value: {init_val} | ' \
               'Depreciation Rate: {depr_rate}'.format(init_val=self._init_val, depr_rate=self._depr_rate)

    # static-level method to return a yearly depreciation rate from a passed-in monthly depreciation rate
    @staticmethod
    def annual_depreciation_rate(monthly_depreciation_rate):
        # Check if the input argument monthly_depreciation_rate is an int or a float. If it is, calculate and return the
        # annual depreciation rate from the input monthly depreciation rate by multiplying the monthly depreciation rate
        # by 12. The monthly_depreciation_rate is cast to a float before performing calculations in order to avoid
        # truncation or other complications from the use of floats and ints together in mathematics in Python.
        if isinstance(monthly_depreciation_rate, (int, float)):
            return float(monthly_depreciation_rate) * 12
        # Else, if the input argument monthly_depreciation_rate is not an int or a float, log an error and raise a
        # TypeError with an error message telling users that the input into annual_depreciation_rate() must be a float
        # or an int.
        else:
            logging.error('monthly_depreciation_rate input into annual_depreciation_rate(monthly_depreciation_rate) '
                          'must be an int or a float. Your input {input} is of type {type}, not a float or an '
                          'int.'.format(input=monthly_depreciation_rate, type=type(monthly_depreciation_rate)))
            raise TypeError('monthly_depreciation_rate input into annual_depreciation_rate(monthly_depreciation_rate) '
                            'must be an int or a float. Your input {input} is of type {type}, not a float or an '
                            'int.'.format(input=monthly_depreciation_rate, type=type(monthly_depreciation_rate)))


# Declare the Lexus class derived from the Car class
class Lexus(Car):
    # Standard initialization function
    # Default depreciation rate for the Lexus class is set to 0.15 by making the depr_rate a keyword argument with a
    # default setting of 0.15.
    def __init__(self, init_val, depr_rate=0.15):
        # Call super in order to avoid duplicating duplicating the functionality within this __init__ that is already
        # contained within the base Assets class __init__
        super(Lexus, self).__init__(init_val, depr_rate)

    # Function to generate and return the string value of the Lexus object
    def __str__(self):
        # Returns string of the Lexus's attributes. This is accomplished by placing the attributes of the Lexus into a
        # tuple of tuples with the attribute name ('Initial Value' and 'Depreciation Rate') and attribute's
        # corresponding value, and casting this tuple of tuples to a string.
        return 'Lexus | Initial Value: {init_val} | ' \
               'Depreciation Rate: {depr_rate}'.format(init_val=self._init_val, depr_rate=self._depr_rate)

    # Function to generate and return the string value of the Lexus object
    def __repr__(self):
        # Returns string of the Lexus's attributes. This is accomplished by placing the attributes of the Lexus into a
        # tuple of tuples with the attribute name ('Initial Value' and 'Depreciation Rate') and attribute's
        # corresponding value, and casting this tuple of tuples to a string.
        return 'Lexus | Initial Value: {init_val} | ' \
               'Depreciation Rate: {depr_rate}'.format(init_val=self._init_val, depr_rate=self._depr_rate)

    # static-level method to return a yearly depreciation rate from a passed-in monthly depreciation rate
    @staticmethod
    def annual_depreciation_rate(monthly_depreciation_rate):
        # Check if the input argument monthly_depreciation_rate is an int or a float. If it is, calculate and return the
        # annual depreciation rate from the input monthly depreciation rate by multiplying the monthly depreciation rate
        # by 12. The monthly_depreciation_rate is cast to a float before performing calculations in order to avoid
        # truncation or other complications from the use of floats and ints together in mathematics in Python.
        if isinstance(monthly_depreciation_rate, (int, float)):
            return float(monthly_depreciation_rate) * 12
        # Else, if the input argument monthly_depreciation_rate is not an int or a float, log an error and raise a
        # TypeError with an error message telling users that the input into annual_depreciation_rate() must be a float
        # or an int.
        else:
            logging.error('monthly_depreciation_rate input into annual_depreciation_rate(monthly_depreciation_rate) '
                          'must be an int or a float. Your input {input} is of type {type}, not a float or an '
                          'int.'.format(input=monthly_depreciation_rate, type=type(monthly_depreciation_rate)))
            raise TypeError('monthly_depreciation_rate input into annual_depreciation_rate(monthly_depreciation_rate) '
                            'must be an int or a float. Your input {input} is of type {type}, not a float or an '
                            'int.'.format(input=monthly_depreciation_rate, type=type(monthly_depreciation_rate)))


# Declare the Lamborghini class derived from the Car class
class Lamborghini(Car):
    # Standard initialization function
    # Default depreciation rate for the Lamborghini class is set to 0.05 by making the depr_rate a keyword argument with
    # a default setting of 0.05.
    def __init__(self, init_val, depr_rate=0.05):
        # Call super in order to avoid duplicating duplicating the functionality within this __init__ that is already
        # contained within the base Assets class __init__
        super(Lamborghini, self).__init__(init_val, depr_rate)

    # Function to generate and return the string value of the Lamborghini object
    def __str__(self):
        # Returns string of the Lamborghini's attributes. This is accomplished by placing the attributes of the
        # Lamborghini into a tuple of tuples with the attribute name ('Initial Value' and 'Depreciation Rate') and
        # attribute's corresponding value, and casting this tuple of tuples to a string.
        return 'Lamborghini | Initial Value: {init_val} | ' \
               'Depreciation Rate: {depr_rate}'.format(init_val=self._init_val, depr_rate=self._depr_rate)

    # Function to generate and return the string value of the Lamborghini object
    def __repr__(self):
        # Returns string of the Lamborghini's attributes. This is accomplished by placing the attributes of the
        # Lamborghini into a tuple of tuples with the attribute name ('Initial Value' and 'Depreciation Rate') and
        # attribute's corresponding value, and casting this tuple of tuples to a string.
        return 'Lamborghini | Initial Value: {init_val} | ' \
               'Depreciation Rate: {depr_rate}'.format(init_val=self._init_val, depr_rate=self._depr_rate)

    # static-level method to return a yearly depreciation rate from a passed-in monthly depreciation rate
    @staticmethod
    def annual_depreciation_rate(monthly_depreciation_rate):
        # Check if the input argument monthly_depreciation_rate is an int or a float. If it is, calculate and return the
        # annual depreciation rate from the input monthly depreciation rate by multiplying the monthly depreciation rate
        # by 12. The monthly_depreciation_rate is cast to a float before performing calculations in order to avoid
        # truncation or other complications from the use of floats and ints together in mathematics in Python.
        if isinstance(monthly_depreciation_rate, (int, float)):
            return float(monthly_depreciation_rate) * 12
        # Else, if the input argument monthly_depreciation_rate is not an int or a float, log an error and raise a
        # TypeError with an error message telling users that the input into annual_depreciation_rate() must be a float
        # or an int.
        else:
            logging.error('monthly_depreciation_rate input into annual_depreciation_rate(monthly_depreciation_rate) '
                          'must be an int or a float. Your input {input} is of type {type}, not a float or an '
                          'int.'.format(input=monthly_depreciation_rate, type=type(monthly_depreciation_rate)))
            raise TypeError('monthly_depreciation_rate input into annual_depreciation_rate(monthly_depreciation_rate) '
                            'must be an int or a float. Your input {input} is of type {type}, not a float or an '
                            'int.'.format(input=monthly_depreciation_rate, type=type(monthly_depreciation_rate)))
