#!/usr/bin/env python3
"""
Reference Architecture: Edge-to-Cloud Connectivity
Based on: https://www.hivemq.com/blog/a-guide-event-driven-architecture-edge-to-cloud-connectivity/

Usage:
    python 02_edge_to_cloud.py              # dark background (default)
    python 02_edge_to_cloud.py --bg white   # white background
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
    suffix = "_light" if background == "white" else ""
    output = os.path.join(os.path.dirname(__file__), f"02_edge_to_cloud{suffix}")

    broker_bg = "#0a3d5c" if background == "black" else "#d6eaf8"
    cloud_bg = "#2a1a3d" if background == "black" else "#e8daef"
    edge_bg = "#1a3a1a" if background == "black" else "#d5f5e3"

    with Diagram(
        "Edge-to-Cloud Event-Driven Architecture",
        show=False,
        filename=output,
        outformat="png",
        direction="LR",
        graph_attr=global_attr,
    ):
        with Cluster(
            "Plant Floor (OT Layer)",
            graph_attr={"bgcolor": cluster_bg, "fontcolor": cluster_fc},
        ):
            plc = Custom("PLCs", f"{ICONS}/PLC.png")
            modbus = Custom("Modbus\nDevices", f"{ICONS}/Modbus.png")
            sensor = Custom("Industrial\nSensors", f"{ICONS}/Sensor.png")

        with Cluster(
            "Edge Layer (Protocol Translation)",
            graph_attr={"bgcolor": edge_bg, "fontcolor": cluster_fc},
        ):
            edge = Custom("HiveMQ\nEdge", f"{HMQ_ICONS}/hivemq_edge_cloud_asset.png")

        with Cluster(
            "On-Site MQTT Broker (Unified Namespace)",
            graph_attr={"bgcolor": broker_bg, "fontcolor": cluster_fc},
        ):
            uns_broker = Custom("HiveMQ\nPlatform", f"{HMQ_ICONS}/hivemq_platform_asset.png")
            datahub = Custom("HiveMQ\nData Hub", f"{ICONS}/Data-Security.png")

        with Cluster(
            "Cloud Broker Cluster",
            graph_attr={"bgcolor": cloud_bg, "fontcolor": cluster_fc},
        ):
            cloud_broker = Custom("HiveMQ\nCloud", f"{HMQ_ICONS}/hivemq_edge_cloud_asset.png")

        with Cluster(
            "Enterprise Integrations",
            graph_attr={"bgcolor": cluster_bg, "fontcolor": cluster_fc},
        ):
            kafka = Custom("Apache\nKafka", f"{ICONS}/Data-real-time.png")
            datalake = Custom("Data Lake /\nSnowflake", f"{ICONS}/Data-lake.png")
            dashboard = Custom("Real-Time\nDashboards", f"{ICONS}/Monitor stats.png")

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

    print(f"Generated: 02_edge_to_cloud{suffix}.png")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--bg", choices=["black", "white"], default="black")
    args = parser.parse_args()
    main(args.bg)
