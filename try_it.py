"""
Quick manual test — run this to see receive_shares() and
send_share_with_retry() actually working together.

How to run:
    python3 try_it.py
"""

import threading
import time
from network.transfer import receive_shares, send_share_with_retry

HOST = "127.0.0.1"  # localhost — sender and receiver both on your own machine
PORT = 5050

# --- Step A: start the receiver in the background ---
server_thread = threading.Thread(
    target=receive_shares,
    kwargs={"host": HOST, "port": PORT},
    daemon=True,
)
server_thread.start()

time.sleep(0.5)

# --- Step B: send one share to it, using your retry function ---
my_share = (1, b"hello world")
success = send_share_with_retry(HOST, PORT, my_share)

print("Did it work?", success)

time.sleep(0.5)
print("Done.")
