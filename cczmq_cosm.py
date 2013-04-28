#!/usr/bin/env python3
__author__ = 'adam'

import zmq
import eeml
import eeml.datastream
import eeml.unit
import cosm

# parameters
API_KEY = cosm.APIKEY #'YOUR PERSONAL API KEY'
API_URL = cosm.APIURL


context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("tcp://127.0.0.1:5555")
socket.setsockopt_string(zmq.SUBSCRIBE, "")

while True:

    data = socket.recv_json()
    phaseA = data['msg']['ch1']['watts']
    phaseB = data['msg']['ch2']['watts']
    phaseC = data['msg']['ch3']['watts']
    temp = data['msg']['tmpr']

    pac = eeml.datastream.Cosm(API_URL, API_KEY)
    pac.update([
        eeml.Data(0, phaseA, tags=("power", "energy", "Phase A"), unit=eeml.unit.Watt()),
        eeml.Data(1, phaseB, tags=("power", "energy", "Phase B"), unit=eeml.unit.Watt()),
        eeml.Data(2, phaseC, tags=("power", "energy", "Phase C"), unit=eeml.unit.Watt()),
        eeml.Data(3, temp, tags=("temperature",), unit=eeml.unit.Celsius())
    ])
    #print(pac.geteeml())
    pac.put()


