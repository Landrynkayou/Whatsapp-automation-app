from controller.messageController import *
from utils.oppenZapp import *
from multiprocessing import Process, Lock

if __name__ == "__main__" :
    lock = Lock()

    # createMessage("Rebec","Hello")
    createMessage("Yohan", "Yo")


    scheduleMessages(lock)
    
