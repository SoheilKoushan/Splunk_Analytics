'''
Project Title: Mini Distributed Log Analytics System (Splunk)
Author(s): Soheil Koushan & Aaron Phipps
Date: 12/03/2026

Introduction:
Modern cloud infrastructure produces enormous volumes of server logs. These logs contain valuable signals about
performance, system health, and potential security threats. Large organizations rely on platforms such as Splunk and
Elastic Stack to collect, process, and analyze these logs across distributed systems.

Here, we will build a simplified distributed log analytics platform using Python. The system will simulate multiple
servers sending logs to a central analytics node, which will parse the data, store it using efficient data structure,
perform statistical analysis, detect anomalies, and visualise system behaviour.

The final system resembles a miniature version of production observability pipelines used in industry.

System Architecture:

Server Nodes (log stream)
    |
    |
    |
Log Collector
    |
    |
    |
Analytics Engine
    |
    |
    |
Visualization Dashboard

Simply, servers generate logs, Collector receives them, and Analytics processes them.

Example log format:
timestamp, server_id, ip, endpoint, status, response_time
2026-03-23T18:27:30, server1, 192.168.1.3, /api/data, 200, 0.145
'''

# Python log generator
import random
import datetime

servers = ["server1", "server2", "server3"]
ips = ["192.168.0.2", "192.168.0.5", "10.0.0.8", "172.16.0.1"]
pages = ["/", "/login", "/api/data", "/products"]
status = [200, 200, 200, 404, 500]

with open("distributed_logs.csv", "w") as f:
    for i in range(10000):
        time = (datetime.datetime.now() + datetime.timedelta(minutes=random.uniform(-10,10))).isoformat()
        server = random.choice(servers)
        ip = random.choice(ips)
        page = random.choice(pages)
        code = random.choice(status)
        response = round(random.uniform(0.05,1.2),3)

        f.write(f"{time}, {server}, {ip}, {page}, {code}, {response}\n")

# Log Collector
import pandas as pd
columns = ["time", "server", "ip", "endpoint", "status", "response"]
df = pd.read_csv("distributed_logs.csv", names=columns)
print(df.head())

# Data structures for Fast Queries
'''
As those logs become massive, we must index them efficiently.
So, our goal is to create fast lookup structures.
'''
from collections import defaultdict
ip_index = defaultdict(list)

for i, row in df.iterrows():
    ip_index[row["ip"]].append(i)

# Server Performance Metrics (compute system health metrics)
# 1- average response time per server
server_perf = df.groupby("server")['response'].mean()

# 2- error rate
error_rate = df[df['status'] >= 500].shape[0] / df.shape[0]

# 3- endpoint popularity
endpoint_count = df['endpoint'].value_counts()

# Statistical Anomaly Detection
'''
The goal is to detect unusual system behaviour
the method we are using is a z index
z = x - mu / sigma
'''

mean = df['response'].mean()
std = df['response'].std()

df['zscore'] = (df['response'] - mean) / std
anomalies = df[abs(df['zscore']) > 3]


'''
Time Series Traffic Analysis
(analyse server load patterns)
'''
df['time'] = pd.to_datetime(df['time'])
traffic = df.set_index('time').resample('1Min').count()
print(traffic)

import matplotlib.pyplot as plt
traffic['ip'].plot()
plt.title("Traffic per Minute")
deltaT = datetime.timedelta(minutes=5)
plt.xlim(df['time'].min() - deltaT,df['time'].max() + deltaT)
plt.show()