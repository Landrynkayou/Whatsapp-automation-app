from controller.messageController import *
from controller.statusController import *

if __name__ == "__main__" :
    # sendMessages()
    createStatus("/home/hitechangel/Pictures/chat2.png", True, "My App")
    
    # postStatus("/home/hitechangel/Pictures/chat2.png", "My App", True)
    scheduleStatus()
    # createMessage("Rebec","Hello")
    # createMessage("Artino","Am Good","00:37")
    # createMessage("Python","Testing connection with database","00:36")
    # sleep(3)
    # scheduleMessages()
