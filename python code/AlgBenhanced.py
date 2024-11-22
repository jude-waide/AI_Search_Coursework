############
############ ALTHOUGH I GIVE YOU THIS TEMPLATE PROGRAM WITH THE NAME 'skeleton.py', 
############ YOU CAN RENAME IT TO ANYTHING YOU LIKE. HOWEVER, FOR THE PURPOSES OF 
############ THE EXPLANATION IN THESE COMMENTS, I ASSUME THAT THIS PROGRAM IS STILL 
############ CALLED 'skeleton.py'.
############
############ IF YOU WISH TO IMPORT STANDARD MODULES, YOU CAN ADD THEM AFTER THOSE BELOW.
############ NOTE THAT YOU ARE NOT ALLOWED TO IMPORT ANY NON-STANDARD MODULES! TO SEE
############ THE STANDARD MODULES, TAKE A LOOK IN 'validate_before_handin.py'.
############
############ DO NOT INCLUDE ANY COMMENTS ON A LINE WHERE YOU IMPORT A MODULE.
############

import os
import sys
import time
import random
import math
from multiprocessing import Process, Queue

############ START OF SECTOR 0 (IGNORE THIS COMMENT)
############
############ NOW PLEASE SCROLL DOWN UNTIL THE NEXT BLOCK OF CAPITALIZED COMMENTS.
############
############ DO NOT TOUCH OR ALTER THE CODE IN BETWEEN! YOU HAVE BEEN WARNED!
############ BY 'DO NOT TOUCH' I REALLY MEAN THIS. EVEN CHANGING THE SYNTAX, BY
############ ADDING SPACES OR COMMENTS OR LINE RETURNS AND SO ON, COULD MEAN THAT
############ CODES MIGHT NOT RUN WHEN I RUN THEM!
############

def read_file_into_string(input_file, ord_range):
    the_file = open(input_file, 'r') 
    current_char = the_file.read(1) 
    file_string = ""
    length = len(ord_range)
    while current_char != "":
        i = 0
        while i < length:
            if ord(current_char) >= ord_range[i][0] and ord(current_char) <= ord_range[i][1]:
                file_string = file_string + current_char
                i = length
            else:
                i = i + 1
        current_char = the_file.read(1)
    the_file.close()
    return file_string

def remove_all_spaces(the_string):
    length = len(the_string)
    new_string = ""
    for i in range(length):
        if the_string[i] != " ":
            new_string = new_string + the_string[i]
    return new_string

def integerize(the_string):
    length = len(the_string)
    stripped_string = "0"
    for i in range(0, length):
        if ord(the_string[i]) >= 48 and ord(the_string[i]) <= 57:
            stripped_string = stripped_string + the_string[i]
    resulting_int = int(stripped_string)
    return resulting_int

def convert_to_list_of_int(the_string):
    list_of_integers = []
    location = 0
    finished = False
    while finished == False:
        found_comma = the_string.find(',', location)
        if found_comma == -1:
            finished = True
        else:
            list_of_integers.append(integerize(the_string[location:found_comma]))
            location = found_comma + 1
            if the_string[location:location + 5] == "NOTE=":
                finished = True
    return list_of_integers

def build_distance_matrix(num_cities, distances, city_format):
    dist_matrix = []
    i = 0
    if city_format == "full":
        for j in range(num_cities):
            row = []
            for k in range(0, num_cities):
                row.append(distances[i])
                i = i + 1
            dist_matrix.append(row)
    elif city_format == "upper_tri":
        for j in range(0, num_cities):
            row = []
            for k in range(j):
                row.append(0)
            for k in range(num_cities - j):
                row.append(distances[i])
                i = i + 1
            dist_matrix.append(row)
    else:
        for j in range(0, num_cities):
            row = []
            for k in range(j + 1):
                row.append(0)
            for k in range(0, num_cities - (j + 1)):
                row.append(distances[i])
                i = i + 1
            dist_matrix.append(row)
    if city_format == "upper_tri" or city_format == "strict_upper_tri":
        for i in range(0, num_cities):
            for j in range(0, num_cities):
                if i > j:
                    dist_matrix[i][j] = dist_matrix[j][i]
    return dist_matrix

