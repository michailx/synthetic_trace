#!/usr/bin/python
# -*- coding: utf-8 -*-

from curve_functions import *
from scapy.all import *
from time import time

ICMP_DATA = "michail dot xirouchakis at gmail dot com " * 34
TEST_DURATION_SEC = 300
CURVE_TYPES = {'constant': constant, 'linear': linear, 'quadratic': quadratic, 'sine': sine,
               'noise': deterministic_noise}


def create_icmp_pkt(src_ip, dst_ip, data=ICMP_DATA, timestamp=time()):
    """
    Returns an ICMP Echo Request with user-defined data and timestamp.
    """

    packet = IP(src=src_ip, dst=dst_ip)/ICMP()/data
    packet.time = timestamp
    return packet


def create_pkts(src_ip, dst_ip, max_pps, curve_type='constant'):
    """
    Returns a list of packets (ICMP Echo Requests).
    """

    list_of_packets = []

    list_of_timestamps = _create_timestamps(CURVE_TYPES[curve_type], max_pps)

    print "Creating ICMP Echo Requests."
    for timestamp in list_of_timestamps:
        packet = create_icmp_pkt(src_ip, dst_ip, timestamp=timestamp)
        list_of_packets.append(packet)

    return list_of_packets


def _create_timestamps(curve_function, max_pps, start_time=time(), run_time=TEST_DURATION_SEC):
    """
    Returns a list of timestamps (float; seconds since epoch).
    """
    # Check input variables
    if max_pps <= 0:
        print "You set input parameter max_pps to", max_pps, ". This is invalid. Exiting..."
        sys.exit()

    return curve_function(max_pps, start_time, run_time)


def export_trace(packets_list, filename="trace_"+str(int(time()))+".pcap"):
    """
    Export trace as a pcap file.
    """

    print "Exporting trace to file:", filename
    wrpcap(filename, packets_list)


if __name__ == "__main__":
    print "Running script", sys.argv[0]
    print "User provided", (len(sys.argv)-1), "command-line arguments:"

    if len(sys.argv) != 5:
        print str(sys.argv[1:])
        print "These arguments are invalid. Exiting..."
        sys.exit()

    user_input = {'src_ip': sys.argv[1], 'dst_ip': sys.argv[2], 'max_pps': int(sys.argv[3]), 'curve_type': sys.argv[4]}
    print "* Source IP:", user_input['src_ip']
    print "* Destination IP:", user_input['dst_ip']
    print "* Maximum Throughput (pps):", user_input['max_pps']
    print "* Curve:", user_input['curve_type']

    if user_input['curve_type'] not in CURVE_TYPES.keys():
        print "Only supporting curves", CURVE_TYPES.keys(), ". Exiting..."
        sys.exit()

    export_trace(create_pkts(**user_input), "trace_"+str(user_input['curve_type'])+"_"+str(int(time()))+".pcap")
