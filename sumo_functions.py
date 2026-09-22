TRAFFIC_LIGHT_PATTERN_FILE = ""


def vector_to_traffic_light_pattern(
    vec: [int], traffic_light_file: str = TRAFFIC_LIGHT_PATTERN_FILE
):
    """Converts a vector into a traffic light xml"""


def set_traffic_light_file(traffic_light_file: str):
    TRAFFIC_LIGHT_PATTERN_FILE = traffic_light_file


def score_traffic_light_pattern(
    traffic_light_file: str = TRAFFIC_LIGHT_PATTERN_FILE,
) -> int:
    """Runs SUMO with the traffic_light_file and returns a score"""
