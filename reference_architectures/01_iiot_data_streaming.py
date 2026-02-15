#!/usr/bin/env python3
"""
Reference Architecture: Industrial IoT Data Streaming
Based on: https://www.hivemq.com/blog/building-industrial-iot-data-streaming-architecture-mqtt/

Three-tier MQTT-based IIoT streaming: Data Producers (sensors, PLCs, MES)
publish to HiveMQ Broker cluster, which distributes to Data Consumers
(Kafka, time-series DBs, analytics, ERP).
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

# Icon paths
ICONS = os.path.join(os.path.dirname(__file__), "..", "icons", "PNGs")
HMQ_ICONS = os.path.join(os.path.dirname(__file__), "..", "icons")


def main():
    output = os.path.join(os.path.dirname(__file__), "01_iiot_data_streaming")

    with Diagram(
        "IIoT Data Streaming Architecture",
        show=False,
        filename=output,
        outformat="png",
        direction="LR",
        graph_attr=GLOBAL_ATTR,
    ):
        # Data Producers
        with Cluster(
            "Data Producers (OT)",
            graph_attr={"bgcolor": DARK_GREY, "fontcolor": HIVEMQ_WHITE},
        ):
            sensor = Custom("Vibration\nSensors", f"{ICONS}/Sensor.png")
            plc = Custom("PLCs\n(Modbus/OPC-UA)", f"{ICONS}/PLC.png")
            factory = Custom("MES /\nSCADA", f"{ICONS}/Factory.png")

        # HiveMQ Broker Cluster
        with Cluster(
            "HiveMQ Platform (MQTT Broker Cluster)",
            graph_attr={"bgcolor": "#0a3d5c", "fontcolor": HIVEMQ_WHITE},
        ):
            broker1 = Custom("Broker\nNode 1", f"{HMQ_ICONS}/hivemq_platform_asset.png")
            broker2 = Custom("Broker\nNode 2", f"{HMQ_ICONS}/hivemq_platform_asset.png")
            broker3 = Custom("Broker\nNode 3", f"{HMQ_ICONS}/hivemq_platform_asset.png")

            broker1 - Edge(color=HIVEMQ_TEAL, style="dotted", label="Cluster\nDiscovery") - broker2
            broker2 - Edge(color=HIVEMQ_TEAL, style="dotted") - broker3

        # Data Consumers
        with Cluster(
            "Data Consumers (IT)",
            graph_attr={"bgcolor": DARK_GREY, "fontcolor": HIVEMQ_WHITE},
        ):
            kafka = Custom("Apache\nKafka", f"{ICONS}/Data-real-time.png")
            tsdb = Custom("Time-Series\nDatabase", f"{ICONS}/Data-Historian.png")
            analytics = Custom("ML / Stream\nAnalytics", f"{ICONS}/Monitor stats.png")
            erp = Custom("ERP\nSystem", f"{ICONS}/Data Applications.png")

        # Connections: Producers -> Broker
        sensor >> Edge(label="MQTT 5", color=HIVEMQ_YELLOW, fontcolor=HIVEMQ_YELLOW) >> broker1
        plc >> Edge(label="Sparkplug B", color=HIVEMQ_YELLOW, fontcolor=HIVEMQ_YELLOW) >> broker2
        factory >> Edge(color=HIVEMQ_YELLOW) >> broker3

        # Connections: Broker -> Consumers
        broker1 >> Edge(label="Kafka\nExtension", color=HIVEMQ_TEAL, fontcolor=HIVEMQ_TEAL) >> kafka
        broker2 >> Edge(color=HIVEMQ_TEAL) >> tsdb
        broker3 >> Edge(color=HIVEMQ_TEAL) >> analytics
        broker2 >> Edge(color=HIVEMQ_TEAL) >> erp

    print("Generated: 01_iiot_data_streaming.png")


if __name__ == "__main__":
    main()
