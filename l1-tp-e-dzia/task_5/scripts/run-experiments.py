"""Script for time measurement experiments on linear regression models."""
import argparse
import datetime
import os
import pickle
from typing import List
from typing import Tuple
from typing import Type

import pandas as pd
import matplotlib.pyplot as plt

import l1.task_5.lr as lr


def get_args() -> argparse.Namespace:
    """Parses script arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--datasets-dir',
        required=True,
        help='Name of directory with generated datasets',
        type=str,
    )

    return parser.parse_args()


def run_experiments(
        models: List[Type[lr.base.LinearRegression]],
        datasets: List[Tuple[List[float], List[float]]]) -> pd.DataFrame:
    """Runs exeriments."""
    results = pd.DataFrame({"size": [], "model": [], "time": []})
    for dataset in datasets:
        X = dataset[0]
        y = dataset[1]
        size = len(X)
        for model_name in models:
            model = model_name()

            start = datetime.datetime.now()
            model.fit(X=X, y=y)
            model.predict(X=X)
            end = datetime.datetime.now()

            time_elapsed = end - start
            values_list = [[size, model_name.__name__,
                            time_elapsed.total_seconds()]]
            df = pd.DataFrame(values_list, columns=['size', 'model', 'time'])
            results = results.append(df)
    return results


def make_plot(results: pd.DataFrame) -> None:
    """Makes plot of results."""
    fig, ax = plt.subplots()
    for key, grp in results.groupby('model'):
        ax = grp.plot(ax=ax, kind='line', x='size', y='time', label=key,
                      style='.-', title='Plot time of execution')
    plt.savefig(
        '../plots/plots-{}.png'.format(
            datetime.datetime.now()).replace(":", "-").replace(" ", "_"))


def read_datasets(datasets_dir):
    """Read datasets from specified dir."""
    datasets = []
    for file in os.listdir(datasets_dir):
        filename = datasets_dir + '/' + file
        with open(filename, 'rb') as fp:
            data = pickle.load(fp)
            datasets.append(data)
    datasets.sort(key=lambda x: len(x[0]))
    return datasets


def main() -> None:
    """Runs script."""
    args = get_args()
    datasets_dir = args.datasets_dir

    models = [
        lr.LinearRegressionNumpy,
        lr.LinearRegressionProcess,
        lr.LinearRegressionSequential,
        lr.LinearRegressionThreads,
    ]

    datasets = read_datasets(datasets_dir)
    results = run_experiments(models, datasets)
    # print(results)

    make_plot(results)


if __name__ == '__main__':
    main()