def read_in_algorithm_codes_and_tariffs(alg_codes_file):
    flag = "good"
    code_dictionary = {}   
    tariff_dictionary = {}  
    if not os.path.exists(alg_codes_file):
        flag = "not_exist"  
        return code_dictionary, tariff_dictionary, flag
    ord_range = [[32, 126]]
    file_string = read_file_into_string(alg_codes_file, ord_range)  
    location = 0
    EOF = False
    list_of_items = []  
    while EOF == False: 
        found_comma = file_string.find(",", location)
        if found_comma == -1:
            EOF = True
            sandwich = file_string[location:]
        else:
            sandwich = file_string[location:found_comma]
            location = found_comma + 1
        list_of_items.append(sandwich)
    third_length = int(len(list_of_items)/3)
    for i in range(third_length):
        code_dictionary[list_of_items[3 * i]] = list_of_items[3 * i + 1]
        tariff_dictionary[list_of_items[3 * i]] = int(list_of_items[3 * i + 2])
    return code_dictionary, tariff_dictionary, flag

############
############ HAVE YOU TOUCHED ANYTHING ABOVE? BECAUSE EVEN CHANGING ONE CHARACTER OR
############ ADDING ONE SPACE OR LINE RETURN WILL MEAN THAT THE PROGRAM YOU HAND IN
############ MIGHT NOT RUN PROPERLY!
############
############ THE RESERVED VARIABLE 'input_file' IS THE CITY FILE UNDER CONSIDERATION.
############
############ IT CAN BE SUPPLIED BY SETTING THE VARIABLE BELOW OR VIA A COMMAND-LINE
############ EXECUTION OF THE FORM 'python skeleton.py city_file.txt'. WHEN SUPPLYING
############ THE CITY FILE VIA A COMMAND-LINE EXECUTION, ANY ASSIGNMENT OF THE VARIABLE
############ 'input_file' IN THE LINE BELOW iS SUPPRESSED.
############
############ IT IS ASSUMED THAT THIS PROGRAM 'skeleton.py' SITS IN A FOLDER THE NAME OF
############ WHICH IS YOUR USER-NAME, E.G., 'abcd12', WHICH IN TURN SITS IN ANOTHER
############ FOLDER. IN THIS OTHER FOLDER IS THE FOLDER 'city-files' AND NO MATTER HOW
############ THE NAME OF THE CITY FILE IS SUPPLIED TO THIS PROGRAM, IT IS ASSUMED THAT 
############ THE CITY FILE IS IN THE FOLDER 'city-files'.
############
############ END OF SECTOR 0 (IGNORE THIS COMMENT)

input_file = "AISearchfile058.txt"

############ START OF SECTOR 1 (IGNORE THIS COMMENT)
############
############ PLEASE SCROLL DOWN UNTIL THE NEXT BLOCK OF CAPITALIZED COMMENTS STARTING
############ 'HAVE YOU TOUCHED ...'
############
############ DO NOT TOUCH OR ALTER THE CODE IN BETWEEN! YOU HAVE BEEN WARNED!
############

if len(sys.argv) > 1:
    input_file = sys.argv[1]

############ END OF SECTOR 1 (IGNORE THIS COMMENT)

############ START OF SECTOR 2 (IGNORE THIS COMMENT)
path_for_city_files = os.path.join("..", "city-files")
############ END OF SECTOR 2 (IGNORE THIS COMMENT)

############ START OF SECTOR 3 (IGNORE THIS COMMENT)
path_to_input_file = os.path.join(path_for_city_files, input_file)
if os.path.isfile(path_to_input_file):
    ord_range = [[32, 126]]
    file_string = read_file_into_string(path_to_input_file, ord_range)
    file_string = remove_all_spaces(file_string)
    print("I have found and read the input file " + input_file + ":")
else:
    print("*** error: The city file " + input_file + " does not exist in the city-file folder.")
    sys.exit()

location = file_string.find("SIZE=")
if location == -1:
    print("*** error: The city file " + input_file + " is incorrectly formatted.")
    sys.exit()
    
comma = file_string.find(",", location)
if comma == -1:
    print("*** error: The city file " + input_file + " is incorrectly formatted.")
    sys.exit()
    
