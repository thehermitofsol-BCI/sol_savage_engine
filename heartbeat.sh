#!/bin/bash
# Sol Savage COO Node: Sticky Heartbeat Monitor
# Continuous feedback for the Industrial Ledger

ID="ss_heartbeat"

while true; do
    # Count assets in the technical wash queue
    COUNT=$(ls -1 ~/sol_savage_enterprise/01_receiving/raw/ 2>/dev/null | grep -v ".json" | wc -l)
    
    # Check for recent Hardening logs
    LAST_SYNC=$(tail -n 1 ~/sol_savage_enterprise/logs/rclone.log 2>/dev/null | cut -c 1-20)
    
    # Update the Persistent Notification
    termux-notification \
        --id "$ID" \
        --title "Sol Savage Engine: ACTIVE" \
        --content "Queue: $COUNT Assets | Last Sync: ${LAST_SYNC:-Initial}" \
        --ongoing \
        --priority low \
        --icon "settings" \
        --button1 "Sync Now" --button1-action "bash ~/.termux/tasker/hardening.sh"

    sleep 15 # Refresh every 15 seconds
done
