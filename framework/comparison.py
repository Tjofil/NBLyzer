import csv
from statistics import mean
from matplotlib import pyplot as plt

def get_exec_times(file_name: str) -> dict[int, list[float]]:
    f = open(file_name)
    reader = csv.DictReader(f)
    exec_times = dict[int, list[float]]()
    a = 0
    for row in reader:
        file_str, time = row['file name'].replace('.ipynb', ''), row['execute time']
        if not file_str.isnumeric():
            continue
        file = int(file_str)
        if file not in exec_times:
            exec_times[file] = list[float]()
        exec_times[file].append(float(time))
        a+= 1
    
    print(a)
    f.close()
    return exec_times

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

    plt.savefig("/home/tjofi/code/NBLyzer/comparison.jpg", edgecolor = 'black', dpi = 800)

def save_avg(times_rows: dict[int, float], times_no_rows: dict[int, float]) -> None:
    f = open('/home/tjofi/code/NBLyzer/output/file_avg.csv', 'w')
    writer = csv.DictWriter(f, fieldnames=['file', 'nblyzer', 'extension'])
    writer.writeheader()
    for time_rows, time_no_rows in zip(times_rows.items(), times_no_rows.items()):
        writer.writerow({'file': str(time_rows[0]), 'nblyzer': time_no_rows[1], 'extension': time_rows[1]})
    f.close()

def save_exec(times_rows: dict[int, list[float]], times_no_rows: dict[int, list[float]]) -> None:
    f = open('/home/tjofi/code/NBLyzer/output/file_exec.csv', 'w')
    writer = csv.DictWriter(f, fieldnames=['file', 'nblyzer', 'extension'])
    writer.writeheader()
    for time_rows, time_no_rows in zip(times_rows.items(), times_no_rows.items()):
        for exec_rows, exec_no_rows in zip(time_rows[1], time_no_rows[1]):
            writer.writerow({'file': str(time_rows[0]), 'nblyzer': exec_no_rows, 'extension': exec_rows})
    f.close()

def main():
    times_rows = get_exec_times('/home/tjofi/code/NBLyzer/output/rows.csv')
    times_no_rows = get_exec_times('/home/tjofi/code/NBLyzer/output/no_rows.csv')

    mean_times_rows = {file : mean(times) for file, times in times_rows.items()}
    mean_times_no_rows = {file : mean(times) for file, times in times_no_rows.items()}

    # save_exec(times_rows, times_no_rows)
    # save_avg(mean_times_rows, mean_times_no_rows)

    print(len(times_rows))

    differences = dict(map(lambda x : (x[0], x[1]/mean_times_no_rows[x[0]]), mean_times_rows.items()))

    print(mean(differences.values()))

    plot(mean_times_rows, mean_times_no_rows)

if __name__ == '__main__':
    main()