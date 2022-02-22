# 
# diseaseSim.py - simulates the spread of disease through a population
#
# Student Name   : Mitchell Spencer 
# Student Number : 19034205
#
# Version history:
#
# 25/4/19 - beta version released for FOP assignment
#

import numpy as np
import matplotlib.pyplot as plt
import random
import sys

# tuple fixer
def replace(tup, x, y):
    tup_list = list(tup)
    for element in tup_list:
        if element == x:
            tup_list[tup_list.index(element)] = y
    new_tuple = tuple(tup_list)
    return new_tuple

# distributes infected and non-infected peeps on the grid taking into account the boundaries.
def distribute(grid, num_r, num_c, numpeep, barriers):
    for n in range(numpeep):
        rpos = random.randint(0, num_r-1)
        cpos = random.randint(0, num_c-1)
        while (barriers[rpos,cpos] == 1):
            rpos = random.randint(0,num_r-1)
            cpos = random.randint(0,num_c-1)
        grid[rpos,cpos]+=1
    return grid

# distributes default barriers
def barrierdis(grid, num_r, num_c):
    for i in range(num_r):
        for j in range(num_c):
            if i == 0 or i == num_r-1:
                grid[i,j] = 1
            elif j == 0 or j == num_c-1:
                grid[i,j] = 1
    return grid

# distributes CSV barriers
def barriercsv():
    barlist = []
    fileobj = open('barriers.csv', 'r')
    for line in fileobj:
        line_s = line.strip()
        ints = [int(x) for x in line_s.split(',')]
        barlist.append(ints)
    fileobj.close()
    barriercsv = np.array(barlist, dtype=int)
    rows = barriercsv.shape[0]
    cols = barriercsv.shape[1]
    return barriercsv, rows, cols

# makes scatter
def makeScatter(grid, num_r, num_c):
    r_values = []
    c_values = []
    count_values = []
    for row in range(num_r):
        for col in range(num_c):
            if grid[row,col] > 0:
                r_values.append(row)
                c_values.append(col)
                count_values.append(grid[row,col]*100)
#                print("Value at (", row, ",", col, ") is ", grid[row, col])
    return(r_values, c_values, count_values)

# plots grid
def plotGrids():
    plt.figure(figsize=(9,7))
    Irows, Icols, Icount = makeScatter(infected, NUM_ROWS, NUM_COLS)
    plt.scatter(Icols, Irows, s=Icount, c="r", alpha=0.5)
    Urows, Ucols, Ucount = makeScatter(uninfected, NUM_ROWS, NUM_COLS)
    plt.scatter(Ucols, Urows, s=Ucount, c="b", alpha=0.5)
    Urows, Ucols, Ucount = makeScatter(immune, NUM_ROWS, NUM_COLS)
    plt.scatter(Ucols, Urows, s=Ucount, c='g', alpha=0.5)
    Brows, Bcols, Bcount = makeScatter(barriers, NUM_ROWS, NUM_COLS)
    plt.scatter(Bcols, Brows, s=Bcount, c = 'k', marker = 's', alpha=0.5)
    plt.show()

# This randomises whether a peep can move 1 to the left, right, up or down or diagonoally 
#and if a peep is in the corner, it can move any way still.
def movePeeps(cur, next, r, c, barriers):
    
    if neighin == 'M': #defines movement for moore cells (N,S,E,W,NE,SE,SW,NW)
        for peep in range(cur[r,c]):
            rMove = random.randint(-1,1)
            cMove = random.randint(-1,1)
            if barriers[r+rMove, c+cMove] == 1:
                rMove = 0
                cMove = 0
            next[r + rMove, c + cMove] += 1
            
    if neighin == 'V': #defines movement for von neumann cells (only N,S,E,W)
        for peep in range(cur[r,c]):
            rMove = random.randint(-1,1)
            cMove = random.randint(-1,1)
            dirDecider = random.randint(0,1) #determines whether to move vertically or horizontally
            if dirDecider == 0: #determines direction of Von Neumann moves
                rMove = 0
            elif dirDecider == 1:
                cMove = 0
            if barriers[r+rMove, c+cMove] == 1:
                rMove = 0
                cMove = 0
            next[r+rMove, c+cMove] += 1

