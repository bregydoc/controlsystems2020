import control as ct
import numpy as np
from typing import Tuple, Union
from enum import Enum
from sklearn.neural_network import MLPClassifier, MLPRegressor
from sklearn.multioutput import MultiOutputClassifier
from sklearn.model_selection import train_test_split
from joblib import dump, load

# Number = Union[int, float, complex]


class NumberKind(Enum):
    INTEGER = 1
    COMPLEX = 2
    REAL = 3
    CONJUGATED = 4


def generate_pole_root(kind: NumberKind, lower_bound: float = -100, upper_bound: float = 100) \
        -> Union[Tuple[complex], Tuple[complex, complex]]:

    if kind == NumberKind.REAL:
        return np.random.uniform(lower_bound, upper_bound, 1)[0] + 0j,
    elif kind == NumberKind.COMPLEX:
        ri = np.random.uniform(lower_bound, upper_bound, 2)
        return ri[0] + 1j * ri[1],
    elif kind == NumberKind.INTEGER:
        return np.random.randint(lower_bound, upper_bound, 1)[0] + 0j,
    elif kind == NumberKind.CONJUGATED:
        ri = np.random.uniform(lower_bound, upper_bound, 2)
        i = ri[0] + 1j * ri[1]
        return i, complex.conjugate(i)


def generate_random_gain(lower_bound: float = 0.5, upper_bound: float = 30) -> Union[float, int]:
    if np.random.rand() > 0.5:
        return np.random.uniform(lower_bound, upper_bound, 1)[0]
    else:
        return np.random.randint(lower_bound, upper_bound, 1)[0]


def generate_example(z_range: list, p_range: list) -> Tuple[ct.TransferFunction, Tuple[list, list, list]]:
    total_zeros = np.random.randint(z_range[0], z_range[1], 1)[0]
    total_poles = np.random.randint(p_range[0], p_range[1], 1)[0]

    num = []
    den = []

    selected_zeros_kinds = np.random.choice(to_select, total_zeros)
    for z in selected_zeros_kinds:
        for i in generate_pole_root(z):
            num.append(i)

    selected_poles_kinds = np.random.choice(to_select, total_poles)
    for p in selected_poles_kinds:
        for i in generate_pole_root(p):
            den.append(i)

    tf = ct.TransferFunction(num, den)

    return tf, ct.bode(tf, Plot=False)


if __name__ == "__main__":
    to_select = [NumberKind.INTEGER, NumberKind.REAL, NumberKind.COMPLEX, NumberKind.CONJUGATED]
    zeros_range = [0, 4]
    poles_range = [1, 5]

    x_train = []
    y_train = []

    for ex in range(10000):
        try:
            e = generate_example(zeros_range, poles_range)
        except:
            continue
        mag, pha, freq = e[1]
        x = np.concatenate((mag, pha, freq))
        num_part = []
        tf = e[0] * generate_random_gain()
        for n in tf.num[0][0]:
            num_part.append(n.real)
            num_part.append(n.imag)
        den_part = []
        for d in tf.den[0][0]:
            den_part.append(d.real)
            den_part.append(d.imag)

        num_part = np.concatenate((num_part, np.zeros(max(zeros_range[1]*2 - len(num_part), 0))))
        den_part = np.concatenate((den_part, np.zeros(max(poles_range[1]*2 - len(den_part), 0))))

        y = np.concatenate((num_part, den_part))

        if len(y) == zeros_range[1] * 2 + poles_range[1] * 2:
            x_train.append(list(x))
            y_train.append(list(y))
            if ex % 1000 == 0:
                print(f"generated {ex} samples")

    x_train = np.array(x_train)
    y_train = np.array(y_train)
    print("done")
    print(x_train.shape)
    print(y_train.shape)



    X_train, X_test, y_train, y_test = train_test_split(x_train, y_train, random_state=1)
    # clf = MLPRegressor(solver='adam', alpha=0.0001, hidden_layer_sizes=(700, 300, 200, 500, 100), max_iter=10000)
    clf = load('bode_hero_model.joblib')
    clf = clf.fit(X_train, y_train)

    print(clf.score(X_test, y_test))

    dump(clf, 'bode_hero_model.joblib')
