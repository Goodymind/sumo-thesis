TRAFFIC_LIGHT_PATTERN_FILE = ""


def vector_to_traffic_light_pattern(
    vec: [int], traffic_light_file: str = TRAFFIC_LIGHT_PATTERN_FILE
) -> str:
    """Converts a vector into a traffic light xml and returns file name of traffic light pattern"""
    return traffic_light_file


def set_traffic_light_file(traffic_light_file: str):
    TRAFFIC_LIGHT_PATTERN_FILE = traffic_light_file


def score_traffic_light_pattern(
    traffic_light_file: str = TRAFFIC_LIGHT_PATTERN_FILE,
) -> float:
    """Runs SUMO with the traffic_light_file and returns a score"""


def score_encoding(
    vec: [int], traffic_light_file: str = TRAFFIC_LIGHT_PATTERN_FILE
) -> float:
    return score_traffic_light_pattern(
        vector_to_traffic_light_pattern(vec, traffic_light_file)
    )
