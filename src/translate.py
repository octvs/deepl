import argparse
import os
import re
import subprocess
import sys

import deepl

languages = {"de": "DE", "en": "EN-US", "tr": "TR"}


def side_by_side(strings, terminal_w=os.get_terminal_size().columns, gap=4):
    w = (terminal_w - gap - 1) // 2
    separator = " " * (gap // 2) + "|" + " " * (gap // 2)
    result = []
    while any(strings):
        line = []
        for i, s in enumerate(strings):
            buf = s[:w]
            try:
                n = buf.index("\n")
                line.append(buf[:n].ljust(w))
                strings[i] = s[n + 1 :]
            except ValueError:
                line.append(buf.ljust(w))
                strings[i] = s[w:]
        result.append(separator.join(line))
    return "\n".join(result)


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
    result = translator.translate_text(
        input,
        source_lang=languages[args._from],
        target_lang=languages[args._to],
    )
    print(side_by_side([input, result.text]))


if __name__ == "__main__":
    main()