# defines if a peep becomes infected
def infect(inf, notinf, r, c, prob):
    i_total = 0
    prob = prob*inf[r,c]
    if prob:
        for peep in range(notinf[r,c]):
            if random.random() < prob:
                inf[r, c] +=1
                notinf[r, c] -=1
                print("***** New infection (", r, ",", c, ")")
                i_total +=1
    return i_total

# defines if a peep recovers
def recover(inf, notinf, r, c, prob):
    r_total = 0
    if random.random() < prob:
        for peep in range(inf[r,c]):
            notinf[r,c] +=1
            inf[r,c] -=1
            print("***** New recovery (", r, ",", c, ")")
            r_total +=1
    return r_total

# defines if a peep dies
def die(inf, notinf, r, c, prob):
    d_total = 0
    if random.random() < prob:
        for peep in range(inf[r,c]):
            inf[r,c] -=1
            print("***** New death (", r, ",", c, ")")
            d_total +=1
    return d_total

# makes sure parameter input is an int
def inputchecker(msg):
    while True:
        inp = input(msg)
        try:
            val = int(inp)
            if (val >= 0):
                break
            else:
                return inputchecker("Please make sure the number is more than (or equal to) zero: ")
        except ValueError as e:
            return inputchecker("That is not a number.\nPlease try again: ")
    return val

# makes sure probability input is a float between 0 and 1
def probchecker(msg):
    while True:
        inp = input(msg)
        try:
            val = float(inp)
            if (val > 0 and val <= 1):
                break
            else:
                return probchecker("Please make sure the number is a decimal (between 0 and 1): ")
        except ValueError as e:
            return probchecker("That is not a probability.\nPlease try again: ")
    return val

# Function for printing stats
def statsprint(tuppleparam,num):
    if (tuppleparam[14] == 1): #Before simulation starts
        print('\n\n##### Parameter Input Complete #####')
        print('[1] Total Population: ', tuppleparam[0])
        print('[2] Starting Infected: ', tuppleparam[1])
        print('[3] Starting Uninfected: ', tuppleparam[2])
        print('[4] Starting Immune: ', tuppleparam[3])
        print('[5] Grid Size: ', tuppleparam[5]-2, ' x ', tuppleparam[4]-2)
        print('[6] Probability of Infection: ', tuppleparam[7])
        print('[7] Probability of Recovery: ', tuppleparam[8])
        print('[8] Probability of Death: ', tuppleparam[9])
        print('[9] Number of Timesteps: ', tuppleparam[6])
        print('[10] Printing timesteps on screen?: ', tuppleparam[13])
        print('\nWhat would you like to do?')
        YN = input('[S]tart, [C]hange parameters or [Q]uit: ').upper()
        return YN
    elif (tuppleparam[14] == 2): #After simulation ends
        print("Total Starting population: ", tuppleparam[0])
        print("Starting infected population: ", tuppleparam[1])
        print("Starting uninfected population: ", tuppleparam[2])
        print("Starting immune population: ", tuppleparam[3])
        print("Probability of infection: ", tuppleparam[7])
        print("Probability of recovery: ", tuppleparam[8])
        print("Probability of death: ", tuppleparam[9])
        print("Total number of new infections that occurred: ", tuppleparam[10])
        print("Total number of recoveries that occurred: ", tuppleparam[11])
        print("Total number of deaths that occurred: ", tuppleparam[12])
        print("Total infected peeps remaining: ", tuppleparam[15].sum())
        print("Total uninfected (includes immune) peeps remaining: ", tuppleparam[16].sum() 
                + tuppleparam[3])
        print("Grand total of remaining peeps: ", 
                tuppleparam[2] + tuppleparam[1] + tuppleparam[3] - tuppleparam[12])
        if num == 1:
            print("\n\nWould you like a copy of the results?")
            YN = input('[Y]es or [N]o: ').upper()
            while (YN != 'Y' and YN != 'N'):
                YN = input('Please try again. [Y]es or [N]o?: ').upper()
        elif num == 2:
            return
        return YN

