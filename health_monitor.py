import os
import time
import json
import psutil  # INSTALLATION: pip install psutil
import requests

# ==========================================
# 🩺 HEALTH MONITOR CONFIGURATION
# ==========================================
# Settings for system status reporting
# ==========================================
MONITOR_INTERVAL = int(os.getenv("MONITOR_INTERVAL", "60"))
ALERT_WEBHOOK_URL = os.getenv("ALERT_WEBHOOK_URL") # Slack/Teams webhook
CPU_THRESHOLD = float(os.getenv("CPU_THRESHOLD", "85.0"))
MEMORY_THRESHOLD = float(os.getenv("MEMORY_THRESHOLD", "90.0"))

class SystemMonitor:
    """
    Monitors system resources (CPU, Memory, Disk) and reports health status.
    """
    
    def check_cpu(self) -> dict:
        usage = psutil.cpu_percent(interval=1)
        status = "CRITICAL" if usage > CPU_THRESHOLD else "OK"
        return {"usage": usage, "status": status}

    def check_memory(self) -> dict:
        mem = psutil.virtual_memory()
        status = "CRITICAL" if mem.percent > MEMORY_THRESHOLD else "OK"
        return {"usage": mem.percent, "status": status}

    def send_alert(self, message: str):
        """Sends a JSON alert to the configured webhook."""
        if not ALERT_WEBHOOK_URL:
            print("Warning: ALERT_WEBHOOK_URL not set. Skipping alert.")
            return
        
        payload = {"text": f"🚨 System Alert: {message}"}
        try:
            requests.post(ALERT_WEBHOOK_URL, json=payload, timeout=5)
            print("Alert sent successfully.")
        except Exception as e:
            print(f"Failed to send alert: {e}")

    def run_check(self):
        print("Running system health check...")
        cpu = self.check_cpu()
        mem = self.check_memory()
        
        report = {
            "timestamp": time.time(),
            "cpu": cpu,
            "memory": mem
        }
        
        print(json.dumps(report, indent=2))
        
        if cpu["status"] == "CRITICAL" or mem["status"] == "CRITICAL":
            self.send_alert(f"High resource usage! CPU: {cpu['usage']}%, MEM: {mem['usage']}%")

if __name__ == "__main__":
    monitor = SystemMonitor()
    monitor.run_check()
