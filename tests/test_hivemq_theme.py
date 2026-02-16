import unittest
import os
import sys
import tempfile
import csv
import json

import yaml

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from hivemq_theme import (
    HiveMQPalette,
    get_theme,
    HIVEMQ_YELLOW,
    HIVEMQ_BLACK,
    HIVEMQ_WHITE,
    HIVEMQ_TEAL,
    DARK_GREY,
    GLOBAL_ATTR,
    BASE_NODE_ATTR,
)


class TestGetTheme(unittest.TestCase):
    def test_black_theme_defaults(self):
        global_attr, node_attr, cluster_fc, cluster_bg = get_theme("black")
        self.assertEqual(global_attr["bgcolor"], HIVEMQ_BLACK)
        self.assertEqual(cluster_fc, HIVEMQ_YELLOW)
        self.assertEqual(cluster_bg, DARK_GREY)

    def test_white_theme(self):
        global_attr, node_attr, cluster_fc, cluster_bg = get_theme("white")
        self.assertEqual(global_attr["bgcolor"], HIVEMQ_WHITE)
        self.assertEqual(global_attr["fontcolor"], HIVEMQ_BLACK)
        self.assertEqual(cluster_fc, HIVEMQ_YELLOW)
        self.assertEqual(cluster_bg, "#2C2C2C")

    def test_transparent_theme(self):
        global_attr, node_attr, cluster_fc, cluster_bg = get_theme("transparent")
        self.assertEqual(global_attr["bgcolor"], "transparent")
        self.assertEqual(cluster_bg, "#2C2C2C")

    def test_default_is_black(self):
        default = get_theme()
        black = get_theme("black")
        self.assertEqual(default, black)

    def test_returns_four_tuple(self):
        result = get_theme("black")
        self.assertEqual(len(result), 4)


class TestHiveMQPaletteBootstrap(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.TemporaryDirectory()
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir.name)

    def tearDown(self):
        os.chdir(self.original_cwd)
        self.test_dir.cleanup()

    def test_bootstrap_creates_icons_dir(self):
        HiveMQPalette("test_config.yaml")
        self.assertTrue(os.path.isdir("icons"))

    def test_bootstrap_creates_yaml_config(self):
        HiveMQPalette("test_config.yaml")
        self.assertTrue(os.path.exists("test_config.yaml"))
        with open("test_config.yaml") as f:
            data = yaml.safe_load(f)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["symbol"], "edge")

    def test_bootstrap_creates_csv_config(self):
        HiveMQPalette("test_config.csv")
        self.assertTrue(os.path.exists("test_config.csv"))
        with open("test_config.csv") as f:
            reader = list(csv.DictReader(f))
        self.assertEqual(len(reader), 1)
        self.assertEqual(reader[0]["symbol"], "edge")

    def test_bootstrap_creates_json_config(self):
        HiveMQPalette("test_config.json")
        self.assertTrue(os.path.exists("test_config.json"))
        with open("test_config.json") as f:
            data = json.load(f)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["symbol"], "edge")


class TestHiveMQPaletteLoadIcons(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.TemporaryDirectory()
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir.name)
        os.makedirs("icons")

    def tearDown(self):
        os.chdir(self.original_cwd)
        self.test_dir.cleanup()

    def _write_csv(self, path, rows):
        with open(path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["symbol", "path", "notes"])
            writer.writeheader()
            writer.writerows(rows)

    def test_load_csv(self):
        self._write_csv("icons.csv", [
            {"symbol": "sensor", "path": "./icons/sensor.png", "notes": "Sensor"},
            {"symbol": "plc", "path": "./icons/plc.png", "notes": "PLC"},
        ])
        palette = HiveMQPalette("icons.csv")
        self.assertIn("sensor", palette.icon_data)
        self.assertIn("plc", palette.icon_data)

    def test_load_yaml(self):
        data = [
            {"symbol": "sensor", "path": "./icons/sensor.png", "notes": "Sensor"},
        ]
        with open("icons.yaml", "w") as f:
            yaml.dump(data, f)
        palette = HiveMQPalette("icons.yaml")
        self.assertIn("sensor", palette.icon_data)

    def test_load_json(self):
        data = [
            {"symbol": "sensor", "path": "./icons/sensor.png", "notes": "Sensor"},
        ]
        with open("icons.json", "w") as f:
            json.dump(data, f)
        palette = HiveMQPalette("icons.json")
        self.assertIn("sensor", palette.icon_data)

    def test_symbol_lookup_case_insensitive(self):
        self._write_csv("icons.csv", [
            {"symbol": "Sensor", "path": "./icons/sensor.png", "notes": "Sensor"},
        ])
        palette = HiveMQPalette("icons.csv")
        self.assertIn("sensor", palette.icon_data)

    def test_paths_resolved_to_absolute(self):
        self._write_csv("icons.csv", [
            {"symbol": "sensor", "path": "./icons/sensor.png", "notes": "Sensor"},
        ])
        palette = HiveMQPalette("icons.csv")
        self.assertTrue(os.path.isabs(palette.icon_data["sensor"]["path"]))