# what to do for letter choice
def selection(choice):
    while True:
        print(choice)
        if (choice == 'S'):
            break
        elif (choice == 'C'):
            break
        elif (choice == 'Q'):
            sys.exit()
        else:
            choice = input("Please make a selection...\n[S]tart, [C]hange or [Q]uit ").upper()
    return choice

def output(tuppleparam, name):
    fileout = open('summary_of_results.txt', 'a')
    #"Results from diseaseSim.py"
    fileout.write("##### Results for " + name + " #####" +
            "\nTotal starting population: " + str(tuppleparam[0]) + 
            "\nStarting infected population: " + str(tuppleparam[1]) + 
            "\nStarting uninfected population: " + str(tuppleparam[2]) +
            "\nStarting immune population: " + str(tuppleparam[3]) +
            "\nSize of grid (excluding barriers): " + str(tuppleparam[4]-2) + 
            " x " + str(tuppleparam[5]-2) +
            "\nNumber of timesteps: " + str(tuppleparam[6]) +
            "\nProbability of infection: " + str(tuppleparam[7]) +
            "\nProbability of decovery: " + str(tuppleparam[8]) +
            "\nProbability of death: " + str(tuppleparam[9]) +
            "\nTotal number of infects that occurred: " + str(tuppleparam[10]) +
            "\nTotal number of recoveries that occurred: " + str(tuppleparam[11]) +
            "\nTotal number of deaths that occurred: " + str(tuppleparam[12]) +
            "\nTotal infected people remaining: " + str(tuppleparam[15].sum()) +
            "\nTotal uninfected (or immune) peeps remaining: " + str(tuppleparam[16].sum() 
            + tuppleparam[3]) +
            "\nGrand total of remaining people: " + str(tuppleparam[2] + tuppleparam[1] 
            + tuppleparam[3] - tuppleparam[12]) + "\n\n")
    fileout.close()

# Prints further statistics to a text file
def summary():
    datalist = []
    with open('summary_of_results.txt', 'r') as results:
        for line in results.readlines():
            ints = [int(x) for x in line.split() if x.isdigit()]
            datalist.append(ints)
        results.close()
        TOTALINFECTS = datalist[10::17]
        TOTALRECOVERIES = datalist[11::17]
        TOTALDEATHS = datalist[12::17]
        TOTALINFECTED = datalist[13::17]
        TOTALUNINFECTED = datalist[14::17]
        TOTAL_LEFT = datalist[15::17]
 
    STATS = open('greater_statistics.txt', 'w')
    STATS.write("##### Greater Statistics #####" + 
                "\n Most Infections: " + str(max(TOTALINFECTS)) +
                "\n Most Recoveries: " + str(max(TOTALINFECTS)) +
                "\n Most Deaths: " + str(max(TOTALDEATHS)) +
                "\n Most Left Infected: " + str(max(TOTALINFECTED)) +
                "\n Most Left Uninfected: " + str(max(TOTALUNINFECTED)) +
                "\n Most Left Alive: " + str(max(TOTAL_LEFT)) +
                "\n Lowest Infections: " + str(min(TOTALINFECTS)) +
                "\n Lowest Recoveries: " + str(min(TOTALRECOVERIES)) +
                "\n Lowest Deaths: " + str(min(TOTALDEATHS)) +
                "\n Least Left Infected: " + str(min(TOTALINFECTED)) +
                "\n Least Left Uninfected: " + str(min(TOTALUNINFECTED)) +
                "\n Least Left Alive: " + str(min(TOTAL_LEFT)) +
                "\n Average Infections: [" + str(np.mean(np.array(TOTALINFECTS))) + "]" +
                "\n Average Recoveries: [" + str(np.mean(np.array(TOTALRECOVERIES))) + "]" +
                "\n Average Deaths: [" + str(np.mean(np.array(TOTALDEATHS))) + "]" +
                "\n Average Left Infected: [" + str(np.mean(np.array(TOTALINFECTED))) + "]" +
                "\n Average Left Uninfected: [" + str(np.mean(np.array(TOTALUNINFECTED))) + "]" +
                "\n Average Total Left Alive: [" + str(np.mean(np.array(TOTAL_LEFT))) + "]")

