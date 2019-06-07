"""
@author: Okwudili Ezeme
@date: 2019-June-05
@topic: Decentralized chat framework using ZeroMQ
"""
import argparse
import os
from threading import Thread
import zmq
# not in stdlib, install it yourself using `pip install netifaces`
from netifaces import interfaces, ifaddresses, AF_INET

# portable for Python 2.x and 3.x
try:
    raw_input
except NameError:
    raw_input = input

# create the listener function


def subscriber(subnet):
    """
    @args:
        subnet: the masked part of the IP that is generic. X.Y.Z. of X.Y.Z.{1-254} is subnet
    """
    ctx = zmq.Context.instance()
    listener = ctx.socket(zmq.SUB)
    for index in range(1, 255):
        listener.connect(f"tcp://{subnet}.{index}:9000")
    listener.setsockopt(zmq.SUBSCRIBE, b'')
    while True:
        try:
            print(f'>>> received: {listener.recv_string()}')
        except (KeyboardInterrupt, zmq.ContextTerminated):
            break


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("interface", type=str,
                        help="network interface to use", choices=interfaces(),)
    parser.add_argument(
        "user", type=str, default=os.environ['USER'], nargs='?', help="User's username",)
    args = parser.parse_args()
    inet = ifaddresses(args.interface)[AF_INET]
    addr = inet[0]['addr']
    subnet = addr.rsplit('.', 1)[0]
    ctx = zmq.Context.instance()
    listen_thread = Thread(target=subscriber, args=(subnet,))
    listen_thread.start()
    broadcast = ctx.socket(zmq.PUB)
    broadcast.bind(f"tcp://{args.interface}")
    print(f'>>> Chat starting on {args.interface}:9000 {subnet}.*')
    while True:
        try:
            message = input()
            broadcast.send_string(f'>>> {args.user}, {message}')
        except KeyboardInterrupt:
            break
    broadcast.close(linger=0)
    ctx.term()


if __name__ == "__main__":
    main()
