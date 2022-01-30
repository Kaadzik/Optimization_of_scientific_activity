import numpy as np


class PopulationMember(object):
    def __init__(self, binary_vector, author_slots, author_slots_less_than_100, eval_value):
        self.binary_vector = binary_vector
        self.author_slots = author_slots
        self.author_slots_less_than_100 = author_slots_less_than_100
        self.eval_value = eval_value

    def get_value(self):
        return self.eval_value


def create_population_member(binary_member: list, publications: list, authors: list) -> PopulationMember:
    target_value = 0
    taken_slots = [0] * len(authors)
    taken_slots_less_than_100 = [0] * len(authors)
    for i in range(len(binary_member)):
        if binary_member[i] == 1:
            target_value += publications[i].point_value
            taken_slots[publications[i].author_order_number] += publications[i].unit_slot
            if publications[i].is_less_than_100:
                taken_slots_less_than_100[publications[i].author_order_number] += publications[i].unit_slot
    return PopulationMember(binary_member, taken_slots, taken_slots_less_than_100, target_value)


def random_population_member(Nval: int, publications: list, authors: list) -> PopulationMember:
    cutoff = round(0.06*3*Nval)
    binary_member = [1] * cutoff + [0] * (len(publications)-cutoff)
    np.random.shuffle(binary_member)
    member = create_population_member(binary_member, publications, authors)
    return member


def limits_check(Nval: int, pop_member: PopulationMember, authors: list) -> bool:
    for i in range(len(pop_member.author_slots)):
        if pop_member.author_slots[i] > authors[i].overall_slot: return False
    if sum(pop_member.author_slots) > 3*Nval: return False
    elif [i for i in pop_member.author_slots_less_than_100 if i > 2]: return False
    elif sum(pop_member.author_slots_less_than_100) > 0.05*3*Nval: return False
    else: return True


def generate_roulette_slices(population: list) -> list:
    total_score = 0
    roulette = []
    population.sort(key=lambda x: x.get_value())
    for elem in population:
        total_score += elem.get_value()
    for elem in population:
        roulette.append(elem.get_value()*100/total_score)
    return roulette


def choose_a_parent(roulette: list, population: list) -> PopulationMember:
    rand = np.random.random_sample()*100
    for i in range(len(population)):
        rand -= roulette[i]
        if rand <= 0:
            return population[i]
    return population[-1]


def mutation(parent: PopulationMember, publications: list, authors: list) -> PopulationMember:
    zeros_index = []
    binary_member = parent.binary_vector[:]
    for i in range(len(binary_member)):
        if binary_member[i] == 0:
            zeros_index.append(i)
    for i in range(1):
        change = np.random.choice(zeros_index)
        binary_member[change] = 1
        zeros_index.remove(change)
    child = create_population_member(binary_member, publications, authors)
    return child


def crossover(parent1: PopulationMember, parent2: PopulationMember, publications: list, authors: list)\
        -> (PopulationMember, PopulationMember):
    divider = np.random.randint(len(parent1.binary_vector))
    binary_member1 = parent1.binary_vector[:divider] + parent2.binary_vector[divider:]
    binary_member2 = parent2.binary_vector[:divider] + parent1.binary_vector[divider:]
    child1 = create_population_member(binary_member1, publications, authors)
    child2 = create_population_member(binary_member2, publications, authors)
    return child1, child2


def genetic_algorithm(Nval: int, publications: list, authors: list) -> PopulationMember:
    current_population = []
    number_of_iterations = 7500
    population_size = min(len(publications) // 6, 50)
    mutation_probability = 0.55
    while len(current_population) < population_size:
        population_member = random_population_member(Nval, publications, authors)
        if limits_check(Nval, population_member, authors):
            current_population.append(population_member)
    for curr_iter in range(number_of_iterations):
        roulette_slices = generate_roulette_slices(current_population)
        if np.random.random_sample() < mutation_probability:
            parent1 = choose_a_parent(roulette_slices, current_population)
            child1 = mutation(parent1, publications, authors)
            if limits_check(Nval, child1, authors) and child1.get_value() > current_population[0].get_value():
                current_population.append(child1)
                del current_population[0]
            else: curr_iter -= 1
        else:
            parent1 = choose_a_parent(roulette_slices, current_population)
            parent2 = choose_a_parent(roulette_slices, current_population)
            child1, child2 = crossover(parent1, parent2, publications, authors)
            iter_check = 0
            if limits_check(Nval, child1, authors) and child1.get_value() > current_population[0].get_value():
                current_population.append(child1)
                del current_population[0]
            else: iter_check = 1
            if limits_check(Nval, child2, authors) and child2.get_value() > current_population[0].get_value():
                current_population.append(child2)
                del current_population[0]
            elif iter_check == 1: curr_iter -= 1
    current_population.sort(key=lambda x: x.get_value(), reverse=True)
    return current_population[0]
