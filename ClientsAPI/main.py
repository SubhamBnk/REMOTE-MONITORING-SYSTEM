from detection import *
from database import *
from api import *
from time import sleep
import threading
from variables import *


if __name__ =="__main__":
  
    # thread = threading.Thread(target=AnomalyTermination)
    # thread.start()
    
    runApp(port)
    sleep(5)