num_cities_as_string = file_string[location + 5:comma]
num_cities = integerize(num_cities_as_string)
print("   the number of cities is stored in 'num_cities' and is " + str(num_cities))

comma = comma + 1
stripped_file_string = file_string[comma:]
distances = convert_to_list_of_int(stripped_file_string)

counted_distances = len(distances)
if counted_distances == num_cities * num_cities:
    city_format = "full"
elif counted_distances == (num_cities * (num_cities + 1))/2:
    city_format = "upper_tri"
elif counted_distances == (num_cities * (num_cities - 1))/2:
    city_format = "strict_upper_tri"
else:
    print("*** error: The city file " + input_file + " is incorrectly formatted.")
    sys.exit()

dist_matrix = build_distance_matrix(num_cities, distances, city_format)
print("   the distance matrix 'dist_matrix' has been built.")

############
############ HAVE YOU TOUCHED ANYTHING ABOVE? BECAUSE EVEN CHANGING ONE CHARACTER OR
############ ADDING ONE SPACE OR LINE RETURN WILL MEAN THAT THE PROGRAM YOU HAND IN
############ MIGHT NOT RUN PROPERLY!
############
############ YOU NOW HAVE THE NUMBER OF CITIES STORED IN THE INTEGER VARIABLE 'num_cities'
############ AND THE TWO_DIMENSIONAL MATRIX 'dist_matrix' HOLDS THE INTEGER CITY-TO-CITY 
############ DISTANCES SO THAT 'dist_matrix[i][j]' IS THE DISTANCE FROM CITY 'i' TO CITY 'j'.
############ BOTH 'num_cities' AND 'dist_matrix' ARE RESERVED VARIABLES AND SHOULD FEED
############ INTO YOUR IMPLEMENTATIONS.
############
############ THERE NOW FOLLOWS CODE THAT READS THE ALGORITHM CODES AND TARIFFS FROM
############ THE TEXT-FILE 'alg_codes_and_tariffs.txt' INTO THE RESERVED DICTIONARIES
############ 'code_dictionary' AND 'tariff_dictionary'. DO NOT AMEND THIS CODE!
############ THE TEXT FILE 'alg_codes_and_tariffs.txt' SHOULD BE IN THE SAME FOLDER AS
############ THE FOLDER 'city-files' AND THE FOLDER WHOSE NAME IS YOUR USER-NAME.
############
############ PLEASE SCROLL DOWN UNTIL THE NEXT BLOCK OF CAPITALIZED COMMENTS STARTING
############ 'HAVE YOU TOUCHED ...'
############
############ DO NOT TOUCH OR ALTER THE CODE IN BETWEEN! YOU HAVE BEEN WARNED!
############
############ END OF SECTOR 3 (IGNORE THIS COMMENT)

############ START OF SECTOR 4 (IGNORE THIS COMMENT)
path_for_alg_codes_and_tariffs = os.path.join("..", "alg_codes_and_tariffs.txt")
############ END OF SECTOR 4 (IGNORE THIS COMMENT)

############ START OF SECTOR 5 (IGNORE THIS COMMENT)
code_dictionary, tariff_dictionary, flag = read_in_algorithm_codes_and_tariffs(path_for_alg_codes_and_tariffs)

if flag != "good":
    print("*** error: The text file 'alg_codes_and_tariffs.txt' does not exist.")
    sys.exit()

print("The codes and tariffs have been read from 'alg_codes_and_tariffs.txt':")

############
############ HAVE YOU TOUCHED ANYTHING ABOVE? BECAUSE EVEN CHANGING ONE CHARACTER OR
############ ADDING ONE SPACE OR LINE RETURN WILL MEAN THAT THE PROGRAM YOU HAND IN
############ MIGHT NOT RUN PROPERLY! SORRY TO GO ON ABOUT THIS BUT YOU NEED TO BE 
############ AWARE OF THIS FACT!
############
############ YOU NOW NEED TO SUPPLY SOME PARAMETERS.
############
############ THE RESERVED STRING VARIABLE 'my_user_name' SHOULD BE SET AT YOUR
############ USER-NAME, E.G., "abcd12"
############
############ END OF SECTOR 5 (IGNORE THIS COMMENT)

my_user_name = "jgnt42"

