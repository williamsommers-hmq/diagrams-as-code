#!/usr/bin/env python3
"""
Reference Architecture: Edge-to-Cloud Connectivity
Based on: https://www.hivemq.com/blog/a-guide-event-driven-architecture-edge-to-cloud-connectivity/

Four-layer architecture: Plant floor sensors → HiveMQ Edge (protocol translation)
→ On-site MQTT Broker (UNS hub) → MQTT Bridge → Cloud Broker Cluster
→ Enterprise integrations (Kafka, Kinesis, Snowflake).
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from diagrams import Cluster, Diagram, Edge
from diagrams.custom import Custom

from hivemq_theme import (
    BASE_NODE_ATTR,
    DARK_GREY,
    GLOBAL_ATTR,
    HIVEMQ_TEAL,
    HIVEMQ_WHITE,
    HIVEMQ_YELLOW,
)

ICONS = os.path.join(os.path.dirname(__file__), "..", "icons", "PNGs")
HMQ_ICONS = os.path.join(os.path.dirname(__file__), "..", "icons")


def main():
    output = os.path.join(os.path.dirname(__file__), "02_edge_to_cloud")

    with Diagram(
        "Edge-to-Cloud Event-Driven Architecture",
        show=False,
        filename=output,
        outformat="png",
        direction="LR",
        graph_attr=GLOBAL_ATTR,
    ):
        # Layer 1: Plant Floor
        with Cluster(
            "Plant Floor (OT Layer)",
            graph_attr={"bgcolor": DARK_GREY, "fontcolor": HIVEMQ_WHITE},
        ):
            plc = Custom("PLCs", f"{ICONS}/PLC.png")
            modbus = Custom("Modbus\nDevices", f"{ICONS}/Modbus.png")
            sensor = Custom("Industrial\nSensors", f"{ICONS}/Sensor.png")

        # Layer 2: Edge Gateway
        with Cluster(
            "Edge Layer (Protocol Translation)",
            graph_attr={"bgcolor": "#1a3a1a", "fontcolor": HIVEMQ_WHITE},
        ):
            edge = Custom("HiveMQ\nEdge", f"{HMQ_ICONS}/hivemq_edge_cloud_asset.png")

        # Layer 3: On-Site Broker (UNS)
        with Cluster(
            "On-Site MQTT Broker (Unified Namespace)",
            graph_attr={"bgcolor": "#0a3d5c", "fontcolor": HIVEMQ_WHITE},
        ):
            uns_broker = Custom("HiveMQ\nPlatform", f"{HMQ_ICONS}/hivemq_platform_asset.png")
            datahub = Custom("HiveMQ\nData Hub", f"{ICONS}/Data-Security.png")

        # Layer 4: Cloud
        with Cluster(
            "Cloud Broker Cluster",
            graph_attr={"bgcolor": "#2a1a3d", "fontcolor": HIVEMQ_WHITE},
        ):
            cloud_broker = Custom("HiveMQ\nCloud", f"{HMQ_ICONS}/hivemq_edge_cloud_asset.png")

        # Enterprise Integrations
        with Cluster(
            "Enterprise Integrations",
            graph_attr={"bgcolor": DARK_GREY, "fontcolor": HIVEMQ_WHITE},
        ):
            kafka = Custom("Apache\nKafka", f"{ICONS}/Data-real-time.png")
            datalake = Custom("Data Lake /\nSnowflake", f"{ICONS}/Data-lake.png")
            dashboard = Custom("Real-Time\nDashboards", f"{ICONS}/Monitor stats.png")

        # Connections
        [plc, modbus, sensor] >> Edge(
            label="Modbus / OPC-UA / S7",
            color=HIVEMQ_YELLOW,
            fontcolor=HIVEMQ_YELLOW,
        ) >> edge

        edge >> Edge(
            label="MQTT 5\n(Report by Exception)",
            color=HIVEMQ_YELLOW,
            fontcolor=HIVEMQ_YELLOW,
        ) >> uns_broker

        uns_broker >> Edge(color=HIVEMQ_TEAL) >> datahub

        uns_broker >> Edge(
            label="MQTT Bridge\n(TLS)",
            color=HIVEMQ_YELLOW,
            fontcolor=HIVEMQ_YELLOW,
            style="bold",
        ) >> cloud_broker

        cloud_broker >> Edge(color=HIVEMQ_TEAL) >> kafka
        cloud_broker >> Edge(color=HIVEMQ_TEAL) >> datalake
        cloud_broker >> Edge(color=HIVEMQ_TEAL) >> dashboard

    print("Generated: 02_edge_to_cloud.png")


if __name__ == "__main__":
    main()
