"""
ContinuousOptimalBinning testing.
"""

# Guillermo Navas-Palencia <g.navas.palencia@gmail.com>
# Copyright (C) 2020

import pandas as pd

from pytest import approx, raises

from optbinning import ContinuousOptimalBinning
from sklearn.datasets import load_boston
from sklearn.exceptions import NotFittedError


data = load_boston()
df = pd.DataFrame(data.data, columns=data.feature_names)

variable = "LSTAT"
x = df[variable].values
y = data.target


def test_params():
    with raises(TypeError):
        optb = ContinuousOptimalBinning(name=1)
        optb.fit(x, y)

    with raises(ValueError):
        optb = ContinuousOptimalBinning(dtype="nominal")
        optb.fit(x, y)

    with raises(ValueError):
        optb = ContinuousOptimalBinning(prebinning_method="new_method")
        optb.fit(x, y)

    with raises(ValueError):
        optb = ContinuousOptimalBinning(max_n_prebins=-2)
        optb.fit(x, y)

    with raises(ValueError):
        optb = ContinuousOptimalBinning(min_prebin_size=0.6)
        optb.fit(x, y)

    with raises(ValueError):
        optb = ContinuousOptimalBinning(min_n_bins=-2)
        optb.fit(x, y)

    with raises(ValueError):
        optb = ContinuousOptimalBinning(max_n_bins=-2.2)
        optb.fit(x, y)

    with raises(ValueError):
        optb = ContinuousOptimalBinning(min_n_bins=3, max_n_bins=2)
        optb.fit(x, y)

    with raises(ValueError):
        optb = ContinuousOptimalBinning(min_bin_size=0.6)
        optb.fit(x, y)

    with raises(ValueError):
        optb = ContinuousOptimalBinning(max_bin_size=-0.6)
        optb.fit(x, y)

    with raises(ValueError):
        optb = ContinuousOptimalBinning(min_bin_size=0.5, max_bin_size=0.3)
        optb.fit(x, y)

    with raises(ValueError):
        optb = ContinuousOptimalBinning(monotonic_trend="new_trend")
        optb.fit(x, y)

    with raises(ValueError):
        optb = ContinuousOptimalBinning(min_mean_diff=-1.1)
        optb.fit(x, y)

    with raises(ValueError):
        optb = ContinuousOptimalBinning(max_pvalue=1.1)
        optb.fit(x, y)

    with raises(ValueError):
        optb = ContinuousOptimalBinning(max_pvalue_policy="new_policy")
        optb.fit(x, y)

    with raises(ValueError):
        optb = ContinuousOptimalBinning(cat_cutoff=-0.2)
        optb.fit(x, y)

    with raises(TypeError):
        optb = ContinuousOptimalBinning(user_splits={"a": [1, 2]})
        optb.fit(x, y)

    with raises(TypeError):
        optb = ContinuousOptimalBinning(special_codes={1, 2, 3})
        optb.fit(x, y)

    with raises(ValueError):
        optb = ContinuousOptimalBinning(split_digits=9)
        optb.fit(x, y)

    with raises(ValueError):
        optb = ContinuousOptimalBinning(time_limit=-2)
        optb.fit(x, y)

    with raises(TypeError):
        optb = ContinuousOptimalBinning(verbose=1)
        optb.fit(x, y)


def test_numerical_default():
    optb = ContinuousOptimalBinning()
    optb.fit(x, y)

    assert optb.status == "OPTIMAL"
    assert optb.splits == approx([4.6500001, 5.49499989, 6.86500001, 9.7249999,
                                  11.67499971, 13.0999999, 16.08500004,
                                  19.89999962, 23.31500053],
                                 rel=1e-6)


def test_numerical_default_transform():
    optb = ContinuousOptimalBinning()
    with raises(NotFittedError):
        x_transform = optb.transform(x)

    optb.fit(x, y)

    x_transform = optb.transform([0.2, 4.1, 7.2, 26])
    assert x_transform == approx([39.718, 39.718, 25.56067416, 11.82978723],
                                 rel=1e-6)


def test_numerical_default_fit_transform():
    optb = ContinuousOptimalBinning()

    x_transform = optb.fit_transform(x, y)
    assert x_transform[:5] == approx([30.47142857, 25.56067416, 39.718, 39.718,
                                      30.47142857], rel=1e-6)


def test_verbose():
    optb = ContinuousOptimalBinning(verbose=True)
    optb.fit(x, y)

    assert optb.status == "OPTIMAL"