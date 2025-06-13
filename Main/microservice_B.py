import json
import zmq
import os
import glob

#Microservice that handles deletion of all budgets

def main():
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5555")
    print("✅  Listening on tcp://*:5555 … (Ctrl+C to quit)")

    while True:
        message = socket.recv_string()
        if message == "delete":
            print("Received command to delete")
            socket.send_string("confirm")

        elif message == "confirmed":
            print("Received confirmation")
            socket.send_string("requesting path")
            path = socket.recv_string()
            print("Received path: " + path)
            deletethis = os.path.join(path, "*.json")

            #Store filenames for deletion msg
            deleted_files = []

            #Find and delete all files that match deletethis pattern. Append them to our deleted files list
            for i in glob.glob(deletethis):
                os.remove(i)
                file = os.path.basename(i)
                deleted_files.append(file)

            #Farewell files
            print("Sending deleted files: " + str(deleted_files))
            socket.send_string(json.dumps(deleted_files))

main()