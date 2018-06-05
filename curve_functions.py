#!/usr/bin/python
# -*- coding: utf-8 -*-

from math import sin
from math import radians
from random import randint
from random import seed

SEED_VALUE = 1337  # The value itself is not significant. What is significant is that it's the same for
# all calls of function deterministic_noise()


def constant(pps, start_time, run_time_sec):
    timestamps = []
    interpacket_gap = 1.0 / pps

    for pkt_index in range(0, run_time_sec * pps):
        timestamps.append(start_time + (interpacket_gap * pkt_index))

    return timestamps


def linear(max_pps, start_time, run_time_sec):
    timestamps = []

    # The last second of the test must have pps == max_pps, so:
    pps = [(i * max_pps) / run_time_sec for i in range(1, run_time_sec + 1)]

    for timeslot, pkts in enumerate(pps):
        if pkts == 0:
            continue

        # Each timeslot (which equals 1 second) has a different interpacket_gap equal to:
        interpacket_gap = 1.0 / pkts

        for pkt_index in range(0, pkts):
            timestamps.append(start_time + timeslot + (pkt_index * interpacket_gap))

    return timestamps


def quadratic(max_pps, start_time, run_time_sec):
    timestamps = []

    # The last second of the test must have pps == max_pps, so:
    pps = [int(((i / float(run_time_sec)) ** 2) * max_pps) for i in range(1, run_time_sec + 1)]

    for timeslot, pkts in enumerate(pps):
        if pkts == 0:
            continue

        # Each timeslot (which equals 1 second) has a different interpacket_gap equal to:
        interpacket_gap = 1.0 / pkts

        for pkt_index in range(0, pkts):
            timestamps.append(start_time + timeslot + (pkt_index * interpacket_gap))

    return timestamps


def sine(max_pps, start_time, run_time_sec):
    timestamps = []

    # So the pps values will flactuate between max_pps and 0:
    pps_period = [int(max_pps * (sin(radians(i - 90)) + 1)/2) for i in
                  [0, 22.5, 45, 67.5, 90, 112.5, 135, 157.5, 180, 202.5, 225, 247.5, 270, 292.5, 315, 337.5]]

    # Extend the curve to cover the whole run_time_sec
    periods = run_time_sec / len(pps_period)
    modulo = run_time_sec % len(pps_period)
    pps = pps_period * periods + pps_period[:modulo]

    for timeslot, pkts in enumerate(pps):
        if pkts == 0:
            continue

        # Each timeslot (which equals 1 second) has a different interpacket_gap equal to:
        interpacket_gap = 1.0 / pkts

        for pkt_index in range(0, pkts):
            timestamps.append(start_time + timeslot + (pkt_index * interpacket_gap))

    return timestamps


def deterministic_noise(max_pps, start_time, run_time_sec):
    timestamps = []

    seed(SEED_VALUE)  # Running deterministic_noise() w/out changing the SEED_VALUE will always produce the same result

    # The last second of the test must have pps == max_pps, so:
    pps = [randint(0, max_pps) for _ in range(1, run_time_sec + 1)]

    for timeslot, pkts in enumerate(pps):
        if pkts == 0:
            continue

        # Each timeslot (which equals 1 second) has a different interpacket_gap equal to:
        interpacket_gap = 1.0 / pkts

        for pkt_index in range(0, pkts):
            timestamps.append(start_time + timeslot + (pkt_index * interpacket_gap))

    return timestamps


if __name__ == "__main__":
    times = constant(100, 0, 60)
    print len(times)
    print times