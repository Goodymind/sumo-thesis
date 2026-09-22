import os
import sys
import traci
import xml.etree.ElementTree as ET


ET.register_namespace('xsi', 'http://www.w3.org/2001/XMLSchema-instance')

SUMO_BINARY = "sumo-gui" # 'sumo' for headless
NET_FILE = "katipunan.net.xml"
ROUTE_FILE = "katipunan-route-distribution.rou.xml"
TLS_FILE = "tls.xml"
TLS_ID = "J16"
TLS_PROGRAM_ID = 1 # separate from katipunan.net.xml programID
TRIP_INFO = "tripinfo.xml"
STATISTICS_OUTPUT = "statistics.xml"
SIM_STEPS = 3600

sumo_cmd = [
    SUMO_BINARY, 
    "-n", NET_FILE, 
    "-r", ROUTE_FILE, 
    "-a", TLS_FILE, 
    "--tripinfo-output", TRIP_INFO,
    "--duration-log.statistics",
    "--statistic-output", STATISTICS_OUTPUT,
    "--step-length", "1.0", 
    "--start",
    "--quit-on-end"
]

def set_flow_perhour(rou_file, perhour_by_flow_id):
    tree = ET.parse(rou_file)
    root = tree.getroot()

    for flow_id, new_perhour in perhour_by_flow_id.items():
        flow = root.find(f"./flow[@id='{flow_id}']")
        if flow is None:
            raise ValueError(f"No flow with id '{flow_id}' found")
        flow.set("perHour", str(new_perhour))

    tree.write(rou_file, encoding="UTF-8", xml_declaration=True)

def set_phase_durations(tls_file, program_id, durations):
    tree = ET.parse(tls_file)
    tl_logic = tree.getroot().find(f"./tlLogic[@programID='{program_id}']")
    phases = tl_logic.findall("phase")

    for phase, new_duration in zip(phases, durations):
        phase.set("duration", str(new_duration))

    tree.write(tls_file, encoding="UTF-8", xml_declaration=True)

def simulate():
    traci.start(sumo_cmd)
    try:
        while traci.simulation.getMinExpectedNumber() > 0 and traci.simulation.getTime() < SIM_STEPS:
            traci.simulationStep()
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        traci.close()

    tree = ET.parse(STATISTICS_OUTPUT)
    vts = tree.getroot().find('vehicleTripStatistics')
    print(f"total_vehicles: {vts.get('count')}")
    print(f"average_waiting_time: {vts.get('waitingTime')} s")

if __name__ == "__main__":
    high_demand_flows = {
        "FDR-vehicle": 500,
        "G2-vehicle": 800,
        "KNI-vehicle": 2000,
        "KSI-vehicle": 2000,
        "SR-vehicle": 400,
    }
    medium_demand_flows = {
        "FDR-vehicle": 800,
        "G2-vehicle": 600,
        "KNI-vehicle": 1500,
        "KSI-vehicle": 1500,
        "SR-vehicle": 300,
    }
    low_demand_flows = {
        "FDR-vehicle": 600,
        "G2-vehicle": 400,
        "KNI-vehicle": 1000,
        "KSI-vehicle": 1000,
        "SR-vehicle": 200,
    }


    set_phase_durations(TLS_FILE, TLS_PROGRAM_ID, [31, 32, 33, 34]) 
    set_flow_perhour(ROUTE_FILE, high_demand_flows)
    print("High Demand Flows with Phase Durations [31, 32, 33, 34]")
    simulate()
    set_flow_perhour(ROUTE_FILE, medium_demand_flows)
    print("Medium Demand Flows with Phase Durations [31, 32, 33, 34]")
    simulate()
    set_flow_perhour(ROUTE_FILE, low_demand_flows)
    print("Low Demand Flows with Phase Durations [31, 32, 33, 34]")
    simulate()

    set_phase_durations(TLS_FILE, TLS_PROGRAM_ID, [41, 42, 43, 44])  
    set_flow_perhour(ROUTE_FILE, high_demand_flows)
    print("High Demand Flows with Phase Durations [41, 42, 43, 44]")
    simulate()
    set_flow_perhour(ROUTE_FILE, medium_demand_flows)
    print("Medium Demand Flows with Phase Durations [41, 42, 43, 44]")
    simulate()
    set_flow_perhour(ROUTE_FILE, low_demand_flows)
    print("Low Demand Flows with Phase Durations [41, 42, 43, 44]")
    simulate()

    set_phase_durations(TLS_FILE, TLS_PROGRAM_ID, [51, 52, 53, 54])  
    set_flow_perhour(ROUTE_FILE, high_demand_flows)
    print("High Demand Flows with Phase Durations [51, 52, 53, 54]")
    simulate()
    set_flow_perhour(ROUTE_FILE, medium_demand_flows)
    print("Medium Demand Flows with Phase Durations [51, 52, 53, 54]")
    simulate()
    set_flow_perhour(ROUTE_FILE, low_demand_flows)
    print("Low Demand Flows with Phase Durations [51, 52, 53, 54]")
    simulate()

    set_phase_durations(TLS_FILE, TLS_PROGRAM_ID, [20, 20, 20, 20])  # Reset to original durations
    set_flow_perhour(ROUTE_FILE, high_demand_flows)  # Reset to original flows