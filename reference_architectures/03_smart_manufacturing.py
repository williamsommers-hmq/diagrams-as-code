#!/usr/bin/env python3
"""
Reference Architecture: Smart Manufacturing Data Pipeline
Based on: https://www.hivemq.com/blog/a-practical-guide-iiot-data-streaming-implementation-smart-manufacturing/

End-to-end closed-loop pipeline: CNC machines and legacy equipment → HiveMQ Edge
→ HiveMQ Broker → Kafka → InfluxDB/TimescaleDB → Analytics/ML (Databricks)
→ feedback loop back through MQTT for machine control.
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
    output = os.path.join(os.path.dirname(__file__), "03_smart_manufacturing")

    with Diagram(
        "Smart Manufacturing Closed-Loop Architecture",
        show=False,
        filename=output,
        outformat="png",
        direction="LR",
        graph_attr=GLOBAL_ATTR,
    ):
        # Shop Floor
        with Cluster(
            "Shop Floor",
            graph_attr={"bgcolor": DARK_GREY, "fontcolor": HIVEMQ_WHITE},
        ):
            cnc = Custom("CNC\nMachines", f"{ICONS}/Gear complex.png")
            robot = Custom("Robotic\nArms", f"{ICONS}/Robot.png")
            legacy = Custom("Legacy\nEquipment", f"{ICONS}/PLC.png")

        # Edge Layer
        with Cluster(
            "Edge Gateway Layer",
            graph_attr={"bgcolor": "#1a3a1a", "fontcolor": HIVEMQ_WHITE},
        ):
            edge1 = Custom("HiveMQ Edge\n(Line 1)", f"{HMQ_ICONS}/hivemq_edge_cloud_asset.png")
            edge2 = Custom("HiveMQ Edge\n(Line 2)", f"{HMQ_ICONS}/hivemq_edge_cloud_asset.png")

        # Central Broker
        with Cluster(
            "HiveMQ Enterprise Broker",
            graph_attr={"bgcolor": "#0a3d5c", "fontcolor": HIVEMQ_WHITE},
        ):
            broker = Custom("HiveMQ\nPlatform", f"{HMQ_ICONS}/hivemq_platform_asset.png")
            ctrl_center = Custom("Control\nCenter", f"{ICONS}/Broker-Control-Center.png")

        # Streaming Layer
        with Cluster(
            "Stream Processing",
            graph_attr={"bgcolor": DARK_GREY, "fontcolor": HIVEMQ_WHITE},
        ):
            kafka = Custom("Apache\nKafka", f"{ICONS}/Data-real-time.png")
            flink = Custom("Stream\nAnalytics", f"{ICONS}/Monitor stats.png")

        # Storage & Analytics
        with Cluster(
            "Storage & Intelligence",
            graph_attr={"bgcolor": "#2a1a3d", "fontcolor": HIVEMQ_WHITE},
        ):
            tsdb = Custom("InfluxDB /\nTimescaleDB", f"{ICONS}/Data-Historian.png")
            ml = Custom("ML Platform\n(Databricks)", f"{ICONS}/Data Applications.png")
            oee = Custom("OEE\nDashboard", f"{ICONS}/Monitor browser.png")

        # Forward path: Shop Floor → Edge → Broker → Kafka → Storage
        [cnc, robot] >> Edge(color=HIVEMQ_YELLOW) >> edge1
        legacy >> Edge(label="Modbus", color=HIVEMQ_YELLOW, fontcolor=HIVEMQ_YELLOW) >> edge2

        edge1 >> Edge(label="MQTT 5", color=HIVEMQ_YELLOW, fontcolor=HIVEMQ_YELLOW) >> broker
        edge2 >> Edge(color=HIVEMQ_YELLOW) >> broker

        broker >> Edge(color=HIVEMQ_TEAL) >> ctrl_center
        broker >> Edge(label="Kafka Ext.", color=HIVEMQ_TEAL, fontcolor=HIVEMQ_TEAL) >> kafka

        kafka >> Edge(color=HIVEMQ_TEAL) >> flink
        kafka >> Edge(color=HIVEMQ_TEAL) >> tsdb

        tsdb >> Edge(color=HIVEMQ_TEAL) >> oee
        flink >> Edge(color=HIVEMQ_TEAL) >> ml

        # Closed-loop feedback
        ml >> Edge(
            label="Control\nCommands",
            color="#FF6B6B",
            fontcolor="#FF6B6B",
            style="dashed",
        ) >> broker

    print("Generated: 03_smart_manufacturing.png")


if __name__ == "__main__":
    main()
