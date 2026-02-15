#!/usr/bin/env python3
"""
Reference Architecture: Multi-Site Energy & Utilities
Composite architecture applying patterns from all four HiveMQ blog articles.

Usage:
    python 05_multi_site_energy.py              # dark background (default)
    python 05_multi_site_energy.py --bg white   # white background
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
    output = os.path.join(os.path.dirname(__file__), f"05_multi_site_energy{suffix}")

    broker_bg = "#0a3d5c" if background == "black" else "#d6eaf8"
    cloud_bg = "#2a1a3d" if background == "black" else "#e8daef"

    with Diagram(
        "Multi-Site Energy Grid Architecture",
        show=False,
        filename=output,
        outformat="png",
        direction="LR",
        graph_attr=global_attr,
    ):
        with Cluster(
            "Wind Farm (North Region)",
            graph_attr={"bgcolor": cluster_bg, "fontcolor": cluster_fc},
        ):
            turbines = Custom("Wind\nTurbines", f"{ICONS}/Wind-Turbine.png")
            wind_sensor = Custom("Weather\nSensors", f"{ICONS}/Sensor.png")
            wind_edge = Custom("HiveMQ\nEdge", f"{HMQ_ICONS}/hivemq_edge_cloud_asset.png")

            [turbines, wind_sensor] >> Edge(color=HIVEMQ_YELLOW) >> wind_edge

        with Cluster(
            "Solar Farm (South Region)",
            graph_attr={"bgcolor": cluster_bg, "fontcolor": cluster_fc},
        ):
            panels = Custom("Solar\nPanels", f"{ICONS}/Solar-panel.png")
            inverters = Custom("Power\nInverters", f"{ICONS}/Electricity-Tower.png")
            solar_edge = Custom("HiveMQ\nEdge", f"{HMQ_ICONS}/hivemq_edge_cloud_asset.png")

            [panels, inverters] >> Edge(color=HIVEMQ_YELLOW) >> solar_edge

        with Cluster(
            "Hydro Plant (East Region)",
            graph_attr={"bgcolor": cluster_bg, "fontcolor": cluster_fc},
        ):
            turbine_h = Custom("Hydro\nTurbines", f"{ICONS}/Hydro-Turbine.png")
            flow_ctrl = Custom("Flow\nControl", f"{ICONS}/Gear.png")
            hydro_edge = Custom("HiveMQ\nEdge", f"{HMQ_ICONS}/hivemq_edge_cloud_asset.png")

            [turbine_h, flow_ctrl] >> Edge(color=HIVEMQ_YELLOW) >> hydro_edge

        with Cluster(
            "Central Grid Broker (Cloud)",
            graph_attr={"bgcolor": broker_bg, "fontcolor": HIVEMQ_YELLOW},
        ):
            cloud_broker = Custom("HiveMQ\nCloud Cluster", f"{HMQ_ICONS}/hivemq_platform_asset.png")
            datahub = Custom("Data Hub\n(Validation)", f"{ICONS}/Data-Security.png")

        with Cluster(
            "Grid Intelligence Platform",
            graph_attr={"bgcolor": cloud_bg, "fontcolor": cluster_fc},
        ):
            demand = Custom("Demand\nForecasting", f"{ICONS}/Monitor stats.png")
            grid_dash = Custom("Grid\nDashboard", f"{ICONS}/Monitor browser.png")
            compliance = Custom("Regulatory\nCompliance", f"{ICONS}/Regulatory Compliance.png")
            datalake = Custom("Energy\nData Lake", f"{ICONS}/Data-lake.png")

        wind_edge >> Edge(
            label="MQTT Bridge",
            color=HIVEMQ_YELLOW,
            fontcolor=HIVEMQ_YELLOW,
            style="bold",
        ) >> cloud_broker

        solar_edge >> Edge(
            label="MQTT Bridge",
            color=HIVEMQ_YELLOW,
            fontcolor=HIVEMQ_YELLOW,
            style="bold",
        ) >> cloud_broker

        hydro_edge >> Edge(
            label="MQTT Bridge",
            color=HIVEMQ_YELLOW,
            fontcolor=HIVEMQ_YELLOW,
            style="bold",
        ) >> cloud_broker

        cloud_broker >> Edge(color=HIVEMQ_TEAL) >> datahub

        cloud_broker >> Edge(color=HIVEMQ_TEAL) >> demand
        cloud_broker >> Edge(color=HIVEMQ_TEAL) >> grid_dash
        cloud_broker >> Edge(color=HIVEMQ_TEAL) >> compliance
        cloud_broker >> Edge(color=HIVEMQ_TEAL) >> datalake

    print(f"Generated: 05_multi_site_energy{suffix}.png")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--bg", choices=["black", "white"], default="black")
    args = parser.parse_args()
    main(args.bg)
