'''
Daniel McNulty II

This file contains the stand-alone function do_waterfall()
'''

# Import the LoanPool class from the loan_pool module in the Loan package
from Loan.loan_pool import LoanPool
# Import the StructuredSecurities class from the securities module of the Securitization package
from Securitization.securities import StructuredSecurities
# Import the Tranche class from the tranche module of the Securitization package
from Securitization.tranche import Tranche

# Stand-alone function do_waterfall for parts 1 and 2, with input parameters loan_pool and struct_sec.
def do_waterfall(loan_pool, struct_sec):
    # Check if the inputs for loan_pool and struct_sec are LoanPool and StructuredSecurities objects respectively.
    if isinstance(loan_pool, LoanPool) and isinstance(struct_sec, StructuredSecurities):
        # Set the period to 1
        t = 0
        # Initialize lists to hold the resulting lists from calling get_waterfall within the following while loop.
        #       - loan_pool_wf will hold results from calling get_waterfall on the input loan_pool
        #       - struct_sec_wf will hold the results from calling get_waterfall on the input struct_sec
        #       - res_acct will hold the resulting reserve account within the structured security after each
        #         get_waterfall call on the struct_sec_wf
        loan_pool_wf = []
        struct_sec_wf = []
        res_acct = []

        # While loop that will iterate continuously until there are no more active loans within the loan_pool.
        while loan_pool.active_loans(t) > 0:
            # Look for defaults within the loan pool at the given period and return the recovery value of the defaulted
            # loans
            rec_val = loan_pool.check_defaults(t)
            # Calculate the aggregate monthly payment for all the loans in the loan pool and store it in variable
            # pmt_due
            pmt_due = loan_pool.aggregate_monthly_pmt(t)
            # Call make_payment on the StructuredSecurities object struct_sec with an input amount of pmt_due.
            struct_sec.make_payment(pmt_due, loan_pool.aggregate_principal_due(t), rec_val, loan_pool.active_loans(t))
            # Append the result of calling get_waterfall on input struct_sec to the list struct_sec_wf.
            struct_sec_wf.append(struct_sec.get_waterfall())
            # Append the result of calling get_waterfall with input period t on the input loan_pool to the list
            # loan_pool_wf.
            loan_pool_wf.append(loan_pool.get_waterfall(t))
            # Append the reserve account amount of the StructuredSecurity object struct_sec for the current iteration
            # to the list res_acct.
            res_acct.append(struct_sec._res_acct)
            # Increment the period t by 1.
            struct_sec.increase_time_period()
            t += 1

        # Initialize a list of lists, one list for each tranche in the input StructuredSecurities object struct_sec, in
        # variable tranche_pmts.
        tranche_pmts = [[] for num in range(len(struct_sec.tranches))]
        tranche_prin_pmts = [[] for num in range(len(struct_sec.tranches))]
        tranche_balances = [[] for num in range(len(struct_sec.tranches))]
        # Iterate through all the lists within the struct_sec_wf list.
        for waterfalls in struct_sec_wf:
            # Enumerate each item in the current waterfalls list, then get the total payments for each tranche by adding
            # the interest and principal paid for each waterfall together and then appending it to the list associated
            # with tranche_pmts[num]
            for num, tnch_wtrfl in enumerate(waterfalls):
                tranche_pmts[num].append(tnch_wtrfl[1] + tnch_wtrfl[3])
                tranche_prin_pmts[num].append(tnch_wtrfl[3])
                tranche_balances[num].append(tnch_wtrfl[4])

        # Calculate the metrics of each tranche within the input struct_sec object by zipping the struct_sec tranches
        # list and the tranche_pmts lists together into a generator of tuples and iterating through each tranche and
        # tranche_pmts list, calling the irr, dirr, and avg_life functions with the tranche_pmts list for the current
        # tranche as input, and the abs_rater function with the DIRR of the current tranche as input.
        tranche_met = [(tranche.irr(pmt), tranche.dirr(pmt), tranche.avg_life(prin_pmt, b),
                        Tranche.abs_rater(tranche.dirr(pmt))) for tranche, pmt, prin_pmt, b in zip(struct_sec._tranches,
                                                                                                   tranche_pmts,
                                                                                                   tranche_prin_pmts,
                                                                                                   tranche_balances)]
        # Return the loan_pool_wf, struct_sec_wf, res_acct, tranche_met lists
        return loan_pool_wf, struct_sec_wf, res_acct, tranche_met

    # If the input loan_pool is not of the LoanPool class, then a TypeError is raised telling users the loan_pool input
    # for do_waterfall must be of type LoanPool.
    elif not isinstance(loan_pool, LoanPool):
        raise TypeError('loan_pool input for do_waterfall() must be a LoanPool object. Your input {input} is of type '
                        '{input_type}, not LoanPool.'.format(input=loan_pool, input_type=type(loan_pool)))

    # If the input struct_sec is not of the StructuredSecurities class, then a TypeError is raised telling users the
    # struct_sec input for do_waterfall must be of type StructuredSecurities.
    else:
        raise TypeError('struct_sec input for do_waterfall() must be a StructuredSecurities object. Your input {input} '
                        'is of type {input_type}, not StructuredSecurities.'.format(input=struct_sec,
                                                                                    input_type=type(struct_sec)))


