#!/bin/bash

# 1. Grab the raw magnetic field data (Z-axis is best for planetary grounding)
# We take 5 samples to average out the "noise" into a stable "gear"
MAG_RAW=$(termux-sensor -n 5 -d 50 -s "Magnetometer" | jq -r '.["Magnetometer"].values[2]')

# 2. Calculate the Average Flux
Z_FLUX=$(echo "$MAG_RAW" | awk '{sum+=$1} END {print sum/NR}')

# 3. Calculate the Cranial Stim Target (Neural Resonance)
# This maps the flux to a human-usable frequency (10-40Hz)
STIM_TARGET=$(echo "scale=2; ($Z_FLUX % 30) + 10" | bc)

# 4. Save to a temporary JSON file that code.js can read
# Note: Saving to the current folder so the local server can find it
echo "{\"geomagnetic_flux_delta\": $Z_FLUX, \"cranial_stim_target\": $STIM_TARGET}" > emcs_data.json

echo "Flux Captured: $Z_FLUX | Resonance: $STIM_TARGET Hz"
