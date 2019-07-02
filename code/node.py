"""
@author: Okwudili Ezeme
@date: 2019-June-27
This will run on each of the devices to be connected to the access point
"""
import os
import zmq
import time
import logging
import socket
from .pyre_event import PyreEvent
from pyre import Pyre

class Agent(object):
    """
    A class object that represents each device in the network"""
    def __init__(self, name, ctx, *args, **kwargs):
        return super().__init__(*args, **kwargs)
        self.name = name
        self.context = ctx

    def device(self):
        pid = os.getpid()
        hostname = socket.gethostname()
        hostID = hostname+str(pid)
        node = pyre.Pyre(name=self.name,ctx = self.context)
        node.set_header('hostname',hostID)
        node.start()
        return node

    def router_table(self):
        pass

    def send_recv(self):
        node = self.device()