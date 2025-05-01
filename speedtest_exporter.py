# from prometheus_client import start_http_server, Gauge
from prometheus_client import CollectorRegistry, Gauge, push_to_gateway
import speedtest
import time
import os

pushIp=os.getenv('PUSH_IP', 'No environment variable PUSH_IP set')
pushGateway = 'http://' + pushIp + ':9091'
jobName = 'internet_speed_test'
clientNameLabel = 'client_name'
clientNameValue = os.getenv('CLIENT_NAME', 'No environment variable CLIENT_NAME set')

def run_speed_test():
    s = speedtest.Speedtest(secure=True)
    s.get_best_server()
    download_speed = s.download()
    upload_speed = s.upload()
    ping = s.results.ping
#
    result_dict=s.results.dict()
    isp = result_dict['client']['isp']
    clientIp = result_dict['client']['ip']
#
    return download_speed, upload_speed, ping, isp, clientIp

def push_metrics(download, upload, ping, isp, clientIp):
    registry = CollectorRegistry()
    download_gauge = Gauge('speedtest_download_speed', 'Download speed in Mbps', labelnames=[clientNameLabel,'isp','client_ip'], registry=registry)
    upload_gauge = Gauge('speedtest_upload_speed', 'Upload speed in Mbps', labelnames=[clientNameLabel,'isp','client_ip'],registry=registry)
    ping_gauge = Gauge('speedtest_ping', 'Ping in milliseconds', labelnames=[clientNameLabel,'isp','client_ip'],registry=registry)
    download_gauge.labels(clientNameValue,isp,clientIp).set(download)
    upload_gauge.labels(clientNameValue,isp,clientIp).set(upload)
    ping_gauge.labels(clientNameValue,isp,clientIp).set(ping)
    push_to_gateway(pushGateway, job=jobName, registry=registry, grouping_key={'instance': clientNameValue})

def main():
    while True:
        try:
            download_speed, upload_speed, ping, isp, clientIp = run_speed_test()
            print(f"Download: {download_speed} Mbps, Upload: {upload_speed} Mbps, Ping: {ping} ms")
            push_metrics(download_speed, upload_speed, ping, isp, clientIp)
        except Exception as e:
            print(f"Error: {e}")
        
        time.sleep(15)

if __name__ == '__main__':
    main()