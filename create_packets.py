#!/usr/bin/python
# -*- coding: utf-8 -*-

from scapy.all import *
from time import time

ICMP_DATA = "michail dot xirouchakis at gmail dot com " * 34


def _create_icmp_packets(src_ip, dst_ip, data=ICMP_DATA, timestamp=time()):
    """
    Returns an ICMP Echo Request with user-defined data and timestamp.
    """

    packet = IP(src=src_ip, dst=dst_ip)/ICMP()/data
    packet.time = timestamp
    return packet


CREATE_PACKET_TYPE = {'icmp': _create_icmp_packets}


def create_packets(src_ip, dst_ip, list_of_timestamps, packet_type='icmp'):
    """
    Returns a list of packets.
    """

    list_of_packets = []
    packet_function = CREATE_PACKET_TYPE[packet_type]

    print "Creating", packet_type, "packets..."
    for timestamp in list_of_timestamps:
        packet = packet_function(src_ip, dst_ip, timestamp=timestamp)
        list_of_packets.append(packet)

    return list_of_packets
