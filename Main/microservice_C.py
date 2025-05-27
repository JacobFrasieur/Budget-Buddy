import zmq
import os
import json

#Microservice that handles memo creation

def main():
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5556")
    memos_folder = "Memos"
    filename = os.path.join(memos_folder, "memos.json")
    os.makedirs(memos_folder, exist_ok=True)

    while True:
        message = socket.recv_string()
        if message == "start":
            #Confirm and rec motiv memo from user in main program
            socket.send_string("confirm")
            motiv = socket.recv_string()

            #Create file if it does not exist
            if not os.path.exists(filename):
                with open(filename, "w") as memo:
                    json.dump({"motivations": []}, memo, indent=4)

            #Open file and write to it
            with open(filename, "r") as memo:
                open_memo = json.load(memo)
            open_memo["motivations"].append(motiv)

            #Save the file
            with open(filename, "w") as memo:
                json.dump(open_memo, memo, indent=4)

            socket.send_string("done")

main()