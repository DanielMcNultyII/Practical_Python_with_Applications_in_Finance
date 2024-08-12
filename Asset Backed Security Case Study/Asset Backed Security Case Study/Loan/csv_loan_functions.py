'''
Daniel McNulty II

This file contains functionality for converting csv data into loans and loans into csv data.
'''


# Import the loan_base, loans, mortgage, and loan_pool modules from the Loan package
import Loan.loan_base as loan_base
import Loan.loans as loans
import Loan.mortgage as mortgage
# Import the asset_base, house, and car modules from the Assets package
import Loan.Assets.asset_base as asset_base
import Loan.Assets.house as house
import Loan.Assets.car as car


'''
loan_generator Function:
Generate a loan based on the specifications:
    loan_type - The type of loan
    loan_face - The face value of the loan
    loan_maturity - The maturity of the loan
    asset_type - The type of asset the loan is for
    asset_value - The value of the asset the loan is for
'''
def loan_generator(loan_num, loan_type, loan_face, loan_rate, loan_maturity, asset_type, asset_value):
    # if/elif/else statement that checks for which type of asset the user input and then creates an asset of the user's
    # specified type (Either Assets, Car, Civic, Lexus, Lamborghini, HouseBase, PrimaryHome, or VacationHome). If the
    # user does not input a recognized type, a ValueError is raised with an appropriate error message.
    if asset_type == 'Assets':
        asset = asset_base.Asset(float(asset_value))
    elif asset_type == 'Car':
        asset = car.Car(float(asset_value))
    elif asset_type == 'Civic':
        asset = car.Civic(float(asset_value))
    elif asset_type == 'Lexus':
        asset = car.Lexus(float(asset_value))
    elif asset_type == 'Lamborghini':
        asset = car.Lamborghini(float(asset_value))
    elif asset_type == 'HouseBase':
        asset = house.HouseBase(float(asset_value))
    elif asset_type == 'PrimaryHome':
        asset = house.PrimaryHome(float(asset_value))
    elif asset_type == 'VacationHome':
        asset = house.PrimaryHome(float(asset_value))
    else:
        raise ValueError('Your input for asset_type ({t}) is invalid. Input for asset_type in loan_generator() must be '
                         'one of the following:'
                         '\n\t\t\tAssets'
                         '\n\t\t\tCar, Civic, Lexus, Lamborghini'
                         '\n\t\t\tHouseBase, PrimaryHome, VacationHome'.format(t=asset_type))

    # if/elif/else statement that checks for which type of loan the user input and then creates an asset of the user's
    # specified type (Either Loan, FixedRateLoan, VariableRateLoan, AutoLoan, FixedMortgage, or VariableMortgage). If
    # the user does not input a recognized type, a ValueError is raised with an appropriate error message.
    if loan_type == 'Loan':
        loan = loan_base.Loan(int(loan_num), float(loan_face), float(loan_rate), float(loan_maturity), asset)
    elif loan_type == 'FixedRateLoan':
        loan = loans.FixedRateLoan(int(loan_num), float(loan_face), float(loan_rate), float(loan_maturity), asset)
    elif loan_type == 'VariableRateLoan':
        loan = loans.VariableRateLoan(int(loan_num), float(loan_face), loan_rate, float(loan_maturity), asset)
    elif loan_type == 'AutoLoan':
        loan = loans.AutoLoan(int(loan_num), float(loan_face), float(loan_rate), float(loan_maturity), asset)
    elif loan_type == 'FixedMortgage':
        loan = mortgage.FixedMortgage(int(loan_num), float(loan_face), float(loan_rate), float(loan_maturity), asset)
    elif loan_type == 'VariableMortgage':
        loan = mortgage.VariableMortgage(int(loan_num), float(loan_face), float(loan_rate), float(loan_maturity), asset)
    else:
        raise ValueError('Your input for loan_type ({t}) is invalid. Input for loan_type in loan_generator() must be '
                         'one of the following:'
                         '\n\t\t\tLoan, FixedRateLoan, VariableRateLoan'
                         '\n\t\t\tAutoLoan, FixedMortgage, VariableRateLoan'.format(t=loan_type))

    # Return the created loan.
    return loan


