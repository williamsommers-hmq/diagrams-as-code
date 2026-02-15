#!/usr/bin/env python3
"""
Reference Architecture: Smart Manufacturing Data Pipeline
Based on: https://www.hivemq.com/blog/a-practical-guide-iiot-data-streaming-implementation-smart-manufacturing/

Usage:
    python 03_smart_manufacturing.py              # dark background (default)
    python 03_smart_manufacturing.py --bg white   # white background
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from diagrams import Cluster, Diagram, Edge
from diagrams.custom import Custom

from hivemq_theme import HIVEMQ_TEAL, HIVEMQ_YELLOW, get_theme

ICONS = os.path.join(os.path.dirname(__file__), "..", "icons", "PNGs")
HMQ_ICONS = os.path.join(os.path.dirname(__file__), "..", "icons")


def main(background="black"):
    global_attr, base_node_attr, cluster_fc, cluster_bg = get_theme(background)
    suffix = "_light" if background == "white" else "_transparent" if background == "transparent" else ""
    output = os.path.join(os.path.dirname(__file__), f"03_smart_manufacturing{suffix}")

    broker_bg = "#0a3d5c" if background == "black" else "#d6eaf8"
    cloud_bg = "#2a1a3d" if background == "black" else "#e8daef"
    edge_bg = "#1a3a1a" if background == "black" else "#d5f5e3"

    with Diagram(
        "Smart Manufacturing Closed-Loop Architecture",
        show=False,
        filename=output,
        outformat="png",
        direction="LR",
        graph_attr=global_attr,
    ):
        with Cluster(
            "Shop Floor",
            graph_attr={"bgcolor": cluster_bg, "fontcolor": cluster_fc},
        ):
            cnc = Custom("CNC\nMachines", f"{ICONS}/Gear complex.png")
            robot = Custom("Robotic\nArms", f"{ICONS}/Robot.png")
            legacy = Custom("Legacy\nEquipment", f"{ICONS}/PLC.png")

        with Cluster(
            "Edge Gateway Layer",
            graph_attr={"bgcolor": edge_bg, "fontcolor": cluster_fc},
        ):
            edge1 = Custom("HiveMQ Edge\n(Line 1)", f"{HMQ_ICONS}/hivemq_edge_cloud_asset.png")
            edge2 = Custom("HiveMQ Edge\n(Line 2)", f"{HMQ_ICONS}/hivemq_edge_cloud_asset.png")

        with Cluster(
            "HiveMQ Enterprise Broker",
            graph_attr={"bgcolor": broker_bg, "fontcolor": cluster_fc},
        ):
            broker = Custom("HiveMQ\nPlatform", f"{HMQ_ICONS}/hivemq_platform_asset.png")
            ctrl_center = Custom("Control\nCenter", f"{ICONS}/Broker-Control-Center.png")

        with Cluster(
            "Stream Processing",
            graph_attr={"bgcolor": cluster_bg, "fontcolor": cluster_fc},
        ):
            kafka = Custom("Apache\nKafka", f"{ICONS}/Data-real-time.png")
            flink = Custom("Stream\nAnalytics", f"{ICONS}/Monitor stats.png")

        with Cluster(
            "Storage & Intelligence",
            graph_attr={"bgcolor": cloud_bg, "fontcolor": cluster_fc},
        ):
            tsdb = Custom("InfluxDB /\nTimescaleDB", f"{ICONS}/Data-Historian.png")
            ml = Custom("ML Platform\n(Databricks)", f"{ICONS}/Data Applications.png")
            oee = Custom("OEE\nDashboard", f"{ICONS}/Monitor browser.png")

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

        ml >> Edge(
            label="Control\nCommands",
            color="#FF6B6B",
            fontcolor="#FF6B6B",
            style="dashed",
        ) >> broker

    print(f"Generated: 03_smart_manufacturing{suffix}.png")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--bg", choices=["black", "white", "transparent"], default="black")
    args = parser.parse_args()
    main(args.bg)
