import psutil
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
from database import *
from variables import *
from datetime import datetime


# Function to collect process data
def collect_process_data():
    process_data = []
    pids = []
    for proc in psutil.process_iter(['name', 'pid', 'status', 'username']):
        
        p = psutil.Process(pid=proc.info['pid'])
        cpu_percent = p.cpu_percent(interval=None)
        memory_percent = p.memory_percent()
        process_data.append([cpu_percent, memory_percent])
        pids.append({'pid': proc.info['pid']})
        
    return process_data, pids

def save_display_data():
    print("save_display_data")
    display_data = []
    
    for proc in psutil.process_iter(['name', 'pid', 'status', 'username', 'cpu_percent', 'memory_percent']):
        p = psutil.Process(pid=proc.info['pid'])
        cpu_percent = p.cpu_percent(interval=0)
        memory_percent = p.memory_percent()
        display_data.append(
            {
                "name": proc.info['name'],
                "pid": proc.info['pid'],
                "status": proc.info['status'],
                "username": proc.info['username'],
                "cpu_percent": cpu_percent,
                "memory_percent": memory_percent,
            }
        )
        
    updateDatabase({"pc_name": pc_name}, {"$set":{"data": display_data, 'pc_url':pc_url}})
    return display_data

# Train DBSCAN model
def train_dbscan(process_data):
    # Scale the data
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(process_data)
    model = DBSCAN(eps=0.2, min_samples=15)
    model.fit(scaled_data)
    return model

def terminate_process(pid):
    try:
        process = psutil.Process(pid)
        try:
            process.terminate()
            print(f"Terminated process with PID: {pid}")
            
            return True, "Success"
        except psutil.AccessDenied:
            print("Access denied for process id: ", pid)
            return False, "Access Denied"
        
    except psutil.NoSuchProcess:
        print(f"Process with PID {pid} not found")
        return False, "No Such process"
    
def detect_and_terminate_anomalies(pids, model: DBSCAN):

    for i, label in enumerate(model.labels_):

        if label == -1:  # Anomaly detected

            pid = pids[i]['pid']
            
            if pid != 0:  # Skip terminating process with PID 0
                print(f"Anomaly detected for process with PID: {pid}")
                terminate_process(pid)
    
def setCpuDetails():
    print("setCpuDetails")
    total_processes = len(psutil.pids())
    memory_usage = psutil.virtual_memory().total
    cpu = psutil.cpu_percent(interval=None)
    data = dict(
        total_processes=total_processes,
        memory_usage=memory_usage, 
        cpu=cpu
        )
    
    timestamp = datetime.timestamp(datetime.now())
    updateDatabase({"pc_name": pc_name}, {"$push":{"usage_data": {'timestamp': timestamp, 'data': data}}})
    makeLength10()
    return True

def AnomalyTermination():
    process_data, pids = collect_process_data()
    
    model = train_dbscan(process_data)
    
    detect_and_terminate_anomalies(pids, model)
    save_display_data()
    setCpuDetails()

