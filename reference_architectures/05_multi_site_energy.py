#!/usr/bin/env python3
"""
Reference Architecture: Multi-Site Energy & Utilities
Composite architecture drawing from all 4 blog articles, applied to the
energy/utilities vertical.

Multi-site renewable energy grid: Wind farm + Solar farm + Hydro plant
each with HiveMQ Edge → regional HiveMQ brokers → central cloud broker
→ grid analytics, demand forecasting, and regulatory compliance.
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
    output = os.path.join(os.path.dirname(__file__), "05_multi_site_energy")

    with Diagram(
        "Multi-Site Energy Grid Architecture",
        show=False,
        filename=output,
        outformat="png",
        direction="LR",
        graph_attr=GLOBAL_ATTR,
    ):
        # Site 1: Wind Farm
        with Cluster(
            "Wind Farm (North Region)",
            graph_attr={"bgcolor": DARK_GREY, "fontcolor": HIVEMQ_WHITE},
        ):
            turbines = Custom("Wind\nTurbines", f"{ICONS}/Wind-Turbine.png")
            wind_sensor = Custom("Weather\nSensors", f"{ICONS}/Sensor.png")
            wind_edge = Custom("HiveMQ\nEdge", f"{HMQ_ICONS}/hivemq_edge_cloud_asset.png")

            [turbines, wind_sensor] >> Edge(color=HIVEMQ_YELLOW) >> wind_edge

        # Site 2: Solar Farm
        with Cluster(
            "Solar Farm (South Region)",
            graph_attr={"bgcolor": DARK_GREY, "fontcolor": HIVEMQ_WHITE},
        ):
            panels = Custom("Solar\nPanels", f"{ICONS}/Solar-panel.png")
            inverters = Custom("Power\nInverters", f"{ICONS}/Electricity-Tower.png")
            solar_edge = Custom("HiveMQ\nEdge", f"{HMQ_ICONS}/hivemq_edge_cloud_asset.png")

            [panels, inverters] >> Edge(color=HIVEMQ_YELLOW) >> solar_edge

        # Site 3: Hydro Plant
        with Cluster(
            "Hydro Plant (East Region)",
            graph_attr={"bgcolor": DARK_GREY, "fontcolor": HIVEMQ_WHITE},
        ):
            turbine_h = Custom("Hydro\nTurbines", f"{ICONS}/Hydro-Turbine.png")
            flow_ctrl = Custom("Flow\nControl", f"{ICONS}/Gear.png")
            hydro_edge = Custom("HiveMQ\nEdge", f"{HMQ_ICONS}/hivemq_edge_cloud_asset.png")

            [turbine_h, flow_ctrl] >> Edge(color=HIVEMQ_YELLOW) >> hydro_edge

        # Central Cloud Broker
        with Cluster(
            "Central Grid Broker (Cloud)",
            graph_attr={"bgcolor": "#0a3d5c", "fontcolor": HIVEMQ_YELLOW},
        ):
            cloud_broker = Custom("HiveMQ\nCloud Cluster", f"{HMQ_ICONS}/hivemq_platform_asset.png")
            datahub = Custom("Data Hub\n(Validation)", f"{ICONS}/Data-Security.png")

        # Grid Analytics
        with Cluster(
            "Grid Intelligence Platform",
            graph_attr={"bgcolor": "#2a1a3d", "fontcolor": HIVEMQ_WHITE},
        ):
            demand = Custom("Demand\nForecasting", f"{ICONS}/Monitor stats.png")
            grid_dash = Custom("Grid\nDashboard", f"{ICONS}/Monitor browser.png")
            compliance = Custom("Regulatory\nCompliance", f"{ICONS}/Regulatory Compliance.png")
            datalake = Custom("Energy\nData Lake", f"{ICONS}/Data-lake.png")

        # Edge → Cloud bridges
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

        # Cloud → Analytics
        cloud_broker >> Edge(color=HIVEMQ_TEAL) >> demand
        cloud_broker >> Edge(color=HIVEMQ_TEAL) >> grid_dash
        cloud_broker >> Edge(color=HIVEMQ_TEAL) >> compliance
        cloud_broker >> Edge(color=HIVEMQ_TEAL) >> datalake

    print("Generated: 05_multi_site_energy.png")


if __name__ == "__main__":
    main()
