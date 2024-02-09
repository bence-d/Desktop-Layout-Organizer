import psutil

def kill_processes_by_name(process_name):
    for process in psutil.process_iter(['pid', 'name']):
        if process.info['name'] == process_name:
            try:
                print(f"Terminating {process_name} (PID: {process.info['pid']})")
                psutil.Process(process.info['pid']).terminate()
            except Exception as e:
                print(f"Error terminating {process_name} (PID: {process.info['pid']}): {e}")

if __name__ == "__main__":
    process_name = "dhapi.exe"
    kill_processes_by_name(process_name)