# When processing command line arguments for parameter sweep:
def paramsweep():
    sh_neighbourhood = str(sys.argv[1])
    sh_pop = int(sys.argv[2])
    sh_infect = int(sys.argv[3])
    sh_immune = int(sys.argv[4])
    sh_steps = int(sys.argv[5])
    sh_infprob = float(sys.argv[6])
    sh_recovprob = float(sys.argv[7])
    sh_deathprob = float(sys.argv[8])
    sh_list = [sh_neighbourhood, sh_pop, sh_infect, sh_immune, sh_steps, 
            sh_infprob, sh_recovprob, sh_deathprob]
    return (sh_list)



### START OF PROGRAM CODE ###


bypass = 0
if (len(sys.argv) == 10): #includes the counter argument
    paramtest = paramsweep()
    bypass = 1
elif (len(sys.argv) == 1):
    print("Running default simulation...")
else:
    print("Invalid system arguments. Running default simulation...")

### Defining Parameters ###

# Tallies for end statistics:
total_infects = 0
total_recovers = 0
total_deaths = 0

if bypass != 1:
    # IF NOT USING BASH SCRIPT:
    # Neighbourhood Selection Code (Moore='M' and Von Neumann='V')
    print('\n##### Enter Parameters #####\n')
    neighin = input('Please select a Neighbourhood type:'\
            '\n[M]oore or [V]on Neumann: ').upper()
    while(neighin != 'M' and neighin != 'V'):
        neighin = input("Sorry, please try again: \n[M]oore or [V]on Neumann?").upper()
    if neighin == 'M':
        print("You have selected [" + (neighin) + "]oore Neighbourhoods")
    else: 
        print("You have selected [" + (neighin) + "]on Neumann Neughbourhoods")

    # Total number of people
    totalpop = inputchecker('\nPlease type in how many people you would like in the simulation: ')
    # Total number of infected people
    INIT_INFECTED = inputchecker('Of those people, how many would you like to be infected?: ')
    # Total number of people who are immune
    INIT_IMMUNE = inputchecker('How many people are immune?: ')
    # Total number of people who are uninfected
    INIT_POP= totalpop-INIT_INFECTED-INIT_IMMUNE

    # Determines barriers and time:
    print('\nNow we need to generate barriers for the world.')
    print('Do you want to use the default grid or the csv file?')
    barrier_choice = input('[D]efault or [C]SV: ').upper()
    while (barrier_choice != 'C' and barrier_choice != 'D'):
        barrier_choice = input('Please try again.\n[D]efault or [C]SV: ').upper()
    if (barrier_choice == 'C'):
        barrier_data = barriercsv()
        CSV_BARRIERS = barrier_data[0]
        NUM_ROWS = barrier_data[1]
        NUM_COLS = barrier_data[2]
    elif (barrier_choice == 'D'):
         print('\nPlease enter the size of the world for the people to move around in...')
         #preset is 10
         NUM_COLS = inputchecker('Just enter the number of columns first ("x" axis): ') + 2 
         #preset is 15
         NUM_ROWS = inputchecker('and now please enter the number of rows ("y axis"): ') + 2 

    NUM_STEPS = inputchecker('\nHow many "timesteps" do you want the ' 
                             'simulation to run for?: ') #preset is 10 (must be > 0)
    print('Do you want to print each "timestep" on the screen?: ')#preset is yes
    printscreen = input('[Y]es or [N]o: ').upper()
    while (printscreen != 'Y' and printscreen != 'N'):
        printscreen = input('Please try again. [Y]es or [N]o: ')

    # Determines probabilities:
    PROB_INFECTION = probchecker('\nWhat is the probability for infection?: ') #preset is 0.5 
    PROB_RECOVERY = probchecker('What is the probability for recovery (once infected)?: ') 
    #preset is 0.1
    PROB_DEATH = probchecker('What is the probability of death (once infected)?: ') #preset is 0.1 

    # Confirmation Screen:
    listparam = (totalpop, INIT_INFECTED, INIT_POP, INIT_IMMUNE,
                    NUM_COLS, NUM_ROWS, NUM_STEPS, PROB_INFECTION, PROB_RECOVERY, 
                    PROB_DEATH, total_infects, total_recovers, total_deaths, printscreen, 1)

    answer = statsprint(listparam,1)

    # Confirmation screen selection:
    change = selection(answer)
    if (change == 'C'):
        print("What input/s would you like to change?")
        p_change = input("Please select a parameter from the list above: ")
        print(p_change)
        if p_change == '1':
            input_change = inputchecker("\nNew total population: ")
            totalpop = input_change
            listparam = replace(listparam, listparam[0], input_change)
            answer = statsprint(listparam)
        elif p_change == '2':
            input_change = inputchecker("\nNew starting infected: ")
            INIT_INFECTED = input_change
            listparam = replace(listparam, listparam[1], input_change)
            answer = statsprint(listparam)
        elif p_change == '3':
            print("""\nIf you want to change the people uninfected you need to 
                    increase total population.""")
            answer = statsprint(listparam)
        elif p_change == '4':
            input_change = inputchecker("\nNew starting immune: ")
            INIT_IMMUNE = input_change
            listparam = replace(listparam, listparam[3], input_change)
            answer = statsprint(listparam)
        elif p_change == '5':
            if barrier_choice == 'C':
                print("\nPlease make your changes in the CSV file")
            else:
                input_change = inputchecker(("""\nEnter the new number of columns first 
                        ("x" axis): """) + 2)
                NUM_COLS = input_change
                listparam = replace(listparam, listparam[5], input_change)
                input_change = inputchecker(("""and now enter the new number of rows 
                        ("y axis"): """) + 2)
                NUM_ROWS = input_change
                listparam = replace(listparam, listparam[4], input_change)
            answer = statsprint(listparam)
        elif p_change == '6':
            input_change = inputchecker("\nNew probability of infection: ")
            PROB_INFECTION = input_change
            listparam = replace(listparam, listparam[7], input_change)
            answer = statsprint(listparam)
        elif p_change == '7':
            input_change = probchecker("\nNew probability of recovery: ")
            PROB_RECOVERY = input_change
            listparam = replace(listparam, listparam[8], input_change)
            answer = statsprint(listparam)
        elif p_change == '8':
            input_change = probchecker("\nNew probability of death: ")
            PROB_DEATH = input_change
            listparam = replace(listparam, listparam[9], input_change)
            answer = statsprint(listparam)
        elif p_change == '9':
            input_change = inputchecker("\nNew number of timesteps: ")
            NUM_STEPS = input_change
            listparam = replace(listparam, listparam[6], input_change)
            answer = statsprint(listparam)
        elif p_change == '10':
            input_change = input("\nDo you want to print timesteps on screen?: ").upper()
            printscreen = input_change
            while (printscreen != 'Y' and printscreen != 'N'):
                printscreen = input('Please try again. [Y]es or [N]o: ')
            listparam = replace(listparam, listparam[13], input_change)
            answer = statsprint(listparam)
        else:
            print("Please try again.")

    change = selection(answer)

