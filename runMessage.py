from controller.messageController import *
from utils.oppenZapp import *
from multiprocessing import Process, Lock

if __name__ == "__main__" :
    lock = Lock()

    # createMessage("Rebec","Hello")
    createMessage("Artino","Am Good","07:53")


    scheduleMessages(lock)
    
