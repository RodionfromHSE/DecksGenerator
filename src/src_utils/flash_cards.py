# SETUP
import os
import sys
import logging
logging.basicConfig(level=logging.INFO)

ROOT_DIR = os.path.abspath(os.path.join(__file__, '../../..'))
sys.path.append(ROOT_DIR)
logging.debug(f"Added {ROOT_DIR!r} to PYTHONPATH")

# IMPORTS
from deck_utils.read import read_json, write_json, append_json
from dataclasses import dataclass
import typing as tp

from helpers.src.helpers import smart_format

@dataclass
class FlashCard:
    front: str
    back: str

class FlashCardGenerator:
    """Generate flashcards from data based on templates
    
    Args:
        card_templates (List[Dict]): List of card templates
        audio_hash_key (str | None): Key in data to use for audio hash
    """
    AUDIO_KEY = "audio"
    def __init__(self, card_templates: tp.List[tp.Dict], audio_hash_key: str | None = None) -> None:
        self.card_templates = card_templates
        self.audio_hash_key = audio_hash_key

    def __call__(self, data: dict) -> tp.List[dict]:
        """Generate flashcards for one data sample"""
        if self.audio_hash_key:
            data[self.AUDIO_KEY] = f"<br>[sound:{data[self.audio_hash_key]}]"
        flashcards = []
        for template in self.card_templates:
            front = smart_format(template.front, **data)
            back = smart_format(template.back, **data)
            flashcards.append(FlashCard(front, back))
        return flashcards