else: #IF USING BASH SCRIPT:
    barrier_choice = 'C'
    barrier_data = barriercsv()
    CSV_BARRIERS = barrier_data[0]
    NUM_ROWS = barrier_data[1]
    NUM_COLS = barrier_data[2]
    neighin = paramtest[0]
    totalpop = paramtest[1]
    INIT_INFECTED = paramtest[2]
    INIT_IMMUNE = paramtest[3]
    NUM_STEPS = paramtest[4]
    PROB_INFECTION = paramtest[5]
    PROB_RECOVERY = paramtest[6]
    PROB_DEATH = paramtest[7]
    printscreen = 'N'
    INIT_POP = totalpop-INIT_INFECTED-INIT_IMMUNE

### PARAMETER ENTRY COMPLETE ###

# Creates world (array) for each peep's type
barriers = np.zeros((NUM_ROWS, NUM_COLS), dtype=np.int)
infected = np.zeros((NUM_ROWS, NUM_COLS), dtype=np.int)
uninfected = np.zeros((NUM_ROWS, NUM_COLS), dtype=np.int)
immune = np.zeros((NUM_ROWS, NUM_COLS), dtype=np.int)

# Applies barrier distribution to barrier array
if (barrier_choice == 'C'):
    barriers = CSV_BARRIERS
    barriers = barrierdis(barriers, NUM_ROWS, NUM_COLS)
