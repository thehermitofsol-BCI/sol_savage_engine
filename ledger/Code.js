// SOL SAVAGE BCI: 10Hz Tactile Trigger
function triggerHapticPulse() {
    if ("vibrate" in navigator) {
        // 10ms pulse every 100ms = 10Hz resonance
        navigator.vibrate(10); 
    }
}

async function updateEngine() {
    const statusEl = document.getElementById('status');
    const resonanceEl = document.getElementById('resonance');

    try {
        const response = await fetch('emcs_data.json');
        const data = await response.json();

        if (data.status === "SYNCHRONIZED") {
            statusEl.textContent = "SYNCHRONIZED";
            statusEl.style.color = "#00f2ff"; // Electric Blue
            triggerHapticPulse(); // BCI Handshake
        } else {
            statusEl.textContent = "DISCONNECTED";
            statusEl.style.color = "#ff4444";
        }

        if (data.resonance) {
            resonanceEl.textContent = data.resonance.toFixed(2) + " Hz";
        }

    } catch (error) {
        console.error("Engine Exception:", error);
        statusEl.textContent = "EXCEPTION";
        statusEl.style.color = "#ffff00";
    }
}

// Global Ignition
setInterval(updateEngine, 100); 
updateEngine();

