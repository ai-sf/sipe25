#!/bin/bash

set -e  # Exit on error

# Default values
DOMAIN=""
OUTPUT_DIR="mirror-site"
DEPTH=3

# Parse arguments
if [ $# -lt 1 ]; then
    echo "Usage: $0 <domain> [output_dir] [depth]"
    exit 1
fi

DOMAIN="$1"
if [ $# -ge 2 ]; then
    OUTPUT_DIR="$2"
fi
if [ $# -ge 3 ]; then
    DEPTH="$3"
fi

echo "Downloading mirror for domain: $DOMAIN"
echo "Output directory: $OUTPUT_DIR"
echo "Depth: $DEPTH"

# Clean up any existing directories
if [ -d "httrack" ]; then
    echo "Removing existing httrack directory..."
    rm -rf httrack
fi

if [ -d "$OUTPUT_DIR" ]; then
    echo "Removing existing output directory..."
    rm -rf "$OUTPUT_DIR"
fi

# Run HTTrack
echo "Running HTTrack..."
httrack "https://${DOMAIN}/" \
    --mirror \
    --stay-on-same-address \
    --depth="$DEPTH" \
    -O "httrack" \
    "+*.${DOMAIN}/*" \
    -v

# Move files to output directory
if [ -d "httrack/${DOMAIN}" ]; then
    echo "Moving files to $OUTPUT_DIR..."
    mkdir -p "$OUTPUT_DIR"
    mv httrack/${DOMAIN}/* "$OUTPUT_DIR/"
    rm -rf httrack
    echo "Mirror downloaded successfully to $OUTPUT_DIR"
else
    echo "Error: Expected HTTrack output directory not found: httrack/${DOMAIN}"
    exit 1
fi