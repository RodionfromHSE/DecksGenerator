"""
Helper functions for reading and printing configs
"""
from omegaconf import OmegaConf
import json
import typing as tp
import os

__ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
__CONFIG_DIR = os.path.join(__ROOT_DIR, "conf")

def read_config(config_path: str = os.path.join(__CONFIG_DIR, "config.yaml")) -> OmegaConf:
    """
    :@param config_path: path to config directory
    :@return: OmegaConf object
    """
    config_path = os.path.abspath(config_path)
    cfg = OmegaConf.load(config_path)
    cfg = OmegaConf.create(OmegaConf.to_yaml(cfg, resolve=True))
    return cfg

def pprint_config(cfg: OmegaConf) -> None:
    "Pretty print config"
    print(json.dumps(OmegaConf.to_container(cfg), indent=2))
