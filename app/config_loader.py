"""Loads runtime configuration from a YAML file."""
import yaml


def load_config(path: str = "config.yml") -> dict:
    with open(path) as fh:
        return yaml.load(fh.read())
