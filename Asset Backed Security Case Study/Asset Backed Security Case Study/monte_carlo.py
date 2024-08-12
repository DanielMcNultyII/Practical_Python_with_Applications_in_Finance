'''
Daniel McNulty II

This file contains the code necessary to run Monte Carlo simulations.
'''


# Import the numpy package
import numpy
# Import the multiprocessing package
import multiprocessing as mp
# Import the mc_do_waterfall function from the do_waterfall module
from do_waterfall import do_waterfall, mc_do_waterfall
# Import the LoanPool class from the loan_pool module in the Loan package
from Loan.loan_pool import LoanPool
# Import the StructuredSecurities class from the securities module of the Securitization package
from Securitization.securities import StructuredSecurities
# Import the Tranche class from the tranche module of the Securitization package
from Securitization.tranche import Tranche


# simulate_waterfall function, which calls the do_waterfall function nsim number of times for an input loan pool and
# structured security object. Each do_waterfall output tranche dirr and weighted average life is stored. The average
# of all the stored dirr and weighted average lives calculated for each tranche is then determined and output.
def simulate_waterfall(loan_pool, struct_sec, nsim):
    # Initialize lists which will store relevant outputs:
    #   - metrics to hold the current do_waterfall output
    #   - dirr_al_vals to hold all the calculated do_waterfall dirr and weighted average life outputs for each tranche,
    #     and ultimately the averages for each tranche
    metrics = []
    dirr_al_vals = [[[], []] for tranche in struct_sec._tranches]

    # For loop which will call the do_waterfall function nsim times, resetting the loan_pool and struct_sec objects
    # prior to each call, and store resulting dirrs and weighted average lives in the metrics list.
    for sim in range(nsim):
        # Reset loan_pool and struct_sec before calling do_waterfall.
        loan_pool.reset()
        struct_sec.reset()

        # Call do_waterfall with loan_pool and struct_sec as inputs. Store the resulting dirrs and weighted average
        # lives calculated into the metrics list.
        metrics.append(do_waterfall(loan_pool, struct_sec)[3])

    # Loop through each entry in the metrics list.
    for met in metrics:
        # For each entry in metrics, loop through each tranche and add the dirr and weighted average life corresponding
        # to eac tranche to the dirr_al_vals list.
        for num, tup in enumerate(met):
            # If thue calculated dirr is inf, do not include it in the list of output dirrs for the current tranche.
            if tup[1] != numpy.inf:
                # If the calculated dirr is not inf, add the absolute value of it to the list of output dirrs for the
                # crrent tranche.
                dirr_al_vals[num][0].append(abs(tup[1]))
            # If the calculated weighted average life is inf, do not include it in the list of output weighted average
            # lives for the current tranche.
            if tup[2] != numpy.inf:
                # If nithe calculated weighted average life is not inf, add it to the list of output weighted average
                # lives for the current tranche.
                dirr_al_vals[num][1].append(tup[2])

    # Loop through each list in the dirr_al_vals list, which should correspond to 1 list per tranche.
    for num in range(len(dirr_al_vals)):
        # Take the average of each list in the current dirr_al_vals entry list. This is the equivalent of taking the
        # average of the calculated dirrs and weighted average lives for a given tranche. Store the results in the
        # dirr_al_vals list over where the list of output dirrs and weighted average lives used to be.
        dirr_al_vals[num][0] = numpy.average(dirr_al_vals[num][0])
        dirr_al_vals[num][1] = numpy.average(dirr_al_vals[num][1])

    # Return the list of average tranche dirrs and weighted average lives.
    return dirr_al_vals

