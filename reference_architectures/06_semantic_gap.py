#!/usr/bin/env python3
"""
Reference Architecture: The Semantic Gap
Shows the missing ontology/semantic layer between data collection and AI inference.
Data flows from PLCs/sensors upward, loses context without the semantic layer,
and arrives at AI models as raw numbers without meaning.

Usage:
    python 06_semantic_gap.py              # dark background (default)
    python 06_semantic_gap.py --bg white   # white background
    python 06_semantic_gap.py --bg transparent
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from diagrams import Cluster, Diagram, Edge
from diagrams.custom import Custom

from hivemq_theme import DARK_GREY, HIVEMQ_TEAL, HIVEMQ_YELLOW, get_theme

ICONS = os.path.join(os.path.dirname(__file__), "..", "icons", "PNGs")
HMQ_ICONS = os.path.join(os.path.dirname(__file__), "..", "icons")

# Colors for the "gap" / missing layer
GAP_RED = "#FF4444"
DIMMED = "#666666"


def main(background="black"):
    global_attr, base_node_attr, cluster_fc, cluster_bg = get_theme(background)
    suffix = "_light" if background == "white" else "_transparent" if background == "transparent" else ""
    output = os.path.join(os.path.dirname(__file__), f"06_semantic_gap{suffix}")

    # Clear/white cluster backgrounds for white mode, dark for black
    if background == "black":
        layer_bg = DARK_GREY
        gap_bg = "#4a1a1a"
        ai_bg = "#2a1a3d"
        label_color = HIVEMQ_YELLOW
        border_color = "#666666"
    else:
        layer_bg = "transparent"
        gap_bg = "transparent"
        ai_bg = "transparent"
        label_color = "#333333"
        border_color = "#CCCCCC"

    with Diagram(
        "The Semantic Gap: What's Missing Between Data and AI",
        show=False,
        filename=output,
        outformat="png",
        direction="LR",
        graph_attr={
            **global_attr,
            "ranksep": "1.8",
            "nodesep": "0.8",
            "ratio": "0.75",
            "size": "16,12!",
        },
    ):
        # --- Layer 1: Data Collection (left) ---
        with Cluster(
            "Layer 1\nData Collection (OT/Edge)",
            graph_attr={"bgcolor": layer_bg, "fontcolor": label_color, "fontsize": "18",
                        "pencolor": border_color, "penwidth": "2"},
        ):
            plc = Custom("PLCs", f"{ICONS}/PLC.png")
            sensor = Custom("Industrial\nSensors", f"{ICONS}/Sensor.png")
            modbus = Custom("Modbus\nDevices", f"{ICONS}/Modbus.png")
            edge = Custom("HiveMQ\nEdge", f"{HMQ_ICONS}/hivemq_edge_cloud_asset.png")

            [plc, sensor, modbus] >> Edge(color=HIVEMQ_YELLOW) >> edge

        # --- Layer 2: The Missing Semantic Layer (middle) ---
        with Cluster(
            "Layer 2\nOntology / Semantic Layer  ⚠ MISSING",
            graph_attr={
                "bgcolor": gap_bg,
                "fontcolor": GAP_RED,
                "fontsize": "18",
                "style": "dashed",
                "pencolor": GAP_RED,
                "penwidth": "3",
            },
        ):
            question1 = Custom("Context?\n(What is this data?)", f"{ICONS}/Question.png")
            question2 = Custom("Relationships?\n(How does it connect?)", f"{ICONS}/Question.png")
            question3 = Custom("Meaning?\n(Units, ranges, type)", f"{ICONS}/Question.png")

        # --- Layer 3: AI / Model Inference (right) ---
        with Cluster(
            "Layer 3\nAI & Model Inference",
            graph_attr={"bgcolor": ai_bg, "fontcolor": label_color, "fontsize": "18",
                        "pencolor": border_color, "penwidth": "2"},
        ):
            ml_model = Custom("ML Model\n(Prediction)", f"{ICONS}/Data Applications.png")
            dashboard = Custom("Analytics\nDashboard", f"{ICONS}/Monitor stats.png")
            digital_twin = Custom("Digital\nTwin", f"{ICONS}/digital-twin.png")

        # --- Data flows from Layer 1 through the gap ---
        edge >> Edge(
            label="Raw values:\n0x1A3F, 47.2, 1, 0 ...",
            color=HIVEMQ_YELLOW,
            fontcolor=HIVEMQ_YELLOW,
            style="bold",
        ) >> question1

        edge >> Edge(
            color=HIVEMQ_YELLOW,
            style="bold",
        ) >> question2

        edge >> Edge(
            color=HIVEMQ_YELLOW,
            style="bold",
        ) >> question3

        # --- Gap to AI: data arrives without meaning ---
        question1 >> Edge(
            label="No context →\njust numbers",
            color=GAP_RED,
            fontcolor=GAP_RED,
            style="dashed",
        ) >> ml_model

        question2 >> Edge(
            color=GAP_RED,
            style="dashed",
        ) >> dashboard

        question3 >> Edge(
            label="No semantics →\ngarbage in, garbage out",
            color=GAP_RED,
            fontcolor=GAP_RED,
            style="dashed",
        ) >> digital_twin

    print(f"Generated: 06_semantic_gap{suffix}.png")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--bg", choices=["black", "white", "transparent"], default="black")
    args = parser.parse_args()
    main(args.bg)
