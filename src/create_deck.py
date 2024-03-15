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
from src_utils.flash_cards import FlashCardGenerator, FlashCard

def gen_and_add_audio_path(data: tp.List[tp.Dict], cfg: OmegaConf) -> tp.List[tp.Dict]:
    """Generate audio and add audio path to data"""
    path_audio_key, audio_key, audio_dir, lang = cfg.audio.path_key, cfg.audio.key, cfg.audio.dir, cfg.audio.lang
    _create_dir(audio_dir)
    for idx, sample in enumerate(tqdm(data, desc="Adding audio path")):
        tts = gTTS(sample[audio_key], lang=lang)
        path = os.path.join(audio_dir, f"{idx}.mp3")
        tts.save(path)
        sample[path_audio_key] = path
    return data

def start_pipeline(cfg: OmegaConf) -> None:
    """Start pipeline of the script"""
    data = read_json(cfg.result.result)
    gen = FlashCardGenerator(cfg.anki.card_templates, cfg.result.audio.path_key)

    flashcards = []
    for sample in tqdm(data, desc="Generating flashcards"):
        flashcards.extend(gen(sample))

    api = AnkiApi()
    deck_name = cfg.anki.deck
    api.create_deck(deck_name)
    for flashcard in tqdm(flashcards, desc="Creating deck"):
        api.add_flashcard(deck_name, flashcard.front, flashcard.back)
        
    

@click.command()
@click.option("--verbose", "-v", is_flag=True, help="Whether to print config")
@click.option("--deck", help="Name of deck config")
def main(verbose: bool, deck: str) -> None:
    overrides = [f"+deck={deck}"]
    cfg: OmegaConf = read_config(overrides=overrides)
    if verbose:
        pprint_config(cfg)
    start_pipeline(cfg)

if __name__ == "__main__":
    main()
