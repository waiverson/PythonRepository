# coding=utf-8
__author__ = 'xyc'

import urllib,re



_URL = "http://www.bankofcanada.ca/stats/assets/csv/fx-seven-day.csv"
def get(refresh=False):
    if refresh:
        get.rates = {}
    if get.rates:  # 这里的判断是单例的关键
        return get.rates
    with urllib.request.urlopen(_URL) as file:
        for line in file:
            line = line.rstrip().decode("utf-8")
            if not line or line.startswith(("#", "Date")):
                continue
            name, currency, *rest = re.split(r"\s*,\s*", line)
            key = "{} ({})".format(name, currency)
            try:
                get.rates[key] = float(rest[-1])
            except ValueError as err:
                print("error {}: {}".format(err, line))
    return get.rates


get.rates = {}