# Healthcare Data Pipeline with Snowflake, Snowpipe & dbt

This project is an end-to-end data engineering pipeline I built to practice working with semi-structured healthcare data using Snowflake, Snowpipe, dbt, Python, and dimensional modeling.

The pipeline simulates a hospital system continuously generating patient admission data. The source dataset is converted into small JSON batches, uploaded to a Snowflake internal stage, automatically ingested into a raw table through Snowpipe, and then transformed with dbt into analytics-ready fact and dimension tables.

## Technologies

- Snowflake — Data warehouse and semi-structured JSON processing

- Snowpipe — Continuous ingestion of newly staged files

- Snowflake Internal Stages — Landing area for JSON batches

- Python — Batch generation and file ingestion

- dbt — SQL transformations and dependency management

- dbt-utils — Surrogate key generation

- JSON / VARIANT — Semi-structured source data

- Dimensional Modeling — Fact and dimension design
  
## Architecture

## Data Ingestion

The original healthcare dataset is split into smaller JSON files using Python to simulate new hospital records arriving over time.

A Python producer uploads each batch to a Snowflake internal stage using PUT. After a successful upload, the producer notifies Snowpipe, which loads the new file into the RAW layer.

The raw table stores the incoming records using Snowflake's VARIANT data type instead of immediately flattening the JSON.

This keeps the ingestion layer close to the original source and separates ingestion from transformation.

The RAW layer also stores metadata such as the source filename and load timestamp for traceability.

## Transformation with dbt
dbt was used as a transformation tool for the project , the data transformation was split into three phases such as staging, intermediate and marts. 
### Staging
The staging layer parses the JSON stored in the Snowflake VARIANT column and converts it into structured relational data.

This includes:

- Extracting JSON attributes

- Renaming fields to consistent snake_case names

- Casting values into appropriate Snowflake data types

- Cleaning and standardizing string values

- Handling empty or invalid values

- Preserving ingestion metadata

### Intermediate 
This layer contains transformation and bussiness logic that do not belong in either the staging or the marts layer . making the transformation logic more clean and readable. 

### Marts
The final layer uses a star schema to prepare the healthcare data for analytics based on the project's decided grain.

The grain of the main fact table is:
