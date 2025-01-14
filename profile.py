#!/usr/bin/env python

import os 

import geni.portal as portal
import geni.rspec.pg as rspec
import geni.rspec.igext as IG
import geni.rspec.emulab.pnext as PN
import geni.rspec.emulab.spectrum as spectrum


tourDescription = """
### srsRAN 5G using the POWDER Outdoor OTA Lab: Please see the document "Outdoor Experimentation Steps.docx" for instructions to run the profile. 


"""

tourInstructions = """

Please see the document "Outdoor Experimentation Steps.docx" for instructions to run the profile.

"""

BIN_PATH = "/local/repository/bin"
ETC_PATH = "/local/repository/etc"
UBUNTU_IMG = "urn:publicid:IDN+emulab.net+image+emulab-ops//UBUNTU22-64-STD"
COTS_UE_IMG = "urn:publicid:IDN+emulab.net+image+PowderTeam:cots-jammy-image"
COMP_MANAGER_ID = "urn:publicid:IDN+emulab.net+authority+cm"
DEFAULT_SRSRAN_HASH = "4ac5300d4927b5199af69e6bc2e55d061fc33652"
OPEN5GS_DEPLOY_SCRIPT = os.path.join(BIN_PATH, "deploy-open5gs.sh")
SRSRAN_DEPLOY_SCRIPT = os.path.join(BIN_PATH, "deploy-srsran.sh")

##This can be renamed depending on the name/make of the gNB
def x310_node_pair(idx, x310_radio):
    node = request.RawPC("{}-gnb".format(x310_radio))
    node.component_manager_id = COMP_MANAGER_ID
    node.hardware_type = params.sdr_nodetype

    if params.sdr_compute_image:
        node.disk_image = params.sdr_compute_image
    else:
        node.disk_image = UBUNTU_IMG

    node_radio_if = node.addInterface("usrp_if")
    node_radio_if.addAddress(rspec.IPv4Address("192.168.40.1",
                                               "255.255.255.0"))

    radio_link = request.Link("radio-link-{}".format(idx))
    radio_link.bandwidth = 10*1000*1000
    radio_link.addInterface(node_radio_if)

    radio = request.RawPC("{}-gnb-sdr".format(x310_radio))
    radio.component_id = x310_radio
    radio.component_manager_id = COMP_MANAGER_ID
    radio_link.addNode(radio)

    nodeb_cn_if = node.addInterface("nodeb-cn-if")
    nodeb_cn_if.addAddress(rspec.IPv4Address("192.168.1.{}".format(idx + 2), "255.255.255.0"))
    cn_link.addInterface(nodeb_cn_if)

    #May not need this anymore. Hence, commented this out for now. 
    #ethue = node.addInterface("ethue")
    #ethue.addAddress(rspec.IPv4Address("192.168.{}.1".format(idx*10 + 10), "255.255.255.252"))

    if params.srsran_commit_hash:
        srsran_hash = params.srsran_commit_hash
    else:
        srsran_hash = DEFAULT_SRSRAN_HASH

    cmd = "{} '{}'".format(SRSRAN_DEPLOY_SCRIPT, srsran_hash)
    node.addService(rspec.Execute(shell="bash", command=cmd))
    node.addService(rspec.Execute(shell="bash", command="/local/repository/bin/tune-cpu.sh"))
    node.addService(rspec.Execute(shell="bash", command="/local/repository/bin/tune-sdr-iface.sh"))

def b210_nuc_pair(b210_node):
    node = request.RawPC("{}-cots-ue".format(b210_node))
    node.component_manager_id = COMP_MANAGER_ID
    node.component_id = b210_node
    node.disk_image = COTS_UE_IMG
    node.addService(rspec.Execute(shell="bash", command="/local/repository/bin/module-off.sh"))
    node.addService(rspec.Execute(shell="bash", command="/local/repository/bin/update-udhcpc-script.sh"))

pc = portal.Context()

node_types = [
    ("d430", "Emulab, d430"),
    ("d740", "Emulab, d740"),
]
pc.defineParameter(
    name="sdr_nodetype",
    description="Type of compute node paired with the SDRs",
    typ=portal.ParameterType.STRING,
    defaultValue=node_types[1],
    legalValues=node_types
)