############ START OF SECTOR 6 (IGNORE THIS COMMENT)
############
############ YOU CAN SUPPLY, IF YOU WANT, YOUR FULL NAME. THIS IS NOT USED AT ALL BUT SERVES AS
############ AN EXTRA CHECK THAT THIS FILE BELONGS TO YOU. IF YOU DO NOT WANT TO SUPPLY YOUR
############ NAME THEN EITHER SET THE STRING VARIABLES 'my_first_name' AND 'my_last_name' AT 
############ SOMETHING LIKE "Mickey" AND "Mouse" OR AS THE EMPTY STRING (AS THEY ARE NOW;
############ BUT PLEASE ENSURE THAT THE RESERVED VARIABLES 'my_first_name' AND 'my_last_name'
############ ARE SET AT SOMETHING).
############
############ END OF SECTOR 6 (IGNORE THIS COMMENT)

my_first_name = "Jude"
my_last_name = "Waide"

############ START OF SECTOR 7 (IGNORE THIS COMMENT)
############
############ YOU NEED TO SUPPLY THE ALGORITHM CODE IN THE RESERVED STRING VARIABLE 'algorithm_code'
############ FOR THE ALGORITHM YOU ARE IMPLEMENTING. IT NEEDS TO BE A LEGAL CODE FROM THE TEXT-FILE
############ 'alg_codes_and_tariffs.txt' (READ THIS FILE TO SEE THE CODES).
############
############ END OF SECTOR 7 (IGNORE THIS COMMENT)

algorithm_code = "GA"

############ START OF SECTOR 8 (IGNORE THIS COMMENT)
############
############ PLEASE SCROLL DOWN UNTIL THE NEXT BLOCK OF CAPITALIZED COMMENTS STARTING
############ 'HAVE YOU TOUCHED ...'
############
############ DO NOT TOUCH OR ALTER THE CODE IN BETWEEN! YOU HAVE BEEN WARNED!
############

if not algorithm_code in code_dictionary:
    print("*** error: the algorithm code " + algorithm_code + " is illegal")
    sys.exit()
print("   your algorithm code is legal and is " + algorithm_code + " -" + code_dictionary[algorithm_code] + ".")

start_time = time.time()

############
############ HAVE YOU TOUCHED ANYTHING ABOVE? BECAUSE EVEN CHANGING ONE CHARACTER OR
############ ADDING ONE SPACE OR LINE RETURN WILL MEAN THAT THE PROGRAM YOU HAND IN
############ MIGHT NOT RUN PROPERLY! SORRY TO GO ON ABOUT THIS BUT YOU NEED TO BE 
############ AWARE OF THIS FACT!
############
############ YOU CAN ADD A NOTE THAT WILL BE ADDED AT THE END OF THE RESULTING TOUR FILE IF YOU LIKE,
############ E.G., "in my basic greedy search, I broke ties by always visiting the first 
############ city found" BY USING THE RESERVED STRING VARIABLE 'added_note' OR LEAVE IT EMPTY
############ IF YOU WISH. THIS HAS NO EFFECT ON MARKS BUT HELPS YOU TO REMEMBER THINGS ABOUT
############ YOUR TOUR THAT YOU MIGHT BE INTERESTED IN LATER. NOTE THAT I CALCULATE THE TIME OF
############ A RUN USING THE RESERVED VARIABLE 'start_time' AND INCLUDE THE RUN-TIME IN 'added_note' LATER.
############
############ IN FACT, YOU CAN INCLUDE YOUR ADDED NOTE IMMEDIATELY BELOW OR EVEN INCLUDE YOUR ADDED NOTE
############ AT ANY POINT IN YOUR PROGRAM: JUST DEFINE THE STRING VARIABLE 'added_note' WHEN YOU WISH
############ (BUT DON'T REMOVE THE ASSIGNMENT IMMEDIATELY BELOW).
############
############ END OF SECTOR 8 (IGNORE THIS COMMENT)

added_note = ""

