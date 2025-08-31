import json
from openpyxl import load_workbook

def excel_to_jsonl_with_formulas(excel_path, jsonl_path):
    wb = load_workbook(excel_path, data_only=False)  # data_only=False preserves formulas
    
    with open(jsonl_path, "w") as f:
        for sheet in wb.sheetnames:
            ws = wb[sheet]
            
            headers = [cell.value for cell in next(ws.iter_rows(min_row=1, max_row=1))]
            
            for row_idx, row in enumerate(ws.iter_rows(min_row=2), start=2):
                row_data = {"sheet": sheet, "row": row_idx, "cells": []}
                
                for col_idx, cell in enumerate(row, start=1):
                    col_letter = cell.column_letter
                    header = headers[col_idx - 1] if headers and col_idx <= len(headers) else None
                    
                    row_data["cells"].append({
                        "cell": f"{col_letter}{row_idx}",
                        "header": header,
                        "value": cell.value,
                        "formula": cell.formula if hasattr(cell, "formula") else None
                    })
                
                f.write(json.dumps(row_data) + "\n")
