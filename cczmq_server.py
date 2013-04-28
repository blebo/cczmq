#!/usr/bin/env python3
__author__ = 'adam'

import serial
import xml.etree.ElementTree as etree
import zmq

SERIAL_PORT = "/dev/ttyUSB0"

def parse(data):
    """
    Parse 'XML like' binary string and return a dict of all attributes.
    """
    datastring = data.decode("ascii").rstrip()

    result = {}

    msg = etree.fromstring(datastring)
    result['msg'] = {}
    for section in msg:

        if section.tag == "date":
            result['msg'][section.tag] = {}
            for tag in section:
                result['msg'][section.tag][tag.tag] = int(tag.text)

        elif section.tag == "src":
            result['msg'][section.tag] = {}
            for tag in section:
                if tag.tag == "name":
                    result['msg'][section.tag][tag.tag] = tag.text
                elif tag.tag == "sver":
                    result['msg'][section.tag][tag.tag] = float(tag.text)
                else:
                    result['msg'][section.tag][tag.tag] = int(tag.text)

        elif section.tag in ["ch"+str(n+1) for n in range(9)]:
            result['msg'][section.tag] = {}
            for tag in section:
                value = int(tag.text)
                if tag.tag == "watts" and value != "":
                    result['msg'][section.tag][tag.tag] = value
                else:
                    result['msg'][section.tag][tag.tag] = None

        elif section.tag == "tmpr":
            result['msg'][section.tag] = float(section.text)

        elif section.tag == "hist":
            result['msg'][section.tag] = {}
            for tag in section:
                if tag.tag == "hrs":
                    result['msg'][section.tag][tag.tag] = {}
                    for subtag in tag:
                        result['msg'][section.tag][tag.tag][subtag.tag] = float(subtag.text)
                elif tag.tag in ["days", "mths", "yrs"]:
                    result['msg'][section.tag][tag.tag] = {}
                    for subtag in tag:
                        result['msg'][section.tag][tag.tag][subtag.tag] = int(subtag.text)

    return result

if __name__ == "__main__":


    cc = serial.Serial(SERIAL_PORT, 9600, timeout=10)

    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.bind("tcp://*:5555")

    while cc:

        xml = cc.readline()

        if xml:
            data = parse(xml)
            socket.send_json(data)

            #print("================")
            #print(xml)
            #print("++++")
            #print(data)


    cc.close()
