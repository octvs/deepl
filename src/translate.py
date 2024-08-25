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
    print(
        translator.translate_text(
            input,
            source_lang=languages[args._from],
            target_lang=languages[args._to],
        )
    )


if __name__ == "__main__":
    main()
