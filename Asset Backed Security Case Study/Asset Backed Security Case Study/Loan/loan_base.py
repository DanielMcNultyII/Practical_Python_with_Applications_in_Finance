'''
Daniel McNulty II

This file contains the Loan base class
'''


# Import the logging module
import logging
# Import the Asset class from the asset_base module within the Assets package
from Loan.Assets.asset_base import Asset
from Loan.Assets.car import Car
# Import memoize from the memoization module
from Utilities.memoization import memoize


# Declare the Loan base class
class Loan(object):
    # Initialize and assign class-level variables for the loan class objects' face, rate, and term to be used if users
    # input incorrect types (float/int) into the Loan object initialization function.
    _dface = 1.0
    _drate = 1.0
    _dterm = 1.0

    # Standard initialization function
    def __init__(self, loan_num=1, face=1, annual_rate=1, term=1, asset=Car(200000), rec_rate=1):
        # First check if the input asset is of the type Assets. Checking for the base type Assets will allow for all types
        # derived from Assets (HouseBase, Car, Civic, etc.) to pass this check. If this conditional is satisfied, then
        # initialize and set the object level protected variable asset to the user input Assets object asset. Then
        # initialize and set the face, rate, term, default, and loan_id protected object level variables of the Loan
        # object.
        if isinstance(asset, Asset):
            self._asset = asset
            # Initialize and set the object level protected variables for face, and to the user input face, rate, and
            # term values. Cast numeric input parameter to a float in order to avoid any complications (ie. truncation)
            # that could occur when doing arithmetic with floats and ints in Python with later Loan class functions/
            # methods. If user input for any of the numeric values is not a float or an int, set that value to the
            # default value for that attribute as defined by the default value variables above. Assumes that the rate
            # input by the user is the annual rate and uses the static-level method monthly_rate() to convert the input
            # to its corresponding monthly rate and store it within the object variable rate.
            self._face = float(face) if isinstance(face, (float, int)) else float(Loan._dface)
            self._rate = Loan.monthly_rate(annual_rate) if isinstance(annual_rate, (float, int)) else float(Loan._drate)
            self._term = float(term) if isinstance(face, (float, int)) else float(Loan._dterm)

            # Initialize an object-level protected variable called default, which is False if the loan has not been
            # defaulted on and True if it has been defaulted on. At initialization, set to False since a loan cannot be
            # defaulted on right at the outset.
            self._default = False

            # If a loan_num was input, then set the Loan object level variable loan_num to the input loan_num.
            # Otherwise, set the Loan's loan_num variable to 0. This is intended to act as an identifier for each
            # individual loan used.
            self._loan_num = loan_num if loan_num is not None else 0
            self._rec_rate = rec_rate
            self._rec_val = 0.0

        # Else if the input for asset is not of the Assets class, log an error and then raise a TypeError with an error
        # message stating that the input for the Loan's asset variable must be of the Assets class or any of its
        # derived classes.
        else:
            logging.error('Input for the Loan asset variable must be of the Assets class or any of its derived classes.'
                          'Your input {asset} is not of the Assets class or one of its derived '
                          'classes'.format(asset=asset))
            raise TypeError('Input for the Loan asset variable must be of the Assets class or any of its derived '
                            'classes. Your input {asset} is not of the Assets class or one of its derived '
                            'classes'.format(asset=asset))

    # Function to generate and return the string value of the Loan object
    def __str__(self):
        # Returns string of the Loan's attributes. This is accomplished by placing the attributes of the Loan into a
        # tuple of tuples with the attribute name and attribute's corresponding value, and casting this tuple of tuples
        # to a string.
        return 'Loan | Face: {face} | Rate: {rate} | Term: {term} | ' \
               'Assets: {asset}'.format(face=self._face,
                                       rate=Loan.annual_rate(self._rate),
                                       term=self._term,
                                       asset=self._asset)

    # Function to generate and return the string value of the Loan object
    def __repr__(self):
        # Returns string of the Loan's attributes. This is accomplished by placing the attributes of the Loan into a
        # tuple of tuples with the attribute name and attribute's corresponding value, and casting this tuple of tuples
        # to a string.
        return 'Loan | Face: {face} | Rate: {rate} | Term: {term} | ' \
               'Assets: {asset}'.format(face=self._face,
                                       rate=Loan.annual_rate(self._rate),
                                       term=self._term,
                                       asset=self._asset)

    # @classmethod default_loan_values(cls, iface, irate, iterm) function
    #   Set the default face, rate, and term values at the class level to be used if the face, rate, or term input into
    #   the initialization function are not of the form float or int. If the iface, irate, and/or iterm values input
    #   into this function are not of float or int type, then keep the value or values for which the new inputs are not
    #   float or ints unchanged. Cast all default values to float in order to avoid any truncation or complications that
    #   can arise from performing mathematics with both floats and ints.
    @classmethod
    def default_loan_values(cls, iface, irate, iterm):
        cls._dface = float(iface) if isinstance(iface, (float, int)) else float(Loan._dface)
        cls._drate = float(irate) if isinstance(irate, (float, int)) else float(Loan._drate)
        cls._dterm = float(iterm) if isinstance(iterm, (float, int)) else float(Loan._dterm)

    # Getter property for the face value of the Loan class object
    @property
    def face(self):
        logging.debug('face(self) return: {face}'.format(face=self._face))
        return self._face

    # Setter property for the face value of the Loan class object
    @face.setter
    def face(self, iface):
        # Check if the input value iface is a float or an int. If it is, then set the Loan object's face value to iface
        logging.debug('Checking if face setter input is an int or float')
        if isinstance(iface, (int, float)):
            logging.debug('Loan face set to face setter input {face}'.format(face=iface))
            self._face = iface
        # If input iface is not of type int or float, log an error and then raise a TypeError with an error message
        # stating that the input for the face setter must be of type float or int.
        else:
            logging.error('The face value (face) setter input must be a float or an int. Your input of {input} is of '
                          'type {type}, not a float or an int.'.format(input=iface, type=type(iface)))
            raise TypeError('The face value (face) setter input must be a float or an int. Your input of {input} is of '
                            'type {type}, not a float or an int.'.format(input=iface, type=type(iface)))

    # Getter for the rate of the Loan class object. The getter function returns the monthly rate of the loan object by
    # returning the value in the protected rate variable for the Loan class.
    def rate(self, t):
        # Check if input period t is greater than the maturity of the loan. if it is, then use an info-level log to
        # display that t is greater than the term of the loan.
        if t > self.term:
            logging.info('t {period} is greater than the loan maturity {term}'.format(period=t, term=self.term))

        return_rate = self._rate
        logging.debug('rate getter return: {rate}'.format(rate=return_rate))
        return return_rate

    # Setter function for the rate of the Loan class object. Takes in an annual rate and stores it within the class
    # variable rate as the corresponding monthly rate using the monthly_rate() static-level method.
    def set_rate(self, irate, t):
        # Check if input period t is greater than the maturity of the loan. if it is, then use an info-level log to
        # display that t is greater than the term of the loan.
        if t > self.term:
            logging.info('t {period} is greater than the loan maturity {term}'.format(period=t, term=self.term))

        # Check if the input value irate is a float or an int. If it is, then set th Loan object's rate value to irate
        if isinstance(irate, (int, float)):
            logging.debug('Loan rate set to set_rate(irate) input {rate}'.format(rate=irate))
            self._rate = Loan.monthly_rate(irate)
        # If input irate is not of type int or float, log an error and then raise a TypeError with an error message
        # stating that the input for the rate setter must be of type float or int.
        else:
            logging.error('The rate value (rate) setter input must be a float or an int. Your input of {input} is of'
                          'type {type}, not a float or an int'.format(input=irate, type=type(irate)))
            raise TypeError('The rate value (rate) setter input must be a float or an int. Your input of {input} is of'
                            'type {type}, not a float or an int'.format(input=irate, type=type(irate)))

    # static-level method to return the monthly interest rate for a passed-in annual rate by dividing the annual rate by
    # 12.
    @staticmethod
    def monthly_rate(annual_rate):
        # Check if the input argument annual_rate is an int or a float. If it is, calculate and return the monthly rate
        # from the input annual rate by dividing the annual rate by 12. The annual_rate is cast to a float before
        # performing calculations in order to avoid truncation or other complications from the use of floats and ints
        # together in mathematics in Python.
        logging.debug('Checking if monthly_rate(annual_rate) input is an int or float')
        if isinstance(annual_rate, (int, float)):
            monthly_rate = float(annual_rate)/12.0
            logging.debug('monthly_rate({input_rate}) return: {return_rate}'.format(input_rate=annual_rate,
                                                                                    return_rate=monthly_rate))
            return monthly_rate
        # Else, if the input argument annual_rate is not an int or a float, log an error and raise a ValueError with an
        # error message that states the input into monthly_rate() must be an int or a float.
        else:
            logging.error('Input into monthly_rate(annual_rate) must be an int or a float. Your input annual_rate '
                          '{input} is of type {type}, not a float or an int'.format(input=annual_rate,
                                                                                    type=type(annual_rate)))
            raise ValueError('Input into monthly_rate(annual_rate) must be an int or a float. Your input annual_rate '
                             '{input} is of type {type}, not a float or an int'.format(input=annual_rate,
                                                                                       type=type(annual_rate)))

    # static-level method to return the annual interest rate for a passed-in monthly rate.
    @staticmethod
    def annual_rate(monthly_rate):
        # Check if the input argument monthly_rate is an int or a float. If it is, calculate and return the annual rate
        # from the input monthly rate by multiplying the monthly rate by 12. The monthly_rate is cast to a float before
        # performing calculations in order to avoid truncation or other complications from the use of floats and ints
        # together in mathematics in Python.
        logging.debug('Checking if annual_rate(monthly_rate) input is an int or float')
        if isinstance(monthly_rate, (int, float)):
            annual_rate = float(monthly_rate)*12.0
            logging.debug('annual_rate({input_rate}) return: {return_rate}'.format(input_rate=monthly_rate,
                                                                                   return_rate=annual_rate))
            return annual_rate
        # Else, if the input argument monthly_rate is not an int or a float, log an error and raise a ValueError with an
        # error message that states the input into annual_rate() must be an int or a float.
        else:
            logging.error('Input into annual_rate(monthly_rate) must be an int or a float. Your input monthly_rate '
                          '{input} is of type {type}, not a float or an int'.format(input=monthly_rate,
                                                                                    type=type(monthly_rate)))
            raise ValueError('Input into annual_rate(monthly_rate) must be an int or a float. Your input monthly_rate '
                             '{input} is of type {type}, not a float or an int'.format(input=monthly_rate,
                                                                                       type=type(monthly_rate)))

    # Getter property for the term of the Loan class object
    @property
    def term(self):
        term_return = self._term
        logging.debug('term getter return: {term}'.format(term=term_return))
        return term_return

    # Setter property for the term of the Loan class object
    @term.setter
    def term(self, iterm):
        # Check if iterm is an int or a float. If iterm is an int or a float, set the Loan object's term value to iterm
        logging.debug('Checking if term setter input is an int or float')
        if isinstance(iterm, (int, float)):
            logging.debug('Loan term set to term setter input {term}'.format(term=iterm))
            self._term = iterm
        # If input iterm is not of type int or float, log an error and then raise a TypeError with an error message
        # stating that the input for the term setter must be of type float or int.
        else:
            logging.error('The term value (term) setter input must be a float or an int. Your input {input} is of '
                          'type {type}, not a float or an int'.format(input=iterm, type=type(iterm)))
            raise TypeError('The term value (term) setter input must be a float or an int. Your input {input} is of '
                            'type {type}, not a float or an int'.format(input=iterm, type=type(iterm)))

    # Getter property for the term of the Loan class object
    @property
    def asset(self):
        logging.debug('asset(self) return: {asset}'.format(asset=self._asset))
        return self._asset

    # Setter property for the term of the Loan class object
    @asset.setter
    def asset(self, iasset):
        # Check if the input for the asset setter property is of the Assets class. If it is, then set the Loan object's
        # asset variable to the input iasset.
        logging.debug('Checking if asset setter input is a Assets')
        if isinstance(iasset, Asset):
            logging.debug('Loan asset set to asset setter input {asset}'.format(asset=iasset))
            self._asset = iasset
        # If the input iasset is not an instance of the Assets class or one of its derived classes, log an error and then
        # raise a TypeError with an error message telling users that the input for the asset variable must be an Assets
        # object.
        else:
            logging.error('Input for the Loan base class asset variable must be an Assets object (ie. HouseBase, Car, '
                          'etc.). Your input {input) is of type {type}, not an Assets object'.format(input=iasset,
                                                                                                    type=type(iasset)))
            raise TypeError('Input for the Loan base class asset variable must be an Assets object (ie. HouseBase, Car, '
                            'etc.). Your input {input) is of type {type}, not an Assets object'.format(input=iasset,
                                                                                                      type=type(iasset)))

    # Getter property for the recovery rate of the Loan class object
    @property
    def rec_rate(self):
        rec_rate_return = self._rec_rate
        logging.debug('rec rate getter return: {rr}'.format(rr=rec_rate_return))
        return rec_rate_return

    # Setter property for the recovery rate of the Loan class object
    @rec_rate.setter
    def rec_rate(self, irec):
        # Check if irec is an int or a float. If irec is an int or a float, set the Loan object's recovery rate value to
        # irec
        logging.debug('Checking if rec rate setter input is an int or float')
        if isinstance(irec, (int, float)):
            logging.debug('Loan rec rate set to rec rate setter input {rr}'.format(rr=irec))
            self._rec_rate = irec
        # If input irec is not of type int or float, log an error and then raise a TypeError with an error message
        # stating that the input for the rec rate setter must be of type float or int.
        else:
            logging.error('The rec rate value (irec) setter input must be a float or an int. Your input {input} is of '
                          'type {type}, not a float or an int'.format(input=irec, type=type(irec)))
            raise TypeError('The rec rate value (irec) setter input must be a float or an int. Your input {input} is of '
                            'type {type}, not a float or an int'.format(input=irec, type=type(irec)))

    # Getter property for the loan_num of the Loan class object
    @property
    def loan_num(self):
        logging.debug('loan_num(self) return: {loan_num}'.format(loan_num=self._loan_num))
        return self._loan_num

    # Setter property for the loan_num of the Loan class object
    @loan_num.setter
    def loan_num(self, i_loan_num):
        # Check if the input for the loan_num setter property is an int. If it is, then set the Loan object's loan_num
        # variable to the input i_loan_num.
        logging.debug('Checking if loan_num setter input is an int')
        if isinstance(i_loan_num, int):
            logging.debug('Loan loan_num set to loan_num setter input {loan_num}'.format(loan_num=self._loan_num))
            self._loan_num = i_loan_num
        # If the input i_loan_num is not an int, log an error and then raise a TypeError with an error message telling
        # users that the input for the loan_num variable must be an int.
        else:
            logging.error('Input for the Loan base class loan_num variable must be an int. Your input {input) is of '
                          'type {type}, not an int'.format(input=i_loan_num, type=type(i_loan_num)))
            raise TypeError('Input for the Loan base class loan_num variable must be an int. Your input {input) is of '
                            'type {type}, not an int'.format(input=i_loan_num, type=type(i_loan_num)))

    # Getter property for the loan_num of the Loan class object
    @property
    def default(self):
        logging.debug('default(self) return: {default}'.format(default=self._default))
        return self._default

    # class-level method to calculate the monthly payment of a passed in Loan class object. Getter functions are used to
    # access the input loan class object's face, rate, and term variables since they are protected variables.
    @classmethod
    def calc_monthly_pmt(cls, iface, irate, iterm, t=0.0):
        # Check if input period t is greater than the maturity of the loan. if it is, then use an info-level log to
        # display that t is greater than the term of the loan.
        if t > iterm:
            logging.info('t {period} is greater than the loan maturity {term}'.format(period=t, term=iterm))
            logging.debug('Checking if input iface, irate, iterm, and t into calc_monthly_pmt are all ints and/or floats')
        # If the input t is 0, return 0 monthly payment since there's no payment at issuance.
        if t == 0.0:
            return 0.0
        # Check if the input iface, irate, iterm, and t variables are ints or floats
        if isinstance(iface, (int, float)) and isinstance(irate, (int, float)) and isinstance(iterm, (int, float)) \
           and isinstance(t, (int, float)):
            # Check if the term and rate of the Loan object is not 0. If they are not, calculate and return the monthly
            # loan payment using the standard formula provided in lecture 2-03 Loans.
            logging.debug('Checking if input iterm and irate into calc_monthly_pmt are not 0')
            if iterm != 0.0 and irate != 0.0:
                mp = (irate * iface)/(1.0 - ((1.0 + irate)**(-iterm)))
                logging.debug('calc_monthly_pmt(self, {face}, {rate}, {term}) return: {mp}'.format(face=iface,
                                                                                                   rate=irate,
                                                                                                   term=iterm,
                                                                                                   mp=mp))
                return mp
            # Otherwise, if the term or rate of the Loan object is 0, log an error and then raise a ZeroDivisionError
            # with an error message stating that this causes division by 0 and the term value cannot be 0 in order to
            # calculate a monthly payment value.
            else:
                logging.error('Division by 0: Loan object term and rate values cannot be 0 in order to calculate a '
                              'monthly payment value. Your input term and rate values are '
                              '\n\tterm = {term}'
                              '\n\trate = {rate}'.format(term=iterm, rate=irate))
                raise ZeroDivisionError('Division by 0: Loan object term and rate values cannot be 0 in order to '
                                        'calculate a monthly payment value. Your input term and rate values are '
                                        '\n\tterm = {term}'
                                        '\n\trate = {rate}'.format(term=iterm, rate=irate))
        # Otherwise, if any of the inputs are not a float or an int, log an error and then raise a TypeError with an
        # error message that states all the input into calc_monthly_pmt() must be of type int or float.
        else:
            logging.error('All input into class method calc_monthly_pmt(iface, irate, iterm, t) must be of type int '
                          'or float. Current inputs are '
                          '\n\tface = {face}, {face_type}'
                          '\n\trate = {rate}, {rate_type}'
                          '\n\tterm = {term}, {term_type}'.format(face=iface, rate=irate, term=iterm,
                                                                  face_type=type(iface), rate_type=type(irate),
                                                                  term_type=type(iterm)))
            raise TypeError('All input into class method calc_monthly_pmt(iface, irate, iterm, t) must be of type int '
                            'or float. Current inputs are '
                            '\n\tface = {face}, {face_type}'
                            '\n\trate = {rate}, {rate_type}'
                            '\n\tterm = {term}, {term_type}'.format(face=iface, rate=irate, term=iterm,
                                                                    face_type=type(iface), rate_type=type(irate),
                                                                    term_type=type(iterm)))

    # monthly_payment() function which takes in a dummy period parameter, since it's possible some loan types will have
    # a monthly payment dependent on the period.
    def monthly_payment(self, t=0.0):
        # Check if the Loan has been defaulted on, if the Loan object-level protected variable default is True. If it
        # is, then return 0.
        if self._default:
            logging.info('This Loan has been defaulted on. Monthly payment is 0.')
            return 0.0
        # Check if the input t is an int or a float
        if isinstance(t, (int, float)):
            # Check if the input t is within the lifetime of the loan, from period 0 to the loan's maturity
            logging.debug('Checking if the input t into monthly_payment(t) is within the maturity of the loan '
                          'object (0 to {term})'.format(term=self._term))
            if 0.0 <= t:
                logging.debug('Checking if the input t into monthly_payment(t) is equal to the maturity of the loan'
                              '({term}) and if the term and rate of the loan are not equal to '
                              '0'.format(term=self._term))
                # Check if the input period is equal to the loan's maturity. If it is, then return 0.0.
                #if t == self._term:
                #    logging.debug('Determined that t ({input}) is equal to the loan maturity {term}, monthly_payment(t)'
                #                  'returns 0'.format(input=t, term=self._term))
                #    return 0.0
                # Check if input period t is greater than the maturity of the loan. if it is, then use an info-level log
                # to display that t is greater than the term of the loan.
                if t > self.term:
                    logging.info('t {period} is greater than the loan maturity {term}'.format(period=t, term=self.term))
                    return 0.0
                # Check if the term and rate of the Loan object is not 0. If they are not, calculate and return the
                # monthly loan payment using the class-level method calc_monthly_pmt(), which was defined previously,
                # with input argument self.
                elif self._term != 0.0 and self._rate != 0.0:
                    logging.debug('Determined that t ({input} is not equal to the loan maturity but is within the '
                                  'range of the maturity (0 to {term}), and both term and rate ({rate}) are not equal'
                                  'to 0. Returning monthly payment as calculated by '
                                  'calc_monthly_pmt'.format(input=t, rate=self.rate(t), term=self._term))
                    return Loan.calc_monthly_pmt(self.face, self.rate(t), self.term, t)
                # Otherwise, if the term or rate of the Loan object is 0, log an error and then raise a
                # ZeroDivisionError with an error message stating that this causes division by 0 and the term value
                # cannot be 0 in order to calculate a monthly payment value.
                else:
                    logging.error('Division by 0: Loan object term and rate values cannot be 0 in order to calculate a '
                                  'monthly payment value. Your input term and rate values are '
                                  '\n\tterm = {term}'
                                  '\n\trate = {rate}'.format(term=self.term, rate=self.rate))
                    raise ZeroDivisionError('Division by 0: Loan object term and rate values cannot be 0 in order to '
                                            'calculate a monthly payment value. Your input term and rate values are '
                                            '\n\tterm = {term}'
                                            '\n\trate = {rate}'.format(term=self.term, rate=self.rate))
            # If the input t is outside the lifespan of the loan, log an error message and raise a ValueError with an
            # error message stating that the input period is outside the lifespan of the loan.
            else:
                logging.error('Input t = {input} is outside of the maturity of the loan '
                              '(0 to {term}).'.format(input=t, term=self.term))
                raise ValueError('Input t = ' + str(t) + ' is outside of the maturity of the loan (0 to '
                                 + str(self._term) + ')')
        # Otherwise, if any of the inputs are not a float or an int, log an error and then raise a TypeError with an
        # error message that states the period input t into monthly_payment() must be of type int or float.
        else:
            logging.error('Period input t into monthly_payment(t) must be of type int or float. Your input t = '
                          '{period} is of type {period_type}, not an int or a float'.format(period=t,
                                                                                            period_type=type(t)))
            raise TypeError('Period input t into monthly_payment(t) must be of type int or float. Your input t = '
                            '{period} is of type {period_type}, not an int or a float'.format(period=t,
                                                                                              period_type=type(t)))

    # total_payments() function which calculates the total amount due on the loan.
    def total_payments(self):
        # Check if the Loan has been defaulted on, if the Loan object-level protected variable default is True. If it
        # is, then return 0.
        if self._default:
            logging.info('This Loan has been defaulted on. Total payments is 0.')
            return 0.0
        # Calculate the total payment owed by using a list comprehension that generates a list of every payment for
        # each period and then taking the sum of said list.
        total_pay = sum([self.monthly_payment(t) for t in range(int(self._term))])
        logging.debug('List comprehension to calculate and sum all monthly payments performed in total_payments(). '
                      'Returned {payment}'.format(payment=total_pay))
        return total_pay

    # total_interest() function which calculates the total interest due on the loan.
    def total_interest(self):
        # Check if the Loan has been defaulted on, if the Loan object-level protected variable default is True. If it
        # is, then return 0.
        if self._default:
            logging.info('This Loan has been defaulted on. Total interest is 0.')
            return 0.0
        # First call total_payments() to calculate the total payment that must made on the loan and store what is
        # returned in variable all_pmts. Then, check if the value returned by total_payments() is a float or int.
        all_pmts = self.total_payments()
        logging.debug('total_payments() called within total_interest(t). Returned {payment}. Now checking if said '
                      'result is a float or an int'.format(payment=all_pmts))
        if isinstance(all_pmts, (int, float)):
            # If the value returned by total_payments() is a float or int, subtract the face value of the loan from the
            # the total payment due on the loan. This yields the total amount of interest that is due on the loan.
            total_int = all_pmts - self.face
            logging.debug('Total interest calculated as {interest} in total_interest(t)'.format(interest=total_int))
            return total_int
        # If all_pmts is not a float or a int, log an error and then raise a TypeError with an error message stating
        # total_payments() did not return a float or an int.
        else:
            logging.error('total_payments() did not return a float or an int within total_interest(). It returned '
                          '{tp_return}'.format(tp_return=all_pmts))
            raise TypeError('total_payments() did not return a float or an int within total_interest(). It returned '
                            '{tp_return}'.format(tp_return=all_pmts))

    # class-level method to calculate the balance of a passed in Loan class object and period value. Getter functions
    # are used to access the input loan class object's face, rate, and term variables since they are protected
    # variables.
    @classmethod
    def calc_balance(cls, iface, irate, iterm, t):
        # Check if the input into the calc_balance(t) is a float or an int.
        logging.debug('Checking if input period t into calc_balance(t) is an int or a float')
        if isinstance(t, (int, float)):
            # If t is a float or an int, check if the input t is greater than or equal to 0.0 and less than the term of
            # the loan.
            logging.debug('Checking if input t into calc_balance() is greater than or equal to 0')
            if 0.0 <= t:
                # Check if the input period is greater than or equal to the maturity input. If it is, output 0.
                logging.debug('Checking if input t into calc_balance() is greater than or equal to the input maturity '
                              'of the loan ({term}), as well as if the term and rate input are not equal to '
                              '0'.format(term=iterm))
                # Check if input period t is greater than the maturity of the loan. if it is, then use an info-level log
                # to display that t is greater than the term of the loan.
                if t > iterm:
                    logging.info('t {period} is greater than the loan maturity {term}'.format(period=t, term=iterm))
                    return 0.0
                # Check if the term and rate of the Loan object is not 0. If they are not, calculate and return the
                # balance using the standard formula provided in lecture 2-03 Loans and delegating to the class-level
                # method calc_monthly_payment() to determine the monthly payment within the formula.
                elif iterm != 0.0 and irate != 0.0:
                    logging.debug('t input into calc_balance determined to be less than the maturity of the loan input '
                                  '({term}), but greater than 0, and the input rate was determined not to be 0.')
                    period = float(t)
                    bal = (iface * ((1.0 + irate)**period)) - \
                          (Loan.calc_monthly_pmt(iface, irate, iterm, t) * ((((1.0 + irate)**period) - 1.0) / irate))
                    logging.debug('Balance calculated by calc_balance is {calc_bal}'.format(calc_bal=bal))
                    return bal
                # Otherwise, if the term or rate of the Loan object is 0, log an error and then raise a
                # ZeroDivisionError with an error message stating that this causes division by 0 and the term value
                # cannot be 0 in order to calculate a monthly payment value.
                else:
                    logging.error('Division by 0: Loan object term and rate values cannot be 0 in order to calculate a '
                                  'monthly payment value. Your input term and rate values are '
                                  '\n\tterm = {term}'
                                  '\n\trate = {rate}'.format(term=iterm, rate=irate))
                    raise ZeroDivisionError('Division by 0: Loan object term and rate values cannot be 0 in order to '
                                            'calculate a monthly payment value. Your input term and rate values are '
                                            '\n\tterm = {term}'
                                            '\n\trate = {rate}'.format(term=iterm, rate=irate))
            # Otherwise, if t is negative, log an error and raise a ValueError with an error message stating that the
            # input parameter t cannot be below 0.
            else:
                logging.error('Input period t into calc_balance(t) cannot be below 0. Your input {input} is below '
                              '0'.format(input=t))
                raise ValueError('Input period t into calc_balance(t) cannot be below 0. Your input {input} is below '
                                 '0'.format(input=t))
        # Otherwise, if t is neither a float or an int, log an error and raise a TypeError with an error message telling
        # users input into the calc_balance() class method must be of type int or float.
        else:
            logging.error('Period input t into calc_balance(t) must be of type int or float. Your input t = {period} '
                          'is of type {period_type}, not an int or a float'.format(period=t,
                                                                                   period_type=type(t)))
            raise TypeError('Period input t into calc_balance(t) must be of type int or float. Your input t = {period} '
                            'is of type {period_type}, not an int or a float'.format(period=t,
                                                                                     period_type=type(t)))

    # balance() function which calculates the remaining balance on a loan using the formula provided in lecture 2-03
    # Loans. Decorated with @memoize
    @memoize
    def balance(self, t=0.0):
        # Check if the Loan has been defaulted on, if the Loan object-level protected variable default is True. If it
        # is, then return 0.
        if self._default:
            logging.info('This Loan has been defaulted on. Remaining balance is 0.')
            return 0.0
        # Check if the input into the balance(t) is a float or an int.
        logging.debug('Checking if input period t into balance(t) is an int or a float')
        if isinstance(t, (int, float)):
            # If t is a float or an int, check if the input t is greater than or equal to 0.0.
            logging.debug('Checking if input t into balance() is greater than or equal to 0')
            if 0.0 <= t:
                # Check if the input period is greater than or equal to the loan's maturity. If it is, then return 0.0.
                # Check if the input period is greater than or equal to the maturity input. If it is, output 0.
                logging.debug('Checking if input t into balance() is greater than or equal to the maturity of the loan '
                              '({term}), as well as if the term and rate input are not equal to '
                              '0'.format(term=self._term))
                # Check if input period t is greater than the maturity of the loan. if it is, then use an info-level log
                # to display that t is greater than the term of the loan.
                if t > self.term:
                    logging.info('t {period} is greater than the loan maturity {term}'.format(period=t, term=self.term))
                    return 0.0
                # Check if the term and rate of the Loan object is not 0. If they are not, calculate and return the
                # loan balance using the classmethod calc_balance(), which is defined above.
                elif self._term != 0.0 and self.rate(t) != 0.0:
                    logging.debug('t input into balance() determined to be less than the maturity of the loan ({term})'
                                  ', but greater than 0, and the input rate was determined not to be 0.')
                    bal = Loan.calc_balance(self._face, self.rate(t), self._term, float(t))
                    logging.debug('calc_balance() called within balance() to find the balance. Returned '
                                  '{balance}'.format(balance=bal))
                    return bal
                # Otherwise, if the term or rate of the Loan object is 0, log an error and then raise a
                # ZeroDivisionError with an error message stating that this causes division by 0 and the term value
                # cannot be 0 in order to calculate a monthly payment value.
                else:
                    logging.error('Division by 0: Loan object term and rate values cannot be 0 in order to calculate a '
                                  'monthly payment value. Your input term and rate values are '
                                  '\n\tterm = {term}'
                                  '\n\trate = {rate}'.format(term=self.term, rate=self.rate))
                    raise ZeroDivisionError('Division by 0: Loan object term and rate values cannot be 0 in order to '
                                            'calculate a monthly payment value. Your input term and rate values are '
                                            '\n\tterm = {term}'
                                            '\n\trate = {rate}'.format(term=self.term, rate=self.rate))
            # Otherwise, if t is negative raise a ValueError with an error message stating that the input parameter t
            # cannot be below 0.
            else:
                logging.error('Input period t into balance(t) cannot be below 0. Your input {input} is below '
                              '0'.format(input=t))
                raise ValueError('Input period t into balance(t) cannot be below 0. Your input {input} is below '
                                 '0'.format(input=t))
        # Otherwise, if t is neither a float or an int, log an error and raise a TypeError with an error message telling
        # users input into the balance() function must be of type int or float.
        else:
            logging.error('Period input t into balance(t) must be of type int or float. Your input t = {period} is of'
                          'type {period_type}, not an int or a float'.format(period=t,
                                                                             period_type=type(t)))
            raise TypeError('Period input t into balance(t) must be of type int or float. Your input t = {period} is of'
                            'type {period_type}, not an int or a float'.format(period=t,
                                                                               period_type=type(t)))

    # interest_due() function which calculates the interest due on a loan using the formula provided in lecture 2-03
    # Loans. Decorated with @memoize.
    @memoize
    def interest_due(self, t=0.0):
        # Check if the Loan has been defaulted on, if the Loan object-level protected variable default is True. If it
        # is, then return 0.
        if self._default:
            logging.info('This Loan has been defaulted on. Interest due is 0.')
            return 0.0
        # Check if input period t is greater than the maturity of the loan. if it is, then use an info-level log to
        # display that t is greater than the term of the loan.
        if t > self.term:
            logging.info('t {period} is greater than the loan maturity {term}'.format(period=t, term=self.term))
        # Check if the input into the interest_due(t) is a float or an int.
        logging.debug('Checking if input period t into interest_due(t) is an int or a float')
        if isinstance(t, (int, float)):
            # If the input t is 0, return 0 interest due since there's no payment at issuance.
            if t == 0.0:
                return 0.0
            # If t is a float or an int, check if the input t is greater than or equal to 0.0
            if 0.0 < t:
                # Calculate the remaining balance of the loan using the calc_balance() function and store the result
                # in variable remaining_balance. Input t is cast to a float before being passed into calc_balance() in
                # order to avoid any truncation or other issues using ints with floats in mathematics within Python.
                remaining_balance = Loan.calc_balance(self._face, self.rate(t-1), self._term, float(t-1))
                logging.debug('calc_balance() called within interest_due() to determine the remaining balance at input'
                              'period t ({period}). Returned {balance}).'.format(period=t, balance=remaining_balance))
                logging.debug('Checking if input t into interest_due() is greater than or equal to the maturity of the '
                              'loan ({term}), as well as if the remaining balance calculated above is of type float '
                              '0'.format(term=self._term))
                # Check if the input period t is equal to the loan's maturity. If it is, then return 0.0.
                #if t == self._term:
                #    logging.debug('t input into interest_due() determined to be greater than or equal to the loan'
                #                  'maturity ({term}). Returning 0.0'.format(term=self._term))
                #    return 0.0
                # Check if input period t is greater than the maturity of the loan. if it is, then use an info-level log
                # to display that t is greater than the term of the loan and return 0.
                if t > self.term:
                    logging.info('t {period} is greater than the loan maturity {term}'.format(period=t, term=self.term))
                    return 0.0
                # Check if the variable remaining_balance is of type float. If it is, then return the product of
                # multiplying the remaining balance by the rate of the loan.
                elif isinstance(remaining_balance, float):
                    logging.debug('t input into interest_due(t) determined to be less than the maturity of the loan '
                                  '({term}), but greater than 0, and the remaining balance calculated has been '
                                  'determined to be a float.'.format(term=self._term))
                    int_due = remaining_balance * self.rate(t)
                    logging.debug('interest_due() calculated by multiplying the calculated remaining balance by the '
                                  'loan rate. Yielded {interest}.'.format(interest=int_due))
                    return int_due
                # Otherwise, if variable remaining balance is not of type float, raise a TypeError with an error message
                # stating that balance() did not return a float.
                else:
                    logging.error('balance() did not return a float within interest_due(). It returned '
                                  '{b_return}'.format(b_return=remaining_balance))
                    raise TypeError('balance() did not return a float within interest_due(). It returned '
                                    '{b_return}'.format(b_return=remaining_balance))
            # Otherwise, if t is negative, log an error and raise a ValueError with an error message stating that the
            # input parameter t cannot be below 0.
            else:
                logging.error('Input period t into interest_due(t) cannot be below 0. Your input period t = {period} '
                              'is below 0'.format(period=t))
                raise ValueError('Input period t into interest_due(t) cannot be below 0. Your input period t = '
                                 '{period} is below 0'.format(period=t))
        # Otherwise, if t is neither a float or an int, log an error and raise a TypeError with an error message telling
        # users input into the interest_due() function must be of type int or float.
        else:
            logging.error('Period input t into interest_due(t) must be of type int or float. Your input t = {period} '
                          'is of type {period_type}, not an int or a float'.format(period=t,
                                                                                   period_type=type(t)))
            raise TypeError('Period input t into interest_due(t) must be of type int or float. Your input t = {period} '
                            'is of type {period_type}, not an int or a float'.format(period=t,
                                                                                     period_type=type(t)))

    # principal_due() function which calculates the principal due on a loan using the formula provided in lecture 2-03
    # Loans. Decorated with @memoize.
    @memoize
    def principal_due(self, t=0.0):
        # Check if the Loan has been defaulted on, if the Loan object-level protected variable default is True. If it
        # is, then return 0.
        if self._default:
            logging.info('This Loan has been defaulted on. Principal due is is 0.')
            return 0.0
        # Check if the input into the explicit_principal_due(t) is a float or an int.
        logging.debug('Checking if input period t into principal_due(t) is an int or a float')
        if isinstance(t, (int, float)):
            # If t is a float or an int, check if the input t is greater than or equal to the maturity of the loan. If
            # it is, then return 0.0.
            logging.debug('Checking if input period t into principal_due(t) is greater than to the maturity of the '
                          'loan ({term}), equal to the maturity of the loan, less than the maturity of the loan but '
                          'greater than 0, or less than 0.'.format(term=self._term))
            # Check if the input period is equal to the maturity of the loan. If it is, then return 0.0.
            #if t == self._term:
            #    logging.debug('Input period t into principal_due(t) determined to be greater than the maturity of the '
            #                 'loan ({term}). Returning 0.0'.format(term=self._term))
            #    return 0.0
            # Check if input period t is greater than the maturity of the loan. if it is, then use an info-level log to
            # display that t is greater than the term of the loan and return 0.0.
            if t > self.term:
                logging.info('t {period} is greater than the loan maturity {term}'.format(period=t, term=self.term))
                return 0.0
            # If the input t is 0, return 0 principal due since there's no payment at issuance.
            if t == 0.0:
                return 0.0
            # Otherwise, check if the input t is greater than or equal to 0.0 and less than the term of the
            # loan.
            elif 0.0 <= t <= self._term:
                logging.debug('Input period t into principal_due(t) determined to be between 0 and the maturity of the '
                              'loan ({term})'.format(term=self._term))
                # Utilize the calc_monthly_pmt() class-method to calculate the monthly payment on the loan and store the
                # output to variable monthly_dues.
                monthly_dues = Loan.calc_monthly_pmt(self._face, self.rate(t), self._term, t)
                # Utilize the interest_due() function with passed in parameter t to calculate the interest due on the
                # loan after t payments are made and then store the result in variable current_interest. t is cast to a
                # float before being passed in as an input to interest_due() in order to avoid any complications or
                # truncation from utilizing ints and floats within mathematics in Python.
                current_interest = self.interest_due(float(t))
                # Check if both the monthly_dues and current_interest variables are of type float. If they are, then
                # subtract the current_interest from the monthly_dues in order to find the principal due. Then, return
                # this value.
                logging.debug('calc_monthly_pmt() called within principal_due(). Returned ({mp}). interest_due() '
                              'called within principal_due(). Returned ({id}). Checking if the two results are '
                              'floats'.format(mp=monthly_dues, id=current_interest))
                if isinstance(monthly_dues, float) and isinstance(current_interest, float):
                    prin_due = monthly_dues - current_interest
                    logging.debug('Both calc_monthly_pmy() and interest_due() returned floats. Principal due '
                                  'calculated by subtracting interest due from the monthly payment. Returned '
                                  '{p_due}'.format(p_due=prin_due))
                    return prin_due
                # Otherwise, if the monthly_dues is not a float, log an error and raise a TypeError with an error
                # message stating that monthly_payment() did not return a float within principal_due().
                elif type(monthly_dues) is not float:
                    logging.error('monthly_payment() did not return a float within principal_due(). It returned '
                                  '{mp_return}'.format(mp_return=monthly_dues))
                    raise TypeError('monthly_payment() did not return a float within principal_due(). It returned '
                                    '{mp_return}'.format(mp_return=monthly_dues))
                # Otherwise, if the interest due is not a float, log an error and raise a TypeError with an error
                # message stating that interest_due() did not return a float within principal_due().
                else:
                    logging.error('interest_due() did not return a float within principal_due(). It returned '
                                  '{id_return}'.format(id_return=current_interest))
                    raise TypeError('interest_due() did not return a float within principal_due(). It returned '
                                    '{id_return}'.format(id_return=current_interest))
            # Otherwise, if t is negative, log an error and raise a ValueError with an error message stating that the
            # input parameter t cannot be below 0.
            else:
                logging.error('Input period t into principal_due(t) cannot be below 0. Your input period t = {period} '
                              'is below 0'.format(period=t))
                raise ValueError('Input period t into principal_due(t) cannot be below 0. Your input period t = '
                                 '{period} is below 0'.format(period=t))
        # Otherwise, if t is neither a float or an int, log an error and raise a TypeError with an error message telling
        # users input into the principal_due() function must be of type int or float.
        else:
            logging.error('Period input t into principal_due(t) must be of type int or float. Your input t = {period} '
                          'is of type {period_type}, not an int or a float'.format(period=t,
                                                                                   period_type=type(t)))
            raise TypeError('Period input t into principal_due(t) must be of type int or float. Your input t = '
                            '{period} is of type {period_type}, not an int or a float'.format(period=t,
                                                                                              period_type=type(t)))

    # recovery_value() method that returns the current asset value for the given period times a recovery multiplier of
    # rec_rate
    def recovery_value(self, t=0.0):
        # Check if input period t is greater than or equal to the maturity of the loan. if it is, then use an info-level
        # log to display that t is greater than or equal to the term of the loan and return 0.0.
        if t >= self.term:
            logging.info('t {period} is greater than or equal to the loan maturity {term}'.format(period=t, term=self.term))
            return 0.0

        # Check if the passed in period t is a float or an int
        logging.debug('Checking if input period t into recovery_value(t) is an int or a float')
        if isinstance(t, (int, float)):
            logging.debug('Input t into recovery_value(t) determined to be an int or float.')
            # If t is a float or an int, then delegate to the current_value() function from the Assets class to find the
            # current value of the asset the Loan is for, multiply the result by the recovery multiplier 0.6, and then
            # return the product. t is cast to a float prior to being passed into the current_value() function in order
            # to avoid complications (ie. truncation) from using floats and ints together in Python arithmetic
            # operations
            # Recovery Value based on Asset Value: curr_val = self._asset.current_value(float(t-1))
            curr_val = self.balance(t-1)
            self._rec_val = curr_val * float(self._rec_rate)
            logging.debug('current_value() function from the Assets class called on the Loan object variable asset in '
                          'order to determine the current value of the asset. Returned {value}. Recovery value then'
                          'determined by multiplying the found current value by a recovery factor of 0.6. Returned '
                          '{recover}'.format(value=curr_val, recover=self._rec_val))
            return self._rec_val
        # Otherwise, if t is not an int or a float, log an error and raise a TypeError with an error message stating
        # that the period input t must be an int or a float.
        else:
            logging.error('Period input t into recovery_value(t) must be of type int or float. Your input t = {period} '
                          'is of type {period_type}, not an int or a float'.format(period=t,
                                                                                   period_type=type(t)))
            raise TypeError('Period input t into recovery_value(t) must be of type int or float. Your input t = '
                            '{period} is of type {period_type}, not an int or a float'.format(period=t,
                                                                                              period_type=type(t)))

    # equity() method that returns the available equity (The asset value less the loan balance)
    def equity(self, t=0.0):
        # Check if input period t is greater than the maturity of the loan. if it is, then use an info-level log to
        # display that t is greater than the term of the loan.
        if t > self.term:
            logging.info('t {period} is greater than the loan maturity {term}'.format(period=t, term=self.term))

        # Check if the passed in period t is a float or an int
        logging.debug('Checking if input period t into equity(t) is an int or a float')
        if isinstance(t, (int, float)):
            logging.debug('Input t into equity(t) determined to be an int or float.')
            # If t is a float or an int, then delegate to the current_value() function from the Assets class to find the
            # current value of the asset the Loan is for, subtract the current balance of the loan as calculated by
            # balance() from the current value of the asset, and then return the result.  t is cast to a float prior to
            # being passed into the current_value() function in order to avoid complications (ie. truncation) from using
            # floats and ints together in Python arithmetic operations
            curr_val = self.asset.current_value(float(t))
            bal = self.balance(float(t))
            eq = curr_val - bal
            logging.debug('current_value() function from the Assets class called on the Loan object variable asset in '
                          'order to determine the current value of the asset. Returned {value}. balance() function '
                          'also called to determine the remaining balance at input period ({period}). Returned {b}. '
                          'Equity then determined by subtracting the remaining balance from the current value yielding '
                          '{equity}.'.format(value=curr_val, period=t, b=bal, equity=eq))
            return eq
        # Otherwise, if t is not an int or a float, log an error and raise a TypeError with an error message stating
        # that the period input t must be an int or a float.
        else:
            logging.error('Period input t into equity(t) must be of type int or float. Your input t = {period} is of '
                          'type {period_type}, not an int or a float'.format(period=t,
                                                                             period_type=type(t)))
            raise TypeError('Period input t into equity(t) must be of type int or float. Your input t = {period} is of '
                            'type {period_type}, not an int or a float'.format(period=t,
                                                                               period_type=type(t)))

    # check_default method that determines whether or not the Loan object defaults based on an input number
    # default_notification. Takes optional input t for the period in order to return the recovery value of the
    # underlying asset at the time the Loan is defaulted on.
    def check_default(self, default_notification, t=0.0):
        # Check if loan has already defaulted. If it has, set rec_val to 0, return 0, and ignore the rest of the check
        # since the recovery value has already been paid out.
        if self._default:
            self._rec_val = 0.0
            return 0.0
        # If the input default_notification is equal to 0, then set the Loan's protected object level default variable
        # to True. This signifies that the Loan has been defaulted on and will let the monthly_payment, total_payment,
        # total_interest, balance, principal_due, and interest_due functions know to return 0 when called from now on.
        elif default_notification == 0:
            self._default = True
            return self.recovery_value(t)
        # Otherwise, if default_notification is not 0, return 0.0.
        else:
            return 0.0

    # reset method that sets the Loan object level default variable to False
    def reset(self):
        self._default = False
