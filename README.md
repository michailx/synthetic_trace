# synthetic_trace

Synthetic trace
=========
The aim of this project is to create a custom trace, i.e., a .pcap file, according to user input.
The user provides information such as the Source and Destination IPs, the type of traffic (e.g., ICMP Echo Request) as
well as the packet rate.
Regarding the packet rate, the user can define the actual traffic load curve (pps), e.g. a decaying sine curve.

Dependencies
----
The following two packages are mandatory for this project:
+ [Scapy][scapy_github]
+ [Numpy][numpy_installation_homepage]

Please make sure you have installed them before attempting to run this script.

Run
----
+ First compose a configuration file in JSON format. I have provided an example file,
[test-conf.json][conf_example_github]
+ Then run python script create_custom_trace.py with input arguments:
```python
./create_custom_trace.py <SOURCE_IP> <DESTINATION_IP> <PATH_TO_CONFIG_FILE> 
```

For example:
```python
./create_custom_trace.py 10.0.0.1 10.0.0.2 conf/test-conf.json 
```

Extending this work
----
The user can extend this work by:
+ adding more traffic load curves in file [curve_functions.py][curve_functions_github]
+ adding more traffic types in file [create_packets.py][create_packets_github]


TODO
----
List of things __TODO__:

x

Getting help
----
Please raise an issue on Github.

[scapy_github]: https://github.com/secdev/scapy
[numpy_installation_homepage]: https://www.scipy.org/install.html
[conf_example_github]: https://github.com/michailx/synthetic_trace/blob/master/conf/test-conf.json
[curve_functions_github]: https://github.com/michailx/synthetic_trace/blob/master/curve_functions.py
[create_packets_github]: https://github.com/michailx/synthetic_trace/blob/master/create_packets.py