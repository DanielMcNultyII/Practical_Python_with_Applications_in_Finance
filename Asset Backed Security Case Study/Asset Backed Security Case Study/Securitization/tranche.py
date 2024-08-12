'''
Daniel McNulty II

This file contains the Tranche base class and StandardTranche derived class
'''

# Import the logging module
import logging
# Import the numpy package
import numpy
# Import the numpy financial package
import numpy_financial
# Import the logging package
import logging


class Tranche(object):
    # Dict containing the ABS rating table {DIRR{BPS): 'Rating'}
    abs_dirr_ratings = {0.06: 'AAA', 0.67: 'AA1', 1.3: 'AA2', 2.7: 'AA3', 5.2: 'A1', 8.9: 'A2', 13.0: 'A3',
                        19.0: 'BAA1', 27.0: 'BAA2', 46.0: 'BAA3', 72.0: 'BA1', 106.0: 'BA2', 143.0: 'BA3', 183.0: 'B1',
                        231.0: 'B2', 311.0: 'B3', 2500.0: 'CAA', 10000.0: 'CA'}

    # Standard initialization function
    # Initialize with notional, rate, and subordinate_flag.
    def __init__(self, notional, notional_per, rate, sub_flag):
        self._notional = float(notional)
        self._notional_per = float(notional_per)
        self._rate = float(rate)
        self._sub_flag = sub_flag

    # Getter property for the tranche subordination flag
    @property
    def sub_flag(self):
        logging.debug('sub_flag(self) return: {sf}'.format(sf=self._sub_flag))
        return self._sub_flag

    # irr function to find the annual internal rate of return
    def irr(self, period_payments):
        cf = period_payments
        cf[0] = -self._notional

        # Delegate to the numpy package irr function, passing in a list with the initial investment's notional as a
        # negative number and the total payments for each time period (in order). Multiplies the result by 12 in order
        # to make it annual.
        return numpy_financial.irr(cf) * 12.0

    # dirr function to find the reduction in yield
    def dirr(self, period_payments):
        # Find the absolute value of subtracting tranche's IRR from the tranche's rate
        return (self._rate*12) - self.irr(period_payments)

    # avg_life function to find the average life of the security
    def avg_life(self, prin_payments, b):
        if b[-1] == 0:
            try:
                return sum(i*prin_payments[i] for i in range(len(prin_payments))) / self._notional
            except:
                return numpy.inf
        else:
            return numpy.inf

    # abs_rater function that translates an input DIRR value to a letter rating using the abs_dirr_ratings dict above.
    @staticmethod
    def abs_rater(dirr):
        # Check if the input DIRR is an int or a float.
        if isinstance(dirr, (int, float)):
            # Cast the input DIRR to a float and multiply it by 10000.0 in order to convert it to its value in BPS
            # points, which are the units used in the abs_dirr_rating dict.
            bps_dirr = float(dirr) * 10000.0
            # Sort the list of DIRR keys within the abs_dirr_ratings dict and store the result in abs_dirrs
            abs_dirrs = sorted(list(Tranche.abs_dirr_ratings))

            # If the input DIRR is greater than the largest dirr value in abs_dirrs, then return the rating associated
            # with the largest DIRR value in the abs_dirrs_ratings dict.
            if bps_dirr > abs_dirrs[-1]:
                return Tranche.abs_dirr_ratings[abs_dirrs[-1]]

            # If the input DIRR is less than or equal to the lowest DIRR value in abs_dirrs, then return the rating
            # associated with the lowest DIRR value in the abs_dirrs_ratings dict.
            elif bps_dirr <= abs_dirrs[0]:
                return Tranche.abs_dirr_ratings[abs_dirrs[0]]

            # Otherwise, use a for loop to iterate through all the indices of abs_dirr, n. Then, check if the input DIRR
            # value is greater than the DIRR value in abs_dirrs[n] and less than or equal to the DIRR value in
            # abs_dirrs[n]. Once the input DIRR value meets this criteria, return the rating associated with the DIRR
            # value abs_dirrs[n+1] in abs_dirrs_rating.
            else:
                for n in range(0, len(abs_dirrs)):
                    if abs_dirrs[n] < bps_dirr <= abs_dirrs[n + 1]:
                        return Tranche.abs_dirr_ratings[abs_dirrs[n + 1]]
                    else:
                        continue

        # If the input DIRR value is not a float or an int, raise a TypeError with a message telling users that the
        # input into abs_rater() must be a float or an int.
        else:
            logging.error('The input dirr for abs_rater(dirr) must be a float or an int. Your input for dirr = {input} '
                          'is of type {type}, not float or int.'.format(input=dirr, type=type(dirr)))
            raise TypeError('The input dirr for abs_rater(dirr) must be a float or an int. Your input for dirr = '
                            '{input} is of type {type}, not float or int.'.format(input=dirr, type=type(dirr)))


