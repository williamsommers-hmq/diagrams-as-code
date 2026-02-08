import sys
import os

# Add parent directory to path to import hivemq_theme
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from diagrams import Cluster, Diagram, Edge
from diagrams.generic.device import Tablet as Sensor
from hivemq_theme import HiveMQPalette, GLOBAL_ATTR, DARK_GREY, HIVEMQ_YELLOW, BASE_NODE_ATTR

# Initialize palette
palette = HiveMQPalette('icons.csv') # It will create icons.csv if missing in current dir

with Diagram("Multi-Region Global Architecture",
             show=False,
             direction="LR",
             filename="images/multi-region_global_architecture",
             outformat="svg",
             graph_attr=GLOBAL_ATTR):

    with Cluster("US-East (Primary)", graph_attr={"bgcolor": DARK_GREY, "fontcolor": "white"}):
        us_edge = palette.get_node("edge", "Baltimore Edge")
        us_broker = palette.get_node("broker", "US Broker Cluster")

        Sensor("Factory Assets", **BASE_NODE_ATTR) >> us_edge
        us_edge >> Edge(color=HIVEMQ_YELLOW, label="spB / TLS") >> us_broker

    with Cluster("EU-West (Disaster Recovery)", graph_attr={"bgcolor": DARK_GREY, "fontcolor": "white"}):
        eu_broker = palette.get_node("cloud", "EU DR Cluster")

    # Multi-Region Bridge
    us_broker >> Edge(
        label="Cloud-to-Cloud Bridge",
        color=HIVEMQ_YELLOW,
        style="dashed",
        fontcolor=HIVEMQ_YELLOW
    ) >> eu_broker
