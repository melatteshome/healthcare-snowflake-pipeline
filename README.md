Healthcare Data Pipeline

This project builds an end-to-end data pipeline for processing healthcare patient data using Python, Snowflake, Snowpipe, and dbt.

A Python producer splits the healthcare dataset into smaller JSON batches and uploads them to a Snowflake internal stage. Snowpipe continuously loads the files into a raw Snowflake table, where the JSON data is stored using the VARIANT data type.

dbt is then used to parse, clean, transform, and model the raw data into analytics-ready tables.

