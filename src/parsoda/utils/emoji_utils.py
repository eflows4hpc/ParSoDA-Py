# -*- coding: utf-8 -*-


def load_emojis(file_path):
    import json
    emojis = {}
    with open(file_path, 'r') as f:
        emoji_json = json.load(f)
    for jsonOb in emoji_json:
        emojis[jsonOb["emoji"]] = jsonOb["polarity"]
    return emojis


def get_emojis(text: str):
    import emoji
    found_emojis = []
    for language, emojis in emoji.unicode_codes.UNICODE_EMOJI.items():
        for e in emojis:
            if text.find(e) >= 0:
                found_emojis.append(e)
    return found_emojis
