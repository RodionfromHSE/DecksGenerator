## Attention

> The whole project has to be rewritten. The code is not clean and not well-structured; it's hard to maintain and extend it.

Top-priority:
- [ ] Rewrite the self-made anki api for `anki-connect-api` with all the functions I need.
- [ ] Fix the problem with absolute paths for audio
Audio storage:
```bash
$ankiMediaPath = "$env:APPDATA\Anki2\User 1\collection.media" # Windows
ankiMediaPath="$HOME/Library/Application Support/Anki2/User 1/collection.media" # Mac
ankiMediaPath="$HOME/.local/share/Anki2/User 1/collection.media" # Linux
```
You can use relative paths in `[sound:PATH]` in the card's field so that it'd be synced with the media folder.

# DecksGenerator
A collection of scripts for conversion list of english words to complete [en-ru] anki decks with sentences and definitions for each word.



## Cloning the project
**The project has submodules!**

```bash
git clone --recurse-submodules $url
```
If you forgot to use `--recurse-submodules` when cloning, you can run `git submodule update --init --recursive` to fetch the submodules.


## Sources

1. [Words](https://github.com/openlanguageprofiles/olp-en-cefrj/blob/master/README.md)
2. [English Profiles](https://englishprofile.org/wordlists/evp)

## Motivation

I want to create en-ru decks based on English Profiles to help a lot of Russian speaking English learners.