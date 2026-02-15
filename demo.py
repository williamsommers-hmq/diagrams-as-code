#!/usr/bin/env python3
"""
Main demo: Unified IIoT Architecture

Usage:
    python demo.py                  # dark background (default)
    python demo.py --bg white       # white background
    python demo.py --bg transparent # transparent background
"""
import argparse

from diagrams import Cluster, Diagram, Edge
from diagrams.generic.device import Tablet as Sensor
from diagrams.onprem.analytics import Spark
from diagrams.onprem.database import PostgreSQL

from hivemq_theme import HiveMQPalette, HIVEMQ_YELLOW, HIVEMQ_TEAL, get_theme

palette = HiveMQPalette("icons.csv")


def main(background="black"):
    global_attr, base_node_attr, cluster_fc, cluster_bg = get_theme(background)
    suffix = "_light" if background == "white" else "_transparent" if background == "transparent" else ""

    print(f"Generating demo architecture diagram ({background} background)...")

    with Diagram(
        "Unified IIoT Architecture Demo",
        show=False,
        filename=f"images/demo_architecture{suffix}",
        outformat="png",
        graph_attr=global_attr,
    ):
        with Cluster("Factory Floor (OT)", graph_attr={"bgcolor": cluster_bg, "fontcolor": cluster_fc}):
            sensors = Sensor("Vibration Sensors", **base_node_attr)
            plcs = Sensor("Control Systems", **base_node_attr)
            edge_gateway = palette.get_node("edge", "HiveMQ Edge Gateway")
            [sensors, plcs] >> Edge(label="Modbus/OPC UA", color=HIVEMQ_YELLOW, fontcolor=HIVEMQ_YELLOW) >> edge_gateway

        with Cluster("Cloud / Enterprise (IT)", graph_attr={"bgcolor": cluster_bg, "fontcolor": cluster_fc}):
            enterprise_broker = palette.get_node("broker", "HiveMQ Enterprise")
            analytics = Spark("Analytics Engine", **base_node_attr)
            db = PostgreSQL("TimeSeries DB", **base_node_attr)
            enterprise_broker >> Edge(color=HIVEMQ_TEAL) >> analytics
            enterprise_broker >> Edge(color=HIVEMQ_TEAL) >> db
            analytics >> Edge(color=HIVEMQ_TEAL) >> db

        edge_gateway >> Edge(
            label="MQTT Sparkplug B",
            color=HIVEMQ_YELLOW,
            style="bold",
            fontcolor=HIVEMQ_YELLOW,
        ) >> enterprise_broker

    print(f"Diagram generated: images/demo_architecture{suffix}.png")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--bg", choices=["black", "white", "transparent"], default="black")
    args = parser.parse_args()
    main(args.bg)