# mc_simulate_waterfall function, which is the above simulate_waterfall function modified to work better for monte
# carlo simulations that use multiprocessing. It calls the mc_do_waterfall function nsim number of times for an input
# loan pool and structured security object. Each do_waterfall output tranche dirr and weighted average life is stored.
# The average of all the stored dirr and weighted average lives calculated for each tranche is then determined and
# output.
def mc_simulate_waterfall(loan_pool, struct_sec, nsim):
    # Create a dirrs and als list to store the dirrs and weighted average lives calculated for each simulation later.
    dirrs = []
    als = []
    # Create a dirrs_by_tranche and als_by_tranche list to store lists of calculated dirrs and weighted average lives
    # for each tranche in the input struct_sec.
    dirrs_by_tranche = [[] for tranche in struct_sec._tranches]
    als_by_tranche = [[] for tranche in struct_sec._tranches]

    # For loop which will call the mc_do_waterfall function nsim times, resetting the loan_pool and struct_sec objects
    # prior to each call, and store resulting dirrs and weighted average lives in the metrics list.
    for sim in range(nsim):
        # Reset loan_pool and struct_sec before calling do_waterfall.
        loan_pool.reset()
        struct_sec.reset()

        # Call do_waterfall with loan_pool and struct_sec as inputs. Store the resulting dirrs and weighted average
        # lives calculated into the metrics list.
        wtrfl_res = mc_do_waterfall(loan_pool, struct_sec)

        # Store the resulting dirrs and weighted average lives of the mc_do_waterfall output in the dirrs and als lists
        # respectively.
        dirrs.append(wtrfl_res[3])
        als.append(wtrfl_res[4])

    # Loop through each tranche in the struct_sec object.
    for i in range(len(struct_sec.tranches)):
        # Add the absolute values of each dirr calculated for the current tranche to the dirrs_by_tranche list.
        dirrs_by_tranche[i] = [abs(d[i]) for d in dirrs]
        # Add each average life calculated for the current tranche to the als_by_tranche list.
        als_by_tranche[i] = [a[i] for a in als]

    # Return the dirrs_by_tranche and als_by_tranche lists.
    return dirrs_by_tranche, als_by_tranche

# parallel_simulate_waterfall function, calls the above mc_simulate_waterfall function nsim number of times across
# numProcesses number of processes for an input loan pool and structured security object. Each mc_simulate_waterfall
# output tranche dirr and weighted average life is stored. The average of all the stored dirr and weighted average lives
# calculated for each tranche is then determined and output.
def parallel_simulate_waterfall(loan_pool, struct_sec, nsim, numProcesses):
    # Create a dirrs_by_tranche and als_by_tranche list to store lists of calculated dirrs and weighted average lives
    # for each tranche in the input struct_sec.
    dirrs_by_tranche = [[] for tranche in struct_sec._tranches]
    als_by_tranche = [[] for tranche in struct_sec._tranches]

    # Determine the number of simulations to have each process perform.
    nsim_per_process = int(round(nsim/numProcesses, 0))

    # Start numProcesses worker processes.
    with mp.Pool(processes=numProcesses) as pl:
        # Call mc_simulate_waterfall numProcesses number of times and run them asyncronously using the numProcesses
        # worker processes. Store the results as a list in the sim_wtrfls_outputs variable.
        sim_wtrfls_outputs = [pl.apply_async(mc_simulate_waterfall,
                                            (loan_pool, struct_sec, nsim_per_process)) for i in range(numProcesses)]

        # Loop through all the entries in the sim_wtrfls_outputs list generated above.
        for res in sim_wtrfls_outputs:
            # Loop through each entry in the res list. As these res entries are outputs from the mc_simulate_waterfall
            # function, they should have a length equal to the number of tranches in the struct_sec object input.
            for i in range(len(struct_sec.tranches)):
                # Take the dirrs and weighted average lives stored in res for the tranche specified by i and store them
                # in the entries corresponding to said tranche in the dirrs_by_tranche and als_by_tranche lists.
                # respectively
                r = res.get()
                dirrs_by_tranche[i].extend(r[0][i])
                als_by_tranche[i].extend(r[1][i])

        # Take the averages of each entry in the dirrs_by_tranche and als_by_tranche lists, storing the result in the
        # dirr_al_avgs list.
        dirr_al_avgs = [(numpy.average(d), numpy.average(a)) for d, a in zip(dirrs_by_tranche, als_by_tranche)]

        # Output dirr_al_avgs
        return dirr_al_avgs

# Calculate yield using a static method that takes in the dirr and weighted average life of a tranche.
def calculate_yield(dirr, wal):
    # Cast inputs to float in order to avoid truncation.
    dirr = float(dirr)
    wal = float(wal)
    return ((7.0/(1.0 + (.08 * numpy.exp(-0.19*(wal/12.0))))) + (0.019 * numpy.sqrt((wal/12.0)*(dirr*100.0)))) / 100.0

