# internet_metrics
Docker compose to setup internet speed exporter with prometheus and grafana to monitor and visualize

# requirements
docker

# STEP 1. build exporter
cd to cloned directory and run
```
docker build -t speedtest-exporter .
```
# STEP 2. run container
PUSH_IP : IP address or hostname of the prometheus push gateway
CLIENT_NAME : A label to identify the client
```
docker run -d --restart unless-stopped speedtest-exporter -s <PUSH_IP> -n <CLIENT_NAME>
```

For example,
```
docker run -d --restart unless-stopped speedtest-exporter -s 1.2.3.4 -n Bob
```
# STEP 3. access grafana dashboard in browser
Access http://<PUSH_IP>:3000 with provided password.
Check internet-speed dashboard in grafana  

# STEP 4. stop containers
```
docker stop <container-id>
```

# How it looks

![internet speed dashboard](files/internet_metrics_screenshot.jpg)

# Disclaimer
The metrics are collected using speedtest-cli. All metrics are not entirely reliable as per the details in:
https://github.com/sivel/speedtest-cli