pc.defineParameter(
    name="cn_nodetype",
    description="Type of compute node to use for CN node (if included)",
    typ=portal.ParameterType.STRING,
    defaultValue=node_types[0],
    legalValues=node_types
)

pc.defineParameter(
    name="sdr_compute_image",
    description="Image to use for compute connected to SDRs",
    typ=portal.ParameterType.STRING,
    defaultValue="",
    advanced=True
)

pc.defineParameter(
    name="srsran_commit_hash",
    description="Commit hash for srsRAN",
    typ=portal.ParameterType.STRING,
    defaultValue="",
    advanced=True
)

#Need Dustin's help in this
######
outdoor_ota_gNB = [
    ("ota-x310-1",
     "USRP gNB #1"),
    ("ota-x310-2",
     "USRP gNB2 #2"),
]
pc.defineParameter(
    name="x310_radio1",
    description="X310 Radio as gNB1",
    typ=portal.ParameterType.STRING,
    defaultValue=outdoor_ota_gNB[0],
    legalValues=outdoor_ota_gNB
)

pc.defineParameter(
    name="x310_radio2",
    description="X310 Radio as gNB2",
    typ=portal.ParameterType.STRING,
    defaultValue=outdoor_ota_gNB[1],
    legalValues=outdoor_ota_gNB
)

indoor_ota_nucs = [
    ("ota-nuc{}".format(i), "Indoor OTA nuc{} with B210 and COTS UE".format(i)) for i in range(1, 5)
]

pc.defineStructParameter(
    name="ue_nodes",
    description="Indoor OTA NUC with COTS UE",
    defaultValue=[{ "node_id": "ota-nuc2" }],
    multiValue=True,
    min=1,
    max=4,
    members=[
        portal.Parameter(
            "node_id",
            "Indoor OTA NUC",
            portal.ParameterType.STRING,
            indoor_ota_nucs[0],
            indoor_ota_nucs
        )
    ]
)
#######
pc.defineStructParameter(
    "freq_ranges", "Frequency Ranges To Transmit In",
    defaultValue=[{"freq_min": 3400.0, "freq_max": 3460.0}],
    multiValue=True,
    min=0,
    max=3,
    multiValueTitle="Frequency ranges to be used for transmission.",
    members=[
        portal.Parameter(
            "freq_min",
            "Frequency Range Min",
            portal.ParameterType.BANDWIDTH,
            3400.0,
            longDescription="Values are rounded to the nearest kilohertz."
        ),
        portal.Parameter(
            "freq_max",
            "Frequency Range Max",
            portal.ParameterType.BANDWIDTH,
            3460.0,
            longDescription="Values are rounded to the nearest kilohertz."
        ),
    ]
)

params = pc.bindParameters()
pc.verifyParameters()
request = pc.makeRequestRSpec()
request.setRoutingStyle("none")

role = "cn"
cn_node = request.RawPC("cn5g")
cn_node.component_manager_id = COMP_MANAGER_ID
cn_node.hardware_type = params.cn_nodetype
cn_node.disk_image = UBUNTU_IMG
cn_if = cn_node.addInterface("cn-if")
cn_if.addAddress(rspec.IPv4Address("192.168.1.1", "255.255.255.0"))
cn_link = request.Link("cn-link")
cn_link.setNoBandwidthShaping()
cn_link.addInterface(cn_if)
cn_node.addService(rspec.Execute(shell="bash", command=OPEN5GS_DEPLOY_SCRIPT))

# single x310 for for observation or another gNodeB
x310_node_pair(0, params.x310_radio1)
x310_node_pair(1, params.x310_radio2)

for ue_node in params.ue_nodes:
    b210_nuc_pair(ue_node.node_id)

for frange in params.freq_ranges:
    request.requestSpectrum(frange.freq_min, frange.freq_max, 0)

tour = IG.Tour()
tour.Description(IG.Tour.MARKDOWN, tourDescription)
tour.Instructions(IG.Tour.MARKDOWN, tourInstructions)
request.addTour(tour)

pc.printRequestRSpec(request)
