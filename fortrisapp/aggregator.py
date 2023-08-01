import json
import logging
from typing import Dict

import pandas as pd

options_to_json = {"orient": "split", "index": False}
options_to_csv = {"index": False}


def aggregate(result: Dict, uuid_prices: str, uuid_rank: str, format: str = "json") -> Dict | str:
    assert format in {"json", "csv"}, f"Wrong Format {format}"
    prices = pd.DataFrame.from_dict(json.loads(result[uuid_prices]), orient="index").reset_index()
    prices.columns = ["crypto", "prices"]

    rank = pd.DataFrame.from_dict(json.loads(result[uuid_rank]), orient="index").reset_index()
    rank.columns = ["crypto", "rank"]

    result_merge = pd.merge(prices, rank, how="outer", on="crypto")

    result_formatted = (
        result_merge.to_json(**options_to_json)
        if format == "json"
        else result_merge.to_csv(**options_to_csv)
    )

    logging.info(result_formatted)
    return result_formatted
