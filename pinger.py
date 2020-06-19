from concurrent.futures import ProcessPoolExecutor, as_completed
import csv
import pyping

# Simple Function that return 0 if ping is ok and 1 if is not
# pyping from https://github.com/certator/pyping/blob/master/pyping/core.py is used
def ping_device(device):
    r = pyping.ping(device, timeout=100, count=2, packet_size=44)
    return (device, r.ret_code)

# Sample function that pings hosts from the list in Separate Processes  ( simultaneously)
# concurrent.futures is used
def ping_devices(devices,workers):
    future_list = []
    device_list = []
    with ProcessPoolExecutor(max_workers=workers) as executor:

        for device in devices:
            future = executor.submit(ping_device, device)
            future_list.append(future)
        for f in as_completed(future_list):
            device_list.append(f.result())
    return device_list

if __name__ == '__main__':
    ok_hosts = []
    nok_hosts = []
    hosts = []

    #Load some hosts list
    with open('hosts.csv') as file:
        devices = csv.reader(file)
        for device in devices:
            hosts.append(device[0].strip())

    # Ping hosts from the list with 100 workers
    device_list = ping_devices(hosts,100)

    # Generate  2 lists with Ok and Nok hosts
    for device in device_list:
        if device[1] == 0:
            ok_hosts.append(device[0])
        else:
            nok_hosts.append(device[0])

    print("Failed hosts", nok_hosts)
    print("Ok hosts", ok_hosts)