#!/usr/bin/python3
from netmiko import ConnectHandler, ssh_exception
from paramiko.ssh_exception import SSHException
from prometheus_client import start_http_server, Summary
from prometheus_client import Gauge
from prometheus_client.core import GaugeMetricFamily, REGISTRY, CounterMetricFamily
import random
from getpass import getpass
import yaml
import sys
import os

# get credentials
os.system("python -m pip install –upgrade pip")
os.system("pip3 install netmiko")
os.system("pip3 install paramiko")
os.system("pip3 install prometheus_client")

with open(r'user_credentials.yaml') as yamlfile:
    user_credentials = yaml.load(yamlfile, Loader=yaml.FullLoader)
    # print(user_credentials)
    device_type = user_credentials['Details']['device_type']
    ip = user_credentials['Details']['ip']
    user = user_credentials['Details']['username']
    passwd = user_credentials['Details']['password']
    host_name = user_credentials['Details']['hostname']

if __name__ == '__main__':

    # define gauges
    checkpoint_current_remote_users_count = Gauge('checkpoint_current_remote_users_count',
                                                       'This is gauge to get Current Remote Users in Checkpoint')
    checkpoint_peak_users_count = Gauge('checkpoint_peak_users_count',
                                            'This is gauge to get Peak number of users in Checkpoint')
    checkpoint_cpu_user_time_percentage = Gauge('checkpoint_cpu_user_time_percentage',
                                                'This is gauge to get cpu user time in percentage of Checkpoint')
    checkpoint_cpu_system_time_percentage = Gauge('checkpoint_cpu_system_time_percentage',
                                                'This is gauge to get system time in percentage of Checkpoint')
    checkpoint_cpu_idle_percentage = Gauge('checkpoint_cpu_idle_time_percentage',
                                                'This is gauge to get cpu Idle time in percentage of Checkpoint')
    checkpoint_cpu_usage_percentage = Gauge('checkpoint_cpu_usage_percentage',
                                                'This is gauge to get cpu usage in percentage of Checkpoint')
    checkpoint_cpu_interrupts_per_second_count = Gauge('checkpoint_cpu_interrupts_per_second_count',
                                                'This is gauge to get cpu interrupts per second count of Checkpoint')
    checkpoint_cpu_user_count_number = Gauge('checkpoint_cpu_user_count_number',
                                                'This is gauge to get cpu number in count of Checkpoint')
    checkpoint_cpu_temperature = Gauge('checkpoint_cpu_temperature',
                                             'This is gauge to get cpu temperature in celsius of Checkpoint')
    checkpoint_cpu_temperature_internal = Gauge('checkpoint_cpu_temperature_internal',
                                             'This is gauge to get cpu internal temperature in celsius of Checkpoint')
    checkpoint_cpu_ddr_temperature = Gauge('checkpoint_cpu_ddr_temperature',
                                             'This is gauge to get cpu ddr temperature in celsius of Checkpoint')
    checkpoint_cpu_wifi1_temperature = Gauge('checkpoint_cpu_wifi1_temperature',
                                           'This is gauge to get cpu WiFi1 temperature in celsius of Checkpoint')
    checkpoint_cpu_voltage_3v3= Gauge('checkpoint_cpu_voltage_3v3',
                                       'This is gauge to get cpu voltage of 3v3 in volt of Checkpoint')
    checkpoint_cpu_voltage_12v = Gauge('checkpoint_cpu_voltage_12v',
                                       'This is gauge to get cpu voltage of 12v in volt of Checkpoint')
    checkpoint_cpu_voltage_1v8 = Gauge('checkpoint_cpu_voltage_1v8',
                                       'This is gauge to get cpu voltage of 1v8 in volt of Checkpoint')
    checkpoint_cpu_voltage_0v9 = Gauge('checkpoint_cpu_voltage_0v9',
                                       'This is gauge to get cpu voltage of 0v9 in volt of Checkpoint')
    checkpoint_cpu_voltage_1v2 = Gauge('checkpoint_cpu_voltage_1v2',
                                       'This is gauge to get cpu voltage of 1v2 in volt of Checkpoint')
    checkpoint_cpu_voltage_1v2_SRM = Gauge('checkpoint_cpu_voltage_1v2_SRM',
                                       'This is gauge to get cpu voltage of 1v2 SRM in volt of Checkpoint')

    start_http_server(9994)

    while True:

        # define connector

        fwext = {
            'device_type': device_type,
            'ip': ip,
            'username': user,
            'password': passwd,
        }

        hostname = host_name

        # try to connect

        try:
            net_connect = ConnectHandler(**fwext)
        except SSHException as e:  # replace with netmiko exception
            print("Can't connect to device {},\n{}".format(hostname, e))
            sys.exit(1)
        except ssh_exception.NetMikoTimeoutException as e:
            print("Timeout for device {},\n{}".format(hostname, e))
            sys.exit(1)
        except ssh_exception.NetMikoAuthenticationException as e:
            print("Invalid Credentials for device {},\n{}".format(hostname, e))
            sys.exit(1)

        # send the command to the firewall and extract value

        vpn_users = net_connect.send_command("fw tab -t userc_users -s")
        vpn_users_lines = vpn_users.split('\n')
        current = 0
        peak = 0
        for line in vpn_users_lines:
            if 'NAME' in line:
                continue
            vars = line.split()
            current = vars[3]
            peak = vars[4]
            print(vpn_users)

            # print("Current Remote Users: ", current)
            # print("Peak number of users:", peak)

        checkpoint_cpu_status_command = net_connect.send_command("cpstat os -f cpu")
        cpu_status_lines = checkpoint_cpu_status_command.split('\n')
        cpu_user_time_percentage = 0
        cpu_system_time_percentage = 0
        cpu_usage_percentage = 0
        cpu_idle_time_percentage = 0
        cpu_queue_length_number = 0
        cpu_interrupts_per_sec_number = 0
        cpu_count_number = 0
        for line in cpu_status_lines:
            if 'CPU User Time' in line:
                vars = line.split()
                cpu_user_time_percentage = vars[4]
            if 'CPU System Time' in line:
                vars = line.split()
                cpu_system_time_percentage = vars[4]
            if 'CPU Idle Time' in line:
                vars = line.split()
                cpu_idle_time_percentage = vars[4]
            if 'CPU Usage' in line:
                vars = line.split()
                cpu_usage_percentage = vars[3]
            if 'CPU Interrupts/Sec' in line:
                vars = line.split()
                cpu_interrupts_per_sec_number = vars[2]
            if 'CPUs Number' in line:
                vars = line.split()
                cpu_count_number = vars[2]
        print(checkpoint_cpu_status_command)

        checkpoint_cpu_environment_command = net_connect.send_command("cpstat os -f sensors")
        checkpoint_cpu_environment_lines = checkpoint_cpu_environment_command.split('\n')
        cpu_temp = 0
        # ddr_temp = 0

        for line in checkpoint_cpu_environment_lines:
            # Temperature Sensors
            if 'CPU Temperature ' in line:
                vars = line.split()
                vars = line.split("|")
                cpu_temperature = vars[2]

            if 'CPU Temperature(internal)' in line:
                vars = line.split()
                vars = line.split("|")
                cpu_temperature_internal = vars[2]

            if 'DDR Temperature' in line:
                vars = line.split()
                vars = line.split("|")
                ddr_temperature = vars[2]

            if 'WIFI1 Temperature' in line:
                vars = line.split()
                vars = line.split("|")
                wifi1_temperature = vars[2]

            # Voltage Sensors
            if 'Voltage 3V3' in line:
                vars = line.split()
                vars = line.split("|")
                voltage_3v3 = vars[2]
            if 'Voltage 12V' in line:
                vars = line.split()
                vars = line.split("|")
                voltage_12v = vars[2]
            if 'Voltage 1V8' in line:
                vars = line.split()
                vars = line.split("|")
                voltage_1v8 = vars[2]
            if 'Voltage 0V9' in line:
                vars = line.split()
                vars = line.split("|")
                voltage_0v9 = vars[2]
            if 'Voltage 1V2' in line:
                vars = line.split()
                vars = line.split("|")
                voltage_1v2 = vars[2]
            if 'Voltage 1V2_SRM' in line:
                vars = line.split()
                vars = line.split("|")
                voltage_1V2_SRM = vars[2]


        print(checkpoint_cpu_environment_command)
        print(cpu_temperature)
        print(cpu_temperature_internal)
        print(ddr_temperature)
        print(wifi1_temperature)
        print(voltage_3v3)
        print(voltage_12v)
        print(voltage_1v8)
        print(voltage_0v9)
        print(voltage_1v2)
        print(voltage_1V2_SRM)
        # print(cpu_temp)

        # disconnect

        net_connect.disconnect()

        checkpoint_current_remote_users_count.set(current)
        checkpoint_peak_users_count.set(peak)
        checkpoint_cpu_user_time_percentage.set(cpu_user_time_percentage)
        checkpoint_cpu_system_time_percentage.set(cpu_system_time_percentage)
        checkpoint_cpu_idle_percentage.set(cpu_idle_time_percentage)
        checkpoint_cpu_usage_percentage.set(cpu_usage_percentage)
        checkpoint_cpu_interrupts_per_second_count.set(cpu_interrupts_per_sec_number)
        checkpoint_cpu_user_count_number.set(cpu_count_number)
        checkpoint_cpu_temperature.set(cpu_temperature)
        checkpoint_cpu_temperature_internal.set(cpu_temperature_internal)
        checkpoint_cpu_ddr_temperature.set(ddr_temperature)
        checkpoint_cpu_wifi1_temperature.set(wifi1_temperature)
        checkpoint_cpu_voltage_3v3.set(voltage_3v3)
        checkpoint_cpu_voltage_12v.set(voltage_12v)
        checkpoint_cpu_voltage_1v8.set(voltage_1v8)
        checkpoint_cpu_voltage_0v9.set(voltage_1v2)
        checkpoint_cpu_voltage_1v2.set(voltage_1v2)
        checkpoint_cpu_voltage_1v2_SRM.set(voltage_1V2_SRM)



