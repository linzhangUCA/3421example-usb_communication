import sys
from time import time, ticks_ms, ticks_diff
import select

# SETUP
pico_messenger = select.poll()  # create a poll object 
pico_messenger.register(sys.stdin, select.POLLIN) # peek at serial port input
# Variables
tx_interval_ms = 100  # 10Hz
last_ms = ticks_ms()
msg_id = 0
print("Pico is ready...")

# LOOP
while True:
    # Transmit data (TX)
    now_ms = ticks_ms()
    if ticks_diff(now_ms, last_ms) >= tx_interval_ms:
        out_msg = f"[Pico, {now_ms}]: Hello, {msg_id}\n"
        sys.stdout.write(out_msg)  # main.py will send this to computer
        msg_id += 1
        last_ms = now_ms  # update last time stamp
    # Receive data (RX)
    is_waiting = pico_messenger.poll(0)  # check if data waitining in USB, timeout=0     
    if is_waiting:
        in_msg = sys.stdin.readline().strip()  # take out whitespaces
        if in_msg:
            print(f"Pico received: {in_msg}")  # debug only, will send to computer
