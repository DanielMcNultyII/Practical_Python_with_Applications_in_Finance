'''
Daniel McNulty II

This file contains the LoanPool class
'''


# Import reduce from functools
from functools import reduce
# Import the Loan class from the loan_base module
from Loan.loan_base import Loan
# Import the logging module
import logging
# Import the csv_loan_functions module
import Loan.csv_loan_functions as csv_loan_functions
# Import the numpy package
import numpy


# Declare the LoanPool class
class LoanPool(object):
    # Dict holding the probability of default for a loan for given time periods
    _period_default_prob = {0:0, 1: 0.0005, 11: 0.001, 60: 0.002, 120: 0.004, 180: 0.002, 210: 0.001}

    # Standard initialization function
    def __init__(self, loan_list):
        # Check if the input loan_list is of type list
        if isinstance(loan_list, list):
            # If the input loan_list is of type list, check that all the elements within it are Loan class objects or
            # objects from its derived classes.
            if all(isinstance(loan, Loan) for loan in loan_list):
                # Declare a variable loans and then set it equal to to the input list of loans.
                self._loans = loan_list
            # If the input loan_list is a list, but not all of the elements in the list are Loan objects or objects of
            # classes derived from Loan, then log an error and raise a TypeError with an error message stating that the
            # input for a LoanPool's loans variable must be a list of only Loan elements.
            else:
                logging.error('Input for the LoanPool variable loans must be a list of Loans or objects derived from '
                              'the Loan class. Your input list {in_list} does not have only '
                              'Loans.'.format(in_list=loan_list))
                raise TypeError('Input for the LoanPool variable loans must be a list of Loans or objects derived from '
                                'the Loan class. Your input list {in_list} does not have only '
                                'Loans.'.format(in_list=loan_list))
        # If input loan_list is not a list, log an error and raise a TypeError with an error message stating that the
        # input for a LoanPool's loans variable must be a list of only Loan elements.
        else:
            logging.error('Input for the LoanPool variable loans must be a list of Loans or objects derived from the'
                          'Loan class. Your input {input} is of type {type}, not a list.'.format(input=loan_list,
                                                                                                 type=type(loan_list)))
            raise TypeError('Input for the LoanPool variable loans must be a list of Loans or objects derived from the'
                            'Loan class. Your input {input} is of type {type}, not a '
                            'list.'.format(input=loan_list, type=type(loan_list)))

    # Function to generate and return the string value of the LoanPool object
    def __str__(self):
        # Returns a tuple containing the total principal, WAR, and WAM of the LoanPool object
        return 'Loan Pool: {tot_prin}, {WAR}, {WAM}'.format(tot_prin=('Total Principal', self.total_principal()),
                                                            WAR=('WAR', self.weighted_avg_rate()),
                                                            WAM=('WAM', self.weighted_avg_maturity()))

    # Function to generate and return the string value of the LoanPool object
    def __repr__(self):
        # Returns a tuple containing the total principal, WAR, and WAM of the LoanPool object
        return 'Loan Pool: {tot_prin}, {WAR}, {WAM}'.format(tot_prin=('Total Principal', self.total_principal()),
                                                            WAR=('WAR', self.weighted_avg_rate()),
                                                            WAM=('WAM', self.weighted_avg_maturity()))

    # Function to make LoanPool an iterable
    def __iter__(self):
        return iter(self._loans)

    # Getter property for the list loans of the LoanPool class object
    @property
    def loans(self):
        return self._loans

    # Setter property for the list loans of the LoanPool class object
    @loans.setter
    def loans(self, iloans):
        # Check if the input iloans is of type list. If it is, set the LoanPool object's loans variable to iloans.
        if isinstance(iloans, list):
            if all(isinstance(loan, Loan) for loan in iloans):
                self._loans = iloans
            # If the input iloans is a list, but not all of the elements in the list are Loan objects or objects of
            # classes derived from Loan, then log an error and raise a TypeError with an error message stating that the
            # input to the loans setter function must be a list of Loan objects or objects of classes derived from the
            # Loan class.
            else:
                logging.error('Input into the LoanPool loans setter function must be a list of Loans or objects '
                              'derived from the Loan class. Your input {input} does not contain '
                              'only loans.'.format(input=iloans))
                raise TypeError('Input into the LoanPool loans setter function must be a list of Loans or objects '
                                'derived from the Loan class. Your input {input} does not contain '
                                'only loans.'.format(input=iloans))
        # If the input iloans is not of type list, raise a TypeError with an error message stating the input to the
        # loans setter function must be a list of Loan objects or objects of classes derived from the Loan class.
        else:
            logging.error('Input into the LoanPool loans setter function must be a list of Loans or objects derived '
                          'from the Loan class. Your input {input} is of type {type}, not a list.'.format(input=iloans,
                                                                                                          type=type(iloans)))
            raise TypeError('Input into the LoanPool loans setter function must be a list of Loans or objects derived '
                            'from the Loan class. Your input {input} is of type {type}, not a list.'.format(input=iloans,
                                                                                                            type=type(iloans)))

    # Method to get the total loan principal
    def total_principal(self):
        # Uses a list comprehension to generate a list of all the face values from all the loans within the LoanPool's
        # loan list loans that have not been defaulted on. Then uses the sum() function to return the sum of this
        # generated list.
        return sum([loan._face for loan in self._loans if not loan.default])

    # Method to get the total loan balance for a given period
    def total_balance(self, t=0.0):
        # Check if the value of t is an int or float
        if isinstance(t, (int, float)):
            # Uses a list comprehension to generate a list of all the balances calculated using balance(t) from all the
            # loans within the LoanPool's loan list loans that have not been defaulted on. Then uses the sum() function
            # to return the sum of this generated list. t is cast to a float when input into explicit_balance() in order
            # to avoid complications (ie. truncation) from using floats and ints together in calculations within Python.
            return sum([loan.balance(float(t)) for loan in self._loans if not loan.default])
        # If t is not an int or a float, log an error and raise a Type Error with an error message stating the input
        # into total_balance(t) must be a float or an int.
        else:
            logging.error('Input into total_balance(t) must be a float or an int. Your input t = {input} is of type '
                          '{type}, not a float or an int.'.format(input=t, type=type(t)))
            raise TypeError('Input into total_balance(t) must be a float or an int. Your input t = {input} is of type '
                            '{type}, not a float or an int.'.format(input=t, type=type(t)))

    # Method to get the aggregate interest due of the loan pool in a given period (Month)
    def aggregate_principal_due(self, t=0.0):
        # Check if the value of t is an int or float
        if isinstance(t, (int, float)):
            # Uses a list comprehension to generate a list of all the principal_due() calculated from all the loans
            # within the LoanPool's loan list loans that have not been defaulted on. Then uses the sum() function to
            # return the sum of this generated list. t is cast to a float when input into principal_due() in order to
            # avoid complications (ie. truncation) from using floats and ints together in calculations within Python.
            return sum([loan.principal_due(float(t)) for loan in self._loans if not loan.default])
        # If t is not an int or a float, log an error and raise a Type Error with an error message stating the input
        # into aggregate_principal_due(t) must be a float or an int.
        else:
            logging.error('Input into aggregate_principal_due(t) must be a float or an int. Your input t = {input} is '
                          'of type {type}, not a float or an int.'.format(input=t, type=type(t)))
            raise TypeError('Input into aggregate_principal_due(t) must be a float or an int. Your input t = {input} is '
                            'of type {type}, not a float or an int.'.format(input=t, type=type(t)))

    # Method to get the aggregate interest due of the loan pool in a given period (Month)
    def aggregate_interest_due(self, t=0.0):
        # Check if the value of t is an int or float
        if isinstance(t, (int, float)):
            # Uses a list comprehension to generate a list of all the interest_due() calculated from all the loans
            # within the LoanPool's loan list loans that have not been defaulted on. Then uses the sum() function to
            # return the sum of this generated list. t is cast to a float when input into interest_due() in order to
            # avoid complications (ie. truncation) from using floats and ints together in calculations within Python.
            return sum([loan.interest_due(float(t)) for loan in self._loans if loan.balance(float(t)) > 0 and not loan.default])
        # If t is not an int or a float, log an error and raise a Type Error with an error message stating the input
        # into aggregate_interest_due(t) must be a float or an int.
        else:
            logging.error('Input into aggregate_interest_due(t) must be a float or an int. Your input t = {input} is '
                          'of type {type}, not a float or an int.'.format(input=t, type=type(t)))
            raise TypeError('Input into aggregate_interest_due(t) must be a float or an int. Your input t = {input} is '
                            'of type {type}, not a float or an int.'.format(input=t, type=type(t)))

    # Method to get the aggregate total payment due of the loan pool in a given period (Month)
    def aggregate_monthly_pmt(self, t=0.0):
        # Check if the value of t is an int or float
        if isinstance(t, (int, float)):
            # Uses a list comprehension to generate a list of all the monthly_payment() calculated from all the loans
            # within the LoanPool's loan list loans that have not been defaulted on. Then uses the sum() function to
            # return the sum of this generated list. t is cast to a float when input into monthly_payment() in order to
            # avoid complications (ie. truncation) from using floats and ints together in calculations within Python.
            return sum([loan.monthly_payment(float(t)) for loan in self._loans if not loan.default])
        # If t is not an int or a float, raise a Type Error with an error message stating the input into
        # aggregate_monthly_pmt(t) must be a float or an int.
        else:
            logging.error('Input into aggregate_monthly_pmt(t) must be a float or an int. Your input t = {input} is of '
                          'type {type}, not a float or an int.'.format(input=t, type=type(t)))
            raise TypeError('Input into aggregate_monthly_pmt(t) must be a float or an int. Your input t = {input} is '
                            'of type {type}, not a float or an int.'.format(input=t, type=type(t)))

    # Method that returns the number of 'active' loans (Loans with a balance greater than 0) at a given period.
    def active_loans(self, t=0.0):
        # Check if t = 0. If it does, the pool has just been initiated and we can assume all the loans within are active
        if t == 0:
            return len(self._loans)
        # Check if the value of t is an int or float
        elif isinstance(t, (int, float)):
            # Uses a list comprehension to generate a list of all the loans in the LoanPool class' list of loans loans
            # that have a balance, as calculated by explicit_balance(t), greater than 0 at the start of period t / the
            # end of period t-1 and that have not been defaulted on. Then uses the len() function on the generated list
            # on order to return the number of loans in it. t is cast to a float when input into explicit_balance() in
            # order to avoid complications (ie. truncation) from using floats and ints together in calculations within
            # Python.
            return len([loan for loan in self._loans if loan.balance(float(t-1)) > 0 and not loan.default])
        # If t is not an int or a float, log an error and raise a Type Error with an error message stating the input
        # into active_loans(t) must be a float or an int.
        else:
            logging.error('Input into active_loans(t) must be a float or an int. Your input t = {input} is of type '
                          '{type}, not a float or an int.'.format(input=t, type=type(t)))
            raise TypeError('Input into active_loans(t) must be a float or an int. Your input t = {input} is of type '
                            '{type}, not a float or an int.'.format(input=t, type=type(t)))

    # Method to calculate the Weighted Average Rate (WAR) of the loans in the LoanPool
    def weighted_avg_rate(self):
        # Create two iterators, one containing all the face values and the other containing all the rates from each loan
        # in the LoanPool. Then use izip() from the itertools module to create an iterator of tuples containing each
        # face value and its corresponding rate value. Assign this newly-made iterator to variable faces_and_rates.
        faces_and_rates = zip(iter(loan._face for loan in self._loans), iter(loan._rate for loan in self._loans))

        # Declare and implement function cum_face_rate_prod(total, face_rate_tuple)), which takes in input parameters of
        # variable total and a tuple of (face, rate). Then, it multiplies face by rate, adds the product to total, and
        # returns the sum. face and rate are cast to floats in order to avoid any complications (ie. Truncation) from
        # using ints and floats together in mathematical operations.
        def cum_face_rate_prod(total, face_rate_tuple):
            face = face_rate_tuple[0]
            rate = face_rate_tuple[1]
            return total + (float(face) * float(rate))

        # Utilize the reduce() function to apply cum_face_rate_prod(total, (face, rate)) to each value in
        # faces_and_rates, calling cum_face_rate_prod(total, (face, rate)) incrementally after setting total to 0
        # initially. This yields the sum of the products of the face and corresponding rate values from faces_and_terms,
        # which is then divided by the sum of an iterator that contains face values from each loan in the LoanPool.
        return reduce(cum_face_rate_prod, faces_and_rates, 0) / sum(iter(loan._face for loan in self._loans))

    # Method to calculate the Weighted Average Maturity (WAM) of the loans in the LoanPool
    def weighted_avg_maturity(self):
        faces_and_terms = zip(iter(loan._face for loan in self._loans), iter(loan._term for loan in self._loans))

        # Declare and implement function cum_face_term_prod(total, face_term_tuple), which takes in input parameters of
        # variable total and a tuple of (face, term). Then, it multiplies face by term, adds the product to total, and
        # returns the sum. face and term are cast to floats in order to avoid any complications (ie. Truncation) from
        # using ints and floats together in mathematical operations.
        def cum_face_term_prod(total, face_term_tuple):
            face = face_term_tuple[0]
            term = face_term_tuple[1]
            return total + (float(face) * float(term))

        # Utilize the reduce() function to apply cum_face_rate_prod(total, (face, rate)) to each value in
        # faces_and_terms, calling cum_face_rate_prod(total, (face, rate)) incrementally after setting total to 0
        # initially. This yields the sum of the products of the face and corresponding rate values from faces_and_terms,
        # which is then divided by the sum of an iterator that contains face values from each loan in the LoanPool.
        return reduce(cum_face_term_prod, faces_and_terms, 0) / sum(iter(loan._face for loan in self._loans))

    # get_waterfall function for the LoanPool class, which stores the monthly_payment, principal_due, interest_due,
    # recovery value from defaulted loans, and balance of each loan in the LoanPool at given time t in a list of lists
    # and returns said list. Takes default notification and period as input.
    def get_waterfall(self, t=0):
        waterfall_list = []
        for num, loan in enumerate(self._loans):
            waterfall_list.append([loan.monthly_payment(t), loan.principal_due(t), loan.interest_due(t),
                                   loan._rec_val, loan.balance(t)])
        return waterfall_list

    # csv_loader function to convert the data in a given csv file into a list of loan objects and add it to the LoanPool
    # object's loans list.
    def csv_loader(self, loan_file):
        self._loans.extend(csv_loan_functions.csv_to_loans(loan_file))

    # static method current_def_prob() function to determine the current default rate for a given period t.
    @staticmethod
    def current_def_prob(t):
        # Get a list of the keyword startPeriods and store it in variable start_periods
        start_periods = sorted(list(LoanPool._period_default_prob))

        # Check if the input period is an int or float.
        if isinstance(t, int):
            # Initially check if the input period is negative. If it is, log an error and raise a ValueError with an
            # error message that states the input period for rate(t) must be a positive int.
            if t < 0.0:
                logging.error('The input period for rate(t) must be a positive int. Your input t = {input} is below'
                              '0'.format(input=t, type=type(t)))
                raise ValueError('The input period for rate(t) must be a positive int. Your input t = {input} is below'
                                 '0'.format(input=t, type=type(t)))
            # Otherwise, check if the input period is greater than or equal to the last startPeriod in start_periods.
            # If it is, then return the value associated with that startPeriod in the period_default_prob dict.
            elif t >= start_periods[-1]:
                return LoanPool._period_default_prob[start_periods[-1]]
            # If the above criteria has not been reached, initialize a for loop that goes through the range of indices
            # of the above-created start_times.
            else:
                for n in range(0, len(start_periods)):
                    # Otherwise, check if the input period is between the startPeriods in start_periods that are
                    # referred to by start_periods[n] and start_periods[n + 1]. If it is, then return the value within
                    # the LoanPool period_default_prob dict that corresponds to startPeriod start_periods[n].
                    if start_periods[n] <= t < start_periods[n + 1]:
                        return LoanPool._period_default_prob[start_periods[n]]
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

    # check_defaults() generates a list of uniform random integers, one for each loan, and then calls check_default on
    # each loan, passing in the random number as the check_default's default_notification input parameter.
    def check_defaults(self, t):
        # Set to constant seed for testing and debugging
        # numpy.random.seed(1)

        # Initialize a variable recovery_value and set it to 0. This will store the total recovery value of all the
        # underlying assets of the defaulted loans.
        recovery_value = 0.0

        if t == 0:
            return recovery_value

        # Find the current probability of default by using the above declared and implemented static method
        # current_def_prob(t). Store the result in variable current_default rate.
        current_default_rate = LoanPool.current_def_prob(t)

        # Use numpy.random.uniform to generate a numpy array of the same length as the length of the LoanPool's loans
        # list filled with "random" numbers generated from a uniform distribution. In order to ensure the odds of a
        # given number occurring is the same as the default probability for the time period, the range of the uniform
        # distribution is from 0 to the inverse of the default probability for the time period, half inclusive (Includes
        # 0, but not 1/current_default_rate)
        default_notifications = list(numpy.random.randint(0, int(1/current_default_rate), len(self._loans)))

        # Create a generator of tuples, each containing a loan from the LoanPool's loans list and a corresponding
        # default_notifications value. Then iterate through the generator, unpacking each loan in the generator's tuples
        # into variable loan and each default notification int in the generator's tuple into variable default_
        # notification.
        for loan, default_notification in zip(self._loans, default_notifications):
            # If the loan referred to by variable loan has been defaulted on already, continue onto the next iteration
            # of the for loop without doing anything else.
            #if loan.default:
            #    loan.rec_val = 0.0

            # Otherwise, call check_default on the loan referred to by variable loan and add the return onto the value
            # stored in recovery_value. If the loan has defaulted in this period, check_default will return the loan's
            # underlying asset's recovery value at period t. If the loan has not been defaulted on, check_default will
            # return 0.0.
            recovery_value += loan.check_default(default_notification, t)

        # Return the recovery_value of all the underlying assets of loans that have been defaulted on in period t
        return recovery_value

    # reset function to restore loan objects within the LoanPool to their original state
    def reset(self):
        # Use a for loop to iterate through all the loans in the loans list of the LoanPool
        for loan in self._loans:
            # Call reset() on the loan in loans that variable loan corresponds to
            loan.reset()