class TestHiveMQPaletteBOM(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.TemporaryDirectory()
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir.name)
        os.makedirs("icons")

    def tearDown(self):
        os.chdir(self.original_cwd)
        self.test_dir.cleanup()

    def test_print_bom_empty(self):
        palette = HiveMQPalette("config.yaml")
        palette.print_bom()  # should not raise

    def test_print_bom_with_entries(self):
        palette = HiveMQPalette("config.yaml")
        palette.used_symbols = [
            {"symbol": "edge", "label": "Edge GW", "notes": "HiveMQ Edge"},
        ]
        palette.print_bom()  # should not raise

    def test_generate_readme_default_path(self):
        palette = HiveMQPalette("config.yaml")
        palette.used_symbols = [
            {"symbol": "edge", "label": "Edge GW", "notes": "HiveMQ Edge"},
        ]
        palette.generate_readme("Test_Diagram", "test.png")
        self.assertTrue(os.path.exists("README.md"))
        with open("README.md") as f:
            content = f.read()
        self.assertIn("# Test Diagram", content)
        self.assertIn("test.png", content)
        self.assertIn("Edge GW", content)

    def test_generate_readme_custom_path(self):
        palette = HiveMQPalette("config.yaml")
        palette.used_symbols = [
            {"symbol": "edge", "label": "Edge GW", "notes": "HiveMQ Edge"},
        ]
        palette.generate_readme("Test_Diagram", "test.png", output_path="custom_output.md")
        self.assertTrue(os.path.exists("custom_output.md"))
        self.assertFalse(os.path.exists("README.md"))


class TestIconValidation(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.TemporaryDirectory()
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir.name)
        os.makedirs("icons")
        # Create a real icon file for validation
        with open("icons/test_icon.png", "wb") as f:
            f.write(b"\x89PNG")  # minimal PNG header

    def tearDown(self):
        os.chdir(self.original_cwd)
        self.test_dir.cleanup()

    def test_get_node_missing_icon_raises(self):
        """get_node should raise FileNotFoundError for missing icon files."""
        data = [{"symbol": "missing", "path": "./icons/nonexistent.png", "notes": ""}]
        with open("icons.yaml", "w") as f:
            yaml.dump(data, f)
        palette = HiveMQPalette("icons.yaml")
        with self.assertRaises(FileNotFoundError):
            # Need a Diagram context for Custom nodes, but validation happens before
            from diagrams import Diagram
            with Diagram("test", show=False, outformat="png"):
                palette.get_node("missing", "Missing Icon")

    def test_get_node_valid_icon(self):
        """get_node should succeed when icon file exists."""
        data = [{"symbol": "test", "path": "./icons/test_icon.png", "notes": "Test"}]
        with open("icons.yaml", "w") as f:
            yaml.dump(data, f)
        palette = HiveMQPalette("icons.yaml")
        from diagrams import Diagram
        with Diagram("test", show=False, outformat="png"):
            node = palette.get_node("test", "Test Icon")
            self.assertIsNotNone(node)

    def test_used_symbols_tracked(self):
        """get_node should track used symbols for BOM."""
        data = [{"symbol": "test", "path": "./icons/test_icon.png", "notes": "Test"}]
        with open("icons.yaml", "w") as f:
            yaml.dump(data, f)
        palette = HiveMQPalette("icons.yaml")
        from diagrams import Diagram
        with Diagram("test", show=False, outformat="png"):
            palette.get_node("test", "Test Icon")
        self.assertEqual(len(palette.used_symbols), 1)
        self.assertEqual(palette.used_symbols[0]["symbol"], "test")


class TestProjectIconConfigs(unittest.TestCase):
    """Validate that the actual project icon configs are consistent."""

    def setUp(self):
        self.project_root = os.path.join(os.path.dirname(__file__), "..")

    def test_icons_csv_has_234_entries(self):
        csv_path = os.path.join(self.project_root, "icons.csv")
        if not os.path.exists(csv_path):
            self.skipTest("icons.csv not found")
        with open(csv_path) as f:
            rows = list(csv.DictReader(f))
        self.assertEqual(len(rows), 234)

    def test_all_csv_icons_exist(self):
        csv_path = os.path.join(self.project_root, "icons.csv")
        if not os.path.exists(csv_path):
            self.skipTest("icons.csv not found")
        with open(csv_path) as f:
            rows = list(csv.DictReader(f))
        missing = []
        for row in rows:
            full_path = os.path.normpath(os.path.join(self.project_root, row["path"]))
            if not os.path.exists(full_path):
                missing.append(f"{row['symbol']}: {row['path']}")
        self.assertEqual(missing, [], f"Missing icon files:\n" + "\n".join(missing))

    def test_no_duplicate_symbols_in_csv(self):
        csv_path = os.path.join(self.project_root, "icons.csv")
        if not os.path.exists(csv_path):
            self.skipTest("icons.csv not found")
        with open(csv_path) as f:
            rows = list(csv.DictReader(f))
        symbols = [r["symbol"] for r in rows]
        dupes = [s for s in symbols if symbols.count(s) > 1]
        self.assertEqual(list(set(dupes)), [], f"Duplicate symbols: {set(dupes)}")

    def test_csv_and_yaml_match(self):
        csv_path = os.path.join(self.project_root, "icons.csv")
        yaml_path = os.path.join(self.project_root, "icons", "icons.yaml")
        if not os.path.exists(csv_path) or not os.path.exists(yaml_path):
            self.skipTest("Config files not found")
        with open(csv_path) as f:
            csv_symbols = {r["symbol"] for r in csv.DictReader(f)}
        with open(yaml_path) as f:
            yaml_data = yaml.safe_load(f)
            yaml_symbols = {e["symbol"] for e in yaml_data}
        self.assertEqual(csv_symbols, yaml_symbols, "CSV and YAML symbol sets differ")


if __name__ == "__main__":
    unittest.main()
