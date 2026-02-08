#!/usr/bin/env python3
from diagrams import Cluster, Diagram, Edge
from diagrams.generic.device import Tablet as Sensor
from diagrams.onprem.analytics import Spark
from diagrams.onprem.database import PostgreSQL

# Import our theme
from hivemq_theme import HiveMQPalette, GLOBAL_ATTR, BASE_NODE_ATTR, HIVEMQ_YELLOW, DARK_GREY, HIVEMQ_TEAL, HIVEMQ_WHITE

# Initialize the palette
# This will ensure icons/ folder exists and load definitions
palette = HiveMQPalette("icons.csv")

def main():
    print("Generating demo architecture diagram...")
    
    with Diagram("Unified IIoT Architecture Demo", 
                 show=False, 
                 filename="images/demo_architecture",
                 outformat="png", 
                 graph_attr=GLOBAL_ATTR):

        with Cluster("Factory Floor (OT)", graph_attr={"bgcolor": DARK_GREY, "fontcolor": HIVEMQ_WHITE}):
            # Standard diagram nodes
            sensors = Sensor("Vibration Sensors", **BASE_NODE_ATTR)
            plcs = Sensor("Control Systems", **BASE_NODE_ATTR)
            
            # Custom node from our palette
            edge_gateway = palette.get_node("edge", "HiveMQ Edge Gateway")
            
            # Connections
            [sensors, plcs] >> Edge(label="Modbus/OPC UA", color=HIVEMQ_YELLOW, fontcolor=HIVEMQ_YELLOW) >> edge_gateway

        with Cluster("Cloud / Enterprise (IT)", graph_attr={"bgcolor": DARK_GREY, "fontcolor": HIVEMQ_WHITE}):
            # Custom node
            enterprise_broker = palette.get_node("broker", "HiveMQ Enterprise")
            
            # Standard nodes
            analytics = Spark("Analytics Engine", **BASE_NODE_ATTR)
            db = PostgreSQL("TimeSeries DB", **BASE_NODE_ATTR)

            # Connections
            enterprise_broker >> Edge(color=HIVEMQ_TEAL) >> analytics
            enterprise_broker >> Edge(color=HIVEMQ_TEAL) >> db
            analytics >> Edge(color=HIVEMQ_TEAL) >> db

        # Bridge connection
        edge_gateway >> Edge(
            label="MQTT Sparkplug B", 
            color=HIVEMQ_YELLOW, 
            style="bold",
            fontcolor=HIVEMQ_YELLOW
        ) >> enterprise_broker

    print(f"Diagram generated: demo_architecture.png")
    
    # Generate documentation
    palette.generate_readme("Unified IIoT Architecture Demo", "images/demo_architecture.png")

if __name__ == "__main__":
    main()
