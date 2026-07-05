import json
import re

import requests

from ..data.implings import Impling

MAIN_URL = "https://oldschool.runescape.wiki/w/{0}_impling"
headers = {"User-Agent": "scroll calculator"}

title_pattern = r'.*title\=\"Clue scroll \(\w+\)\">(.*)</a>.*'
chance_pattern = r'.*data-drop-oneover\="\d+/\d+\"\>?(.*)?</span>.*'

def retrieve_scroll_chance():

    data = {}

    for impling in Impling:

        print(f"Retrieving scroll drop chances for {impling.name} impling")

        r = requests.get(MAIN_URL.format(impling.name.title()), headers=headers)
        if r.status_code not in [200]:
            raise RuntimeError(f"Can't download the page\r\n{r.url}\r\n{r.reason}\r\n{r.status_code}")

        text = r.text.split('<h3 id="Tertiary">Tertiary</h3>')[-1]
        text = text.split("</table>")[0]
        text = text.split("<tbody>")[-1]
        text = text.split("</tbody>")[0]
        title_matches =  re.findall(re.compile(title_pattern), text)
        chance_matches = re.findall(re.compile(chance_pattern), text)
        data[impling.name] = list(zip(title_matches, chance_matches))

    return data