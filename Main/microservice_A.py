#Created by Emmanuel Murillo
import zmq
import json
import sys

def tally_expenses(budget_data):
    """
    Sum each expense category in budget_data['expenses']
    and return a dict of category → total (omitting zeros).
    """
    expenses = budget_data.get("expenses", {})
    totals = {}
    for category, entries in expenses.items():
        total = sum(v for v in entries.values() if isinstance(v, (int, float)))
        if total > 0:
            totals[category] = total
    return totals

def main():
    ctx = zmq.Context()
    sock = ctx.socket(zmq.REP)
    sock.bind("tcp://*:5554")
    # Raise a zmq.Again exception if no message in 1 second:
    sock.setsockopt(zmq.RCVTIMEO, 1000)
    print("📡  Listening on tcp://*:5555 … (Ctrl+C to quit)")

    try:
        while True:
            try:
                msg = sock.recv()  # will timeout after 1 second
            except zmq.Again:
                # no request arrived in 1 s — loop back so Ctrl+C is caught
                continue

            try:
                payload = json.loads(msg.decode("utf-8"))
                result = tally_expenses(payload)
                reply = json.dumps(result)
            except Exception as e:
                reply = json.dumps({"error": str(e)})

            sock.send_string(reply)

    except KeyboardInterrupt:
        print("\n🛑 KeyboardInterrupt received—shutting down…")

    finally:
        sock.close()
        ctx.term()
        sys.exit(0)

if __name__ == "__main__":
    main()
