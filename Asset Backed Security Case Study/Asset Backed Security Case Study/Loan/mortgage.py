'''
Daniel McNulty II

This file contains classes pertaining to mortgages. Specifically:
    -MortgageMixin
        -FixedMortgage
        -VariableMortgage
'''


# Import the base Loan class from the loan_base module
from Loan.loan_base import Loan
# Import the FixedRateLoan and VariableRateLoan classes from the loans module.
from Loan.loans import FixedRateLoan, VariableRateLoan
# Import the base HouseBase class from the house module
from Loan.Assets.house import HouseBase
# Import the logging module
import logging


# Declare the MortgageMixin class, which does not derive from loan itself, instead simply defines things specific to a
# mortgage
class MortgageMixin(object):
    # MortgageMixin.__init__(self)
    #   Since we know that the MortgageMixin will be related to the Loan class, we put the
    #   super(MortgageMixin, self).__init__(), which invokes the __init__ function of the base
    #   class if there is a base class
    #       At the moment there is no base class.
    def __init__(self, house, loan_num=1, face=1, rate=1, term=1):
        # Check if the input for the house variable is of the HouseBase class. Checking if its part of the HouseBase
        # class allows for the input to be of either the HouseBase class or one of HouseBase's derived classes
        # (ie. PrimaryHome, VacationHome).
        if isinstance(house, HouseBase):
            # Initialize MortgageMixin object level protected variables.
            self._home = house
            self._loan_num = loan_num
            self._face = face
            self._rate = rate
            self._term = term
        # If the input for home is not of the HouseBase class, then log an error and raise a TypeError with an error
        # message stating that the input for the MortgageMixin's home variable must be of the HouseBase class or any of
        # its derived classes.
        else:
            logging.error('Input for the MortgageMixin home variable must be of the HouseBase class or any of its '
                          'derived classes. Your input ({input}) is of type {type}, not of the HouseBase class or any '
                          'of its variables.'.format(input=house, type=type(house)))
            raise TypeError('Input for the MortgageMixin home variable must be of the HouseBase class or any of its '
                            'derived classes. Your input ({input}) is of type {type}, not of the HouseBase class or '
                            'any of its variables.'.format(input=house, type=type(house)))

    # Private Mortgage Insurance (PMI)
    #   If your mortgage loan is greater than 80% of the asset value (ie. If you have a $100,000 home and your mortgage
    #   is over $80,000 dollars), you're required by law to pay for PMI
    #       Complex formula
    #   Currently returns 0.0075% of the loan's face value if the LTV (Loan-To-Value ratio) is less than 80%.
    def pmi(self):
        # Calculate the LTV of the mortgage
        ltv = float(self._face) / float(self._home.init_val)
        # If the LTV is greater than or equal to 80% (0.8), return .0075% (.000075) of the face value of the loan.
        # Otherwise, return 0.0, since there is no need for the PMI.
        return 0.000075 * self._face if ltv >= 0.8 else 0.0

    # Declare and implement monthly_payment()
    def monthly_payment(self, t=0.0):
        # Check if the input t is an int or a float
        if isinstance(t, (int, float)):
            # Check if the input period is greater than or equal to the loan's maturity. If it is, then return 0.0.
            if t >= self._term:
                return 0.0
            # Check if the input t is within the lifetime of the loan, from period 0 to the loan's maturity
            elif 0.0 <= t < self._term:
                # Call super to avoid duplicating the monthly_payment() formula within the Loan base class and add the
                # result of pmi() to the result of calling monthly_payment(). Return the sum.
                return super(MortgageMixin, self).monthly_payment(t) + self.pmi()
            # Otherwise, if t is negative, log an error and raise a ValueError with an error message to the screen
            # stating that the input parameter t cannot be below 0.
            else:
                logging.error('Input period t into monthly_payment(t) cannot be below 0. Your input t = {input} is '
                              'below 0.'.format(input=t))
                raise ValueError('Input period t into monthly_payment(t) cannot be below 0. Your input t = {input} is '
                                 'below 0.'.format(input=t))
        # If t is not a float or an int, log an error and raise a TypeError with an error message stating that the input
        # for monthly_payment() needs to be a float or int.
        else:
            logging.error('Input period t into monthly_payment(t) must be of type int or float. Your input t = {input} '
                          'is of type {type}, not int or float.'.format(input=t, type=type(t)))
            raise TypeError('Input period t into monthly_payment(t) must be of type int or float. Your input t = '
                            '{input} is of type {type}, not int or float.'.format(input=t, type=type(t)))

    # Declare and implement explicit_principal_due()
    def principal_due(self, t=0.0):
        # Check if the input t is an int or a float
        if isinstance(t, (int, float)):
            # Check if the input period is greater than or equal to the loan's maturity. If it is, then return 0.0.
            if t >= self._term:
                return 0.0
            # Check if the input t is within the lifetime of the loan, from period 0 to the loan's maturity
            elif 0.0 <= t < self._term:
                # Subtract the interest due in a given period as calculated by interest_due() from the monthly payment
                # for that period as calculated by monthly_payment()
                return self.monthly_payment(t) - self.interest_due(t)
            # Otherwise, if t is negative, log an error and raise a ValueError with an error message to the screen
            # stating that the input period t for monthly_payment(t) cannot be below 0.
            else:
                logging.error('Input period t into principal_due(t) cannot be below 0. Your input t = {input} is below '
                              '0.'.format(input=t))
                raise ValueError('Input period t into principal_due(t) cannot be below 0. Your input t = {input} is '
                                 'below 0.'.format(input=t))
        # If t is not a float or an int, raise a TypeError with an error message stating that the input period t for
        # monthly_payment(t) needs to be a float or int and return nothing
        else:
            logging.error('Input period t into principal_due(t) must be of type int or float. Your input t = {input} '
                          'is of type {type}, not int or float.'.format(input=t, type=type(t)))
            raise TypeError('Input period t into principal_due(t) must be of type int or float. Your input t = {input} '
                            'is of type {type}, not int or float.'.format(input=t, type=type(t)))


