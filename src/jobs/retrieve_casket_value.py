import re

import requests

from ..data.caskets import Casket, WIKI_CASKET_REGEXES


MAIN_URL = "https://oldschool.runescape.wiki/w/Reward_casket_({0})"
MASTER_SCROLL_CHANCE_REGEX_PATTERN = r'.*data-drop-oneover=\"\d+\/\d+\">(\d+\/\d+)*</span>.*'

def retrieve_casket_value():
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:152.0) Gecko/20100101 Firefox/152.0"}
    data = {}
    for casket in Casket:

        data[casket.name] = {}

        print(f"Retrieving reward for {casket} & master scroll probability")

        if casket == Casket.WATSON:
            r = requests.get(MAIN_URL.format(Casket.MASTER.name.lower()), headers=headers)
        else:
            r = requests.get(MAIN_URL.format(casket.name.lower()),headers=headers)
        if r.status_code not in [200]:
            raise RuntimeError(f"Can't download the page\r\n{r.url}\r\n{r.reason}\r\n{r.status_code}")

        haystack = r.text.replace("\n", "")

        regex_pattern = re.compile(WIKI_CASKET_REGEXES[casket])
        value_match = re.search(regex_pattern, haystack)
        data[casket.name]["reward"] = value_match.groups(0)[0]

        if casket == Casket.WATSON:
            continue
        text = haystack.split('<h3 id="Tertiary">Tertiary</h3>')[-1]
        text = text.split("</tbody>")[0]
        text = text.split("<tr")

        for x in text:
            if "Clue scroll (master)" in x:
                matches = re.findall(MASTER_SCROLL_CHANCE_REGEX_PATTERN, x)
                chance = matches[0].split("/")
                chance = int(chance[0]) / int(chance[1])
                data[casket.name]["master_chance"] = chance
                break

    return data
    

