import argparse
import re
import subprocess
import sys

import deepl

languages = {"de": "DE", "en": "EN-US", "tr": "TR"}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-f",
        "--from",
        type=str,
        default="de",
        help="source language",
        dest="_from",
    )
    parser.add_argument(
        "-t",
        "--to",
        type=str,
        default="en",
        help="target language",
        dest="_to",
    )
    args = parser.parse_args()

    auth_key = re.search(
        "api: (.*)",
        subprocess.run(
            ["pass", "deepl"], capture_output=True, text=True
        ).stdout,
    ).group(1)
    translator = deepl.Translator(auth_key)
    input = sys.stdin.read()
    _fr = languages.get(args._from, args._from)
    _to = languages.get(args._to, args._to)
    print(translator.translate_text(input, source_lang=_fr, target_lang=_to))


if __name__ == "__main__":
    main()
