#First ensure iperf3 is installed in source and destination
sudo apt-get update
sudo apt-get install iperf3

#At the server (destination)
iperf3 -s  #This will cause a message called "Server listening on 5201"

#At the client (source)
iperf3 -c 10.45.0.5 -u -b 1M -t 10
#where 10.45.0.5 is the server (destination) IP address
# -u is UDP test
# -b setting the bandwidth to 1Mbps
# -t setting the duration of test to 10 seconds. 


#Traceroute will provide us with latency for the data transmission
#First install traceroute in the source and destination
sudo apt-get update
sudo apt-get install traceroute

#At the source machine (client), run the traceroute command with -U to indicate UDP packets. 
#The size can be changed (I did not test this) using the command traceroute -U -s 1200 10.45.0.9 where 1200 bytes of UDP packets will be sent
traceroute -U -f 2 -m 2 -p 33435 10.45.4.10

#Capture pcap files from a certain interfaces
sudo tcpdump -i ogstun -w ogstun_capture.pcap
sudo tcpdump -i enx06cf47ef69ee -w ue1_capture.pcap
sudo tcpdump -i enx2eece1f2eb75 -w ue2_capture.pcap
sudo tcpdump -i enxbe54d9f44211 -w ue3_capture.pcap

#Import pcap files from server to VM
scp praghur@pc716.emulab.net:/tmp/gnb1_mac.pcap /home/ubuntu/
scp praghur@pc716.emulab.net:/tmp/gnb1_n3.pcap /home/ubuntu/
scp praghur@pc714.emulab.net:/tmp/gnb2_mac.pcap /home/ubuntu/
scp praghur@pc714.emulab.net:/tmp/gnb2_n3.pcap /home/ubuntu/
scp praghur@pc715.emulab.net:/ogstun_capture.pcap /home/ubuntu/
scp praghur@pc715.emulab.net:/enp4s0f1_capture.pcap /home/ubuntu/
scp praghur@pc716.emulab.net:enp4s0f1_gnb1.pcap /home/ubuntu/
scp praghur@pc714.emulab.net:enp4s0f1_gnb2.pcap /home/ubuntu/
scp praghur@ota-nuc3.emulab.net:ue1_capture.pcap /home/ubuntu/
scp praghur@ota-nuc4.emulab.net:ue2_capture.pcap /home/ubuntu/

#To copy from local VM to remote server --> Do thi in the local VM
scp SNRcalc.py praghur@pc06-fort.emulab.net:/tmp/

