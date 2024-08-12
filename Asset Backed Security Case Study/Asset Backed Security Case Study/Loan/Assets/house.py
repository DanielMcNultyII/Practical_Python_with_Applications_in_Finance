'''
Daniel McNulty II

This file contains the House asset classes
    - HouseBase
        - PrimaryHome
        - VacationHome
'''


# Import the Assets class from the asset_base module
from Loan.Assets.asset_base import Asset
# Import logging
import logging


# Declare the HouseBase class derived from the Assets class
class HouseBase(Asset):
    # Standard initialization function
    # Default depreciation rate for the HouseBase class is set to 0.25 by making the depr_rate a keyword argument with
    # a default setting of 0.25.
    def __init__(self, init_val, depr_rate=0.25):
        # Call super in order to avoid duplicating duplicating the functionality within this __init__ that is already
        # contained within the base Assets class __init__
        super(HouseBase, self).__init__(init_val, depr_rate)

    # Function to generate and return the string value of the HouseBase object
    def __str__(self):
        # Returns string of the HouseBase's attributes. This is accomplished by placing the attributes of the HouseBase
        # into a tuple of tuples with the attribute name ('Initial Value' and 'Depreciation Rate') and attribute's
        # corresponding value, and casting this tuple of tuples to a string.
        return 'House (Base) | Initial Value: {init_val} | ' \
               'Depreciation Rate: {depr_rate}'.format(init_val=self._init_val, depr_rate=self._depr_rate)

    # Function to generate and return the string value of the HouseBase object
    def __repr__(self):
        # Returns string of the HouseBase's attributes. This is accomplished by placing the attributes of the HouseBase
        # into a tuple of tuples with the attribute name ('Initial Value' and 'Depreciation Rate') and attribute's
        # corresponding value, and casting this tuple of tuples to a string.
        return 'House (Base) | Initial Value: {init_val} | ' \
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


# Declare the PrimaryHome class derived from the HouseBase class
class PrimaryHome(HouseBase):
    # Standard initialization function
    # Default depreciation rate for the PrimaryHome class is set to 0.15 by making the depr_rate a keyword argument with
    # a default setting of 0.15.
    def __init__(self, init_val, depr_rate=0.15):
        # Call super in order to avoid duplicating duplicating the functionality within this __init__ that is already
        # contained within the base Assets class __init__
        super(PrimaryHome, self).__init__(init_val, depr_rate)

    # Function to generate and return the string value of the PrimaryHome object
    def __str__(self):
        # Returns string of the PrimaryHome's attributes. This is accomplished by placing the attributes of the
        # PrimaryHome into a tuple of tuples with the attribute name ('Initial Value' and 'Depreciation Rate') and
        # attribute's corresponding value, and casting this tuple of tuples to a string.
        return 'Primary Home | Initial Value: {init_val} | ' \
               'Depreciation Rate: {depr_rate}'.format(init_val=self._init_val, depr_rate=self._depr_rate)

    # Function to generate and return the string value of thePrimaryHome object
    def __repr__(self):
        # Returns string of the PrimaryHome's attributes. This is accomplished by placing the attributes of the
        # PrimaryHome into a tuple of tuples with the attribute name ('Initial Value' and 'Depreciation Rate') and
        # attribute's corresponding value, and casting this tuple of tuples to a string.
        return 'Primary Home | Initial Value: {init_val} | ' \
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
        # Else, if the input argument monthly_depreciation_rate is not an int or a float, raise a TypeError with an
        # error message telling users that the input into annual_depreciation_rate() must be a float or an int.
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


# Declare the VacationHome class derived from the HouseBase class
class VacationHome(HouseBase):
    # Standard initialization function
    # Default depreciation rate for the VacationHome class is set to 0.1 by making the depr_rate a keyword argument with
    # a default setting of 0.1.
    def __init__(self, init_val, depr_rate=0.1):
        # Call super in order to avoid duplicating duplicating the functionality within this __init__ that is already
        # contained within the base Assets class __init__
        super(VacationHome, self).__init__(init_val, depr_rate)

    # Function to generate and return the string value of the VacationHome object
    def __str__(self):
        # Returns string of the VacationHome's attributes. This is accomplished by placing the attributes of the
        # VacationHome into a tuple of tuples with the attribute name ('Initial Value' and 'Depreciation Rate') and
        # attribute's corresponding value, and casting this tuple of tuples to a string.
        return 'Vacation Home | Initial Value: {init_val} | ' \
               'Depreciation Rate: {depr_rate}'.format(init_val=self._init_val, depr_rate=self._depr_rate)

    # Function to generate and return the string value of the VacationHome object
    def __repr__(self):
        # Returns string of the VacationHome's attributes. This is accomplished by placing the attributes of the
        # VacationHome into a tuple of tuples with the attribute name ('Initial Value' and 'Depreciation Rate') and
        # attribute's corresponding value, and casting this tuple of tuples to a string.
        return 'Vacation Home | Initial Value: {init_val} | ' \
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
