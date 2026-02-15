#!/usr/bin/env python3
"""
Reference Architecture: Unified Namespace (UNS)
Based on: https://www.hivemq.com/blog/foundations-of-unified-namespace-architecture-iiot/

Usage:
    python 04_unified_namespace.py              # dark background (default)
    python 04_unified_namespace.py --bg white   # white background
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
    output = os.path.join(os.path.dirname(__file__), f"04_unified_namespace{suffix}")

    broker_bg = "#0a3d5c" if background == "black" else "#d6eaf8"
    cloud_bg = "#2a1a3d" if background == "black" else "#e8daef"

    with Diagram(
        "Unified Namespace (UNS) Reference Architecture",
        show=False,
        filename=output,
        outformat="png",
        direction="TB",
        graph_attr=global_attr,
    ):
        with Cluster(
            "Control Domain (ISA-95 L0-L1)",
            graph_attr={"bgcolor": cluster_bg, "fontcolor": cluster_fc},
        ):
            sensor = Custom("Sensors &\nActuators", f"{ICONS}/Sensor.png")
            plc = Custom("PLCs &\nControllers", f"{ICONS}/PLC.png")
            edge = Custom("HiveMQ\nEdge", f"{HMQ_ICONS}/hivemq_edge_cloud_asset.png")

            [sensor, plc] >> Edge(color=HIVEMQ_YELLOW) >> edge

        with Cluster(
            "Unified Namespace Hub",
            graph_attr={"bgcolor": broker_bg, "fontcolor": HIVEMQ_YELLOW},
        ):
            uns_broker = Custom("HiveMQ\nPlatform", f"{HMQ_ICONS}/hivemq_platform_asset.png")
            datahub = Custom("Data Hub\n(Schema Validation)", f"{ICONS}/Data-Security.png")
            pulse = Custom("HiveMQ\nPulse", f"{ICONS}/Pulse-Server.png")

        with Cluster(
            "Operations Domain (ISA-95 L2-L3)",
            graph_attr={"bgcolor": cluster_bg, "fontcolor": cluster_fc},
        ):
            scada = Custom("SCADA /\nHMI", f"{ICONS}/Monitor browser.png")
            mes = Custom("MES\nSystem", f"{ICONS}/Factory.png")
            historian = Custom("Process\nHistorian", f"{ICONS}/Data-Historian.png")

        with Cluster(
            "Business Domain (ISA-95 L4)",
            graph_attr={"bgcolor": cloud_bg, "fontcolor": cluster_fc},
        ):
            erp = Custom("ERP\nSystem", f"{ICONS}/Data Applications.png")
            bi = Custom("BI &\nReporting", f"{ICONS}/Monitor stats.png")

        with Cluster(
            "Data Persistence Layer",
            graph_attr={"bgcolor": cluster_bg, "fontcolor": cluster_fc},
        ):
            tsdb = Custom("Time-Series\nDB", f"{ICONS}/Data-Historian.png")
            kafka = Custom("Apache\nKafka", f"{ICONS}/Data-real-time.png")
            datalake = Custom("Data Lake", f"{ICONS}/Data-lake.png")

        with Cluster(
            "Remote Site (Plant 2)",
            graph_attr={"bgcolor": cluster_bg, "fontcolor": cluster_fc},
        ):
            remote_broker = Custom("Remote\nBroker", f"{HMQ_ICONS}/hivemq_platform_asset.png")
            remote_edge = Custom("Remote\nEdge", f"{HMQ_ICONS}/hivemq_edge_cloud_asset.png")

        edge >> Edge(
            label="Sparkplug B",
            color=HIVEMQ_YELLOW,
            fontcolor=HIVEMQ_YELLOW,
            style="bold",
        ) >> uns_broker

        uns_broker >> Edge(color=HIVEMQ_TEAL) >> datahub
        uns_broker >> Edge(color=HIVEMQ_TEAL) >> pulse

        uns_broker >> Edge(color=HIVEMQ_YELLOW) >> scada
        uns_broker >> Edge(color=HIVEMQ_YELLOW) >> mes
        uns_broker >> Edge(color=HIVEMQ_YELLOW) >> historian

        uns_broker >> Edge(color=HIVEMQ_TEAL) >> erp
        uns_broker >> Edge(color=HIVEMQ_TEAL) >> bi

        uns_broker >> Edge(label="Kafka Ext.", color=HIVEMQ_TEAL, fontcolor=HIVEMQ_TEAL) >> kafka
        kafka >> Edge(color=HIVEMQ_TEAL) >> tsdb
        kafka >> Edge(color=HIVEMQ_TEAL) >> datalake

        uns_broker >> Edge(
            label="MQTT Bridge\n(TLS)",
            color=HIVEMQ_YELLOW,
            fontcolor=HIVEMQ_YELLOW,
            style="dashed",
        ) >> remote_broker
        remote_edge >> Edge(color=HIVEMQ_YELLOW) >> remote_broker

    print(f"Generated: 04_unified_namespace{suffix}.png")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--bg", choices=["black", "white"], default="black")
    args = parser.parse_args()
    main(args.bg)
