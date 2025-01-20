**GitHub profile**

•	A GitHub profile is now created for outdoor experimentation - praghur/srsRAN_OutdoorOTA. A request is sent to dustin.314@gmail.com to be added as a collaborator for this profile, in case you need to make any edits to the profile. 

•	The main branch of the profile consists of profile.py for creating the experimental profile in POWDER. It consists of 2 gNBs, 2 UEs, and 1 CN.

•	There is a startup script called ‘startup.sh’ in the profile to setup all the nodes in the system including gNBs, UEs, and CN. This would also be updated depending on the name and make of the outdoor nodes. 
Open5gs deployment 

•	The ‘/bin/deploy-open5gs.sh’ script is used to deploy the core network. The UE credentials are added to the database in this script. In outdoor laboratory, slices are no longer required to connect the UEs to the respective gNB. The profile is kept with slicing to allow initial testing with indoor laboratory equipment. 

•	The slice is assigned to each UE differently so that the UE gets attached to the respective gNB. 
o	UE1  IP is 10.45.1.10 
o	UE2  IP is 10.45.2.10 

**gNB deployment**

•	The script ‘/bin/deploy-srsran-x310.sh’ scrip is used to deploy the base stations. It still has the same script for x310. Setup is different for outdoor lab. Dustin to provide details. 

------------------------------------------------------------------------------------------------------------------	
•	When profile is setup in POWDER, the startup takes care of until this step. 
------------------------------------------------------------------------------------------------------------------	

**UE Nodes: Update routing table**

•	For sending a packet from UE1 (10.45.1.10) to UE2 (10.45.2.10) via core network, we need to do the following:
o	In UE1 node, run the command: sudo ip route add 10.45.2.10 via 10.45.0.1
o	In UE2 node, run the command: sudo ip route add 10.45.1.10 via 10.45.0.1

•	Use the script ‘/bin/routing.script’ to copy these routing commands for the UEs. This script needs to be run before we start running any experiment. 
Emulate core network delay

•	Since core network is a computer server, a 2ms delay in the core network is emulated by adding it externally to the node. 

•	In the core network node, run the following command: sudo tc qdisc add dev ogstun root netem delay 1ms.

**(Optional) using start-xxx.sh script**

•	Some scripts located in /bin/ are /bin/start-cn.sh, /bin/start-gnb1.sh, /bin/start-gnb2.sh, and bin/start-ue.sh. Running these scripts are optional as this script uses tmux to split the window into multiple parts. This can be skipped if not required. 

•	Note that, /bin/start-cn.sh script adds the core network delay in Line #6. You can skip manually adding the core network delay if you plan to run the /bin/start-cn.sh script. 

**DL UL Configuration**


•	It is defined for a x300 for now for gNB1 and gNB2. 
•	The DL-UL configuration is changed to 6 DL – 1 S – 3 UL as shown in Line 36 to Line 41 of gnb_x310_2.yml. 

_tdd_ul_dl_cfg:
    dl_ul_tx_period: 10
    nof_dl_slots: 6
    nof_dl_symbols: 0
    nof_ul_slots: 3
    nof_ul_symbols: 0_
 
•	I have changed the QoS to 5GI of 5 that allows lower packet delay budget of 100 ms, priority level of 10, and packet error rate of 10e-6. Check indoor lab with different QCI. 

•	The next steps for setting and running the experiment is shown in \bin\test.sh

•	Install traceroute in the UE nodes 

sudo apt-get update
sudo apt-get install traceroute

•	Start tcpdump in certain interface of the system such as UEs and core network. 
#Capture pcap files from a certain interfaces
sudo tcpdump -i ogstun -w ogstun_capture.pcap
sudo tcpdump -i enx06cf47ef69ee -w ue1_capture.pcap
sudo tcpdump -i enx2eece1f2eb75 -w ue2_capture.pcap

------------------------------------------------------------------------------------------------------------------	
•	With this step, we are ready to run the experiment 
------------------------------------------------------------------------------------------------------------------	

**Running the experiment **

•	Now, we run the experiment by sending 3 UDP packets across the network
traceroute -U -f 2 -m 2 -p 33435 10.45.2.10
_Measure at application layer using wireshark_

•	Run the script for running this script 

•	At the end of the experiment, import the pcap files from the server to the host
#Import pcap files from server to VM
scp praghur@pc7XX.emulab.net:/tmp/gnb1_mac.pcap /home/ubuntu/
scp praghur@pc7XX.emulab.net:/tmp/gnb1_n3.pcap /home/ubuntu/
scp praghur@pc7XX.emulab.net:/tmp/gnb2_mac.pcap /home/ubuntu/
scp praghur@pc7XX.emulab.net:/tmp/gnb2_n3.pcap /home/ubuntu/
scp praghur@pc7XX.emulab.net:/ogstun_capture.pcap /home/ubuntu/
scp praghur@ota-nuc1.emulab.net:ue1_capture.pcap /home/ubuntu/
scp praghur@ota-nuc2.emulab.net:ue2_capture.pcap /home/ubuntu/

•	We need to repeat this experiment for several runs to measure the latency due to the variability. The script ‘\bin\loopscript.sh’ is created such that we run traceroute for 50 times per hour for 24 hours. 

•	The result of this experiment is written in a csv file for more statistical analysis. Also, change the path where the csv file is saved, if required. 

•	Since this experiment will take time to fully run, a shorter version of this script is created for testing purposes. It is called ‘loopscp_shorttime.sh’. It will run the same script for a few seconds so that we can run a quick check about where the results are being saved and how it looks. 





