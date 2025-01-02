from controller.messageController import *

if __name__ == "__main__" :
    # sendMessages()

    createMessage("Rebec","Hello")
    createMessage("Artino","Am Good","00:37")
    createMessage("Python","Testing connection with database","00:36")
    sleep(3)
    scheduleMessages()