# Stand-alone function mc_do_waterfall for Part 3, with input parameters loan_pool and struct_sec.
def mc_do_waterfall(loan_pool, struct_sec):
    # Check if the inputs for loan_pool and struct_sec are LoanPool and StructuredSecurities objects respectively.
    if isinstance(loan_pool, LoanPool) and isinstance(struct_sec, StructuredSecurities):
        # Set the period to 1
        t = 0
        # Initialize lists to hold the resulting lists from calling get_waterfall within the following while loop.
        #       - loan_pool_wf will hold results from calling get_waterfall on the input loan_pool
        #       - struct_sec_wf will hold the results from calling get_waterfall on the input struct_sec
        #       - res_acct will hold the resulting reserve account within the structured security after each
        #         get_waterfall call on the struct_sec_wf
        loan_pool_wf = []
        struct_sec_wf = []
        res_acct = []

        # While loop that will iterate continuously until there are no more active loans within the loan_pool.
        while loan_pool.active_loans(t) > 0:
            # Look for defaults within the loan pool at the given period and return the recovery value of the defaulted
            # loans
            rec_val = loan_pool.check_defaults(t)
            # Calculate the aggregate monthly payment for all the loans in the loan pool and store it in variable
            # pmt_due
            pmt_due = loan_pool.aggregate_monthly_pmt(t)
            # Call make_payment on the StructuredSecurities object struct_sec with an input amount of pmt_due.
            struct_sec.make_payment(pmt_due, loan_pool.aggregate_principal_due(t), rec_val, loan_pool.active_loans(t))
            # Append the result of calling get_waterfall on input struct_sec to the list struct_sec_wf.
            struct_sec_wf.append(struct_sec.get_waterfall())
            # Append the result of calling get_waterfall with input period t on the input loan_pool to the list
            # loan_pool_wf.
            loan_pool_wf.append(loan_pool.get_waterfall(t))
            # Append the reserve account amount of the StructuredSecurity object struct_sec for the current iteration
            # to the list res_acct.
            res_acct.append(struct_sec._res_acct)
            # Increment the period t by 1.
            struct_sec.increase_time_period()
            t += 1

        # Initialize a list of lists, one list for each tranche in the input StructuredSecurities object struct_sec, in
        # variable tranche_pmts.
        tranche_pmts = [[] for num in range(len(struct_sec.tranches))]
        tranche_prin_pmts = [[] for num in range(len(struct_sec.tranches))]
        tranche_balances = [[] for num in range(len(struct_sec.tranches))]
        # Iterate through all the lists within the struct_sec_wf list.
        for waterfalls in struct_sec_wf:
            # Enumerate each item in the current waterfalls list, then get the total payments for each tranche by adding
            # the interest and principal paid for each waterfall together and then appending it to the list associated
            # with tranche_pmts[num]
            for num, tnch_wtrfl in enumerate(waterfalls):
                tranche_pmts[num].append(tnch_wtrfl[1] + tnch_wtrfl[3])
                tranche_prin_pmts[num].append(tnch_wtrfl[3])
                tranche_balances[num].append(tnch_wtrfl[4])

        # Calculate the metrics of each tranche within the input struct_sec object by zipping the struct_sec tranches
        # list and the tranche_pmts lists together into a generator of tuples and iterating through each tranche and
        # tranche_pmts list, calling the irr, dirr, and avg_life functions with the tranche_pmts list for the current
        # tranche as input, and the abs_rater function with the DIRR of the current tranche as input.
        tranche_dirrs = [tranche.dirr(pmt) for tranche, pmt in zip(struct_sec._tranches, tranche_pmts)]
        tranche_als = [tranche.avg_life(prin_pmt, b) for tranche, prin_pmt, b in zip(struct_sec._tranches,
                                                                                     tranche_prin_pmts,
                                                                                     tranche_balances)]

        # Return the loan_pool_wf, struct_sec_wf, res_acct, tranche_met lists
        return loan_pool_wf, struct_sec_wf, res_acct, tranche_dirrs, tranche_als

    # If the input loan_pool is not of the LoanPool class, then a TypeError is raised telling users the loan_pool input
    # for do_waterfall must be of type LoanPool.
    elif not isinstance(loan_pool, LoanPool):
        raise TypeError('loan_pool input for do_waterfall() must be a LoanPool object. Your input {input} is of type '
                        '{input_type}, not LoanPool.'.format(input=loan_pool, input_type=type(loan_pool)))

    # If the input struct_sec is not of the StructuredSecurities class, then a TypeError is raised telling users the
    # struct_sec input for do_waterfall must be of type StructuredSecurities.
    else:
        raise TypeError('struct_sec input for do_waterfall() must be a StructuredSecurities object. Your input {input} '
                        'is of type {input_type}, not StructuredSecurities.'.format(input=struct_sec,
                                                                                    input_type=type(struct_sec)))

