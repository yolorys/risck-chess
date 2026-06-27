#!/bin/bash

# Create data directory if it doesn't exist
mkdir -p ./data

# Download February 2026 data
wget -nc -P ./data "https://huggingface.co/datasets/thomasd1/aix-lichess-database/resolve/main/low_compression/aix_lichess_2026-02_low.parquet"

# Download March 2026 data
wget -nc -P ./data "https://huggingface.co/datasets/thomasd1/aix-lichess-database/resolve/main/low_compression/aix_lichess_2026-03_low.parquet"

# Download April 2026 data
wget -nc -P ./data "https://huggingface.co/datasets/thomasd1/aix-lichess-database/resolve/main/low_compression/aix_lichess_2026-04_low.parquet"

echo "Downloads complete."