# run_monte function which determines fair interest rates for the tranches of the input structured security struct_sec.
# To do so, it calls the simulate_waterfall function to calculate the average dirr and weighted average life of each
# tranche in struct_sec and determining implied yields and tranche rates from these average dirrs and weighted average
# lives. This process is repeated until consecutive runs rates are within a specified tolerance of each other.
def run_monte(loan_pool, struct_sec, tolerance, nsim):
    # Check if the inputs for loan_pool and struct_sec are LoanPool and StructuredSecurities objects respectively.
    if isinstance(loan_pool, LoanPool) and isinstance(struct_sec, StructuredSecurities):
        # Store coefficients which will be needed to determine new tranche rates later on.
        coeff = [1.2, 0.8]
        # Initialize variables to store yields, old tranche rates, new tranche rates, the difference between old and new
        # tranche rates, and the final function output respectively.
        yield_res = [0.0, 0.0]
        old_rates = [0.0, 0.0]
        new_rates = [0.0, 0.0]
        diff_coeff = [0.0, 0.0]
        final_dirr_al_yields = [[0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0]]

        # Begin an infinite loop.
        while True:
            # Call simulate_waterfall for the input loan_pool, struct_sec, and nsim. Store results in the metrics
            # variable.
            metrics = simulate_waterfall(loan_pool, struct_sec, nsim)

            # Zip each tranche in the struct_sec with its corresponding average dirr abd weighted average life in the
            # metrics list, then loop through the resulting iterable.
            for num, tranche, metric in zip(range(len(struct_sec._tranches)), struct_sec._tranches, metrics):
                # Call the calculate_yield method with the average dirr and weighted average life for the current
                # tranche as input. Store the output implied yield in the yield_res list.
                yield_res[num] = calculate_yield(metric[0], metric[1])

                # Annualize the current rate of the current tranche and save it in the old_rates list.
                old_rates[num] = tranche._rate*12.0

                # Determine a new rate for the tranche using the tranche's current rate and the implied yield calculated
                # earlier.
                new_rates[num] = old_rates[num] + (coeff[num] * (yield_res[num] - old_rates[num]))

                # Calculate this tranche's portion of the tolerance check to be performed later on by multiplying the
                # tranche's notional by the percent change in tranche rates between the current rate and the new rate.
                diff_coeff[num] = tranche._notional * numpy.abs((old_rates[num] - new_rates[num]) / old_rates[num])

                # Store the current tranche's average dirr, credit rating, weighted average life, implied yield, and new
                # rate in the final_dirr_al_yields list
                final_dirr_al_yields[num] = [metric[0], Tranche.abs_rater(metric[0]), metric[1], yield_res[num], new_rates[num]]

            # Check if the difference between current and new tranche rates is below the input tolerance.
            if ((diff_coeff[0] + diff_coeff[1]) / struct_sec._tot_not) < tolerance:
                # If the difference is below tolerance, return the final_dirr_al_yields list.
                return final_dirr_al_yields

            # If the difference is above the input tolerance, prepare for the next iteration of the infinite loop.
            else:
                # Reset the input loan_pool.
                loan_pool.reset()
                # Re-initialize struct_sec as well as its tranches with the same terms, except for the tranche rates
                # which are set to the new tranche rates just calculated above.
                struct_sec = StructuredSecurities(loan_pool.total_principal()*.8)
                struct_sec.add_tranche('StandardTranche', 0.7, new_rates[0]/12, 'A')
                struct_sec.add_tranche('StandardTranche', 0.3, new_rates[1]/12, 'B')

    # If the input loan_pool is not of the LoanPool class, then a TypeError is raised telling users the loan_pool input
    # for do_waterfall must be of type LoanPool.
    elif not isinstance(loan_pool, LoanPool):
        raise TypeError('loan_pool input for do_waterfall() must be a LoanPool object. Your input {input} is of type '
                        '{input_type}, not LoanPool.'.format(input=loan_pool, input_type=type(loan_pool)))

    # If the input struct_sec is not of the StructuredSecurities class, then a TypeError is raised telling users the
    # struct_sec input for do_waterfall must be of type StructuredSecurities.
    else:
        raise TypeError('struct_sec input for do_waterfall() must be a StructuredSecurities object. Your input {input} '
                        'is of type {input_type}, not LoanPool.'.format(input=struct_sec, input_type=type(struct_sec)))

