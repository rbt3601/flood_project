# Preprocessing Notes

## Input
The preprocessing pipeline uses valid paired samples generated from the official SpaceNet 8 mapping CSV.

## Output
The pipeline creates:
- train / val / test splits
- metadata.csv

## Current Status
- Pre-event image paths prepared
- Post-event image paths prepared
- Label paths prepared
- Split completed

## Next Step
Rasterize GeoJSON labels into training masks for semantic segmentation.