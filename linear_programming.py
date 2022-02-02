#Code by: Kamil Adamczyk
from ortools.linear_solver import pywraplp
import genetic_algorithm as gen
import numpy as np


def linear_solver(weight_threshold, weight_list, util_list, thresh_list):
    n = len(weight_list)
    binary_vector = []
    # initialize the integer programming model with the open source CBC solver
    solver = pywraplp.Solver('simple_mip_program', pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)
    # Declare binary variable x for each item from 1 to n
    x_dict = {}
    for i in range(n):
        x_dict[i] = solver.IntVar(0, 1, f'x_{i}')
    # Add constraint on total weight of items selected cannot exceed weight threshold
    solver.Add(solver.Sum([weight_list[i] * x_dict[i] for i in range(n)]) <= weight_threshold)
    # Maximize total utility score
    solver.Maximize(solver.Sum([util_list[i] * thresh_list[i] * x_dict[i] for i in range(n)]))
    # Solve!
    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL:
        for i in x_dict:
            binary_vector.append(int(x_dict[i].solution_value()))
    return binary_vector


def solve_per_author(authors: list, publications: list, threshold: str, primary_solution: gen.PopulationMember = None) -> gen.PopulationMember:
    binary_member = []
    for i in range(len(authors)):
        auth_publ_slot_list = []
        auth_publ_val_list = []
        auth_less_than_100 = []
        for j in range(len(authors[i].publications)):
            auth_publ_slot_list.append(authors[i].publications[j].unit_slot)
            auth_publ_val_list.append(authors[i].publications[j].point_value)
            auth_less_than_100.append(authors[i].publications[j].is_less_than_100)
        if not primary_solution: auth_less_than_100 = [not elem for elem in auth_less_than_100]
        binary_member += \
            linear_solver(eval(threshold), auth_publ_slot_list, auth_publ_val_list, auth_less_than_100)
    solution = gen.create_population_member(binary_member, publications, authors)
    return solution


def solve_up_to_threshhold(primary_solution: gen.PopulationMember, threshold: float, authors: list, publications: list, reverse: bool) -> gen.PopulationMember:
    auth_publ_slot_list = []
    auth_publ_val_list = []
    auth_less_than_100 = []
    for i in range(len(primary_solution.binary_vector)):
        if primary_solution.binary_vector[i] == 1:
            auth_publ_slot_list.append(publications[i].unit_slot)
            auth_publ_val_list.append(publications[i].point_value)
            auth_less_than_100.append(publications[i].is_less_than_100)
    if reverse: auth_less_than_100 = [not elem for elem in auth_less_than_100]
    binary_member = linear_solver(threshold, auth_publ_slot_list, auth_publ_val_list, auth_less_than_100)
    counter = 0
    for i in range(len(primary_solution.binary_vector)):
        if primary_solution.binary_vector[i] == 1:
            primary_solution.binary_vector[i] *= binary_member[counter]
            counter += 1
    corrected_solution = gen.create_population_member(primary_solution.binary_vector, publications, authors)
    return corrected_solution


def linear_programming(Nval: int, publications: list, authors: list) -> gen.PopulationMember:
    first_stage_solve = solve_per_author(authors, publications, "authors[i].overall_slot")
    if sum(first_stage_solve.author_slots) > 3*Nval:
        first_stage_solve = solve_up_to_threshhold(first_stage_solve, 3*Nval, authors, publications, True)
    threshold = min(0.05*3*Nval, 3*Nval-sum(first_stage_solve.author_slots))
    second_stage_solve = solve_per_author(authors, publications, "min(authors[i].overall_slot-primary_solution.author_slots[i], 2)", first_stage_solve)
    if sum(second_stage_solve.author_slots) > threshold:
        second_stage_solve = solve_up_to_threshhold(second_stage_solve, threshold, authors, publications, False)
    final_vector = list(np.bitwise_or(first_stage_solve.binary_vector, second_stage_solve.binary_vector))
    final_solution = gen.create_population_member(final_vector, publications, authors)
    return final_solution
