import pandas as pd
import matplotlib.pyplot as plt


def create_test_graph(file_name: str, parameter_name: str):
    datasheet = pd.read_excel(f"{file_name}.xlsx", index_col=0)
    fig, axs = plt.subplots(1, 1)
    fig.suptitle(f"Wyniki scenariuszy testowych: {parameter_name}", fontsize=14)
    fig.text(0.02, 0.5, 'Wartość funkcji celu [pkt]', va='center', rotation='vertical', fontsize=12)
    plt.plot(datasheet["Maximum value"], color='green', label="Najlepszy wynik z 1000 powtórzeń algorytmu")
    plt.plot(datasheet["Average value"], color="blue", label="Średni wynik z 1000 powtórzeń algorytmu")
    plt.plot(datasheet["Minimum value"], color="red", label="Najgorszy wynik z 1000 powtórzeń algorytmu")
    plt.ylim(bottom=2000)
    plt.xlim(left=0)
    plt.grid()
    plt.legend(fontsize=12)
    plt.xlabel(f"{parameter_name}", fontsize=12)
    plt.savefig(f"Test_results/{file_name}.png")
    # plt.show()


datasheet_names = [
    "Iteration_number_test-dataset1",
    "Iteration_number_test-dataset2",
    "Mutation_percentage_test-dataset1",
    "Mutation_percentage_test-dataset2",
    "Population_size_test-dataset1",
    "Population_size_test-dataset2"]

parameter_names = [
    "Liczba iteracji",
    "Liczba iteracji",
    "Prawdopodobieństwo mutacji",
    "Prawdopodobieństwo mutacji",
    "Rozmiar populacji",
    "Rozmiar populacji"]

for i in range(len(datasheet_names)):
    create_test_graph(datasheet_names[i], parameter_names[i])
