#!/bin/bash

# Define the list of nodes
nodes=("pc741" "pc06-fort" "ota-x310-1" "pc09-fort" "ota-x310-2" "ota-nuc1" "ota-nuc2")

# SSH username and hostname
username="praghur"
host_suffix=".emulab.net"

# Loop through the nodes and open terminal windows with SSH commands
for node in "${nodes[@]}"; do
    gnome-terminal -- bash -c "ssh -o StrictHostKeyChecking=no ${username}@${node}${host_suffix}; exec bash" &
done
