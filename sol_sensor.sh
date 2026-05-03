#!/bin/bash
while true; do
  # Mines S25 Magnetometer and formats for the 10Hz Heartbeat
  # Required: Termux:API and jq
  termux-sensor -n 1 -s "Magnetometer" | jq '{geomagnetic_flux_delta: .["Magnetometer"].values, status: "SYNCHRONIZED"}' > emcs_data.json
  sleep 0.1
done

