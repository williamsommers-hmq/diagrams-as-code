import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from diagrams import Cluster, Diagram, Edge
from diagrams.generic.device import Tablet as Sensor
from hivemq_theme import HiveMQPalette, GLOBAL_ATTR, BASE_NODE_ATTR

# Initialize our palette from the CSV
# Initialize our palette from the CSV
palette = HiveMQPalette('icons.csv')

with Diagram("Global Data Fabric", show=False, filename="images/global_data_fabric", outformat="svg", graph_attr=GLOBAL_ATTR):

    with Cluster("US-East (Baltimore Plant)", graph_attr={"bgcolor": "#222", "fontcolor": "white"}):
        # Using keys from our CSV
        baltimore_edge = palette.get_node("edge", "HiveMQ Edge")
        Sensor("PLC / Sensors", **BASE_NODE_ATTR) >> baltimore_edge

    with Cluster("EU-West (Frankfurt Hub)", graph_attr={"bgcolor": "#222", "fontcolor": "white"}):
        eu_broker = palette.get_node("broker", "Enterprise Broker")

    # Bridge connection
    baltimore_edge >> Edge(label="Bridge: spBv1.0/...", color="#FFC000") >> eu_broker