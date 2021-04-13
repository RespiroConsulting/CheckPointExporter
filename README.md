# Custom Checkpoint Exporter
This exporter will connect to Checkpoint device and will fetch number of current VPN users in the checkpoint and status of CPU hardware.
There are two methods to visualise the data.
First one is exporting data to Prometheus server, and it will anticipate the data into metrics.
Second option is exposing data over HTTP (on specific port) (here we are using 9994). in this method exporter will expose all data over HTTP in prometheus data format.

##Execution
Populate the user_credentials.yaml file with Checkpoint USERNAME and PASSWORD along with Checkpoint device name and login page url.

A. If you want to run the exporter using Prometheus client library you have to execute the following command:
```bash
    
```
B. If you want to run the script using python command line. Firstly you have to install following python modules:
```bash
      pip install netmiko
      pip install paramiko
      pip install prometheus_client
   ```
Run "main.py" to execute the processing and visit port http://localhost:8000/ to visualise the data.

## Commands used to extract the data
```bash
    VPN users
    "fw tab -t userc_users -s" 
    
    CPU status data
    "cpstat os -f cpu" 
    
    Hardware environment variables
    "cpstat os -f sensors"
    
```
## Labels
```bash
        checkpoint_current_remote_users_count
        checkpoint_peak_users_count
        checkpoint_cpu_user_time_percentage
        checkpoint_cpu_system_time_percentage
        checkpoint_cpu_idle_percentage
        checkpoint_cpu_usage_percentage
        checkpoint_cpu_interrupts_per_second_count
        checkpoint_cpu_user_count_number
        checkpoint_cpu_temperature
        checkpoint_cpu_temperature_internal
        checkpoint_cpu_ddr_temperature
        checkpoint_cpu_wifi1_temperature
        checkpoint_cpu_voltage_3v3
        checkpoint_cpu_voltage_12v
        checkpoint_cpu_voltage_1v8
        checkpoint_cpu_voltage_0v9
        checkpoint_cpu_voltage_1v2
        checkpoint_cpu_voltage_1v2_SRM
```


## Tested Sample File
```bash
    device_type: checkpoint_gaia
    ip: 192.168.XXX.X
    username: XYZ
    password: ABC
    hostname: 192.168.XXX.X
```

## Contribution
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
