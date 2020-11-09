import random
import math
import matplotlib.pyplot as plt
class Person:
    def __init__(self, num, age, x, y):
        self.name = f'Person {num}'
        self.age = age
        self.pos = [x, y]
        self.infected = False
        self.nearest_infected = {}
        self.distance_to_infected = {}

    def __str__(self):
        return f'{self.name}, Age {self.age}, At {tuple(self.pos)}'

def random_num_gen(upper_bound):
    return random.randint(1, upper_bound)

NUM_PEOPLE = int(input("How Many People Should Be In This Simulation?: "))
DIMENSIONS = int(input("What Should Each Side Of The \"Board\" Measure?: "))
if DIMENSIONS ** 2 <= NUM_PEOPLE:
    raise Exception("Amount Too Low")
SPACE_MOVABLE = int(input("What Is The Maximum Amount Of Spaces A Person In This Simulation Can Move At A Time?: "))
if SPACE_MOVABLE > NUM_PEOPLE / 2 or SPACE_MOVABLE > DIMENSIONS / 2:
    raise Exception("Amount Too High")
TRANSMISSION_DISTANCE = int(input("How Far Can The Simulated Disease Be Transmitted?: "))
if TRANSMISSION_DISTANCE > NUM_PEOPLE / 4:
    raise Exception("Amount Too High")
MAX_TIME = int(input("How Many \"Hours\" Should This Simulation Last?: "))
PERSON_LIST = []
INFECTED_LIST = []
for x in range(NUM_PEOPLE):
    PERSON_LIST.append(Person(x + 1, random_num_gen(80), random_num_gen(DIMENSIONS), random_num_gen(DIMENSIONS)))
INITIAL_INFECTED = PERSON_LIST[random_num_gen(NUM_PEOPLE - 1)]
INITIAL_INFECTED.infected = True
INFECTED_LIST.append(INITIAL_INFECTED)
print(f'{str(INITIAL_INFECTED)} Is Patient Zero')

plot_x = []
plot_y = []
hours = 1
while hours <= MAX_TIME:
    for y in PERSON_LIST:
        y.pos[random_num_gen(2) - 1] += random.choice([random_num_gen(SPACE_MOVABLE), -random_num_gen(SPACE_MOVABLE)])
        if y.pos[0] < 0:
            y.pos[0] = 0
        elif y.pos[1] < 0:
            y.pos[1] = 0
        elif y.pos[0] > DIMENSIONS:
            y.pos[0] = DIMENSIONS
        elif y.pos[1] > DIMENSIONS:
            y.pos[1] = DIMENSIONS
    for z in INFECTED_LIST:
        def calc_distance(person):
            return math.sqrt((z.pos[0] - person.pos[0]) ** 2 + (z.pos[1] - person.pos[1]) ** 2)
        PRONE_PEOPLE = [person for person in PERSON_LIST if person.infected == False and calc_distance(person) <= TRANSMISSION_DISTANCE]
        if PRONE_PEOPLE:
            CHOSEN_PERSON = random.choice(PRONE_PEOPLE)
            WEIGHT_LIST = [CHOSEN_PERSON]
            if CHOSEN_PERSON.age in range(1, 20):
                weight = 50
            elif CHOSEN_PERSON.age in range(20, 40):
                weight = 25
            elif CHOSEN_PERSON.age in range(40, 60):
                weight = 6
            elif CHOSEN_PERSON.age in range(60, 80):
                weight = 3
            else:
                weight = 1
            i = 1
            while i <= weight:
                WEIGHT_LIST.append([])
                i += 1
            if random.choice(WEIGHT_LIST) == CHOSEN_PERSON:
                CHOSEN_PERSON.infected = True
                INFECTED_LIST.append(CHOSEN_PERSON)
                print(f'{str(CHOSEN_PERSON)} Has Been Infected By {str(z)} {hours} Hour(s) In. So Far, {len(INFECTED_LIST)} People Have Been Infected.')
    plot_x.append(hours)
    plot_y.append(len(INFECTED_LIST))
    hours += 1

plt.plot(plot_x, plot_y)
plt.title("Simulation Infections Over Time")
plt.xlabel("Hours")
plt.ylabel("Infections")
plt.show()