# Declare the FixedMortgage class derived from the base MortgageMixin and FixedRateLoan classes
class FixedMortgage(MortgageMixin, FixedRateLoan):
    # Standard initialization function
    def __init__(self, loan_num=None, face=None, annual_rate=None, term=None, home=None):
        # Check if the input for the home variable is of the HouseBase class. Checking if its part of the HouseBase
        # class allows for the input to be of either the HouseBase class or one of HouseBase's derived classes
        # (ie. PrimaryHome, VacationHome).
        if isinstance(home, HouseBase):
            # Call on the FixedRateLoan __init__ function individually, since the MortgageMixin function takes
            # precedence over it in super().
            FixedRateLoan.__init__(self, loan_num, face, annual_rate, term, home)
            super(FixedMortgage, self).__init__(home)
        # If the input for home is not of the HouseBase class, then log an error and raise a TypeError with an error
        # message stating that the input for the FixedMortgage's home variable must be of the HouseBase class or any of
        # its derived classes.
        else:
            logging.error('Input for the FixedMortgage home variable must be of the HouseBase class or any of its '
                          'derived classes. Your input ({input}) is of type {type}, not of the HouseBase class or any '
                          'of its variables.'.format(input=home, type=type(home)))
            raise TypeError('Input for the FixedMortgage home variable must be of the HouseBase class or any of its '
                            'derived classes. Your input ({input}) is of type {type}, not of the HouseBase class or '
                            'any of its variables.'.format(input=home, type=type(home)))

    # Function to generate and return the string value of the FixedMortgage object
    def __str__(self):
        # Returns string of the FixedMortgage's attributes. This is accomplished by placing the attributes of the
        # FixedMortgage into a tuple of tuples with the attribute name and attribute's corresponding value, and casting
        # this tuple of tuples to a string.
        return 'Fixed Mortgage | Face: {face} | Rate: {rate} | Term: {term} | ' \
               'Assets: {asset}'.format(face=self._face,
                                       rate=Loan.annual_rate(self._rate),
                                       term=self._term,
                                       asset=self._asset)

    # Function to generate and return the string value of the FixedMortgage object
    def __repr__(self):
        # Returns string of the FixedMortgage's attributes. This is accomplished by placing the attributes of the
        # FixedMortgage into a tuple of tuples with the attribute name and attribute's corresponding value, and casting
        # this tuple of tuples to a string.
        return 'Fixed Mortgage | Face: {face} | Rate: {rate} | Term: {term} | ' \
               'Assets: {asset}'.format(face=self._face,
                                       rate=Loan.annual_rate(self._rate),
                                       term=self._term,
                                       asset=self._asset)


# Declare the VariableMortgage class derived from the base MortgageMixin and VariableRateLoan classes
class VariableMortgage(MortgageMixin, VariableRateLoan):
    # Standard initialization function
    def __init__(self, loan_num=None, face=None, rate_dict=None, term=None, home=None):
        # Check if the input for the home variable is of the HouseBase class. Checking if its part of the HouseBase
        # class allows for the input to be of either the HouseBase class or one of HouseBase's derived classes
        # (ie. PrimaryHome, VacationHome).
        if isinstance(home, HouseBase):
            # Call on the VariableRateLoan __init__ function individually, since the MortgageMixin function takes
            # precedence over it in super() as it is listed first in the VariableMortgage declaration.
            VariableRateLoan.__init__(self, loan_num, face, rate_dict, term, home)
            super(VariableMortgage, self).__init__(home)
        # If the input for home is not of the HouseBase class, then log an error and raise a TypeError with an error
        # message stating that the input for the VariableMortgage's home variable must be of the HouseBase class or any
        # of its derived classes.
        else:
            logging.error('Input for the VariableMortgage home variable must be of the HouseBase class or any of its '
                          'derived classes. Your input ({input}) is of type {type}, not of the HouseBase class or any '
                          'of its variables.'.format(input=home, type=type(home)))
            raise TypeError('Input for the VariableMortgage home variable must be of the HouseBase class or any of its '
                            'derived classes. Your input ({input}) is of type {type}, not of the HouseBase class or '
                            'any of its variables.'.format(input=home, type=type(home)))

    # Function to generate and return the string value of the VariableRateLoan object
    def __str__(self):
        # Returns string of the VariableMortgage's attributes. This is accomplished by placing the attributes of the
        # VariableMortgage into a tuple of tuples with the attribute name and attribute's corresponding value, and
        # casting this tuple of tuples to a string.
        return 'Variable Mortgage: {face}, {rate_dict}, {term}, {asset}'.format(face=('Face', self._face),
                                                                                rate_dict=('Rate', self._rate_dict),
                                                                                term=('Term', self._term),
                                                                                asset=('House', self._asset))

    # Function to generate and return the string value of the VariableMortgage object
    def __repr__(self):
        # Returns string of the VariableMortgage's attributes. This is accomplished by placing the attributes of the
        # VariableMortgage into a tuple of tuples with the attribute name and attribute's corresponding value, and
        # casting this tuple of tuples to a string.
        return 'Variable Mortgage: {face}, {rate_dict}, {term}, {asset}'.format(face=('Face', self._face),
                                                                                rate_dict=('Rate', self._rate_dict),
                                                                                term=('Term', self._term),
                                                                                asset=('House', self._asset))
