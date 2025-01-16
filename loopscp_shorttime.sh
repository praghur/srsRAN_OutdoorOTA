#!/bin/bash

# Function to run traceroute 40 times randomly within an hour and write results to a CSV file
run_traceroute() {
  for i in {1..3}
  do
    result=$(traceroute -U -f 2 -m 2 -p 33435 10.45.2.10)
    echo "$(date), $result" >> traceroute_results.csv
    sleep 1  # Sleep for a random time between 30 and 120 seconds
  done
}

# Initialize the CSV file with headers
echo "Timestamp, Traceroute Result" > traceroute_results.csv

# Run the traceroute function every hour for 24 hours
for i in {1..2}
do
  run_traceroute
  sleep 2  # Wait for an hour before the next set of runs
done