############ START OF SECTOR 9 (IGNORE THIS COMMENT)
############
############ NOW YOUR CODE SHOULD BEGIN BUT FIRST A COMMENT.
############
############ IF YOU ARE IMPLEMENTING GA THEN:
############  - IF YOU EXECUTE YOUR MAIN LOOP A FIXED NUMBER OF TIMES THEN USE THE VARIABLE 'max_it' TO DENOTE THIS NUMBER
############  - USE THE VARIABLE 'pop_size' TO DENOTE THE SIZE OF YOUR POPULATION (THIS IS '|P|' IN THE PSEUDOCODE)
############
############ IF YOU ARE IMPLEMENTING AC THEN:
############  - IF YOU EXECUTE YOUR MAIN LOOP A FIXED NUMBER OF TIMES THEN USE THE VARIABLE 'max_it' TO DENOTE THIS NUMBER
############  - USE THE VARIABLE 'num_ants' TO DENOTE THE NUMBER OF ANTS (THIS IS 'N' IN THE PSEUDOCODE)
############
############ IF YOU ARE IMPLEMENTING PS THEN:
############  - IF YOU EXECUTE YOUR MAIN LOOP A FIXED NUMBER OF TIMES THEN USE THE VARIABLE 'max_it' TO DENOTE THIS NUMBER
############  - USE THE VARIABLE 'num_parts' TO DENOTE THE NUMBER OF PARTICLES (THIS IS 'N' IN THE PSEUDOCODE)
############
############ DOING THIS WILL MEAN THAT THIS INFORMATION IS WRITTEN WITHIN 'added_note' IN ANY TOUR-FILE PRODUCED.
############ OF COURSE, THE VALUES OF THESE VARIABLES NEED TO BE ACCESSIBLE TO THE MAIN BODY OF CODE.
############ IT'S FINE IF YOU DON'T ADOPT THESE VARIABLE NAMES BUT THIS USEFUL INFORMATION WILL THEN NOT BE WRITTEN TO ANY
############ TOUR-FILE PRODUCED BY THIS CODE.
############
############ END OF SECTOR 9 (IGNORE THIS COMMENT)

# IMPORANT
# N.B. Any enhancements not accompanied by a link to a paper I came up with myself, although they may have been discovered already by others

if __name__ == "__main__": 
    # PARAMETERS
    max_it = 40000
    pop_size = num_cities
    processCount = 6
    eliteCount = 5  # Number of genes carried over at each iteration
    eliteFitnessScale = 3   # The factor the fitness of the elite genes are multiplied by
    timed = True    # Enable 1 minute timer
mutationChance = 0.1


# FUNCTIONS SEEN BY ALL PROCESSES
class Individual:
    def __init__(self, num_cities):
        self.tour = []
        candidates = [x for x in range(num_cities)]
        for i in range(num_cities):
            r = int(random.random()*len(candidates))
            self.tour.append(candidates[r])
            del candidates[r]
        self.tourLength = 0
        self.fitness = 0

    # (003) Calculate fitness
    def calculateFitness(self, popMax):
        # Scales fitness from 0 to 1 based on how far between the min and max tour length the individual is
        tour_length = bestIndividual.tourLength
        if popMax != tour_length:
            self.fitness = 1 - (self.tourLength-tour_length)/(popMax-tour_length)
        else:
            self.fitness = 1

# Returns the length of a tour
def cost(tour, dist_matrix):
    total = dist_matrix[tour[0]][tour[-1]]
    for i in range(len(tour)-1):
        total += dist_matrix[tour[i]][tour[i+1]]
    return total

# Selects two random parents from population using roulette wheel
def selection(population, totalFitness):
    parents = []
    for i in range(2):
        rand = random.random() * totalFitness
        val = population[0].fitness
        i = 0
        while rand > val:
            i += 1
            val += population[i].fitness
        parents.append(population[i])
    return parents[0], parents[1]

