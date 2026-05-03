#!89; do
  # 1. Grab raw magnetic data (Z-axis)
  MAG_RAW=$(termux-sensor -n 1 -s "Magnetometer" | jq -r '.["Magnetometer"].values[2]')
  
  # 2. Check for null data (Prevents crash)
  if [ -z "$MAG_RAW" ] || [ "$MAG_RAW" == "null" ]; then
    Z_FLUX=0
  else
    Z_FLUX=$MAG_RAW
  fi
  
  # 3. Calculate Neural Resonance (Static 10Hz for Alpha Sync)
  STIM_TARGET=10.00
  
  # 4. Inject into the Heartbeat File
  echo "{\"geomagnetic_flux_delta\": $Z_FLUX, \"cranial_stim_target\": $STIM_TARGET, \"status\": \"SYNCHRONIZED\"}" > emcs_data.json
  
  # Calculate Delta between Market Value and Acquisition Cost from the MSI
ENTROPY_DELTA=$(curl -s "YOUR_MSI_ENDPOINT?query=current_margin")

# Inject into Heartbeat with 10Hz resonance
echo "{\"geomagnetic_flux_delta\": $Z_FLUX, \"entropy_correction\": $ENTROPY_DELTA, \"status\": \"SYNCHRONIZED\"}" > emcs_data.json

  
  # Frequency Delay (100ms = 10Hz)
  sleep 0.1
done
nnvr