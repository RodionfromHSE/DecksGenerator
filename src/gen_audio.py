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

def get_anki_media_folder() -> str:
    """Get Anki media folder"""
    if sys.platform.startswith("win"):
        anki_media_folder = os.path.join(os.getenv("APPDATA"), "Anki2", "User 1", "collection.media")
    elif sys.platform == "darwin":  # macOS
        anki_media_folder = os.path.expanduser("~/Library/Application Support/Anki2/User 1/collection.media")
    else:  # Linux and other Unix-based systems
        anki_media_folder = os.path.expanduser("~/.local/share/Anki2/User 1/collection.media")
    return anki_media_folder

def gen_and_add_audio_path(data: tp.List[tp.Dict], cfg: OmegaConf) -> tp.List[tp.Dict]:
    """Generate audio and add audio path to data"""
    path_audio_key, audio_key, audio_dir, lang, top_level_domain = cfg.audio.path_key, cfg.audio.key, cfg.name, cfg.audio.lang, cfg.audio.tld
    audio_full_dir = os.path.join(get_anki_media_folder(), audio_dir)
    _create_dir(audio_full_dir)
    for idx, sample in enumerate(tqdm(data, desc="Adding audio path")):
        tts = gTTS(sample[audio_key], lang=lang)
        rel_path = os.path.join(audio_dir, f"{idx}.mp3")
        path = os.path.join(audio_full_dir, f"{idx}.mp3")
        tts.save(path)
        sample[path_audio_key] = rel_path
    return data

def start_pipeline(cfg: OmegaConf) -> None:
    """Start pipeline of the script"""
    data = read_json(cfg.result.result)
    data_with_audio = gen_and_add_audio_path(data, cfg.result)
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
