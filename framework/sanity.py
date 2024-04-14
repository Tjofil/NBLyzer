import csv
from statistics import mean
from matplotlib import pyplot as plt

def get_exec_times(file_name: str) -> tuple[dict[int, list[float]], dict[int, list[float]]]:
    f = open(file_name)
    reader = csv.DictReader(f)
    exec_times_rows = dict[int, list[float]]()
    exec_times_no_rows = dict[int, list[float]]()
    for row in reader:
        file, rows, no_rows = int(row['file']), row['extension'], row['nblyzer']
        
        if file not in exec_times_rows:
            exec_times_rows[file] = list[float]()

        if file not in exec_times_no_rows:
            exec_times_no_rows[file] = list[float]()

        exec_times_rows[file].append(float(rows))
        exec_times_no_rows[file].append(float(no_rows))
    f.close()
    return exec_times_rows, exec_times_no_rows

def get_mean_exec_times(file_name: str) -> tuple[dict[int, float], dict[int, float]]:
    f = open(file_name)
    reader = csv.DictReader(f)
    exec_times_rows = dict[int, float]()
    exec_times_no_rows = dict[int, float]()
    for row in reader:
        file, rows, no_rows = int(row['file']), row['extension'], row['nblyzer']
        exec_times_rows[file] = float(rows)
        exec_times_no_rows[file] = float(no_rows)
    f.close()
    return exec_times_rows, exec_times_no_rows

def plot(times_rows: dict[int, float], times_no_rows: dict[int, float]) -> None:
    plt.gcf().set_size_inches(16,14)

    plt.plot(times_no_rows.keys(), times_no_rows.values(), 'bo')
    plt.plot(times_rows.keys(), times_rows.values(), 'ro')
    plt.title("Runtime comparison of old and new implementation (K = 5)")
    plt.xlabel("Notebook ID")
    plt.ylabel("Mean Runtime per Notebook [sec]")
    plt.yscale('log')
    plt.legend(["Old NBLyzer", "Extension"])
    plt.grid(color = '0.8', linestyle = '--')

    plt.savefig("/home/tjofi/code/NBLyzer/comparison3.jpg", edgecolor = 'black', dpi = 800)


def main():
    # times_rows, times_no_rows = get_exec_times('/home/tjofi/code/NBLyzer/output/file_exec.csv')

    # mean_times_rows = {file : mean(times) for file, times in times_rows.items()}
    # mean_times_no_rows = {file : mean(times) for file, times in times_no_rows.items()}

    mean_times_rows, mean_times_no_rows = get_mean_exec_times('/home/tjofi/code/NBLyzer/output/file_avg.csv')

    differences = dict(map(lambda x : (x[0], x[1]/mean_times_no_rows[x[0]]), mean_times_rows.items()))

    print(mean(differences.values()))

    plot(mean_times_rows, mean_times_no_rows)

if __name__ == '__main__':
    main()