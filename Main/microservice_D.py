import zmq
from colorama import Fore

colors = {
    "error": Fore.RED,
    "success": Fore.GREEN,
    "default": Fore.RESET,
    "yellow": Fore.YELLOW,
    "blue": Fore.BLUE,
    "red": Fore.RED,
    "green": Fore.GREEN,
}

def main():
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5557")

    while True:
        if socket.recv_string() == "start":
            socket.send_string("confirm")
            text = socket.recv_string()
            socket.send_string("received")
            cat = socket.recv_string()

            socket.send_string(color(text, cat))

def color(text, cat):
    color = colors.get(cat, colors["default"])
    return f"{color}{text}{Fore.RESET}"

main()