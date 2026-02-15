#!/usr/bin/env python3
"""
Reference Architecture: Industrial IoT Data Streaming
Based on: https://www.hivemq.com/blog/building-industrial-iot-data-streaming-architecture-mqtt/

Three-tier MQTT-based IIoT streaming: Data Producers (sensors, PLCs, MES)
publish to HiveMQ Broker cluster, which distributes to Data Consumers
(Kafka, time-series DBs, analytics, ERP).

Usage:
    python 01_iiot_data_streaming.py              # dark background (default)
    python 01_iiot_data_streaming.py --bg white   # white background
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
    output = os.path.join(os.path.dirname(__file__), f"01_iiot_data_streaming{suffix}")

    with Diagram(
        "IIoT Data Streaming Architecture",
        show=False,
        filename=output,
        outformat="png",
        direction="LR",
        graph_attr=global_attr,
    ):
        with Cluster(
            "Data Producers (OT)",
            graph_attr={"bgcolor": cluster_bg, "fontcolor": cluster_fc},
        ):
            sensor = Custom("Vibration\nSensors", f"{ICONS}/Sensor.png")
            plc = Custom("PLCs\n(Modbus/OPC-UA)", f"{ICONS}/PLC.png")
            factory = Custom("MES /\nSCADA", f"{ICONS}/Factory.png")

        with Cluster(
            "HiveMQ Platform (MQTT Broker Cluster)",
            graph_attr={"bgcolor": "#0a3d5c" if background == "black" else "#d6eaf8", "fontcolor": cluster_fc},
        ):
            broker1 = Custom("Broker\nNode 1", f"{HMQ_ICONS}/hivemq_platform_asset.png")
            broker2 = Custom("Broker\nNode 2", f"{HMQ_ICONS}/hivemq_platform_asset.png")
            broker3 = Custom("Broker\nNode 3", f"{HMQ_ICONS}/hivemq_platform_asset.png")

            broker1 - Edge(color=HIVEMQ_TEAL, style="dotted", label="Cluster\nDiscovery") - broker2
            broker2 - Edge(color=HIVEMQ_TEAL, style="dotted") - broker3

        with Cluster(
            "Data Consumers (IT)",
            graph_attr={"bgcolor": cluster_bg, "fontcolor": cluster_fc},
        ):
            kafka = Custom("Apache\nKafka", f"{ICONS}/Data-real-time.png")
            tsdb = Custom("Time-Series\nDatabase", f"{ICONS}/Data-Historian.png")
            analytics = Custom("ML / Stream\nAnalytics", f"{ICONS}/Monitor stats.png")
            erp = Custom("ERP\nSystem", f"{ICONS}/Data Applications.png")

        sensor >> Edge(label="MQTT 5", color=HIVEMQ_YELLOW, fontcolor=HIVEMQ_YELLOW) >> broker1
        plc >> Edge(label="Sparkplug B", color=HIVEMQ_YELLOW, fontcolor=HIVEMQ_YELLOW) >> broker2
        factory >> Edge(color=HIVEMQ_YELLOW) >> broker3

        broker1 >> Edge(label="Kafka\nExtension", color=HIVEMQ_TEAL, fontcolor=HIVEMQ_TEAL) >> kafka
        broker2 >> Edge(color=HIVEMQ_TEAL) >> tsdb
        broker3 >> Edge(color=HIVEMQ_TEAL) >> analytics
        broker2 >> Edge(color=HIVEMQ_TEAL) >> erp

    print(f"Generated: 01_iiot_data_streaming{suffix}.png")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--bg", choices=["black", "white"], default="black")
    args = parser.parse_args()
    main(args.bg)
