# Custom Checkpoint Exporter
This exporter will connect to Checkpoint device and will fetch number of current VPN users in the checkpoint and status of CPU hardware.
There are two methods to visualise the data.
First one is exporting data to Prometheus server, and it will anticipate the data into metrics.
Second option is exposing data over HTTP (on specific port) (here we are using 9994). in this method exporter will expose all data over HTTP in prometheus data format.

##Execution

### Prometheus client library should be installed in your machine

1. Make sure you are using the python 3.6 and newer version to run this exporter.
2. Only PyYAML 5.1 or over is supported with this exporter.
3. Install following python modules:
```bash
      pip3 install netmiko
      pip3 install paramiko
      pip3 install prometheus_client
   ```
(Tip: It should be installed using pip3 only which is compatible for python 3)

4. Populate the user_credentials.yaml file with Checkpoint's USERNAME and PASSWORD along with Checkpoint device name and login page url before running
```bash
    device_type: checkpoint_gaia
    ip: XXX.XXX.X.XXX
    username: XYZ
    password: ABC
    hostname: XXX.XXX.X.XXX
```
5. You have to put the admin Username and Password and Checkpoint IP address in this User_Credentials.yaml file.
6. Update the main.py with the correct location of user_credentials.yaml file.
7. Update the system IP address in main.py at start_http_server to display metrics
6. Run "main.py" to execute the processing and visit port http://localhost:9994/ to visualize the data.

###If you want to run the exporter using Prometheus client library and inspect the data in Grafana:

1. Create the chechkpoint.service file with following code
```bash
[Unit]
Description=Check Point service
Wants=network-online.target
After=network-online.target

[Service]
User=root
Group=root

ExecStart=/exact path where main.py located in your system/main.py \
         --config.file /exact path where user_credetials.yaml located in your system/user_credentials.yml

[Install]
WantedBy=multi-user.target
```

###Run the following commands to start the checkpoint service
```bash
sudo systemctl daemon-reload
sudo systemctl start checkpointexporter
sudo systemctl status checkpointexporter (to check the status)
```

1. Update the system IP address in main.py (at http.server command) to display metrics at http://your-ip:9994
2. If it configured correctly, the checkpointexporter status shows as running, you would be able to access http://your-ip:9994 and see the metrics.

###To configure this exporter in prometheus, add this address as one of the target to your prometheus.yml
```bash
  - job_name: 'CheckPoint'
    scrape_interval: 1m
    static_configs:
    - targets: ['your-ip:9994']
```
Restart prometheus service

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





## Contribution
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
MIT
