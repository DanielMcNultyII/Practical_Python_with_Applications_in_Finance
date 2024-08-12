'''
Daniel McNulty II

Runs the various functions created within this case study.
'''


# Import the LoanPool class from the loan_pool module of the Loan package
from Loan.loan_pool import LoanPool
# Import the StructuredSecurities class from the securities module of the Securitization package
from Securitization.securities import StructuredSecurities
# Import the monte_carlo library as mc
import monte_carlo as mc
# Import the timer class from the timer module of the Utilities package
import Utilities.timer as timer

def main():
    # Create a loan pool consisting of all the loans outlined in the Loans.csv
    lp = LoanPool([])
    lp.csv_loader('Loans.csv')
    # Create a structured security with total notional equal to all the 80% of the total principal of the loan pool
    # created above
    ss = StructuredSecurities(lp.total_principal()*.8)
    # Add two tranches to the structured security
    ss.add_tranche('StandardTranche', 0.7, 0.05/12.0, 'A')
    ss.add_tranche('StandardTranche', 0.3, 0.08/12.0, 'B')

    # MONTE CARLO WITHOUT MULTIPROCESSING ------------------------------------------------------------------------------
    # Create and start a timer to show how long the run_monte function takes without multiprocessing
    n_t = timer.Timer(timer_name="Normal Timer")
    n_t.start()
    # Run the run_monte function, which does not include multiprocessing, and print the results to the output window
    print(mc.run_monte(lp, ss, 0.05, 100))
    # Stop the timer after the run_monte has run and print how long the function took to run to the output window
    n_t.end()

    print("\n-------------------------------------------------------------------------------------------------------\n")

    # MONTE CARLO WITH MULTIPROCESSING ---------------------------------------------------------------------------------
    # Create and start a timer to show how long the run_monte function takes with multiprocessing
    p_t = timer.Timer(timer_name="Parallel Timer")
    p_t.start()
    # Run the parallel_run_monte function, which is functionally the same as the run_monte function but utilizes
    # multiprocessing. Print the results to the output window
    print(mc.parallel_run_monte(lp, ss, 0.05, 100, 5))
    # Stop the timer after the parallel_run_monte has run and print how long the function took to run to the output
    # window
    p_t.end()


########################################################################################################################
if __name__ == '__main__':
    main()
