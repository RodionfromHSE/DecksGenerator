# SETUP
import os
import sys
import logging
logging.basicConfig(level=logging.DEBUG)

ROOT_DIR = os.path.abspath(os.path.join(__file__, '../..'))
sys.path.append(ROOT_DIR)
logging.debug(f"Added {ROOT_DIR!r} to PYTHONPATH")

# IMPORTS
import typing as tp
import click
from omegaconf import OmegaConf
from tqdm import tqdm
import json

from helpers.src.config_helpers import read_config, pprint_config
from helpers.src.read_write import read_json, write_json

def parse_one(cfg: OmegaConf, result_raw: tp.Dict[str, tp.Any]) -> tp.List[tp.Dict[str, tp.Any]] | None:
    """Parse one result. Return None if result is invalid

    :param parse_cfg: config for parsing
    :param result_raw: raw result

    1. Extract meta_existing from result_raw
    2. Extract meta_raw from result_raw
    3. Parse meta_raw to meta
    """
    meta_existing = {key: result_raw[key] for key in cfg.keys_to_be_saved}
    meta_raw = result_raw["result"]
    try:
        meta = json.loads(meta_raw)
        meta = meta if isinstance(meta, list) else [meta]

        results = []
        for meta_new in meta:
            res = {**meta_existing, **meta_new}
            for key, remapped_key in cfg.get("remap", {}).items():
                res[remapped_key] = res.pop(key)
            results.append(res)
        return results
    except Exception as e:
        logging.debug(f"Error parsing word with existing meta {meta_existing!r}\n{e}")
    return None

def parse_json(result_cfg: OmegaConf, results_raw: tp.List[tp.Dict]) -> tp.List[tp.Dict]:
    """Parse results_raw to results"""
    n_skipped = 0
    results = []
    for result_raw in tqdm(results_raw):
        result = parse_one(cfg=result_cfg, result_raw=result_raw)
        if result is not None:
            results.extend(result)
        else:
            print("Skipping: ", result_raw)
            n_skipped += 1

    
    logging.info(f"{len(results)} were parsed")
    if n_skipped > 0:
        n_words = len(results_raw)
        logging.warning(f"Skipped {n_skipped} results ({n_skipped / n_words * 100:.2f}%)")
    return results

def parse(cfg: OmegaConf) -> None:
    """Parse results_raw to results"""
    results_raw = read_json(cfg.result.result_raw)
    results = parse_json(result_cfg=cfg.result, results_raw=results_raw)
    write_json(data=results, path=cfg.result.result)

@click.command()
@click.option("--verbose", "-v", is_flag=True, help="Whether to print config")
@click.option("--result", help="Name of result config")
def main(verbose: bool, result: str) -> None:
    overrides = [f"+dataset/result@result={result}"]
    cfg: OmegaConf = read_config(overrides=overrides)
    if verbose:
        pprint_config(cfg)
    parse(cfg)

if __name__ == "__main__":
    main()
