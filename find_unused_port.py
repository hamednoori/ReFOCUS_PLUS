from __future__ import division
import os
import ast
import sys
import subprocess
import signal
import socket
import logging
import thread
import time
import tempfile
import math
import random
import networkx as nx
from collections import defaultdict, deque
from math import log
import sumolib
from k_shortest_paths import k_shortest_paths
from optparse import OptionParser
from bs4 import BeautifulSoup
from collections import defaultdict
from decimal import Decimal
avgLengthall = 0
avgSpeedall = 0
dict_edgeRSUs = {}
list_predict = []
dict_lane ={}
listfN=[]
laneallgraph =[]
edgeallgraph =[]
edgeallsgraph =[]
visit_bfs =[]
dict_fc ={}
list_source ={}
list_present_network =[]
list_vehicle_set_route =[]
number_of_lane ={}
TMax=0
footprintList =[]
dict_footprint ={}
edgListLength =[]
edgListspeed = []
listcdm=[]
listtraveltime=[]
listNtraveltime=[]
tonodedict={}
listEdgeRSU = []
dict_road_conges_traffic_area={}
# We need to import Python modules from the $SUMO_HOME/tools directory
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("Environment variable SUMO_HOME not defined")
    
import traci

class UnusedPortLock:
    lock = thread.allocate_lock()

    def __init__(self):
        self.acquired = False

    def __enter__(self):
        self.acquire()

    def __exit__(self):
        self.release()

    def acquire(self):
        if not self.acquired:
            UnusedPortLock.lock.acquire()
            self.acquired = True

    def release(self):
        if self.acquired:
            UnusedPortLock.lock.release()
            self.acquired = False

def find_unused_port():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
    sock.bind(('127.0.0.1', 0))
    sock.listen(socket.SOMAXCONN)
    ipaddr, port = sock.getsockname()
    sock.close()
    
    return port
