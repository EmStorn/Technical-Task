import subprocess
import psutil
import time
import csv

data_collection_interval = int(input("Insert interval for data collection in seconds: "))
process_path = input("Type process' path to be monitored: ")

selected_process = subprocess.Popen(process_path)
print('PID is ' + str(selected_process.pid))
process_pid = selected_process.pid

p = psutil.Process(pid=process_pid)
print(p)

def get_process_data():
    measured_parameters = []
    print(p.name())
    print(p.status())  # return cached value
    memory_consumption = p.memory_info()
    wset = memory_consumption.wset
    measured_parameters.append(wset)
    private = memory_consumption.private
    measured_parameters.append(private)
    cpu_percent = p.cpu_percent()
    measured_parameters.append(cpu_percent)
    handles = p.num_handles()
    measured_parameters.append(handles)

    with open(f"Process {process_pid} data.csv", "a", newline="") as collected_data:
        writer = csv.writer(collected_data)
        writer.writerow(measured_parameters)

process_running = True

while process_running is True:
    try:
        get_process_data()
        time.sleep(data_collection_interval)
    except ProcessLookupError:
        process_running = False
        print("Process completed")
    except psutil.NoSuchProcess:
        process_running = False
        print("Process completed")
