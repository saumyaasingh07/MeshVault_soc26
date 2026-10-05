"""
Quick manual test — run this to see the config.py functions actually
working: creating defaults, saving/loading, updating a value, and
adding a peer alias.

How to run:
    python try_config.py
"""

import os
import tempfile
from cli.config import (
    load_config,
    save_config,
    get_defaults,
    set_default,
    add_peer_alias,
    get_peer_alias,
)

test_path = os.path.join(tempfile.gettempdir(), "meshvault_test_config.toml")

if os.path.exists(test_path):
    os.remove(test_path)

print("--- Step 1: Load config when no file exists yet ---")
config = load_config(test_path)
print("Defaults:", get_defaults(config))

print()
print("--- Step 2: Save it, then reload from disk ---")
save_config(config, test_path)
config = load_config(test_path)
print("Reloaded defaults:", get_defaults(config))

print()
print("--- Step 3: Change a default value (n = 7) ---")
set_default(config, "n", 7, test_path)
config = load_config(test_path)
print("Updated defaults:", get_defaults(config))

print()
print("--- Step 4: Add a peer alias ---")
add_peer_alias(config, "192.168.1.50", "alice-laptop", test_path)
config = load_config(test_path)
print("Alias for 192.168.1.50:", get_peer_alias(config, "192.168.1.50"))
print("Alias for unknown peer 10.0.0.9:", get_peer_alias(config, "10.0.0.9"))

print()
print("--- Raw file contents on disk ---")
with open(test_path, "r") as f:
    print(f.read())

print("Done.")
