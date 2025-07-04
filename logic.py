import subprocess
import json
import os
import psutil

# Optional: Block dangerous commands
DANGEROUS = ["rm -rf", "mkfs", "shutdown", "reboot", "poweroff", ":(){:|:&};:"]

def get_graphical_bar(used, total, length=25):
    percent = used / total
    fill = int(percent * length)
    bar = "█" * fill + "░" * (length - fill)
    return f"{bar} {int(percent * 100)}%"

def handle_local_command(prompt):
    prompt = prompt.strip()
    lower = prompt.lower()

    # 🔐 Block dangerous commands
    for danger in DANGEROUS:
        if danger in prompt:
            return "🚫 Command blocked for safety!"

    # ⚡ Quick commands
    if "open firefox" in lower:
        os.system("firefox &")
        return "🦊 Opening Firefox..."

    elif "open efinity" in lower:
        os.system("efinity &")
        return "⚙️ Launching Efinity IDE..."

    elif "show ram" in lower or "memory" in lower:
        mem = psutil.virtual_memory()
        bar = get_graphical_bar(mem.used, mem.total)
        return f"🧠 RAM Usage:\n{bar}\nUsed: {mem.used // (1024**2)}MB / Total: {mem.total // (1024**2)}MB"

    elif "battery" in lower:
        try:
            battery = psutil.sensors_battery()
            if battery:
                status = "🔌 Plugged In" if battery.power_plugged else "🔋 On Battery"
                return f"🔋 Battery: {battery.percent}% ({status})"
            else:
                return "⚠️ Battery info not available."
        except:
            return "⚠️ Battery info not available."

    elif "ip address" in lower or "show ip" in lower:
        ip = subprocess.getoutput("hostname -I")
        return f"🌐 IP Address: {ip.strip()}"

    # 📟 Try executing any terminal command
    try:
        output = subprocess.check_output(prompt, shell=True, stderr=subprocess.STDOUT, timeout=15, text=True)
        return f"📟 Terminal Output:\n{output.strip()}"
    except subprocess.CalledProcessError as e:
        return f"❌ Command Error:\n{e.output.strip()}"
    except subprocess.TimeoutExpired:
        return "⏳ Command timed out after 15 seconds."
    except Exception as e:
        return f"⚠️ Unexpected error: {str(e)}"

def ask_ollama(prompt, model="mistral"):
    request = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }

    result = subprocess.run(
        ["curl", "-s", "-X", "POST", "http://localhost:11434/api/generate",
         "-d", json.dumps(request)],
        capture_output=True, text=True
    )

    try:
        response = json.loads(result.stdout)
        return response.get("response", "⚠️ No response.")
    except json.JSONDecodeError as e:
        print("⚠️ JSON Error:", e)
        print("Response was:\n", result.stdout)
        return "⚠️ Error parsing model output."

