from fastapi import UploadFile
import os
from utils.load_csv import csv_to_jsonl
from utils.load_workbook import excel_to_jsonl_with_formulas

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


def handle_uploaded_excel(file: UploadFile) -> str:
    # Save file to disk
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        f.write(file.file.read())

    # Create jsonl output path
    jsonl_path = file_path + ".jsonl"

    # Call your util
    excel_to_jsonl_with_formulas(file_path, jsonl_path)

    return jsonl_path


def handle_uploaded_csv(file: UploadFile) -> str:
    # save file to disk first
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        f.write(file.file.read())

    # create output path
    jsonl_path = file_path + ".jsonl"

    # call your existing util
    csv_to_jsonl(file_path, jsonl_path)

    return jsonl_path