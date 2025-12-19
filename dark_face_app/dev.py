import subprocess
import sys
import os
import time
from watchfiles import run_process

def kill_port(port):
    """Force kill any process listening on the given port (Cross-platform)."""
    import platform
    
    system = platform.system()
    
    if system == "Windows":
        try:
            cmd = f"netstat -ano | findstr :{port}"
            output = subprocess.check_output(cmd, shell=True).decode()
            
            killed_any = False
            for line in output.strip().split('\n'):
                parts = line.strip().split()
                if len(parts) >= 5 and f":{port}" in parts[1]:
                    pid = parts[-1]
                    if pid.isdigit() and pid != '0':
                        print(f"💀 Killing zombie process on port {port} (PID {pid})...")
                        subprocess.run(f"taskkill /F /PID {pid}", shell=True, 
                                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                        killed_any = True
            if killed_any:
                time.sleep(1)
        except subprocess.CalledProcessError:
            pass
        except Exception as e:
            print(f"Warning cleaning port (Windows): {e}")

    else:
        # Linux / MacOS
        try:
            # Try using lsof if available
            cmd = f"lsof -ti:{port} | xargs kill -9"
            # We use subprocess.run with check=False to ignore errors (e.g. no process found)
            # and verify lsof exists first or just catch the shell error
            subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except Exception:
            # Fallback or ignore if lsof not present. 
            # Watchfiles usually handles restart well on POSIX.
            pass

def start_server():
    """Function to run the server."""
    import signal
    
    # Handle signals gracefully to avoid traceback printing by multiprocessing
    def signal_handler(sig, frame):
        # Clean exit without traceback
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    kill_port(7861)
    print("\n🔥 Change detected! Restarting MCP Server...")
    try:
        # Use subprocess.run to handle paths with spaces correctly
        subprocess.run([sys.executable, "mcp_interface.py"])
    except KeyboardInterrupt:
        # Suppress the ugly traceback when watchfiles kills this process
        pass
    except SystemExit:
        pass

if __name__ == "__main__":
    print("👀 Dev Server Active - Watching for changes in 'src' and 'mcp_interface.py'")
    
    # Watch src folder and the interface file itself
    # paths to watch
    paths_to_watch = [
        "src",
        "mcp_interface.py"
    ]
    
    # check if paths exist to avoid errors
    valid_paths = [p for p in paths_to_watch if os.path.exists(p)]
    
    if not valid_paths:
        print("Error: Could not find paths to watch. Make sure you are in the project root.")
        sys.exit(1)
        
    run_process(*valid_paths, target=start_server)