# parallel_run_monte function which determines fair interest rates for the tranches of the input structured security
# struct_sec. To do so, it calls the parallel_simulate_waterfall function to calculate the average dirr and weighted
# average life of each tranche in struct_sec and determining implied yields and tranche rates from these average dirrs
# and weighted average lives. This process is repeated until consecutive runs rates are within a specified tolerance of
# each other.
def parallel_run_monte(loan_pool, struct_sec, tolerance, nsim, numProcesses):
    # Check if the inputs for loan_pool and struct_sec are LoanPool and StructuredSecurities objects respectively.
    if isinstance(loan_pool, LoanPool) and isinstance(struct_sec, StructuredSecurities):
        # Store coefficients which will be needed to determine new tranche rates later on.
        coeff = [1.2, 0.8]
        # Initialize variables to store yields, old tranche rates, new tranche rates, the difference between old and new
        # tranche rates, and the final function output respectively.
        yield_res = [0.0, 0.0]
        old_rates = [0.0, 0.0]
        new_rates = [0.0, 0.0]
        diff_coeff = [0.0, 0.0]
        final_dirr_al_yields = [[0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0]]

        # Begin an infinite loop.
        while True:
            # Call parallel_simulate_waterfall for the input loan_pool, struct_sec, and nsim. Store results in the
            # metrics variable.
            metrics = parallel_simulate_waterfall(loan_pool, struct_sec, nsim, numProcesses)

            # Zip each tranche in the struct_sec with its corresponding average dirr abd weighted average life in the
            # metrics list, then loop through the resulting iterable.
            for num, tranche, metric in zip(range(len(struct_sec._tranches)), struct_sec._tranches, metrics):
                # Call the calculate_yield method with the average dirr and weighted average life for the current
                # tranche as input. Store the output implied yield in the yield_res list.
                yield_res[num] = calculate_yield(metric[0], metric[1])

                # Annualize the current rate of the current tranche and save it in the old_rates list.
                old_rates[num] = tranche._rate*12.0

                # Determine a new rate for the tranche using the tranche's current rate and the implied yield calculated
                # earlier.
                new_rates[num] = old_rates[num] + (coeff[num] * (yield_res[num] - old_rates[num]))

                # Calculate this tranche's portion of the tolerance check to be performed later on by multiplying the
                # tranche's notional by the percent change in tranche rates between the current rate and the new rate.
                diff_coeff[num] = tranche._notional * numpy.abs((old_rates[num] - new_rates[num]) / old_rates[num])

                # Store the current tranche's average dirr, credit rating, weighted average life, implied yield, and new
                # rate in the final_dirr_al_yields list
                final_dirr_al_yields[num] = [metric[0], Tranche.abs_rater(metric[0]), metric[1], yield_res[num], new_rates[num]]

            # Check if the difference between current and new tranche rates is below the input tolerance.
            if ((diff_coeff[0] + diff_coeff[1]) / struct_sec._tot_not) < tolerance:
                # If the difference is below tolerance, return the final_dirr_al_yields list.
                return final_dirr_al_yields

            # If the difference is above the input tolerance, prepare for the next iteration of the infinite loop.
            else:
                # Reset the input loan_pool.
                loan_pool.reset()
                # Re-initialize struct_sec as well as its tranches with the same terms, except for the tranche rates
                # which are set to the new tranche rates just calculated above.
                struct_sec = StructuredSecurities(loan_pool.total_principal()*.8)
                struct_sec.add_tranche('StandardTranche', 0.7, new_rates[0]/12, 'A')
                struct_sec.add_tranche('StandardTranche', 0.3, new_rates[1]/12, 'B')

    # If the input loan_pool is not of the LoanPool class, then a TypeError is raised telling users the loan_pool input
    # for do_waterfall must be of type LoanPool.
    elif not isinstance(loan_pool, LoanPool):
        raise TypeError('loan_pool input for do_waterfall() must be a LoanPool object. Your input {input} is of type '
                        '{input_type}, not LoanPool.'.format(input=loan_pool, input_type=type(loan_pool)))

    # If the input struct_sec is not of the StructuredSecurities class, then a TypeError is raised telling users the
    # struct_sec input for do_waterfall must be of type StructuredSecurities.
    else:
        raise TypeError('struct_sec input for do_waterfall() must be a StructuredSecurities object. Your input {input} '
                        'is of type {input_type}, not LoanPool.'.format(input=struct_sec, input_type=type(struct_sec)))