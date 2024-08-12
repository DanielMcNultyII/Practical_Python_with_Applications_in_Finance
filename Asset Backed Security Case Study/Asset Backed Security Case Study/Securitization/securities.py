'''
Daniel McNulty II

This file contains the StructuredSecurities class
'''

# Import the logging module
import logging
# Import the StandardTranche class from the StandardTranche module
from Securitization.tranche import StandardTranche

class StructuredSecurities(object):
    # Standard initialization function
    def __init__(self, tot_notional):
        # tot_not stores the input total notional value of the structured security
        self._tot_not = float(tot_notional)
        # lp stores the loan pool underlying the security
        # self._lp = lp
        # tranches is initialized as an empty list and will hold the tranches of the StructuredSecurities object
        self._tranches = []
        # mode will hold whether the StructuredSecurity is 'Sequential' or 'Pro Rata'
        self._mode = 'Sequential'
        # res_acct is initialized as 0.0, and will be used to hold the reserve account of the StructuredSecurity
        self._res_acct = 0.0

    # Getter property for the tranche list of the StructuredSecurities class object
    @property
    def tranches(self):
        logging.debug('tranches(self) return: {tranches}'.format(tranches=self._tranches))
        return self._tranches

    # add_tranche 'Factory Method' to add tranches to a StructuredSecurities object. Instantiates and add the tranche to
    # the StructuredSecurities object's list of tranches (tranches)
    def add_tranche(self, tranche_class, notional_per, rate, sub_level):
        # Checks if the input for tranche class is 'StandardTranche'. If it is, then it creates a StandardTranche object
        # with a notional value of the input notional percentage (notional_per) times the total notional of the
        # StructuredSecurities object (tot_not), a rate of the input rate, and a subordination flag of the sub_level
        # input. It then appends the newly-made StandardTranche object to the StructuredSecurities object's tranche list
        # and sorts the StructuredSecurities object's list of tranches based on their subordination level.
        if tranche_class == 'StandardTranche':
            self._tranches.append(StandardTranche((notional_per * self._tot_not), notional_per, rate, sub_level))
            self._tranches = sorted(self._tranches, key=lambda tranche: tranche._sub_flag)
        # If the user inputs anything other than 'StandardTranche' for the tranche_class input, then an exception is
        # raised telling users that input tranche_class into add_tranche must be 'StandardTranche'
        else:
            raise Exception('Input tranche_class into add_tranche must be "StandardTranche".')

    # mode_flagger method to flag 'Sequential' or 'Pro Rata' modes on the object.
    def mode_flagger(self, mode):
        # Checks if the input mode is in the set {'Sequential', 'Pro Rata'}. If it is, then the StructuredSecurities
        # object's mode variable is set to the input mode.
        if mode in {'Sequential', 'Pro Rata'}:
            self._mode = mode
        # If the user does not input either 'Sequential' or 'Pro Rata', then a ValueError is raised telling users that
        # their input mode must be either 'Sequential' or 'Pro Rata'.
        else:
            raise ValueError('Input for mode_flagger must be either "Sequential" or "Pro Rata". Your input {inmode} is '
                             'not a {inmode} is not a valid input.'.format(inmode=mode))

    # increase_time_period method that increases the current time period for each tranche
    def increase_time_period(self):
        # Use a for loop to iterate through all the tranches in the StructuredSecurities object's tranche list tranches
        # and call increase_time_period on each tranche.
        for tranche in self._tranches:
            tranche.increase_time_period()

    # make_payments method
    def make_payment(self, pmt_amt, prin_rec, rec_val, al):
        # Initialize the variable cash_amt to the input pmt_amt plus what is currently stored in the
        # StructuredSecurities object's res_acct variable. Then set the res_acct to 0 since it will be used as part of
        # the payment made.
        cash_amt = pmt_amt + self._res_acct - prin_rec
        self._res_acct = 0.0

        # Use a for loop to cycle through all interest payments on the tranches in the StructuredSecurities tranches
        # list, paying each tranche from the available cash_amt. This is done by first checking that the tranche for the
        # current iteration has a notional value greater than 0, and then calling the make_interest_payment function on
        # the tranche with input variable cash_amt. The return value is stored in cash_amt, as the return of
        # make_interest_payment is what is left over of the input once the interest payment is made.
        for tranche in self._tranches:
            if tranche._current_not_bal > 0:
                cash_amt = tranche.make_interest_payment(cash_amt)

        # Check if there are any active loans. If there are, then set the reserve cash balance to the remaining cash_amt
        # and cash_amt to be used to pay principal to the principal received plus the recovery value from any defaulted
        # loans.
        if al != 0:
            self._res_acct = cash_amt

        # Set the available cash amount to the principal received plus any recovery value obtained from defaulted loans
        cash_amt = prin_rec + rec_val

        # If statement that checks if there is cash left over
        if cash_amt > 0:
            # If the mode of the StructuredSecurities object is 'Sequential', then cycle through each tranche using a
            # for loop, making the maximum principal payment. If there is principal left over after paying a tranche,
            # use it to start paying off the next tranche. If there's a shortfall for a tranche, it's used in the next
            # period's principal due calculation for that tranche.
            if self._mode == 'Sequential':
                for tranche in self._tranches:
                    # Check if the notional of the current tranche has not already been paid and that the current
                    # cash_amt is greater than 0.
                    if tranche._current_not_bal > 0 and cash_amt > 0:
                        cash_amt = tranche.make_principal_payment(cash_amt)

            # If the mode of the StructuredSecurities object is 'Pro Rata', the each tranche is allocated a portion of
            # principal payment based on each tranche's percent of the total notional of the StructuredSecurities
            # object. If there's a shortfall for a tranche, it's used in the next period's principal due calculation
            # for that tranche.
            elif self._mode == 'Pro Rata':
                rem_money_after_prin_pmt = 0.0
                for tranche in self._tranches:
                    # Check if the notional of the current tranche has not already been paid.
                    if tranche.notional_balance > 0:
                        rem_money_after_prin_pmt += tranche.make_principal_payment(tranche._notional_per * cash_amt)
                cash_amt = rem_money_after_prin_pmt

        # If there is leftover cash after all interest and principal payments have been made and there are tranches that
        # still have outstanding notionals, we add the resulting cash_amt to the StructuredSecurities object's res_acct
        # variable
        for tranche in self._tranches:
            if tranche._current_not_bal > 0:
                self._res_acct += cash_amt
                break

    # get_waterfall function that returns a list of lists , with each inner list representing a tranche and containing
    # the interest due, interest paid, interest shortfall, principal paid, and balance of the tranche for the current
    # time period of the StructuredSecurity.
    def get_waterfall(self):
        # Initialize a list containing a list for each tranche in the StructuredSecurities object's tranche list.
        tran_info = [[] for tranche in self._tranches]
        # Enumerate and loop through all the tranches in the StructuredSecurities object's tranche list.
        for num, tranche in enumerate(self._tranches):
            bal = tranche.notional_balance
            pp = tranche.principal_paid
            idu = tranche.interest_due
            ip = tranche.interest_paid
            ishrt = tranche.interest_shortfall

            tran_info[num] = [idu, ip, ishrt, pp, bal]

        return tran_info

    # reset function that sets the StructuredSecurities object's reserved_account object variable to 0.0 and then
    # resets the tranches of the StructuredSecurities object by iterating through all of the object's tranches and
    # calling reset on each tranche.
    def reset(self):
        self._res_acct = 0.0
        for tranche in self._tranches:
            tranche.reset()
