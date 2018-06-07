#!/usr/bin/python
# -*- coding: utf-8 -*-

from curve_functions import *
import numpy
from scapy.all import *
from time import time

ICMP_DATA = "michail dot xirouchakis at gmail dot com " * 34
TEST_DURATION_SEC = 300


def create_icmp_pkt(src_ip, dst_ip, data=ICMP_DATA, timestamp=time()):
    """
    Returns an ICMP Echo Request with user-defined data and timestamp.
    """

    packet = IP(src=src_ip, dst=dst_ip)/ICMP()/data
    packet.time = timestamp
    return packet


def _create_pkts(src_ip, dst_ip, list_of_timestamps):
    """
    Returns a list of packets (ICMP Echo Requests).
    """

    list_of_packets = []

    print "Creating ICMP Echo Requests."
    for timestamp in list_of_timestamps:
        packet = create_icmp_pkt(src_ip, dst_ip, timestamp=timestamp)
        list_of_packets.append(packet)

    return list_of_packets


def _timeseries_to_timestamps(list_of_pps, start_time=time()):
    """
    Returns a list of floats; each element in this list is a packet's timestamp since start_time.

    The function has two input arguments. list_of_pps is a list of integers; each element in this list is number of
    packets during that second. Optional start_time is the timestamp of the first packet, set to current time since
    Epoch by default.
    """
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

    print "Exporting trace to file:", filename
    wrpcap(filename, packets_list)


def user_defined_series():
    # FIXME: As far as defining the individual signals, I need to provide a better UI to the end-user

    # Here I just start the series with a periodic signal (sine) and some noise, and include a linear trend after 60 sec

    s1 = numpy.array(sine(20, TEST_DURATION_SEC))
    s2 = numpy.array(deterministic_noise(5, TEST_DURATION_SEC))
    # 60 seconds later
    s3 = numpy.array([0]*60 + linear(20, TEST_DURATION_SEC-60))  # Add zeros as padding

    additive_curve = s1 + s2 + s3

    # FIXME: I will add 1 packet to all time slots in order to avoid zeroes in multiplicative mode.
    ones = numpy.array([1]*TEST_DURATION_SEC)
    s1 += ones
    s2 += ones
    s3 += ones
    multiplicative_curve = s1 * s2 * s3

    return additive_curve, multiplicative_curve


if __name__ == "__main__":
    print "Running script", sys.argv[0]
    print "User provided", (len(sys.argv)-1), "command-line arguments:"

    if len(sys.argv) != 4:
        print str(sys.argv[1:])
        print "These arguments are invalid. Exiting..."
        sys.exit()

    user_input = {'src_ip': sys.argv[1], 'dst_ip': sys.argv[2], 'max_pps': int(sys.argv[3])}
    print "* Source IP:", user_input['src_ip']
    print "* Destination IP:", user_input['dst_ip']
    print "* Maximum Throughput (pps):", user_input['max_pps']

    current_time = time()

    # User defined series; see function user_defined_series()
    additive_curve, multiplicative_curve = user_defined_series()

    # Composition Mode
    # Additive
    timestamps = _timeseries_to_timestamps(additive_curve, current_time)
    export_trace(_create_pkts(user_input['src_ip'], user_input['dst_ip'], timestamps),
                 "trace_additive_"+str(int(current_time))+".pcap")

    # Multiplicative:
    timestamps = _timeseries_to_timestamps(multiplicative_curve, current_time)
    export_trace(_create_pkts(user_input['src_ip'], user_input['dst_ip'], timestamps),
                 "trace_multiplicative_"+str(int(current_time))+".pcap")

