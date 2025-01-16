#Traceroute will provide us with latency for the data transmission
#First install traceroute in the source and destination
sudo apt-get update
sudo apt-get install traceroute

#At the source machine (client), run the traceroute command with -U to indicate UDP packets. 
#The size can be changed (I did not test this) using the command traceroute -U -s 1200 10.45.0.9 where 1200 bytes of UDP packets will be sent
traceroute -U -f 2 -m 2 -p 33435 10.45.2.10

#Capture pcap files from a certain interfaces
sudo tcpdump -i ogstun -w ogstun_capture.pcap
sudo tcpdump -i enx06cf47ef69ee -w ue1_capture.pcap
sudo tcpdump -i enx2eece1f2eb75 -w ue2_capture.pcap

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

