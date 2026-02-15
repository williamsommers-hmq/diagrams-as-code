#!/usr/bin/env python3
"""
Reference Architecture: Unified Namespace (UNS)
Based on: https://www.hivemq.com/blog/foundations-of-unified-namespace-architecture-iiot/

Hub-and-spoke UNS with HiveMQ Broker as the central hub. Domain-specific
data producers/consumers around it, persistence layer, and MQTT bridges
connecting to remote sites and cloud.
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
    output = os.path.join(os.path.dirname(__file__), "04_unified_namespace")

    with Diagram(
        "Unified Namespace (UNS) Reference Architecture",
        show=False,
        filename=output,
        outformat="png",
        direction="TB",
        graph_attr=GLOBAL_ATTR,
    ):
        # ISA-95 Level 0-1: Control
        with Cluster(
            "Control Domain (ISA-95 L0-L1)",
            graph_attr={"bgcolor": DARK_GREY, "fontcolor": HIVEMQ_WHITE},
        ):
            sensor = Custom("Sensors &\nActuators", f"{ICONS}/Sensor.png")
            plc = Custom("PLCs &\nControllers", f"{ICONS}/PLC.png")
            edge = Custom("HiveMQ\nEdge", f"{HMQ_ICONS}/hivemq_edge_cloud_asset.png")

            [sensor, plc] >> Edge(color=HIVEMQ_YELLOW) >> edge

        # Central UNS Hub
        with Cluster(
            "Unified Namespace Hub",
            graph_attr={"bgcolor": "#0a3d5c", "fontcolor": HIVEMQ_YELLOW},
        ):
            uns_broker = Custom("HiveMQ\nPlatform", f"{HMQ_ICONS}/hivemq_platform_asset.png")
            datahub = Custom("Data Hub\n(Schema Validation)", f"{ICONS}/Data-Security.png")
            pulse = Custom("HiveMQ\nPulse", f"{ICONS}/Pulse-Server.png")

        # ISA-95 Level 2-3: Operations
        with Cluster(
            "Operations Domain (ISA-95 L2-L3)",
            graph_attr={"bgcolor": DARK_GREY, "fontcolor": HIVEMQ_WHITE},
        ):
            scada = Custom("SCADA /\nHMI", f"{ICONS}/Monitor browser.png")
            mes = Custom("MES\nSystem", f"{ICONS}/Factory.png")
            historian = Custom("Process\nHistorian", f"{ICONS}/Data-Historian.png")

        # ISA-95 Level 4: Business
        with Cluster(
            "Business Domain (ISA-95 L4)",
            graph_attr={"bgcolor": "#2a1a3d", "fontcolor": HIVEMQ_WHITE},
        ):
            erp = Custom("ERP\nSystem", f"{ICONS}/Data Applications.png")
            bi = Custom("BI &\nReporting", f"{ICONS}/Monitor stats.png")

        # Persistence Layer
        with Cluster(
            "Data Persistence Layer",
            graph_attr={"bgcolor": DARK_GREY, "fontcolor": HIVEMQ_WHITE},
        ):
            tsdb = Custom("Time-Series\nDB", f"{ICONS}/Data-Historian.png")
            kafka = Custom("Apache\nKafka", f"{ICONS}/Data-real-time.png")
            datalake = Custom("Data Lake", f"{ICONS}/Data-lake.png")

        # Remote Site Bridge
        with Cluster(
            "Remote Site (Plant 2)",
            graph_attr={"bgcolor": DARK_GREY, "fontcolor": HIVEMQ_WHITE},
        ):
            remote_broker = Custom("Remote\nBroker", f"{HMQ_ICONS}/hivemq_platform_asset.png")
            remote_edge = Custom("Remote\nEdge", f"{HMQ_ICONS}/hivemq_edge_cloud_asset.png")

        # Control → UNS Hub
        edge >> Edge(
            label="Sparkplug B",
            color=HIVEMQ_YELLOW,
            fontcolor=HIVEMQ_YELLOW,
            style="bold",
        ) >> uns_broker

        # UNS Hub internals
        uns_broker >> Edge(color=HIVEMQ_TEAL) >> datahub
        uns_broker >> Edge(color=HIVEMQ_TEAL) >> pulse

        # UNS Hub → Operations
        uns_broker >> Edge(color=HIVEMQ_YELLOW) >> scada
        uns_broker >> Edge(color=HIVEMQ_YELLOW) >> mes
        uns_broker >> Edge(color=HIVEMQ_YELLOW) >> historian

        # UNS Hub → Business
        uns_broker >> Edge(color=HIVEMQ_TEAL) >> erp
        uns_broker >> Edge(color=HIVEMQ_TEAL) >> bi

        # UNS Hub → Persistence
        uns_broker >> Edge(label="Kafka Ext.", color=HIVEMQ_TEAL, fontcolor=HIVEMQ_TEAL) >> kafka
        kafka >> Edge(color=HIVEMQ_TEAL) >> tsdb
        kafka >> Edge(color=HIVEMQ_TEAL) >> datalake

        # UNS Hub ↔ Remote Site
        uns_broker >> Edge(
            label="MQTT Bridge\n(TLS)",
            color=HIVEMQ_YELLOW,
            fontcolor=HIVEMQ_YELLOW,
            style="dashed",
        ) >> remote_broker
        remote_edge >> Edge(color=HIVEMQ_YELLOW) >> remote_broker

    print("Generated: 04_unified_namespace.png")


if __name__ == "__main__":
    main()
