import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from hivemq_theme import HiveMQPalette, GLOBAL_ATTR, BASE_NODE_ATTR, HIVEMQ_YELLOW, HIVEMQ_BLACK, HIVEMQ_WHITE
from diagrams import Cluster, Diagram, Edge
from diagrams.custom import Custom
from diagrams.generic.device import Tablet as Sensor
from diagrams.onprem.queue import Kafka
from diagrams.onprem.database import Influxdb

# Initialize palette
palette = HiveMQPalette("icons.csv")

graph_attr = GLOBAL_ATTR
node_attr = BASE_NODE_ATTR

with Diagram("HiveMQ Industrial Data Fabric", show=False, filename="images/hivemq_industrial_data_fabric", direction="LR", graph_attr=graph_attr):
    
    with Cluster("The Edge (OT)", graph_attr={"bgcolor": "#1A1A1A", "fontcolor": HIVEMQ_WHITE}):
        plcs = Sensor("Factory Assets", **node_attr)
        
        # Use palette for Edge
        edge = palette.get_node("edge", "HiveMQ Edge")
        
        plcs >> Edge(color=HIVEMQ_YELLOW, label="Modbus/OPC UA") >> edge

    with Cluster("Enterprise Core (IT)", graph_attr={"bgcolor": "#1A1A1A", "fontcolor": HIVEMQ_WHITE}):
        # Use palette for Broker
        broker = palette.get_node("broker", "HiveMQ Platform")
        
        with Cluster("Analytics Stack"):
            kafka = Kafka("Kafka Stream", **node_attr)
            influx = Influxdb("Historian", **node_attr)

    # Bridge with high-contrast labeling
    edge >> Edge(label="Sparkplug B / TLS", color=HIVEMQ_YELLOW, fontcolor=HIVEMQ_YELLOW) >> broker
    broker >> Edge(color=HIVEMQ_YELLOW) >> [kafka, influx]