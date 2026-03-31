from pathlib import Path


OUTPUT_DIR = Path("outputs")


def ensure_output_dir() -> Path:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    return OUTPUT_DIR
