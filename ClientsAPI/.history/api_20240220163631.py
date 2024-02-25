from flask import Flask, request, jsonify
from detection import terminate_process, save_display_data, setCpuDetails
from variables import *
import threading
app = Flask(__name__)

@app.route('/api/terminate', methods=['POST'])
def terminate():
    data = request.json
    pid = data.get('pid')
    if pid is not None :
        terminated = terminate_process(pid)
        save_display_data()
        return jsonify({'success': terminated[0], 'message':terminated[1]})

@app.route('/api/updateCpuDetail', methods=['GET'])
def updateMostRecentCpuDetail():

    done = setCpuDetails()
    
    if done:
        
        return jsonify(dict(success= True))
    else:
        return jsonify(dict(success= False))
    
@app.route('/api/refresh', methods=['GET'])
def refreshAllDetails():
    thread1 = threading.Thread(target=save_display_data)
    thread2 = threading.Thread(target=setCpuDetails)
    
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()
    
    return jsonify(dict(success = True))
 
    
@app.route('/', methods=['GET'])
def home():
    return "API CPU monitering"

def runApp(port):
     app.run(debug=True, port= port)
    

