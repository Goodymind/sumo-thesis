import os
import sys
import traci
import xml.etree.ElementTree as ET

ET.register_namespace('xsi', 'http://www.w3.org/2001/XMLSchema-instance')

SUMO_BINARY = "sumo" # 'sumo' for headless, 'sumo-gui' for funsies
NET_FILE = "katipunan.net.xml"
ROUTE_FILE = "katipunan-route-distribution.rou.xml"
TLS_FILE = "tls.xml" # traffic light pattern file
TLS_ID = "J16"
TLS_PROGRAM_ID = 1 # separate from katipunan.net.xml programID
TRIP_INFO = "tripinfo.xml"
STATISTICS_OUTPUT = "statistics.xml"
SIM_STEPS = 3600

def vector_to_traffic_light_pattern(
    vec: [int], traffic_light_file: str = None
) -> str:
    """Converts a vector into a traffic light xml and returns file name of traffic light pattern"""
    if traffic_light_file is None:
        traffic_light_file = TLS_FILE

    tree = ET.parse(traffic_light_file)
    tl_logic = tree.getroot().find(f"./tlLogic[@programID='{TLS_PROGRAM_ID}']")
    phases = tl_logic.findall("phase")

    for phase, new_duration in zip(phases, vec):
        phase.set("duration", str(new_duration))

    tree.write(traffic_light_file, encoding="UTF-8", xml_declaration=True)

    return traffic_light_file


def set_traffic_light_file(traffic_light_file: str):
    global TLS_FILE
    TLS_FILE = traffic_light_file


def score_traffic_light_pattern(
    traffic_light_file: str = None,
) -> float:
    """Runs SUMO with the traffic_light_file and returns a score"""
    if traffic_light_file is None:
        traffic_light_file = TLS_FILE

    sumo_cmd = [
        SUMO_BINARY, 
        "-n", NET_FILE, 
        "-r", ROUTE_FILE, 
        "-a", traffic_light_file, 
        "--tripinfo-output", TRIP_INFO,
        "--duration-log.statistics",
        "--statistic-output", STATISTICS_OUTPUT,
        "--step-length", "1.0", 
        "--start",
        "--quit-on-end",
        "--no-warnings"
    ]

    try:
        traci.start(sumo_cmd)
        while traci.simulation.getMinExpectedNumber() > 0 and traci.simulation.getTime() < SIM_STEPS:
            traci.simulationStep()
    except Exception as e:
        print(f"Error occurred: {e}")
        return None
    finally:
        traci.close()

    tree = ET.parse(STATISTICS_OUTPUT)
    vts = tree.getroot().find("vehicleTripStatistics")
    count = int(vts.get('count'))
    # waiting_time = float(vts.get('waitingTime'))
    score = count
    return score

def score_encoding(
    vec: [int], traffic_light_file: str = None
) -> float:

    if traffic_light_file is None:
        traffic_light_file = TLS_FILE

    return score_traffic_light_pattern(
        vector_to_traffic_light_pattern(vec, traffic_light_file)
    )