# Function found in https://www.researchgate.net/publication/220651910_Combined_Mutation_Operators_of_Genetic_Algorithm_for_the_Travelling_Salesman_Problem
# Deep, Kusum & Mebrathu, Hadush. (2011). Combined Mutation Operators of Genetic Algorithm for the Travelling Salesman Problem. IJCOPI. 2. 2-24. 
# (001) Creates a child from two parents
def crossover(parent1, parent2, dist_matrix):
    # Swap two substrings of different lengths and positions between the two parents
    num_cities = len(parent1.tour)
    #4 random points
    i1 = int(random.random()*num_cities)
    i2 = int(random.random()*num_cities)
    i3 = int(random.random()*num_cities)
    i4 = int(random.random()*num_cities)

    # i1 lower point in parent1, i3 lower point in parent2
    if i1 > i2:
        i1, i2 = i2, i1
    if i3 > i4:
        i3, i4 = i4, i3
    i2 += 1
    i4 += 1

    newTour1 = parent1.tour[:]
    newTour2 = parent2.tour[:]
    mid1 = parent1.tour[i1:i2]  # These parts are maintained
    mid2 = parent2.tour[i3:i4]  # These parts are maintained

    # Fix first child
    a = i2 % num_cities     # Position in first parent
    b = i4 % num_cities     # Position in second parent

    # Add elements from parent2
    while a != i1:  # Until full tour built
        if parent2.tour[b] not in mid1:
            newTour1[a] = parent2.tour[b]
            a += 1
            a %= num_cities
        b += 1
        b %= num_cities

    # Add elements from parent1
    a = i4 % num_cities     # Position in second parent
    b = i2 % num_cities     # Position in first parent
    while a != i3:
        if parent1.tour[b] not in mid2:
            newTour2[a] = parent1.tour[b]
            a += 1
            a %= num_cities
        b += 1
        b %= num_cities
    
    # Build children
    child1 = Individual(len(parent1.tour))
    child2 = Individual(len(parent1.tour))
    child1.tour = newTour1
    child2.tour = newTour2
    child1.tourLength = cost(child1.tour, dist_matrix)
    child2.tourLength = cost(child2.tour, dist_matrix)

    # Return best child
    if child1.tourLength < child2.tourLength:
        return child1
    return child2

# Function found in https://www.researchgate.net/publication/220651910_Combined_Mutation_Operators_of_Genetic_Algorithm_for_the_Travelling_Salesman_Problem
# Deep, Kusum & Mebrathu, Hadush. (2011). Combined Mutation Operators of Genetic Algorithm for the Travelling Salesman Problem. IJCOPI. 2. 2-24. 
# (002) Inverted Displacement Mutation
def mutate(individual, dist_matrix):
    # Get a random lengtth substring
    tourLen = len(individual.tour)
    i1 = int(random.random()*tourLen)
    i2 = int(random.random()*tourLen)
    if (i1 > i2):
        i1, i2 = i2, i1
    i2 += 1

    slice = individual.tour[i1:i2]
    slice.reverse() # Invert the substring

    # Move substring to random position in tour
    tour = individual.tour[0:i1] + individual.tour[i2:]
    i3 = int(random.random()*len(tour))
    individual.tour = tour[0:i3] + slice + tour[i3:]

    individual.tourLength = cost(individual.tour, dist_matrix)

# Main loop ran by worker process
def asyncGeneratePopChunk(matrix, orders, results):
    dist_matrix = matrix
    while True:
        # Wait until order has been placed
        chunkSize, population, totalFitness = orders.get()
        newPop = []

        # Create the requested number of individuals
        for i in range(chunkSize):
            parent1, parent2 = selection(population, totalFitness)  # Get two parents
            child = crossover(parent1, parent2, dist_matrix)     # Create child

            # Chance to mutate
            if mutationChance > random.random():
                mutate(child, dist_matrix)

            newPop.append(child)
        results.put(newPop)     # Return individuals to main process 