else:
    barriers = barrierdis(barriers, NUM_ROWS, NUM_COLS)

# Distributes peeps and their types to their proper arrays
infected = distribute(infected, NUM_ROWS, NUM_COLS, INIT_INFECTED, barriers)
uninfected = distribute(uninfected, NUM_ROWS, NUM_COLS, INIT_POP, barriers)
immune = distribute(immune, NUM_ROWS, NUM_COLS, INIT_IMMUNE, barriers)

# Are we plotting grids on screen?
if (printscreen == 'Y'):
    plotGrids()

# Printing to console what is going on
for timestep in range(NUM_STEPS):
    print("\n###################### TIMESTEP", timestep, "#####################\n")
    infected2 = np.zeros((NUM_ROWS, NUM_COLS), dtype=np.int)
    uninfected2 = np.zeros((NUM_ROWS, NUM_COLS), dtype=np.int)
    immune2 = np.zeros((NUM_ROWS, NUM_COLS), dtype=np.int)
    for row in range(NUM_ROWS):
        for col in range(NUM_COLS):
            total_infects = infect(infected, uninfected, row, col, PROB_INFECTION) + total_infects
            total_recovers = recover(infected, uninfected, row, col, PROB_RECOVERY) + total_recovers
            total_deaths = die(infected, uninfected, row, col, PROB_DEATH) + total_deaths
            movePeeps(infected, infected2, row, col, barriers)
            movePeeps(uninfected, uninfected2, row, col, barriers)
            movePeeps(immune, immune2, row, col, barriers)
    infected = infected2
    uninfected = uninfected2
    immune = immune2
    if (printscreen == 'Y'):
        plotGrids()

# Simulation end screen
print("Simulation Complete")
print("\nStatistics:")
listparam = (totalpop, INIT_INFECTED, INIT_POP, INIT_IMMUNE, NUM_COLS, NUM_ROWS, NUM_STEPS, 
        PROB_INFECTION, PROB_RECOVERY, PROB_DEATH, total_infects, total_recovers, total_deaths, 
        printscreen, 2, infected, uninfected)
if bypass != 1:
    yn2 = statsprint(listparam,1)
    if yn2 == 'N':
        sys.exit()
    else:
        output(listparam, "Experiment")
else:
    bashcounter = int(sys.argv[9])
    bashstats = statsprint(listparam,2)
    filename = ("diseaseSim_Trial_" + str(bashcounter) + ".txt")
    output(listparam, filename)
    summary()
