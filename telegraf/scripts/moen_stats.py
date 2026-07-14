import os
import sys
from pyflowater import PyFlo

def get_stats():
    user = os.getenv("MOEN_USER")
    password = os.getenv("MOEN_PASS")
    
    try:
        f = PyFlo(user, password)
        
        for loc in f.locations():
            # Handle the nickname
            raw_nick = loc.get('nickname') if loc.get('nickname') else "Unknown"
            nickname = str(raw_nick).replace(' ', '_')
            
            for dev_summary in loc.get('devices', []):
                dev_id = dev_summary.get('id')
                if not dev_id:
                    continue
                
                # Fetch the full device object
                device = f.device(dev_id)
                
                # Based on your DEBUG output, data is in 'telemetry'
                telemetry = device.get('telemetry', {})
                current = telemetry.get('current', {})
                
                # If 'current' is empty, this might not be the main shutoff
                if not current:
                    continue

                # Map the metrics from the 'current' telemetry block
                stats = {
                    "flow_rate": current.get('flow', 0),
                    "pressure": current.get('psi', 0), # Moen often uses 'psi' in this block
                    "temp": current.get('temp', 0)
                }
                
                # Consumption is usually in the 'telemetry' -> 'usage' block
                usage_data = telemetry.get('usage', {})
                stats["daily_consumption"] = usage_data.get('today', 0)

                # Format and Print for Telegraf
                tag_set = f"location={nickname},device_id={dev_id}"
                field_set = ",".join([f"{k}={v}" for k, v in stats.items()])
                
                print(f"water_usage,{tag_set} {field_set}")

    except Exception as e:
        print(f"ERROR: {str(e)}", file=sys.stderr)

if __name__ == "__main__":
    get_stats()
