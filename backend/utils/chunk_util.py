def chunk_jsonl(jsonl_path, chunk_size=2000):
    with open(jsonl_path, "r") as f:
        lines = f.readlines()

    for i in range(0, len(lines), chunk_size):
        yield lines[i : i + chunk_size]
