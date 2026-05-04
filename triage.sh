#!/data/data/com.termux/files/usr/bin/bash
shopt -s nocaseglob
RAW="$HOME/sol_savage_enterprise/01_receiving/raw/"
T1="${RAW}tier1_high_res/"
echo "[COO] Triage Initiated. Processing assets..."
for img in "$RAW"*.{jpg,png,jpeg,dng}; do
    [ -f "$img" ] || continue
    RES=$(identify -format "%w" "$img" 2>/dev/null || echo 0)
    if [ "$RES" -gt 3000 ]; then
        mv "$img" "$T1" 2>/dev/null
    fi
done
echo "[COO] Triage Complete."
echo ">> Tier 1 Assets: $(ls "$T1" | wc -l)"
