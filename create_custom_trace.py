#!/usr/bin/python
# -*- coding: utf-8 -*-

from scapy.all import *
from time import time
from math import sqrt


ICMP_DATA = "michail dot xirouchakis at gmail dot com " * 34
TEST_DURATION_SEC = 300


def create_icmp_pkt(src_ip, dst_ip, data=ICMP_DATA, timestamp=time()):
    """
    Returns an ICMP Echo Request with user-defined data and timestamp.
    """

    packet = IP(src=src_ip, dst=dst_ip)/ICMP()/data
    packet.time = timestamp
    return packet


def create_pkts(src_ip, dst_ip, max_pps, curve_type="constant"):
    """
    Returns a list of packets (ICMP Echo Requests). User must define the curve type (e.g., constant, linear, quadratic,
    bursts) and the maximum throughput (pps).
    """

    list_of_packets = []
    list_of_timestamps = create_timestamps(max_pps, curve_type)

    print "Creating ICMP Echo Requests."
    for timestamp in list_of_timestamps:
        packet = create_icmp_pkt(src_ip, dst_ip, timestamp=timestamp)
        list_of_packets.append(packet)

    return list_of_packets


def create_timestamps(max_pps, curve_type, runtime=TEST_DURATION_SEC):
    """
    Returns a list of timestamps (float; seconds since epoch).  User must define the curve type (e.g., constant, linear,
    quadratic, bursts) and the maximum throughput (pps).
    """

    # Check input variables
    if max_pps == 0:
        print "You set input parameter max_pps to", max_pps, ". This is invalid. Exiting..."
        sys.exit()
    if curve_type not in ["constant", "bursts", "linear", "quadratic", "sine"]:
        print "You set input parameter curve_type to", curve_type, ". This is invalid. Exiting..."
        sys.exit()

    print "Creating timestamps for generated packets. curve_type:", curve_type, ", Maximum throughput (pps):", max_pps
    start_time = time()
    list_of_timestamps = []

    if curve_type == "constant":
        interpacket_gap = 1.0 / max_pps

        for timestamp in range(0, runtime*max_pps):
            list_of_timestamps.append(start_time + (interpacket_gap*timestamp))

    elif curve_type == "bursts":
        interpacket_gap = 1.0 / max_pps

        # Don't send a single packet every other second.
        send_flag = False
        for timestamp in range(0, runtime*max_pps):

            if timestamp % max_pps == 0:
                # Flip the send_flag after each second.
                send_flag = not send_flag

            if send_flag:
                list_of_timestamps.append(start_time + (interpacket_gap*timestamp))

    elif curve_type == "linear":
        packets = range(1, max_pps+1)  # List will first element 1 and last element equal to max_pps

        for k, v in enumerate(packets):

            if v == 0:
                continue
            else:
                interpacket_gap = 1.0 / v

            for timestamp in range(0, v):  # Will not execute for timestamp equal to v
                list_of_timestamps.append(start_time + k + (interpacket_gap * timestamp))

    elif curve_type == "quadratic":
        # List will first element 1 and last element equal to max_pps
        packets = [i ** 2 for i in range(1, int(sqrt(max_pps))+1)]

        for k, v in enumerate(packets):

            if v == 0:
                continue
            else:
                interpacket_gap = 1.0 / v

            for timestamp in range(0, v):  # Will not execute for timestamp equal to v
                list_of_timestamps.append(start_time + k + (interpacket_gap * timestamp))

    elif curve_type == "sine":
        #packets = [int(ceil((sin(radians(i)) + 1) * 50)) for i in [0, 45, 90, 135, 180, 225, 270, 315]]
        packets_one_period = [50, 86, 100, 86, 50, 15, 0, 15]

        periods = runtime / len(packets_one_period)  # integer, so flooring float
        packets = packets_one_period * periods

        for k, v in enumerate(packets):

            if v == 0:
                continue
            else:
                interpacket_gap = 1.0 / v

            for timestamp in range(0, v):  # Will not execute for timestamp equal to v
                list_of_timestamps.append(start_time + k + (interpacket_gap * timestamp))

    return list_of_timestamps


def export_trace(packets_list, filename="trace_"+str(int(time()))+".pcap"):
    """
    Export trace as a pcap file.
    """

    print "Exporting trace to file:", filename
    wrpcap(filename, packets_list)


if __name__ == "__main__":
    export_trace(create_pkts("10.0.0.1", "10.0.0.2", 100, "sine"))
