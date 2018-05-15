#!/usr/bin/python
# -*- coding: utf-8 -*-

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


def create_pkts(src_ip, dst_ip, pps):
    """
    Returns a list of packets (ICMP Echo Requests). Each packet is sent at the appropriate time so that the user-defined
    rate (pps) is met.
    """

    list_of_packets = []
    list_of_timestamps = create_timestamps(pps)

    print "Creating ICMP Echo Requests."
    for timestamp in list_of_timestamps:
        packet = create_icmp_pkt(src_ip, dst_ip, timestamp=timestamp)
        list_of_packets.append(packet)

    return list_of_packets


def create_timestamps(pps, runtime=TEST_DURATION_SEC):
    """
    Returns a list of timestamps (float; seconds since epoch). Consecutive timestamps are appropriately spaced so that
    the user-defined rate (pps) is met.
    """

    print "Creating timestamps for generated packets. User-defined pps is:", pps
    start_time = time()
    list_of_timestamps = []

    try:
        interpacket_gap = 1.0 / pps
    except ZeroDivisionError:
        print "You set input parameter pps to 0. This is invalid. Exiting..."
        sys.exit()

    for timestamp in range(0, runtime*pps):
        list_of_timestamps.append(start_time + (interpacket_gap*timestamp))

    return list_of_timestamps


def export_trace(packets_list, filename="trace_"+str(int(time()))+".pcap"):
    """
    Export trace as a pcap file.
    """

    print "Exporting trace to file:", filename
    wrpcap(filename, packets_list)


if __name__ == "__main__":
    export_trace(create_pkts("10.0.0.1", "10.0.0.2", 100))
