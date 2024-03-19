# SETUP
import os
import sys
import logging
logging.basicConfig(level=logging.INFO)

ROOT_DIR = os.path.abspath(os.path.join(__file__, '../..'))
sys.path.append(ROOT_DIR)
logging.debug(f"Added {ROOT_DIR!r} to PYTHONPATH")

# IMPORTS
import typing as tp
import click
from omegaconf import OmegaConf
from tqdm import tqdm
import json
from gtts import gTTS

from helpers.src.config_helpers import read_config, pprint_config
from helpers.src.read_write import read_json, write_json, _create_dir
from anki.src.anki_api import AnkiApi
# hash
import hashlib

def get_hash(length: int = 10) -> str:
    """Get hash of length"""
    return hashlib.sha256(os.urandom(1024)).hexdigest()[:length]
    

def gen_hash(data: tp.List[tp.Dict], cfg: OmegaConf) -> tp.List[tp.Dict]:
    """Generate hash for each audio"""
    hash_audio_key = cfg.audio.hash_key
    for idx, sample in enumerate(tqdm(data, desc="Adding audio hash")):
        sample[hash_audio_key] = f"{get_hash()}.mp3"
    return data

def add_audio_to_anki(data: tp.List[tp.Dict], cfg: OmegaConf) -> None:
    """Add audio to Anki"""
    api = AnkiApi()
    hash_audio_key, path_audio_key = cfg.audio.hash_key, cfg.audio.path_key
    for sample in tqdm(data, desc="Adding audio to Anki"):
        api.add_audio(path=sample[path_audio_key], filename=sample[hash_audio_key])

def start_pipeline(cfg: OmegaConf) -> None:
    """Start pipeline of the script"""
    data = read_json(cfg.result.result)
    data_with_audio = gen_hash(data, cfg.result)
    add_audio_to_anki(data_with_audio, cfg.result)
    write_json(data_with_audio, cfg.result.result)

@click.command()
@click.option("--verbose", "-v", is_flag=True, help="Whether to print config")
@click.option("--result", help="Name of result config")
def main(verbose: bool, result: str) -> None:
    overrides = [f"+dataset/result@result={result}"]
    cfg: OmegaConf = read_config(overrides=overrides)
    if verbose:
        pprint_config(cfg)
    start_pipeline(cfg)

if __name__ == "__main__":
    main()