class StandardTranche(Tranche):
    # Standard Initialization Function
    def __init__(self, notional, notional_per, rate, sub_flag):
        # Use super to call the base class __init__ function with notional, notional_per, rate, and sub_flag
        super(StandardTranche, self).__init__(notional, notional_per, rate, sub_flag)
        # Set the current time period to 0
        self._current_period = 0
        # Set the current notional balance to the Tranche's notional value
        self._current_not_bal = self._notional
        # Set the current interest due to 0.0
        self._current_int_due = 0.0
        # Set the current interest shortfall to 0.0
        self._current_int_short = 0.0
        # Set the current interest paid to 0.0
        self._current_int_paid = 0.0
        # Set the current principal paid to 0.0
        self._current_prin_paid = 0.0

    # increase_time_period function, which increases the current time period of the object by 1 and sets the current
    # principal paid, current interest paid, and current interest shortfall to 0.0.
    def increase_time_period(self):
        # Increment the current time period by 1
        self._current_period += 1
        # Set the current interest due on the tranche to the current interest shortfall plus the current interest due on
        # the tranche, as calculated by the tranche's current notional balance times the tranche's interest rate.
        self._current_int_due = self._current_int_short + (self._rate * self._current_not_bal)
        # Set the current principal paid in the new time period to 0.0. This is changed when make_principal_payment is
        # called. That function is defined below.
        self._current_prin_paid = 0.0
        # Set the current interest paid in the new time period to 0.0. This is changed when make_interest_payment is
        # called. That function is defined below.
        self._current_int_paid = 0.0
        # Set the current interest shortfall in the new time period to 0.0. This is changed when make_interest_payment
        # is called. That function is defined below.
        self._current_int_short = 0.0

    # make_principal_payment function, which records a principal payment and the notional balance for the current object
    # time period. Raises an error if called more than once for the current time period and/or if the current notional
    # balance is 0.0.
    def make_principal_payment(self, amt):
        # If the current_prin_paid variable of the tranche is greater than 0.0, then the make_principal_payment function
        # has been called for the current object time period, and so an error is raised with a message stating that the
        # principal for the current time period has already been paid.
        if self._current_prin_paid > 0.0:
            logging.info('Principal for time period {t} has already been paid.'.format(t=self._current_period))
        # If the current_not_bal variable of the trance is equal to 0.0, the current notional balance of the tranche is
        # 0.0, and so an error is raised with a message stating tht the tranche's current notional balance is 0.
        elif self._current_not_bal == 0.0:
            logging.info('Current tranche notional balance is 0. Payment not accepted.')
        # Otherwise, if the make_principal_payment has not been called for the current time period and the current
        # notional balance of the tranche is not 0.0, set the current principal paid variable, current_prin_paid, to the
        # lower of the amt input and the current notional balance (current_not_bal). Then subtract the newly calculated
        # current principal paid from the current notional balance and store the result in the StandardTranche object
        # level variable current_not_bal.Use max(float(amt),0) to avoid negative principal paid
        else:
            self._current_prin_paid = min(self._current_not_bal, max(float(amt),0))
            self._current_not_bal -= self._current_prin_paid
        # Return the difference between amount input into make_principal_payment, amt, and the newly calculated current
        # principal paid, current_prin_paid. Use max() to avoid returning a negative.
        return max(float(amt) - self._current_prin_paid, 0)

    # make_interest_payment function, which records an interest payment and the interest shortfall for the current
    # object time period. Raises an error if called more than once for the current time period and/or if the current
    # interest due is 0.0.
    def make_interest_payment(self, amt):
        # If the current_int_paid variable of the tranche is greater than 0.0, then the make_interest_payment function
        # has been called for the current object time period, and so an error is raised with a message stating that the
        # interest for the current time period has already been paid.
        if self._current_int_paid > 0.0:
            logging.info('Interest for time period {t} has already been paid.'.format(t=self._current_period))
        # If the current_int_due variable of the trance is equal to 0.0, the current interest due of the tranche is
        # 0.0, and so an error is raised with a message stating tht the tranche's current interest due is 0.
        elif self._current_int_due == 0.0:
            logging.info('Current tranche interest due is 0. Payment not accepted.')
        # Otherwise, if the make_interest_payment function has not been called for the current time period and the
        # current interest due on the tranche is not equal to 0.0, then set the current interest paid on the tranche,
        # current_int_paid, to the lower of the amt input into the function and the current interest due on the tranche
        # (current_int_due). Then, set the current interest shortfall (current_int_short_ equal to the difference
        # between the current interest due and the newly calculated current interest paid on the tranche. Use
        # max(float(amt),0) to avoid negative interest paid
        else:
            self._current_int_paid = min(self._current_int_due, max(float(amt),0))
            self._current_int_short = self._current_int_due - self._current_int_paid
        # Return the difference between the amount input into the function, amt, and the newly calculated current
        # interest paid, current_int_paid, on the tranche. Use max() to avoid returning a negative.
        return max(float(amt) - self._current_int_paid, 0)

    # notional_balance function that returns the amount of the notional still owed to the tranche for the current time
    # period (after any payments made). This simply returns the current value of the object level variable
    # current_not_bal. Calculations to determine the current_not_bal value occur within the make_principal_payment
    # function.
    @property
    def notional_balance(self):
        return self._current_not_bal

    # interest_due function that returns the amount of interest due for the current time period. This simply returns the
    # current_int_due object level variable value. The calculations involved in determining the current interest due
    # occur in increase time period.
    @property
    def interest_due(self):
        return self._current_int_due

    # interest_paid function that returns the amount of interest paid for the current time period. This simply returns
    # the current_int_paid object level value. The calculations involved in determining the current interest paid occur
    # in make_interest_payment.
    @property
    def interest_paid(self):
        return self._current_int_paid

    # principal_paid function that returns the amount of principal paid for the current time period. This simply returns
    # the current_prin_paid object level value. The calculations involved in determining the current principal paid
    # occur in make_principal_payment.
    @property
    def principal_paid(self):
        return self._current_prin_paid

    # interest_shortfall function that returns the interest shortfall for the current time period. This simply returns
    # the current_int_short object level value. The calculations involved in determining the current interest shortfall
    # occur in make_interest_payment.
    @property
    def interest_shortfall(self):
        return self._current_int_short

    # reset function that returns tranche to its original state (Time 0). This basically takes the variables of the
    # tranche and sets them to the values they were upon calling __init__, which are all 0 with the exception of
    # current_not_bal, which is set to the notional value of the tranche.
    def reset(self):
        # Set the current time period to 0.
        self._current_period = 0
        # Set the current notional balance to the Tranche's notional value
        self._current_not_bal = self._notional
        # Set the current interest due to 0.0
        self._current_int_due = 0.0
        # Set the current interest shortfall to 0.0
        self._current_int_short = 0.0
        # Set the current interest paid to 0.0
        self._current_int_paid = 0.0
        # Set the current principal paid to 0.0
        self._current_prin_paid = 0.0