'''
csv_to_loans Function
Opens an input csv file path, reads the data within it line by line, and unpacks the data within each line to variables
that are then used as input parameters into the loan generator function declared and implemented above in order to 
generate Loan objects from them. Then places all of the generated loans into a list of loans called loan_list. CSV file
input was based on how the data was formatted in the given Loans Excel Worksheet when it was converted to a CSV file.
'''
def csv_to_loans(loan_csv_file):
    # Initialize an empty list called loan_list which will hold all the Loan objects generated from the information in
    # the input CSV file.
    loan_list = []
    # Use the wth statement to open the specified file using the file context manager and storing it in the
    # file handle variable open_file.
    with open(loan_csv_file, 'r') as open_file:
        # Skip the header line of the file
        next(open_file)

        # Loop through each line in the file
        for line in open_file:
            # Use strip() on the line in order to get rid of any possible blank space. Then, use split(',')
            # in order to segment the line at each instance of the ',' character in it and then unpack each
            # value stored in the line to the loan_type, loan_face, loan_rate, loan_maturity, asset_type,
            # and asset_type respectively. This is highly depended on the order in which the values are
            # written in the csv. If they do not follow the order of the variables in the below unpack, then
            # unexpected results can and probably will occur.
            loan_num, loan_type, loan_face, loan_rate, loan_maturity, asset_type, asset_value = line.strip().strip(',').split(',')

            # Remove any potential spaces in the string held within variable loan_type.
            loan_type = loan_type.replace(' ', '')

            # Use the variables for loan_type, loan_face, loan_rate, loan_maturity, asset_type, and
            # asset_value found in the above unpacking as input into the loan_generator function that is
            # implemented and declared above in order to generate loan objects for the values of each line
            # in the file.
            loan = loan_generator(loan_num, loan_type, loan_face, loan_rate, loan_maturity, asset_type, asset_value)

            # Append the newly-created loan object to the list input_loans
            loan_list.append(loan)

    # Return the generated loan_list
    return loan_list


'''
loans_to_csv Function.
Converts a list of loans to a CSV file. Output CSV file format is based on how the data was formatted in the given Loans
Excel Worksheet when it was converted to a CSV file.
'''
def loans_to_csv(loan_list):
    # Use a context manager to open the file "Recorded Loans.csv" and store it in file handle variable
    # recorded_loans.
    with open('Recorded Loans.csv', 'w') as recorded_loans:
        # Let the user know that the program is currently recording all the input loans into a text file
        # named "Recorded Loans.csv"
        print('\nCurrently recording loans to a text file named "Recorded Loans.csv"')

        # Write a header line to state what each column refers to
        recorded_loans.write('Loan Number,Loan Type,Loan Face Value,Loan Annual Rate,Loan Maturity,Assets Type,'
                             'Assets Initial Value\n')

        # Use a for loop to iterate through all the loans in the list of loans input_loans
        for loan in loan_list:
            # Get the current type of the loan by using type(loan), cast the return to a string, use
            # rsplit('.') to split apart the newly made list where there are '.'s, use the [2] notation on
            # the return of rsplit('.') to get the class name of the loan object, and finally use strip()
            # twice in order to remove the > and ' characters from the class name.
            current_loan_type = str(type(loan)).rsplit('.')[2].strip('>').strip("'")

            # Get the current type of the asset by using type(loan.asset), cast the return to a string, use
            # rsplit('.') to split apart the newly made list where there are '.'s, use the [3] notation on
            # the return of rsplit('.') to get the class name of the asset object, and finally use strip()
            # twice in order to remove the > and ' characters from the class name.
            current_asset_type = str(type(loan.asset)).rsplit('.')[3].strip('>').strip("'")

            # Use join with ',' as the joining character to join a list of string values for
            # current_loan_type (As found above), the loan's face value, loan.rate()*12 in order to store
            # the annual rate of the current loan, the loan's maturity, the current_asset_type (As found
            # above), and the asset's initial value. map() is used with the str function to convert all the
            # loan's variables to strings. A newline character '\n' is tacked onto the end of the written
            # string in order to have each loan occupy its own line.
            recorded_loans.write(','.join(map(str, [loan.loan_num, current_loan_type, loan.face, loan.rate() * 12, loan.term,
                                                    current_asset_type, loan.asset.init_val])) + '\n')

    # Let the user know their loans have been recorded in the csv file "Recorded Loans.csv"
    print('\nYour loans have been recorded in "Recorded Loans.csv"')
