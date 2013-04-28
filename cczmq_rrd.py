#!/usr/bin/env python3
__author__ = 'adam'

import zmq
import subprocess

context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("tcp://127.0.0.1:5555")
socket.setsockopt_string(zmq.SUBSCRIBE, "")

#count = 0

while True:
    #count += 1

    #print("=============", count, "==============================")
    data = socket.recv_json()
    phaseA = data['msg']['ch1']['watts']
    phaseB = data['msg']['ch2']['watts']
    phaseC = data['msg']['ch3']['watts']
    temp = data['msg']['tmpr']
    total = phaseA + phaseB + phaseC
    data_list = (total, phaseA, phaseB, phaseC, temp)
    #print(data_list)


    #perl "rrdtool update powertemp.rrd N:" . $total . ":" . $watts1 . ":" . $watts2 . ":" . $watts3 . ":" . $temp;
    rrd_args = "N:" + str(total) + ":" + str(phaseA) + ":" + str(phaseB) + ":" + str(phaseC) + ":" + str(temp)
    #print(rrd_args)
    subprocess.call(["rrdtool", "update", "/home/jack/currentcost/powertemp.rrd", rrd_args])