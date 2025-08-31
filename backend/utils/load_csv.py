import pandas as pd
import json

def csv_to_jsonl(csv_path, jsonl_path, sheet="Sheet1"):
    df = pd.read_csv(csv_path)
    with open(jsonl_path, "w") as f:
        for i, row in df.iterrows():
            row_data = {"sheet": sheet, "row": i + 2, "cells": []}
            for col, val in row.items():
                row_data["cells"].append(
                    {
                        "cell": f"{col}{i + 2}",
                        "header": col,
                        "value": val,
                        "formula": None,
                    }
                )
            f.write(json.dumps(row_data) + "\n")
