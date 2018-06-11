#!/usr/bin/python
# -*- coding: utf-8 -*-

from math import sin
from math import radians
from random import randint
from random import seed


def constant(max_pps, run_time_sec):
    # All seconds of the test will have pps = max_pps, so:
    pps = [max_pps for _ in range(1, run_time_sec + 1)]
    return pps


def linear(max_pps, run_time_sec):
    # The last second of the test must have pps == max_pps, so:
    pps = [(i * max_pps) / run_time_sec for i in range(1, run_time_sec + 1)]
    return pps


def quadratic(max_pps, run_time_sec):
    # The last second of the test must have pps == max_pps, so:
    pps = [int(((i / float(run_time_sec)) ** 2) * max_pps) for i in range(1, run_time_sec + 1)]
    return pps


def sine(max_pps, run_time_sec):
    # So the pps values will flactuate between max_pps and 0:
    pps_period = [int(max_pps * (sin(radians(i - 90)) + 1)/2) for i in
                  [0, 22.5, 45, 67.5, 90, 112.5, 135, 157.5, 180, 202.5, 225, 247.5, 270, 292.5, 315, 337.5]]

    # Extend the curve to cover the whole run_time_sec
    periods = run_time_sec / len(pps_period)
    modulo = run_time_sec % len(pps_period)
    pps = pps_period * periods + pps_period[:modulo]
    return pps


def deterministic_noise(max_pps, run_time_sec, seed_value):
    seed(seed_value)  # Running deterministic_noise() w/out changing the seed_value will always produce the same result

    # The last second of the test must have pps == max_pps, so:
    pps = [randint(0, max_pps) for _ in range(1, run_time_sec + 1)]
    return pps


CURVE_FUNCTIONS = {'constant': constant, 'linear': linear, 'quadratic': quadratic, 'sine': sine,
                   'noise': deterministic_noise}


if __name__ == "__main__":
    times = constant(100, 0, 60)
    print len(times)
    print times