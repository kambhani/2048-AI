import matplotlib.pyplot as plt
from collections import Counter
import os


def read_max_tiles(filename):
    """Read the max_tile values from a file."""
    with open(filename, 'r') as file:
        return [int(line.split()[1]) for line in file]


def plot_clustered_bar_chart(data, labels, title, xlabel, ylabel, output_file="bar_chart.png"):
    """
    Plot a clustered bar chart.

    :param data: List of dictionaries where each dictionary contains counts of max_tile values.
    :param labels: List of labels for each dataset (e.g., file names).
    :param title: Title of the chart.
    :param xlabel: Label for the x-axis.
    :param ylabel: Label for the y-axis.
    :param output_file: File name to save the chart.
    """
    # Get all unique max_tile values
    all_keys = sorted(set(key for d in data for key in d.keys()))
    x = range(len(all_keys))

    # Width of each bar
    width = 0.25
    offsets = [i * width for i in range(len(data))]

    fig, ax = plt.subplots(figsize=(10, 6))

    for i, (counts, label) in enumerate(zip(data, labels)):
        # Normalize counts to all_keys (fill missing values with 0)
        normalized_counts = [counts.get(key, 0) for key in all_keys]
        ax.bar(
            [pos + offsets[i] for pos in x],
            normalized_counts,
            width,
            label=label
        )

    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_xticks([pos + sum(offsets) / len(offsets) for pos in x])
    ax.set_xticklabels(all_keys)
    ax.legend()
    plt.tight_layout()
    plt.savefig(output_file)
    plt.show()


if __name__ == "__main__":
    # List of file names
    filenames = ["results/expectimax.txt", "results/mcts.txt", "results/random_action.txt"]  # Update with your file paths
    labels = ["Expectimax", "MCTS", "Random Actions"]
    if not all(os.path.exists(fname) for fname in filenames):
        print("Ensure all files exist.")

    # Read max_tile values and count their occurrences
    data = [Counter(read_max_tiles(filename)) for filename in filenames]

    # Plot clustered bar chart
    plot_clustered_bar_chart(
        data,
        labels=labels,
        title="Max Tile Distribution",
        xlabel="Max Tile Values",
        ylabel="Frequency",
        output_file="results/max_tile.png"
    )