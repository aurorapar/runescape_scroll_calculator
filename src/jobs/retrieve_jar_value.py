import re

import requests

from ..data.implings import Impling


MAIN_URL = "https://oldschool.runescape.wiki/w/Impling_jar"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:152.0) Gecko/20100101 Firefox/152.0"}

def retrieve_jar_loot_values():

    r = requests.get(MAIN_URL, headers=headers)

    print("Retrieving loot values for jars")

    if r.status_code not in [200]:
        raise RuntimeError(f'Could not retrieve jar data, responses:\r\n{r.text}\r\n{r.status_code}\r\n{r.reason}')

    text = r.text.split("cannot be sold on the GE.")[-1]
    text = text.split("Item sources")[0]
    text = text.replace("\n", "")

    regex_pattern = re.compile(r'.*<tbody>(.*)</tbody>.*')
    results = re.findall(regex_pattern, text)

    table_body = results[0]
    rows = [x for x in table_body.split('<tr>') if x][1:]

    data = {}
    for impling in Impling:
        for row in rows:
            if impling.name.lower() in row.lower():
                text = row.replace("</span></td></tr>", "").strip()
                text = text.split(">")
                price = text[-5].replace("</span", "")
                loot_value = text[-1]
                data[impling.name] = {
                    "price": price,
                    "loot": loot_value
                }

    return data