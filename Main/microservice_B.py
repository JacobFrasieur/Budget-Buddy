import json

import zmq
import os
import glob


def main():
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5555")

    while True:
        message = socket.recv_string()
        if message == "delete":
            socket.send_string("confirm")

        elif message == "confirmed":
            socket.send_string("requesting path")
            path = socket.recv_string()
            deletethis = os.path.join(path, "*.json")

            #Store filenames for deletion msg
            deleted_files = []

            for i in glob.glob(deletethis):
                os.remove(i)
                file = os.path.basename(i)
                deleted_files.append(file)

            #Farewell files
            socket.send_string(json.dumps(deleted_files))
main()