import json
from pathlib import Path

SOURCE_FILE = Path("dataset/healthcare_dataset.json")
BATCH_DIR = Path("batches")

BATCH_SIZE = 100

BATCH_DIR.mkdir(exist_ok=True)

with open(SOURCE_FILE, "r") as file:
    records = json.load(file)

print(f"Total records: {len(records)}")

for start in range(0, len(records), BATCH_SIZE):
    batch = records[start:start + BATCH_SIZE]

    batch_number = (start // BATCH_SIZE) + 1

    batch_file = BATCH_DIR / f"hospital_batch_{batch_number:03}.json"

    with open(batch_file, "w") as file:
        json.dump(batch, file, indent=2)

    print(f"Created: {batch_file}")