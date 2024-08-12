'''
Daniel McNulty II

Runs the various functions created within parts 1 and 2 of this case study.
'''


# Import the LoanPool class from the loan_pool module of the Loan package
from Loan.loan_pool import LoanPool
# Import the StructuredSecurities class from the securities module of the Securitization package
from Securitization.securities import StructuredSecurities
# Import the mc_do_waterfall function from the do_waterfall module
from do_waterfall import do_waterfall


def main():
    # Create a loan pool consisting of all the loans outlined in the Loans.csv
    lp = LoanPool([])
    lp.csv_loader('Loans.csv')
    # Create a structured security with total notional equal to all the total principal of the loan pool created above
    ss = StructuredSecurities(lp.total_principal()*0.8)
    # Add two tranches to the structured security and set it to be sequentially paying
    ss.add_tranche('StandardTranche', 0.8, 0.05/12.0, 'A')
    ss.add_tranche('StandardTranche', 0.2, 0.08/12.0, 'B')
    ss._mode = 'Sequential'

    # Run the do_waterfall function with the loan pool and structured security created above, then store the outputs
    lp_wtr, ss_wtr, res_acct, metrics = do_waterfall(lp, ss)

    # Create a file called Tranche_Cash_Flows.csv and store the tranche-specific outputs from the above run waterfall in
    # it
    with open('Tranche_Cash_Flows.csv', 'w') as lf:
        # Loop through each tranche's metrics to print them to the output terminal and write them to the
        # Tranche_Cash_Flows.csv file
        for i in range(len(ss._tranches)):
            # Print current tranche's metrics to output terminal
            print('\nTRANCHE {tn} METRICS\nIRR: {irr}\nDIRR: {dirr}\nAL: {al}\n'
                  'ABS Rating: {absr}\n'.format(tn=ss._tranches[i]._sub_flag,
                                                irr=metrics[i][0],
                                                dirr=metrics[i][1],
                                                al=metrics[i][2],
                                                absr=metrics[i][3]))
            # Write the current tranche's metrics to the Tranche_Cash_Flows.csv
            lf.write('\nTRANCHE {tn} METRICS\nIRR,{irr}\nDIRR,{dirr}\nAL,{al}\n'
                     'ABS Rating,{absr}\n'.format(tn=ss._tranches[i]._sub_flag,
                                                  irr=metrics[i][0],
                                                  dirr=metrics[i][1],
                                                  al=metrics[i][2],
                                                  absr=metrics[i][3]))

        # Create divider between the tranche metrics and tranche principal, interest, and recovery value payments in the
        # Tranche_Cash_Flows.csv file
        lf.write('\nTRANCHE CASH FLOWS\nPeriod,Tranche,Interest Due,Interest Paid,Interest Shortfall,Principal Paid,Notional Balance\n')

        # Loop through each tranche and write the interest and principal payments, as well as recovery values if
        # necessary, received by the structured securities tranches in the above run waterfall to the
        # Tranche_Cash_Flows.csv file
        for p in range(len(ss._tranches)):
            for num in range(len(ss_wtr)):
                lf.write('{p},{t},{id},{ip},{ishrt},{pp},{nb}\n'.format(p=num,
                                                                        t=ss.tranches[p].sub_flag,
                                                                        id=ss_wtr[num][p][0],
                                                                        ip=ss_wtr[num][p][1],
                                                                        ishrt=ss_wtr[num][p][2],
                                                                        pp=ss_wtr[num][p][3],
                                                                        nb=ss_wtr[num][p][4]))

    # Create a file called Loan_Cash_Flows.csv and store the following monthly loan-specific outputs for each of the
    # loans in the loan pool from the above run waterfall to the file:
    #       - Loan Number
    #       - Rate
    #       - Term
    #       - Underlying Asset Initial Value
    #       - Underlying Asset Depreciation Rate
    #       - Recovery Rate
    #       - Monthly Payment
    #       - Principal Received
    #       - Principal Due
    #       - Interest Due
    #       - Recovery Value (If loan defaulted)
    #       - End of Month Balance
    with open('Loan_Cash_Flows.csv', 'w') as af:
        # Write the header for the loan cash flow table into the Loan_Cash_Flows.csv file
        af.write('Period,Loan #,Loan Rate,Loan Term,Underlying Asset Initial Value,Underlying Asset Depreciation Rate,Recovery Rate,Monthly Payment,Principal Due,Interest Due,Total Default Recovery,Ending Loan Balance\n')
        # Loop through each loan in the loan pool and write the aforementioned monthly loan-specific waterfall outputs
        # for each given loan to the Loan_Cash_Flows.csv file
        for i in range(len(lp.loans)):
            for num in range(len(lp_wtr)):
                af.write('{t},{ln},{lr},{lt},{uaiv},{uadr},{rr},{mth_pmt},{prn_due},{int_due},{rec},{bal}\n'.format(t=num,
                                                                                                                    ln=lp.loans[i].loan_num,
                                                                                                                    lr=lp.loans[i].rate(),
                                                                                                                    lt=lp.loans[i].term,
                                                                                                                    uaiv=lp.loans[i].asset.init_val,
                                                                                                                    uadr=lp.loans[i].asset.depr_rate,
                                                                                                                    rr=lp.loans[i].rec_rate,
                                                                                                                    mth_pmt=lp_wtr[num][i][0],
                                                                                                                    prn_due=lp_wtr[num][i][1],
                                                                                                                    int_due=lp_wtr[num][i][2],
                                                                                                                    rec=lp_wtr[num][i][3],
                                                                                                                    bal=lp_wtr[num][i][4]))


########################################################################################################################
if __name__ == '__main__':
    main()