if __name__ == "__main__": 

    #INITIALISATION
    population = [Individual(num_cities) for x in range(pop_size)]
    popMax = None

    # Find length of initial random tours 
    for individual in population:
        individual.tourLength = cost(individual.tour, dist_matrix)
        if popMax == None or individual.tourLength > popMax:
            popMax = individual.tourLength 

    bestIndividual = population[0]

    # Set fitness
    for individual in population:
        individual.calculateFitness(popMax)

    # MULTIPROCESSING
    orders = Queue()
    results = Queue()

    #Create worker processes
    processes = [Process(target=asyncGeneratePopChunk, daemon=True, args=(dist_matrix, orders, results,)) for x in range(processCount)]
    for process in processes:
        process.start() #Start worker processes
    
    #Calculate how much work each process should do each iteration
    chunkSize = pop_size // processCount
    chunkSizeRemainder = pop_size % processCount


    # MAIN LOOP
    iteration_time = time.time_ns()
    for t in range(max_it):
        newPop = []
        totalFitness = sum(individual.fitness for individual in population)

        popMax = None

        # (006) Order worker processes to create new pop
        for i in range(processCount):
            num = chunkSize
            if i == 0:
                num += chunkSizeRemainder
            orders.put((num, population, totalFitness))
        
        # Get results
        for i in range(processCount):
            chunk = results.get()
            newPop += chunk

        # Find new longest tour of the population and find new best tour
        popMax = newPop[0].tourLength
        for individual in newPop:
            if individual.tourLength > popMax:
                popMax = individual.tourLength
            if individual.tourLength < bestIndividual.tourLength:
                bestIndividual = Individual(num_cities)
                bestIndividual.tour = individual.tour[:]
                bestIndividual.tourLength = individual.tourLength

        # Order individuals by tour length
        newPop.sort(key = lambda individual: individual.tourLength)

        # (004) elite carryover - Carry over the best n tours out of the top n unique tours of old pop and top n unique tours of new pop (where n = eliteCount)
        carryOver = []
        # Get the top n unique tours from newPop
        i = 0
        while len(carryOver) < eliteCount and i < len(newPop):
            if newPop[i].tourLength not in [x.tourLength for x in carryOver]:
                carryOver.append(newPop[i])
            i+=1
        # Get the top n unique tours from old pop
        i=0
        while len(carryOver) < 2*eliteCount and i < len(population):
            if population[i].tourLength not in [x.tourLength for x in carryOver]:
                carryOver.append(population[i])
            i+=1 
        # Sort by tour length
        carryOver.sort(key = lambda individual: individual.tourLength)
 
        # Check incase there were not n unique tours
        cap = eliteCount
        if len(carryOver) < eliteCount:
            cap = len(carryOver) 
        # Add to population
        population = carryOver[:cap] + newPop[cap:]

        # Update fitness
        for individual in population:
            individual.calculateFitness(popMax)
        # (005) elite scaling - Increase the fitness of the top n individuals based on rank
        for i in range(eliteCount):
            population[i].fitness *= eliteFitnessScale*(5-i)

        # Ensure algorithim does not last for longer than a minute
        if (t==0):
            iteration_time = (time.time_ns() - iteration_time)*1e-9
        if (timed and (time.time()-start_time) + (iteration_time*1.1) > 59.5):
            break
        t += 1

        

    tour = bestIndividual.tour
    tour_length = bestIndividual.tourLength



    ############ START OF SECTOR 10 (IGNORE THIS COMMENT)
    ############
    ############ YOUR CODE SHOULD NOW BE COMPLETE AND WHEN EXECUTION OF THIS PROGRAM 'skeleton.py'
    ############ REACHES THIS POINT, YOU SHOULD HAVE COMPUTED A TOUR IN THE RESERVED LIST VARIABLE 'tour', 
    ############ WHICH HOLDS A LIST OF THE INTEGERS FROM {0, 1, ..., 'num_cities' - 1} SO THAT EVERY INTEGER
    ############ APPEARS EXACTLY ONCE, AND YOU SHOULD ALSO HOLD THE LENGTH OF THIS TOUR IN THE RESERVED
    ############ INTEGER VARIABLE 'tour_length'.
    ############
    ############ YOUR TOUR WILL BE PACKAGED IN A TOUR FILE OF THE APPROPRIATE FORMAT AND THIS TOUR FILE'S
    ############ NAME WILL BE A MIX OF THE NAME OF THE CITY FILE, THE NAME OF THIS PROGRAM AND THE
    ############ CURRENT DATE AND TIME. SO, EVERY SUCCESSFUL EXECUTION GIVES A TOUR FILE WITH A UNIQUE
    ############ NAME AND YOU CAN RENAME THE ONES YOU WANT TO KEEP LATER.
    ############
    ############ DO NOT EDIT ANY TOUR FILE! ALL TOUR FILES MUST BE LEFT AS THEY WERE ON OUTPUT.
    ############
    ############ DO NOT TOUCH OR ALTER THE CODE BELOW THIS POINT! YOU HAVE BEEN WARNED!
    ############

    end_time = time.time()
    elapsed_time = round(end_time - start_time, 1)

    if algorithm_code == "GA":
        try: max_it
        except NameError: max_it = None
        try: pop_size
        except NameError: pop_size = None
        if added_note != "":
            added_note = added_note + "\n"
        added_note = added_note + "The parameter values are 'max_it' = " + str(max_it) + " and 'pop_size' = " + str(pop_size) + "."

    if algorithm_code == "AC":
        try: max_it
        except NameError: max_it = None
        try: num_ants
        except NameError: num_ants = None
        if added_note != "":
            added_note = added_note + "\n"
        added_note = added_note + "The parameter values are 'max_it' = " + str(max_it) + " and 'num_ants' = " + str(num_ants) + "."

    if algorithm_code == "PS":
        try: max_it
        except NameError: max_it = None
        try: num_parts
        except NameError: num_parts = None
        if added_note != "":
            added_note = added_note + "\n"
        added_note = added_note + "The parameter values are 'max_it' = " + str(max_it) + " and 'num_parts' = " + str(num_parts) + "."
        
    added_note = added_note + "\nRUN-TIME = " + str(elapsed_time) + " seconds.\n"

    flag = "good"
    length = len(tour)
    for i in range(0, length):
        if isinstance(tour[i], int) == False:
            flag = "bad"
        else:
            tour[i] = int(tour[i])
    if flag == "bad":
        print("*** error: Your tour contains non-integer values.")
        sys.exit()
    if isinstance(tour_length, int) == False:
        print("*** error: The tour-length is a non-integer value.")
        sys.exit()
    tour_length = int(tour_length)
    if len(tour) != num_cities:
        print("*** error: The tour does not consist of " + str(num_cities) + " cities as there are, in fact, " + str(len(tour)) + ".")
        sys.exit()
    flag = "good"
    for i in range(0, num_cities):
        if not i in tour:
            flag = "bad"
    if flag == "bad":
        print("*** error: Your tour has illegal or repeated city names.")
        sys.exit()
    check_tour_length = 0
    for i in range(0, num_cities - 1):
        check_tour_length = check_tour_length + dist_matrix[tour[i]][tour[i + 1]]
    check_tour_length = check_tour_length + dist_matrix[tour[num_cities - 1]][tour[0]]
    if tour_length != check_tour_length:
        flag = print("*** error: The length of your tour is not " + str(tour_length) + "; it is actually " + str(check_tour_length) + ".")
        sys.exit()
    print("You, user " + my_user_name + ", have successfully built a tour of length " + str(tour_length) + "!")
    len_user_name = len(my_user_name)
    user_number = 0
    for i in range(0, len_user_name):
        user_number = user_number + ord(my_user_name[i])
    alg_number = ord(algorithm_code[0]) + ord(algorithm_code[1])
    tour_diff = abs(tour[0] - tour[num_cities - 1])
    for i in range(0, num_cities - 1):
        tour_diff = tour_diff + abs(tour[i + 1] - tour[i])
    certificate = user_number + alg_number + tour_diff
    local_time = time.asctime(time.localtime(time.time()))
    output_file_time = local_time[4:7] + local_time[8:10] + local_time[11:13] + local_time[14:16] + local_time[17:19]
    output_file_time = output_file_time.replace(" ", "0")
    script_name = os.path.basename(sys.argv[0])
    if len(sys.argv) > 2:
        output_file_time = sys.argv[2]
    output_file_name = script_name[0:len(script_name) - 3] + "_" + input_file[0:len(input_file) - 4] + "_" + output_file_time + ".txt"

    f = open(output_file_name,'w')
    f.write("USER = {0} ({1} {2}),\n".format(my_user_name, my_first_name, my_last_name))
    f.write("ALGORITHM CODE = {0}, NAME OF CITY-FILE = {1},\n".format(algorithm_code, input_file))
    f.write("SIZE = {0}, TOUR LENGTH = {1},\n".format(num_cities, tour_length))
    f.write(str(tour[0]))
    for i in range(1,num_cities):
        f.write(",{0}".format(tour[i]))
    f.write(",\nNOTE = {0}".format(added_note))
    f.write("CERTIFICATE = {0}.\n".format(certificate))
    f.close()
    print("I have successfully written your tour to the tour file:\n   " + output_file_name + ".")

    ############ END OF SECTOR 10 (IGNORE THIS COMMENT)
