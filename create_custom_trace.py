#!/usr/bin/python
# -*- coding: utf-8 -*-

from curve_functions import *
from create_packets import *
from json import load
from json import dumps
from scapy.all import *
from time import time
import numpy


def _timeseries_to_timestamps(list_of_pps, start_time=time()):
    """
    Returns a list of floats; each element in this list is a packet's timestamp since start_time.

    The function has two input arguments. list_of_pps is a list of integers; each element in this list is number of
    packets during that second. Optional start_time is the timestamp of the first packet, set to current time since
    Epoch by default.
    """
    print "Calculating the timestamp of every single packet..."
    timestamps = []

    for timeslot, pkts in enumerate(list_of_pps):
        if pkts == 0:
            continue

        # Each timeslot (which equals 1 second) has a different interpacket_gap equal to:
        interpacket_gap = 1.0 / pkts

        for pkt_index in range(0, pkts):
            timestamps.append(start_time + timeslot + (pkt_index * interpacket_gap))

    return timestamps


def export_trace(packets_list, filename="trace_"+str(int(time()))+".pcap"):
    """
    Export trace as a pcap file.
    """

    print "Exporting trace to file:", filename, ". Please hold on..."
    wrpcap(filename, packets_list)

    print "Done!"


def read_config(conf_file):
    """
    Read configuration file (JSON) format. Returns a python dict with all keys and values found in the JSON file.
    """
    with open(conf_file, 'r') as f:

        try:
            conf_dict = load(f)
        except ValueError as ex:
            print "Error while loading JSON file,", conf_file, ". ERR:", ex, ". Exiting..."
            sys.exit()

    return conf_dict


def _create_timeseries(composition_mode, curve_components):
    """
    Combines all individual curves and returns a time series. Input argument composition_mode can be additive or
    multiplicative, whereas the curve_components dictionary contains all configuration parameter for each individual
    curve.
    """
    # First, I need to discover the highest/latest end time, so I know how much padding to add to each component.
    end_times = []
    for curve in curve_components:
        end_times.append(curve['end_time'])
    end_of_trace = max(end_times)

    # Second, get all components and add padding to each one:
    components = []
    for curve in curve_components:
        curve_function = CURVE_FUNCTIONS[curve['curve_type']]
        function_params = curve['params']
        function_params['run_time_sec'] = curve['end_time'] - curve['start_time']
        # I will assume that minimum start_time is 0.
        c = numpy.array([0]*curve['start_time'] +
                        curve_function(**function_params) +
                        [0]*(end_of_trace - curve['end_time']), dtype=numpy.uint64)
        components.append(c)

    # Third, compose all components into a single time series:
    # FIXME: This could probably be written in a better / more efficient way
    if composition_mode == "additive":
        result = numpy.zeros(end_of_trace, dtype=numpy.uint64)
        for c in components:
            result += c
    elif composition_mode == "multiplicative":
        ones = numpy.ones(end_of_trace, dtype=numpy.uint64)
        result = numpy.ones(end_of_trace, dtype=numpy.uint64)
        for c in components:
            # I will add 1 packet to all time slots in order to avoid zeroes in multiplicative mode.
            result *= (c + ones)
    else:
        print "Invalid composition mode:", composition_mode, ". Exiting..."
        sys.exit()

    return result

if __name__ == "__main__":
    print "Running script", sys.argv[0]
    print "User provided", (len(sys.argv)-1), "command-line arguments:"

    if len(sys.argv) != 4:
        print str(sys.argv[1:])
        print "These arguments are invalid. Exiting..."
        sys.exit()

    user_input = {'src_ip': sys.argv[1], 'dst_ip': sys.argv[2], 'path_to_conf_file': sys.argv[3]}
    print "* Source IP:", user_input['src_ip']
    print "* Destination IP:", user_input['dst_ip']
    print "* Path to configuration file:", user_input['path_to_conf_file']
    json_data = read_config(user_input['path_to_conf_file'])
    print "Read configuration file", user_input['path_to_conf_file'], "and found the following parameters:"
    print "* Type of traffic:", json_data['packet_type']
    print "* Curve composition mode:", json_data['composition_mode']
    print "* Components:", len(json_data['curve_components']), "curves"
    for curve in json_data['curve_components']:
        print "***", dumps(curve)

    current_time = time()
    timeseries = _create_timeseries(json_data['composition_mode'], json_data['curve_components'])

    print "Calculated PPS:", timeseries

    timestamps = _timeseries_to_timestamps(timeseries, current_time)
    export_trace(create_packets(user_input['src_ip'], user_input['dst_ip'], timestamps),
                 "trace_"+json_data['composition_mode']+"_"+str(int(current_time))+".pcap")

