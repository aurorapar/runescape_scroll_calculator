import requests

from ..data.implings import Impling


def retrieve_impling_value(impling):
    if impling not in [i for i in Impling]:
        raise RuntimeError(f'Impling {impling} is not supported')

    url = "https://secure.runescape.com/m=itemdb_oldschool/api/graph/{0}.json".format(impling.value)

    print(f"Retrieving data for {impling.name} Impling")

    header = {"User-Agent": "scroll_calculator"}
    response = requests.get(url)

    if response.status_code not in [200]:
        raise RuntimeError(f'Could not retrieve data for Impling {impling}, responses:\r\n{response.text}\r\n{response.status_code}\r\n{response.reason}')

    return response.json()