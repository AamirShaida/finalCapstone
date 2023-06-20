import math
while True:
    print("""Investment - to calculate the amount of interest you'll earn on your investment
    Bond - to calculate the amount you'll have to pay on a home loan""")
    userinput = input("Enter either 'investment' or 'bond' from the menu above to proceed ").lower()
    #Program will receive input and split into multiple options depending on input
    #Part 1 for investment option
    if userinput == "investment":
        print ("You have chosen investment ")
        deposit = input("Please enter the amount of money you are depositing : £")
        interest_rate_percentage = input("Please enter the interest rate: ")
        months = input("Please enter the number of years you plan on investing: ")
        interest = input("Please enter if you want 'simple' or 'compound' interest: ").lower()
        #received all inputs for investment, will define variables for formula below

        interest_rate = int(interest_rate_percentage)/100
        deposit = int(deposit)
        months = int(months)
        
        if interest == "simple":
            totalamount = deposit*(1 + interest_rate*months)
            print ("Total amount will be £" + str(totalamount))
            break
        elif interest == "compund":
            totalamount = deposit * math.pow((1+interest_rate),months)
            print ("Total amount will be £" + str(totalamount))
            break
        else:
            print("There was an invalid input")
#completed for investment, so loop can be broken

    elif userinput == "bond":
        print("You have chosen bond")
        valueofhouse = input("Please enter the current value of the house ")
        interest_rate = input("Please enter the interest rate ")
        months = input("Please enter the number of months you will take to repay the bond ")

        #inputs for bond have been received, variables for formula will be defined again below
        deposit = int(valueofhouse)
        interest_rate = (int(interest_rate)/100)/12
        months = int(months)

        repayment = (interest_rate * deposit)/(1 - (1 + interest_rate)**(-months))
        print("You will have to pay " + str(repayment) + " each month")
        break
    else:
        print("Please enter either investment or bond") 