Healthcare Data Pipeline with Snowflake, Snowpipe & dbt

This project is an end-to-end data engineering pipeline I built to practice working with semi-structured healthcare data using Snowflake, Snowpipe, dbt, Python, and dimensional modeling.

The pipeline simulates a hospital system continuously generating patient admission data. The source dataset is converted into small JSON batches, uploaded to a Snowflake internal stage, automatically ingested into a raw table through Snowpipe, and then transformed with dbt into analytics-ready fact and dimension tables.

Architecture

Data Ingestion

The original healthcare dataset is split into smaller JSON files using Python to simulate new hospital records arriving over time.

A Python producer uploads each batch to a Snowflake internal stage using PUT. After a successful upload, the producer notifies Snowpipe, which loads the new file into the RAW layer.

The raw table stores the incoming records using Snowflake's VARIANT data type instead of immediately flattening the JSON.

This keeps the ingestion layer close to the original source and separates ingestion from transformation.

The RAW layer also stores metadata such as the source filename and load timestamp for traceability.
