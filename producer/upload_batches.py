import os
import subprocess
import time
from pathlib import Path
from snowflake.ingest import SimpleIngestManager
from snowflake.ingest import StagedFile
import os
from dotenv import load_dotenv

load_dotenv()
SNOWFLAKE_ACCOUNT = os.getenv("SNOWFLAKE_ACCOUNT")
SNOWFLAKE_USER = os.getenv("SNOWFLAKE_USER")
PRIVATE_KEY_PASSPHRASE = os.getenv("SNOWFLAKE_PRIVATE_KEY_PASSPHRASE")
SNOWFLAKE_HOST = f"{SNOWFLAKE_ACCOUNT}.snowflakecomputing.com"

BATCH_DIR = Path("batches")

SNOWFLAKE_CONNECTION = "healthcare"
PIPE_NAME = "HEALTHCARE_DB.RAW.HOSPITAL_PIPE"

import os

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.serialization import (
    load_pem_private_key,
    Encoding,
    PrivateFormat,
    NoEncryption,
)

PRIVATE_KEY_PATH = "/home/melat/.snowflake/keys/rsa_key.p8"

with open(PRIVATE_KEY_PATH, "rb") as key_file:
    private_key_obj = load_pem_private_key(
        key_file.read(),
        password=os.environ["SNOWFLAKE_PRIVATE_KEY_PASSPHRASE"].encode(),
        backend=default_backend(),
    )

private_key = private_key_obj.private_bytes(
    Encoding.PEM,
    PrivateFormat.PKCS8,
    NoEncryption(),
).decode()
    
ingest_manager = SimpleIngestManager(
    account=SNOWFLAKE_ACCOUNT,
    host=SNOWFLAKE_HOST,
    user=SNOWFLAKE_USER,
    pipe=PIPE_NAME,
    private_key=private_key
)

SNOWFLAKE_STAGE = (
    "@HEALTHCARE_DB.RAW.HOSPITAL_STAGE"
)

UPLOAD_INTERVAL = 60  # seconds


def upload_file(file_path: Path):
    """Upload a JSON batch file to the Snowflake internal stage."""

    absolute_path = file_path.resolve()

    sql = f"""
        PUT 'file://{absolute_path}'
        {SNOWFLAKE_STAGE}
        AUTO_COMPRESS = FALSE
        OVERWRITE = FALSE;
    """

    print(f"Uploading {file_path.name}...")

    result = subprocess.run(
        [
            "snow",
            "sql",
            "-c",
            SNOWFLAKE_CONNECTION,
            "-q",
            sql,
        ],
        capture_output=True,
        text=True,
    )

    if result.returncode == 0:
        print(f"✓ Uploaded {file_path.name}")
        notify_snowpipe(file_path)
        return True

    print(f"✗ Failed to upload {file_path.name}")
    print(result.stderr)

    return False


def notify_snowpipe(file_path):

    staged_file = StagedFile(
        file_path.name,
        file_path.stat().st_size
    )

    response = ingest_manager.ingest_files(
        [staged_file]
    )

    if response["responseCode"] == "SUCCESS":
        print(f"✓ Snowpipe notified: {file_path.name}")
    else:
        print(f"✗ Snowpipe notification failed: {response}")



def main():

    batch_files = sorted(BATCH_DIR.glob("*.json"))

    if not batch_files:
        print("No JSON batch files found.")
        return

    print(f"Found {len(batch_files)} batch files.")

    for file_path in batch_files:

        success = upload_file(file_path)

        if success:
            print(f"Waiting {UPLOAD_INTERVAL} seconds...\n")
            time.sleep(UPLOAD_INTERVAL)


if __name__ == "__main__":
    main()