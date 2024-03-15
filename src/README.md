## Generation

1. Generate the new collection of words (see `generate.py`)

## Deck

```bash
result=de_a2

python parse_result.py --result $result
python gen_audio.py --result $result
python save_audio_to_anki.py --result $result
python create_deck.py --deck $result
```